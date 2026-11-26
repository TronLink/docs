# Extension Core (Open Source)

**GitHub**: [https://github.com/TronLink/tronlink-extension-core](https://github.com/TronLink/tronlink-extension-core)

`@tronlink/core` is the JavaScript and TypeScript wallet library used by the TronLink extension. Embed it in a wallet application to derive TRON and EVM accounts and sign locally. For a DApp that asks the user’s installed extension to connect or sign, use the [extension provider](active-requests.en.md).

## Installation

Install the npm package. It includes CommonJS and ES module entry points and TypeScript declarations.

```bash
npm install @tronlink/core
```

See the upstream prerequisites for the required Node.js, pnpm (development) and TypeScript versions. Browser builds need polyfills for Node modules such as `buffer`, `crypto`, and `stream`. [Prerequisites](https://github.com/TronLink/tronlink-extension-core/blob/main/README.md#prerequisites) · [Upstream webpack configuration](https://github.com/TronLink/tronlink-extension-core/blob/main/webpack.config.js)

## Derive a TRON address

Generate a mnemonic, derive the first account’s first address path, then use the derived private key to obtain the address.

```ts
import { BaseWallet, TronWallet } from '@tronlink/core';

const wallet = new TronWallet();
const mnemonic = BaseWallet.generateRandomMnemonic();
const path = wallet.derivePath({ accountIndex: 0, addressIndex: 0 });
const privateKey = wallet.derivePrivateKey({ mnemonic, path });
const address = wallet.getAddressBy({ privateKey });
```

For an EVM address, use `EvmWallet` and call its `derivePath` before deriving the key. [TRON and EVM account example](https://github.com/TronLink/tronlink-extension-core/blob/main/demo/create_account.ts)

## Signing

Both wallet classes support transaction, message, and typed-data signing. For TRON, pass a prepared transaction to `wallet.signTransaction({ privateKey, data: rawTransaction })`. For an EVM transaction, supply the chain configuration and unsigned transaction in `data`. Signing returns the result locally. Broadcasting is a separate step. [TRON signing examples](https://github.com/TronLink/tronlink-extension-core/blob/main/demo/tron_signature.ts) · [EVM signing examples](https://github.com/TronLink/tronlink-extension-core/blob/main/demo/evm_signature.ts)

## Ledger and usage statistics

Ledger signing requires a browser that exposes `navigator.hid`. Use `LedgerTrxSigner` with the device’s TRX app and `LedgerEvmSigner` with its ETH app.

Importing the package, deriving an address, or signing locally does not start a statistics upload. To send a report, the host calls `checkAndReportXY(deps)` and supplies the upload callback. The optional `userStatistics` module groups mainnet activity by day and amount range, using UUIDs assigned to addresses on the device. [Privacy and reporting details](https://github.com/TronLink/tronlink-extension-core/blob/main/PRIVACY.md)

## Version & License

For the current version, see the [package manifest](https://github.com/TronLink/tronlink-extension-core/blob/main/package.json). [Apache License 2.0](https://github.com/TronLink/tronlink-extension-core/blob/main/LICENSE)
