# Start Developing

This document walks you through connecting a DApp to the TronLink wallet end-to-end — from detecting the wallet, requesting authorization, to signing and broadcasting a transaction.

## Overview

TronLink is a browser extension wallet for the TRON network. By integrating TronLink, your DApp can communicate with the TRON network — TronLink injects a `window.tron` object into every page, exposing a `tronWeb` instance, a `request` method, and `on` / `removeListener` for event subscription.

## The `window.tron` Object

```typescript
interface TronProvider {
  isTronLink: true;
  request: (args: { method: string; params?: any }) => Promise<any>; // Invoke wallet features (e.g. eth_requestAccounts)
  tronWeb: TronWeb | false; // Bound to the user's current account/network after authorization; `false` until then
  on(event: string, listener: (...args: any[]) => void): this; // Subscribe to provider events (accountsChanged / chainChanged / connect)
  removeListener(event: string, listener: (...args: any[]) => void): this;
}
```

Once the user authorizes the connection, `window.tron.tronWeb` is fully usable for building, signing and broadcasting transactions.

## Detect TronLink (TIP-6963)

TIP-6963 is the recommended way to detect TronLink (and other TRON wallets) without polluting the global namespace. Listen for the `TIP6963:announceProvider` event and dispatch a `TIP6963:requestProvider` to ask installed wallets to announce themselves.

```javascript
let tronProvider;

window.addEventListener("TIP6963:announceProvider", (e) => {
  if (e.detail.info && e.detail.info.name === "TronLink") {
    tronProvider = e.detail.provider; // === window.tron
  }
});

window.dispatchEvent(new Event("TIP6963:requestProvider"));
```

If `tronProvider` is still undefined after dispatching the request, TronLink is not installed — prompt the user to install it.

## Request Authorization

Use `eth_requestAccounts` to ask the user to connect their wallet. On approval the promise resolves with an array containing the selected address; on failure it rejects with a `{ code, message }` error.

```typescript
try {
  const accounts: string[] = await tronProvider.request({
    method: "eth_requestAccounts",
  });
  console.log("Connected:", accounts[0]);
} catch (err) {
  // err shape: { code: number, message: string }
  console.warn("Authorization failed:", err);
}
```

| code   | Description                                                                                                       |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| 4001   | User rejected the request — clicked **Reject**, closed the popup, or the request did not come from the active tab |
| -32000 | Same origin issued another `eth_requestAccounts` within 20 seconds while the wallet was locked (rate-limited)     |
| 4200   | Unsupported method                                                                                                |

For the full TIP-1102 (`eth_requestAccounts`) specification, see [Proactively Request TronLink Plugin Features](../plugin-wallet/active-requests.md); the legacy `tron_requestAccounts` connection method is documented on the same page.

## Get the `tronWeb` Instance

The simplest helper — returns the existing `tronWeb` if the user has already authorized this DApp, otherwise requests authorization first.

```javascript
async function getTronWeb() {
  if (!tronProvider) throw new Error("TronLink is not installed");
  if (tronProvider.tronWeb?.ready) {
    return tronProvider.tronWeb;
  }
  await tronProvider.request({ method: "eth_requestAccounts" });
  return tronProvider.tronWeb;
}
```

`tronProvider.tronWeb` is normally usable as soon as `eth_requestAccounts` resolves. For everything that happens _after_ the initial authorization — the user switching accounts, locking the wallet, or changing networks — listen for `accountsChanged` / `chainChanged` on the provider. See [Receive Messages from TronLink](../plugin-wallet/passive-messages.md) for the full event set.

After obtaining the `tronWeb` instance you can perform on-chain interactions: TRX/TRC20 transfers, multi-signature transactions, message signing, contract calls, and so on. For full `tronWeb` API usage, see the [TronWeb documentation](https://tronweb.network/docu/docs/intro).

## End-to-End Example: Sign and Broadcast a TRX Transfer

The following self-contained HTML example detects TronLink via TIP-6963, requests authorization, builds a TRX transfer, prompts the user to confirm and sign via the TronLink popup, and broadcasts the signed transaction.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>TronLink Demo</title>
  </head>
  <body>
    <button onclick="connect()">Connect TronLink</button>
    <script>
      let tronProvider;

      window.addEventListener("TIP6963:announceProvider", (e) => {
        if (e.detail.info && e.detail.info.name === "TronLink") {
          tronProvider = e.detail.provider;
        }
      });
      window.dispatchEvent(new Event("TIP6963:requestProvider"));

      async function connect() {
        if (!tronProvider) return alert("TronLink not found!");
        try {
          await tronProvider.request({ method: "eth_requestAccounts" });
        } catch (error) {
          if (error?.code === 4001) return console.info("Connection declined");
          return console.error("Authorization failed", error);
        }

        const tronweb = tronProvider.tronWeb;
        let tx;
        try {
          const to = "REPLACE_WITH_RECIPIENT_ADDRESS";
          // Build a 10 SUN transfer (1 TRX = 1_000_000 SUN).
          tx = await tronweb.transactionBuilder.sendTrx(to, 10, tronweb.defaultAddress.base58);
        } catch (error) {
          return console.error("Could not build transfer", error);
        }

        let signedTx;
        try {
          signedTx = await tronweb.trx.sign(tx);
        } catch (error) {
          if (error === "Confirmation declined by user") return console.info("Signing declined");
          return console.error("Signing failed", error);
        }

        try {
          const receipt = await tronweb.trx.sendRawTransaction(signedTx);
          if (!receipt.result) {
            const message = receipt.message ? tronweb.toUtf8(receipt.message) : "";
            return console.error(receipt.code, message);
          }
          console.log("Check on-chain confirmation for", signedTx.txID);
        } catch (error) {
          console.error("Broadcast outcome unknown. Check transaction before retrying", signedTx.txID, error);
        }
      }
    </script>
  </body>
</html>
```

## Related Documentation

- [Proactively Request TronLink Plugin Features](../plugin-wallet/active-requests.md) — full request/response reference
- [Receive Messages from TronLink](../plugin-wallet/passive-messages.md) — account / network change events
- [General Transfer](transfer.md), [Multi-Signature Transfer](multi-sign-transfer.md), [Message Signature](message-signing.md), [Stake 2.0](stake2.md)
- [TronWeb Documentation](https://tronweb.network/docu/docs/intro)
