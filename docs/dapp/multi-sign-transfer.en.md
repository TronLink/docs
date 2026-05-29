# Multi-Signature Transfer

## Overview

For this section, you may refer to [General Transfer](transfer.en.md)

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

## Query active permissions

`multiSign` requires a valid `permissionId` for an **active** permission on the signing account. Active permissions are returned by `tronWeb.trx.getAccount(address)` under the `active_permission[]` field; each entry exposes `id`, `permission_name`, `threshold`, and the `keys[]` array (address + weight). Owner permissions have a fixed `id` of `0` and are exposed under `owner_permission` separately.

```javascript
const tronweb = window.tron.tronWeb;
const account = await tronweb.trx.getAccount(tronweb.defaultAddress.base58);
// account.active_permission is the array — pick the id whose keys[] includes
// the address you intend to sign with, and whose weight + threshold allow the tx.
const activePermissions = account.active_permission ?? [];
console.log(activePermissions.map(p => ({ id: p.id, name: p.permission_name, threshold: p.threshold })));
```

Use the resulting `id` as `permissionId` below.

## Specification

### Example

```javascript
const tronweb = window.tron.tronWeb;
const toAddress = "TRKb2nAnCBfwxnLxgoKJro6VbyA6QmsuXq";
const activePermissionId = 2; // obtained via tronWeb.trx.getAccount(...).active_permission
const tx = await tronweb.transactionBuilder.sendTrx(
  toAddress, 10,
  { permissionId: activePermissionId }
); // Step 1
try {
  const signedTx = await tronweb.trx.multiSign(tx, undefined, activePermissionId); // Step 2
  await tronweb.trx.sendRawTransaction(signedTx); // Step 3
} catch (e) {}
```

If the user chooses “Reject” in the pop-up window, an exception will be thrown, which the developer can catch for further processing. If the user chooses “Sign” in the pop-up window, the DApp receives and broadcasts the signed transaction.

Note that the broadcast only collects one signature in this call — a fully signed multi-sig tx requires the threshold to be met across multiple `multiSign` calls (one per co-signer). Track the partially-signed transaction off-chain (or via the MCP `tl_multisig_*` tools) until the threshold is reached, then broadcast.

## Errors

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| `4001` | User clicked **Reject** in the signing popup | `tronWeb.trx.multiSign(...)` | No — user declined |
| (thrown) | `permission_id not active` / `permission_id not exist` | `transactionBuilder.sendTrx({permissionId})` — wrong or revoked permission | No — re-query `getAccount(...).active_permission` |
| (thrown) | Signature weight below `threshold` after broadcast | `sendRawTransaction` | No — collect more signatures (one `multiSign` call per co-signer) |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | Broadcast succeeded but execution failed on-chain | `getTransactionInfo(txid)` | **No — the tx is final; never auto-retry** |

For cross-surface translation see the [Error Code Map](../reference/error-code-map.md).
