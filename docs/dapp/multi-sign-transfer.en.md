# Multi-Signature Transfer

## Overview

For this section, you may refer to [General Transfer](transfer.en.md)

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

## Query active permissions

Choose the account that holds the funds. If the connected signer owns the funds, use its address. For a co-signer, enter the controlled account’s address. Read that owner’s permissions on the transaction network and select an entry whose keys include the signer and whose operations allow TRX transfers. Use its actual `id`.

```javascript
const tronweb = window.tron.tronWeb;
const owner = "REPLACE_WITH_OWNER_ADDRESS";
const account = await tronweb.trx.getAccount(owner);
console.table(account.active_permission);
```

## Specification

### <a id="example"></a>Sign and check the weight

Use these helpers with the authorized TronWeb instance on the transaction network. Before broadcasting, the node checks the signatures against the transaction owner’s current permission. [GetSignWeight](https://developers.tron.network/reference/getsignweight)

```javascript
function validateSignWeight(check, permissionId) {
  const { permission, result, current_weight: weight } = check ?? {};
  if (result?.code === "PERMISSION_ERROR") throw new Error("Recheck owner and permission");
  if (!result || typeof result !== "object" || Array.isArray(result) ||
      !permission || !Number.isSafeInteger(permission.threshold) ||
      permission.threshold <= 0 || !Number.isSafeInteger(weight) || weight < 0 ||
      !/^[0-9a-f]{64}$/i.test(permission.operations)) {
    throw new Error("Permission or weight unavailable");
  }
  // TransferContract is operation 1 in the active permission bitmap.
  const allowsTransfer = (parseInt(permission.operations.slice(0, 2), 16) & 2) !== 0;
  if (permission.type !== "Active" || permission.id !== permissionId || !allowsTransfer) {
    throw new Error("Recheck owner and permission");
  }
  return { code: result.code, weight, threshold: permission.threshold };
}

async function checkAndBroadcast(tronweb, signedTx, permissionId) {
  const check = await tronweb.trx.getSignWeight(signedTx);
  const { code, weight, threshold } = validateSignWeight(check, permissionId);
  if (code === "NOT_ENOUGH_PERMISSION" && weight < threshold) {
    return { status: "collect", signedTx };
  }

  // The node may omit the default ENOUGH_PERMISSION code.
  if ((code !== undefined && code !== "ENOUGH_PERMISSION") || weight < threshold) {
    throw new Error("Signature weight check failed");
  }

  const receipt = await tronweb.trx.sendRawTransaction(signedTx);
  if (!receipt.result) {
    const message = receipt.message ? tronweb.toUtf8(receipt.message) : "";
    throw new Error([receipt.code, message].filter(Boolean).join(" ") || "Broadcast rejected");
  }
  return { status: "submitted", txID: signedTx.txID };
}

async function signAndCheck(tronweb, tx) {
  const permissionId = tx.raw_data.contract[0].Permission_id;
  if (!Number.isSafeInteger(permissionId) || permissionId < 2) {
    throw new Error("An active permission ID is required");
  }

  let signedTx;
  try {
    signedTx = await tronweb.trx.multiSign(tx, undefined, permissionId);
  } catch (error) {
    if (error === "Confirmation declined by user") return { status: "declined" };
    throw error;
  }

  return checkAndBroadcast(tronweb, signedTx, permissionId);
}
```

### First signer

Replace the recipient address and use the permission ID selected from the owner’s active permissions above.

```javascript
const recipient = "REPLACE_WITH_RECIPIENT_ADDRESS";
const permissionId = 2; // Replace with the selected permission ID.
if (!account.active_permission?.some(p => p.id === permissionId)) {
  throw new Error("Select an active permission of the transaction owner");
}

// Build a 10 SUN transfer (1 TRX = 1_000_000 SUN).
const tx = await tronweb.transactionBuilder.sendTrx(recipient, 10, owner, { permissionId });
const outcome = await signAndCheck(tronweb, tx);
```

### Additional co-signers

When the outcome has status `collect`, pass its `signedTx` to the next authorized co-signer using your DApp’s handoff flow. Each co-signer connects their wallet on the same network. Before signing, check that the transaction data matches its `txID`, show the co-signer the decoded owner, recipient, amount and expiration, and continue only after they confirm. Pass `coSignTransfer` the received transaction object and a `confirmTransfer` callback that resolves to `true` once the co-signer approves. `signAndCheck` calls `multiSign` on that object so the existing signatures and transaction ID carry forward.

```javascript
function describeTransfer(tronweb, tx) {
  // The signature covers txID, so confirm raw_data hashes to it before showing details.
  const txCheck = tronweb.utils?.transaction?.txCheck;
  if (!txCheck || !txCheck(tx)) throw new Error("Transaction data does not match its txID");
  const contract = tx.raw_data.contract[0];
  if (contract.type !== "TransferContract") throw new Error("Not a TRX transfer");
  const { owner_address, to_address, amount } = contract.parameter.value;
  return {
    owner: tronweb.address.fromHex(owner_address),
    recipient: tronweb.address.fromHex(to_address),
    amount: `${tronweb.fromSun(amount)} TRX`,
    permissionId: contract.Permission_id,
    expires: new Date(tx.raw_data.expiration).toISOString(),
  };
}

async function coSignTransfer(partiallySignedTx, confirmTransfer) {
  const tronweb = window.tron.tronWeb;
  const details = describeTransfer(tronweb, partiallySignedTx);
  // Show the details in your UI; sign only after the co-signer confirms them.
  if (!(await confirmTransfer(details))) return { status: "declined" };
  return signAndCheck(tronweb, partiallySignedTx);
}
```

Repeat the handoff on `collect`. On `declined`, stop the current signing attempt. If the weight lookup fails or required fields are missing, pause and run the full weight check again after recovery. If the permission was revoked or no longer allows this operation, verify the owner and permission ID, rebuild the transaction and collect fresh signatures. If broadcast times out, look up the transaction ID before another submission.

## Errors

**Error shape:** On the TronLink-injected `tronWeb` (extension 4.0.0 and later), when the user rejects `trx.sign`, `trx.multiSign`, or `trx.signMessageV2`, the promise rejects with the **plain string** `'Confirmation declined by user'` — not an `Error` object, and without a numeric `code`. The `{ code: 4001, message: 'User rejected the request.' }` object is returned only by `window.tron.request(...)` methods such as `eth_requestAccounts`. Other failures (locked wallet, invalid payload, watch-only account) use other values — see [Handling rejections](../reference/error-code-map.md#handling-rejections). Do not automatically retry signing.

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'` (string) | User clicked **Reject** in the signing popup | `tronWeb.trx.multiSign(...)` | No — user declined |
| `code: 'SIGERROR'`, `message` decodes to `Validate signature error: permission isn't exit` | `permissionId` does not exist on `owner` (wrong or revoked). `sendTrx` does **not** validate the permission — the node rejects at broadcast | Return value of `sendRawTransaction(...)` (not thrown) | No — re-query `getAccount(owner).active_permission` and rebuild the transaction |
| `code: 'SIGERROR'`, other `Validate signature error: …` messages | Signatures do not satisfy the permission — e.g. total weight below `threshold`, or a signer that is not in its `keys[]` | Return value of `sendRawTransaction(...)` (not thrown) | No — collect the missing signatures (one `multiSign` call per co-signer) |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | Broadcast succeeded but execution failed on-chain | `getTransactionInfo(txid)` | **No — the tx is final; never auto-retry** |

`message` in a `sendRawTransaction` result is hex-encoded; decode it with `tronweb.toUtf8(res.message)`. To check before broadcasting, call `tronweb.trx.getSignWeight(signedTx)`: `result.code` is `PERMISSION_ERROR` when the permission does not exist and `NOT_ENOUGH_PERMISSION` while the signatures are still below `threshold`.

For cross-surface translation see the [Error Code Map](../reference/error-code-map.md).
