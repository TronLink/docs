# Stake2.0

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

When a DApp asks TronLink to sign a `DelegateResourceContract` or `UnDelegateResourceContract` transaction, the signing popup shows the resource type and an estimated resource amount:

- **Resource type** — read from `raw_data.contract[0].parameter.value.resource`. `tronWeb.transactionBuilder.delegateResource` / `undelegateResource` already set this field to `"ENERGY"` for energy. For bandwidth the field is omitted (it is the protobuf default), and TronLink (4.1.4 and later) treats a missing value as `"BANDWIDTH"`. You do not need to add it yourself.
- **Estimated amount** — read from a top-level `__options` object that you add to the transaction: `estimatedBandwidth` is the estimated bandwidth, `estimatedEnergy` is the estimated energy. Only the value matching the resource type is shown. If `__options` is missing, the popup shows `0`; signing still works.

`__options` sits outside `raw_data`, so adding it does not change `txID` or `raw_data_hex`. In contrast, `parameter.value.resource` is part of the signed protocol data. Do not change it after building: a modified value no longer matches `raw_data_hex` / `txID`. `trx.sign` rejects such a transaction (`'Invalid transaction provided'`; extension 4.4.3 and later), and `trx.multiSign` recomputes `txID` from the modified data, so the signed transaction differs from the one you built. To change the resource type, rebuild the transaction.

![Delegate transaction object with raw_data.contract[0].parameter.value.resource and the top-level __options.estimatedBandwidth highlighted](../images/dapp_stake2.0_img_0.jpg)

<style>
img {
  max-width: 100%!important;
}
</style>

For example:

```javascript
// ENERGY — tronWeb sets parameter.value.resource = "ENERGY"
const energyTx = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'ENERGY', 'ownerAddress', false);
energyTx.__options = { estimatedEnergy: 1 }; // placeholder — calculate it as described below

// BANDWIDTH — resource is omitted and displayed as BANDWIDTH
const bandwidthTx = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'BANDWIDTH', 'ownerAddress', false);
bandwidthTx.__options = { estimatedBandwidth: 1 }; // placeholder — calculate it as described below

const signed = await tronWeb.trx.sign(energyTx);
```

`undelegateResource` transactions use the same `__options` fields.

The specific calculation logic of estimatedEnergy and estimatedBandwidth can be found in the last chapter of the "[<a class="tooltip" href="https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606" data-tooltip="https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606">Stake 2.0 Adaptation FAQ</a>](https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606)": "How to convert resource share to amount?"

## Errors

**Error shape:** On the TronLink-injected `tronWeb` (extension 4.0.0 and later), when the user rejects `trx.sign`, `trx.multiSign`, or `trx.signMessageV2`, the promise rejects with the **plain string** `'Confirmation declined by user'` — not an `Error` object, and without a numeric `code`. The `{ code: 4001, message: 'User rejected the request.' }` object is returned only by `window.tron.request(...)` methods such as `eth_requestAccounts`. Other failures (locked wallet, invalid payload, watch-only account) use other values — see [Handling rejections](../reference/error-code-map.md#handling-rejections). Do not automatically retry signing.

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'` (string) | User clicked **Reject** in the signing popup | `tronWeb.trx.sign(tx)` for the delegate / undelegate tx | No — user declined |
| (thrown) | Insufficient TRX staked / nothing to undelegate | `delegateResource` / `undelegateResource` builder | No — fix the on-chain state first |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | Broadcast succeeded but execution failed on-chain | `sendRawTransaction` result or `getTransactionInfo` | **No — the tx is final; never auto-retry** |

For cross-surface translation see the [Error Code Map](../reference/error-code-map.md).

