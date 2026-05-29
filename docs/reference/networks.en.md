# Networks & Addresses

A single reference for the network parameters and common addresses used throughout this documentation.

## Networks

| Network | `chainId` (hex) | EVM chainId (decimal) | RPC endpoint | Explorer |
|---|---|---|---|---|
| Mainnet | `0x2b6653dc` | `728126428` | `https://api.trongrid.io` | [tronscan.org](https://tronscan.org) |
| Shasta testnet | `0x94a9059e` | `2494104990` | `https://api.shasta.trongrid.io` | [shasta.tronscan.org](https://shasta.tronscan.org) |
| Nile testnet | `0xcd8690dc` | `3448148188` | `https://nile.trongrid.io` | [nile.tronscan.org](https://nile.tronscan.org) |

- The `chainId` hex value is what `wallet_switchEthereumChain` (TIP-3326) and the `chainChanged` event use. **`chainId` values are case-sensitive.**
- The EVM (decimal) chainId is what EIP-712 typed-data signing uses in the `domain.chainId` field.

## Testnet faucets

- Shasta: request test TRX from the [Shasta faucet](https://www.trongrid.io/shasta).
- Nile: request test TRX from the [Nile faucet](https://nileex.io/join/getJoinPage).

## Address formats

TRON addresses have two interchangeable encodings:

- **Base58** — starts with `T`, e.g. `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`. This is the user-facing form.
- **Hex** — starts with `41`, e.g. `41...`. This is the on-chain/raw form (the `41` prefix is TRON's address byte).

`tronWeb.address.toHex()` / `tronWeb.address.fromHex()` convert between them.

## Units

- `1 TRX = 1,000,000 SUN`. Amounts in `tronWeb` transaction builders (e.g. `sendTrx`) are expressed in **SUN**.

## Common token contracts (Mainnet)

| Token | Standard | Contract address |
|---|---|---|
| USDT | TRC-20 | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` |

For any other token, look up its contract address on [TronScan](https://tronscan.org/#/tokens). Always verify a token's contract address before integrating — addresses differ per network.
