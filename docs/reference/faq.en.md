# FAQ

Common questions when integrating a DApp with TronLink.

## `window.tron` is undefined / the wallet isn't detected

The provider may not be injected yet, or TronLink isn't installed. Detect it via TIP-6963 instead of reading `window.tron` directly: listen for `TIP6963:announceProvider`, then dispatch `TIP6963:requestProvider`. If no provider announces, TronLink is not installed — prompt the user to install it. See [Start Developing](../dapp/getting-started.md#detect-tronlink-tip-6963).

## `eth_requestAccounts` was rejected (code `4001`)

The user declined the connection (clicked **Reject**, closed the popup, or the request didn't come from the active tab). This is expected — catch the error and let the user retry. See the [error codes](../plugin-wallet/active-requests.md#error-codes).

## I get `-32000` when calling `eth_requestAccounts`

The same origin issued another `eth_requestAccounts` within 20 seconds while the wallet was locked (rate-limited). Wait and retry, and avoid firing the request repeatedly.

## `tronWeb` is `false` / not ready

`window.tron.tronWeb` is `false` until the user authorizes the DApp. Call `eth_requestAccounts` first, then read `tronWeb`. A safe helper checks `tronProvider.tronWeb?.ready`. See [Get the tronWeb Instance](../dapp/getting-started.md#get-the-tronweb-instance).

## Account or network changes aren't reflected in my DApp

`eth_requestAccounts` only covers the initial authorization. For later changes — the user switching accounts, locking the wallet, or changing networks — subscribe to the passive `accountsChanged` and `chainChanged` events. See [Receive Messages from TronLink](../plugin-wallet/passive-messages.md).

## My DApp needs a specific network

Request a switch with `wallet_switchEthereumChain` (TIP-3326), passing the target hex `chainId`. See the [chainId values](networks.md) and [Switch Network](../plugin-wallet/active-requests.md). Confirm the active network by reading `chainChanged`.

## A transaction fails for lack of resources

On-chain operations consume **Energy** (contract execution) and **Bandwidth** (transaction size). Ensure the signing account has enough — obtained by staking TRX (Stake 2.0) or by letting TRX be burned. See the [Glossary](glossary.md) and [Stake 2.0](../dapp/stake2.md).

## Ledger signatures look different (the `v` byte)

TronLink normalizes the trailing byte of Ledger signatures (`01`→`1c`, `00`→`1b`) so Ledger and regular account signatures match. See [Ledger v-field Compatibility](../plugin-wallet/ledger-signing-update.md).

## How do I integrate with the mobile app?

Use the DeepLink (`tronlinkoutside://`) scheme to launch the TronLink app for login, transfer, and signing. See [DeepLink](../mobile/deeplink.md).

## How do I build an AI agent that uses TronLink?

Use the MCP servers, the agent skill set, the signer SDK, or the CLI. Start at [AI Support](../ai-support/ai-llms.md).

## Does TronLink collect usage data?

To keep improving the product experience, TronLink collects some usage statistics. This data is designed to be non-identifying: it does not contain your private keys, mnemonic phrase, wallet address, or transaction hashes, and it is summarized on your device before anything is sent. Wallets are referred to only by a random identifier generated locally, which TronLink cannot link back to your address. The data is used only to improve TronLink and is never sold. The statistics module is open source — see the [Anonymous Analytics Module](https://github.com/TronLink/tronlink-extension-core/blob/main/README.md#anonymous-analytics-module) section of tronlink-extension-core.
