# Multi-Signature Transfer

## Overview

For this section, you may refer to [General Transfer](transfer.en.md)

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

## Query active permissions

Choose the account that holds the funds. If the connected signer owns the funds, use its address. For a co-signer, enter the controlled account’s address. Read that owner’s permissions on the transaction network and select an entry whose keys include the signer and whose operations allow TRX transfers. Use its actual `id`.

```javascript
const tronweb = window.tron.tronWeb;
const owner = window.prompt("Transaction owner", tronweb.defaultAddress.base58);
const account = await tronweb.trx.getAccount(owner);
console.table(account.active_permission);
```

## Specification

### Sign and check the weight

Continue in the same scope. Set the recipient and enter the permission ID you selected. After each additional signature, call `checkAndBroadcast` with the updated transaction on the same network. The node checks the signatures against the transaction owner’s current permission. [GetSignWeight](https://developers.tron.network/reference/getsignweight)

```javascript
async function checkAndBroadcast(signedTx) {
  const contract = signedTx.raw_data.contract[0];
  const check = await tronweb.trx.getSignWeight(signedTx);
  if (!check) throw new Error("Sign-weight response unavailable");
  const { permission, result, current_weight: weight } = check;
  if (result?.code === "PERMISSION_ERROR") throw new Error("Recheck owner and permission");
  if (!result || typeof result !== "object" || Array.isArray(result) ||
      !permission || !Number.isSafeInteger(permission.id) ||
      !Number.isSafeInteger(permission.threshold) ||
      permission.threshold <= 0 || !Number.isSafeInteger(weight) || weight < 0 ||
      !/^[0-9a-f]{64}$/i.test(permission.operations)) {
    throw new Error("Permission or weight unavailable");
  }
  // TransferContract is operation 1 in the active permission bitmap.
  const allowsTransfer = (parseInt(permission.operations.slice(0, 2), 16) & 2) !== 0;
  if (permission.type !== "Active" || permission.id !== contract.Permission_id || !allowsTransfer) {
    throw new Error("Recheck owner and permission");
  }
  if (result.code === "NOT_ENOUGH_PERMISSION" && weight < permission.threshold) {
    return { status: "collect", signedTx };
  }
  // The node may omit the default ENOUGH_PERMISSION code in a successful result.
  if ((result.code !== undefined && result.code !== "ENOUGH_PERMISSION") ||
      weight < permission.threshold) throw new Error("Weight check failed");
  const receipt = await tronweb.trx.sendRawTransaction(signedTx);
  if (!receipt.result) throw new Error([receipt.code, receipt.message].join(" "));
  return { status: "submitted", txID: signedTx.txID };
}

const recipient = window.prompt("Recipient address");
const permissionId = Number(window.prompt("Active permission ID"));
if (!account.active_permission?.some(p => p.id === permissionId)) {
  throw new Error("Select an active permission of the transaction owner");
}
const tx = await tronweb.transactionBuilder.sendTrx(recipient, 10, owner, { permissionId });
let signedTx;
try {
  signedTx = await tronweb.trx.multiSign(tx, undefined, permissionId);
} catch (error) {
  if (error === "Confirmation declined by user") console.info("Signing declined");
  else console.error(tx.txID, error);
}
if (signedTx) {
  try {
    console.log(await checkAndBroadcast(signedTx));
  } catch (error) {
    console.error(signedTx.txID, error);
  }
}
```

On `collect`, keep the partially signed transaction for the next authorized co-signer. If the lookup fails or required fields are missing, pause and run the full check again after recovery. If the permission was revoked or no longer allows this operation, stop collecting signatures, verify the owner and permission ID, rebuild and collect fresh signatures. If broadcast times out, look up the transaction ID before another submission.

## Errors

**Error shape:** On the TronLink-injected `tronWeb` (extension 4.0.0 and later), when the user rejects `trx.sign`, `trx.multiSign`, or `trx.signMessageV2`, the promise rejects with the **plain string** `'Confirmation declined by user'` — not an `Error` object, and without a numeric `code`. The `{ code: 4001, message: 'User rejected the request.' }` object is returned only by `window.tron.request(...)` methods such as `eth_requestAccounts`. Other failures (locked wallet, invalid payload, watch-only account) use other values — see [Handling rejections](../reference/error-code-map.md#handling-rejections). Do not automatically retry signing.

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'` (string) | User clicked **Reject** in the signing popup | `tronWeb.trx.multiSign(...)` | No — user declined |
| `code: 'SIGERROR'`, `message` decodes to `Validate signature error: permission isn't exit` | `permissionId` does not exist on `fromAddress` (wrong or revoked). `sendTrx` does **not** validate the permission — the node rejects at broadcast | Return value of `sendRawTransaction(...)` (not thrown) | No — re-query `getAccount(fromAddress).active_permission` and rebuild the transaction |
| `code: 'SIGERROR'`, other `Validate signature error: …` messages | Signatures do not satisfy the permission — e.g. total weight below `threshold`, or a signer that is not in its `keys[]` | Return value of `sendRawTransaction(...)` (not thrown) | No — collect the missing signatures (one `multiSign` call per co-signer) |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | Broadcast succeeded but execution failed on-chain | `getTransactionInfo(txid)` | **No — the tx is final; never auto-retry** |

`message` in a `sendRawTransaction` result is hex-encoded; decode it with `tronweb.toUtf8(res.message)`. To check before broadcasting, call `tronweb.trx.getSignWeight(signedTx)`: `result.code` is `PERMISSION_ERROR` when the permission does not exist and `NOT_ENOUGH_PERMISSION` while the signatures are still below `threshold`.

For cross-surface translation see the [Error Code Map](../reference/error-code-map.md).
