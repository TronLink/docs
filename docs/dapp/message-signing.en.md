# Message Signature

## Overview

A DApp can ask users to sign a message for login verification. The signed message will be forwarded to the back-end to verify whether a user's login is legitimate.

> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Start Developing](getting-started.md#request-authorization)).

## Specification

### Example

```javascript
const tronweb = window.tron.tronWeb;
try {
  const message = "0x1e"; // UTF-8 text, not raw hex bytes
  const signedString = await tronweb.trx.signMessageV2(message);
} catch (e) {}
```
### Parameters

This example uses a hex-looking **string**. In TronWeb's `signMessageV2`, strings are encoded as UTF-8: `"0x1234"` represents six text characters (bytes `30 78 31 32 33 34`), not the two raw bytes `12 34`. Signing and verification must use the same message representation; use `verifyMessageV2` for a V2 signature. See [TronWeb: Sign and Verify Message](https://tronweb.network/docu/docs/Sign%20and%20Verify%20Message/).

The input types accepted by TronLink's injected wallet bridge must be checked against the TronLink and TronWeb versions you support. This example does not establish support for arbitrary UTF-8 text, number arrays, or `Uint8Array` through that bridge.

### Returns

If the user chooses to sign in the pop-up window, the DApp will get the signed hexadecimal string. For example:

```text
    0xb0e0b150b9b10dc348f25c7f38fc87f16e18c0d230d23946aac519a5ad9e45937f656012d33c09e9d9dec00b03fbb304e797f8991bb823dce676ac91e03a55991b
```

If an error occurs, the following information will be returned:

```text
    
    Uncaught (in promise) Invalid transaction provided
```

## Interaction

When “tronweb.trx.signMessageV2(message);” is executed, a pop-up window will show in the TronLink wallet asking the user to confirm, as shown below. The message content will be in hex: 

![TronLink message-signing approval popup showing the hex payload and Reject / Sign buttons](../images/plugin-wallet_sign_message.jpg)

If the user chooses “Reject” in the pop-up window, an exception will be thrown, which the developer can catch for further processing.

## Errors

**Interface distinction:** Codes documented for `provider.request(...)`, such as `4001` for user rejection, are not a universal contract for `tronWeb.trx.sign`, `multiSign`, or `signMessageV2`. Catch signing exceptions; a numeric `code` may be absent. Confirm the error shape for the TronLink/TronWeb versions you support before classifying it. An unrecognized exception is not proof of user rejection. Do not automatically retry signing.

| Code | Meaning | Where it comes from | Retryable? |
| :---: | --- | --- | :---: |
| (thrown; version-dependent shape) | User clicked **Reject** in the signing popup | `tronWeb.trx.signMessageV2(message)` | No — user declined |
| (thrown) | Invalid input, such as `Invalid transaction provided` | `signMessageV2(...)` / wallet bridge validation | No — check the input rules for your supported versions |
| (thrown) | Provider not injected / wallet not authorized | `window.tron.tronWeb` undefined | No — connect first via `eth_requestAccounts` |

For cross-surface translation (DApp ↔ DeepLink ↔ MCP ↔ CLI) see the [Error Code Map](../reference/error-code-map.md).

