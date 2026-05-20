# Glossary

Definitions of terms, standards, and identifiers used across this documentation.

## TRON & tokens

- **TRX** — the native coin of the TRON network.
- **SUN** — the smallest TRX unit. `1 TRX = 1,000,000 SUN`. Transaction amounts are expressed in SUN.
- **TRC-10** — TRON's native token standard, managed at the protocol level (identified by a numeric token id).
- **TRC-20** — TRON's smart-contract fungible-token standard (analogous to Ethereum's ERC-20).
- **TRC-721** — TRON's non-fungible-token (NFT) standard (analogous to ERC-721).
- **Energy** — the resource consumed when executing smart-contract operations. Obtained by staking TRX (Stake 2.0) or burning TRX.
- **Bandwidth** — the resource consumed by transaction size/byte count. Obtained by staking TRX or burning TRX; a small free daily amount is provided per account.
- **Stake 2.0** — TRON's resource-staking model. Staking TRX yields Energy or Bandwidth; resources can be delegated to other accounts (`DelegateResourceContract` / `UnDelegateResourceContract`). See [Stake 2.0](../dapp/stake2.md).

## Wallet objects & SDK

- **TronWeb** — the JavaScript SDK for building, signing, and broadcasting TRON transactions. See the [TronWeb docs](https://tronweb.network/docu/docs/intro).
- **`window.tron`** — the provider object TronLink injects into every page. Exposes `request`, `tronWeb`, and `on` / `removeListener`.
- **`tronWeb` (instance)** — the `TronWeb` SDK instance bound to the user's account/network, available as `window.tron.tronWeb` after authorization. `false` until authorized.
- **`window.tronLink`** — the legacy provider object (deprecated in favor of `window.tron`).
- **`iTron`** — an object injected only inside the TronLink mobile app's in-app DApp Explorer, exposing native app capabilities. See [DApp Support](../mobile/dapp-support.md).
- **HD wallet** — a Hierarchical Deterministic wallet (BIP-32) deriving many keypairs from a single seed. **BIP-44** defines the derivation path structure; the seed is represented by a **mnemonic** phrase. See [HD Wallets](../hd-wallets.md).

## Standards & proposals

- **TIP** — TRON Improvement Proposal. The full index is at [github.com/tronprotocol/tips](https://github.com/tronprotocol/tips).
- **EIP** — Ethereum Improvement Proposal. TronLink reuses several EIP method names for compatibility.
- **TIP-1102 / EIP-1102** — the wallet connection request (`eth_requestAccounts`). See [Proactively Request TronLink Plugin Features](../plugin-wallet/active-requests.md).
- **TIP-1193 / EIP-1193** — the provider interface and its events (`connect`, `disconnect`, etc.), including the `ProviderRpcError` shape.
- **TIP-3326 / EIP-3326** — the chain-switch request (`wallet_switchEthereumChain`).
- **TIP-6963 / EIP-6963** — multi-wallet provider discovery via the `announceProvider` / `requestProvider` events, so a DApp can pick a specific wallet without competing for `window.tron`.

## Types & identifiers

- **ABI** — Application Binary Interface: the JSON description of a contract's callable methods and events. If a token contract's ABI lacks a recognized method (e.g. `transfer`, `approve`), TronLink may not be able to offer that action.
- **`chainId`** — the network identifier. TronLink uses the hex form (e.g. `0x2b6653dc`) for `wallet_switchEthereumChain` and `chainChanged`, and the decimal EVM form (e.g. `728126428`) for EIP-712 `domain.chainId`. See [Networks & Addresses](networks.md).
- **`ProviderRpcError`** — the EIP-1193 error object emitted on `disconnect`, shaped `{ code: number; message: string; data?: unknown }`.
- **permission id** — the active permission index used for multi-signature transactions (passed to `tronWeb.trx.multiSign`). See [Multi-Signature Transfer](../dapp/multi-sign-transfer.md).
- **base58 / hex address** — the two TRON address encodings (`T...` vs `41...`). See [Networks & Addresses](networks.md#address-formats).

## AI tooling

- **MCP** — Model Context Protocol, the standard TronLink's AI servers implement so agents can call wallet tools. See [AI Support](../ai-support/ai-llms.md).
- **DeepLink** — the `tronlinkoutside://` URL scheme used to drive the TronLink mobile app from a DApp or H5 page. See [DeepLink](../mobile/deeplink.md).
