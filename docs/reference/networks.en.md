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

## Common token contracts (SSOT)

This is the single source of truth (SSOT) for common mainnet token contract addresses. Other pages — [TronLink CLI](../ai-support/tronlink-cli.md) and [TronLink Skills](../ai-support/tronlink-skills.md) — reconcile to this table; when an address changes, update it here first.

| Token | Standard | Mainnet contract address | Decimals | Notes |
|---|---|---|---|---|
| TRX | native | — | 6 | Native coin, no TRC-20 contract |
| USDT | TRC-20 | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 | |
| USDC | TRC-20 | `TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8` | 6 | |
| USDD | TRC-20 | `TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz` | 18 | |
| WTRX | TRC-20 | `TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR` | 6 | Wrapped TRX |
| BTT | TRC-20 | `TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4` | 18 | |
| JST | TRC-20 | `TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9` | 18 | |
| SUN | TRC-20 | `TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S` | 18 | |
| WIN | TRC-20 | `TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7` | 6 | |

For any other token, look up its contract address on [TronScan](https://tronscan.org/#/tokens). Always verify a token's contract address before integrating — addresses differ per network.
