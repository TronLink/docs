# Stake2.0

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

When generating stake 2.0 transactions for DApps, for transactions of the `DelegateResourceContract` or `UnDelegateResourceContract` type, in order to display the estimated results during signature using the Tronlink extension, it is necessary to add the "__options" field to the transaction body.

Inside `__options`, `estimatedBandwidth` is the estimated bandwidth and `estimatedEnergy` is the estimated energy for delegation or undelegation.

When generating stake 2.0 transactions using a non-tronlink extension injected tronweb, in order to display the corresponding type of resource for `DelegateResourceContract` or `UnDelegateResourceContract` type transactions during signature, the "__resource" field needs to be added to the transaction body. (Adding “resource” is only necessary for tronWeb that is not injected by a tronlink extension. TronWeb that is injected by tronlink extension does not require.)

The "__resource" field corresponds to the values "BANDWIDTH" and "ENERGY".

![Stake 2.0 delegate / undelegate signing UI annotated with the __resource ("BANDWIDTH" or "ENERGY") and __options.estimatedBandwidth / estimatedEnergy fields that TronLink reads to render the resource type at signing time](../images/dapp_stake2.0_img_0.jpg)

<style>
img {
  max-width: 100%!important;
}
</style>

> **Resource-field compatibility pending verification:** The prose above refers to `__resource`, while the existing example writes `raw_data.contract[0].parameter.value.resource`. The field read by the signing UI and the applicable extension versions have not been confirmed here. Do not treat these paths as interchangeable. Preserve the builder-generated protocol data, `raw_data_hex`, and `txID` consistency; verify the UI metadata path before adapting this example.

For example:

```javascript
    const transaction = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'BANDWIDTH', 'ownerAddress', false);
    transaction.raw_data.contract[0].parameter.value.resource = "BANDWIDTH"
    transaction.__options = {"estimatedBandwidth": 1}
```

The specific calculation logic of estimatedEnergy and estimatedBandwidth can be found in the last chapter of the "[<a class="tooltip" href="https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606" data-tooltip="https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606">Stake 2.0 Adaptation FAQ</a>](https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606)": "How to convert resource share to amount?"

## Errors

**Interface distinction:** Codes documented for `provider.request(...)`, such as `4001` for user rejection, are not a universal contract for `tronWeb.trx.sign`, `multiSign`, or `signMessageV2`. Catch signing exceptions; a numeric `code` may be absent. Confirm the error shape for the TronLink/TronWeb versions you support before classifying it. An unrecognized exception is not proof of user rejection. Do not automatically retry signing.

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| (thrown; version-dependent shape) | User clicked **Reject** in the signing popup | `tronWeb.trx.sign(tx)` for the delegate / undelegate tx | No — user declined |
| (thrown) | Insufficient TRX staked / nothing to undelegate | `delegateResource` / `undelegateResource` builder | No — fix the on-chain state first |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | Broadcast succeeded but execution failed on-chain | `sendRawTransaction` result or `getTransactionInfo` | **No — the tx is final; never auto-retry** |

For cross-surface translation see the [Error Code Map](../reference/error-code-map.md).

