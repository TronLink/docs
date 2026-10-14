# Error Code Map

TronLink agents traverse three or four error-code dialects when a single user request crosses the DApp provider → DeepLink → MCP → CLI surfaces. This page is a single horizontal join keyed by **business meaning**; use it to translate a code from one dialect to its peers and to decide whether retrying is safe.

> The per-surface tables linked in the column headers remain the SSOT. This page is a navigation aid — when in doubt, branch on the structured field of the surface you actually called (`error.code` for MCP Server TronLink; the `Error: <message>` text for MCP TronLink Signer; exit status + the stderr `error` string for CLI; the `code` field for `window.tron.request` (the rejection string for `tronWeb.trx.*` signing); the callback `code` for DeepLink).

**Error shape:** On the TronLink-injected `tronWeb` (extension 4.0.0 and later), when the user rejects `trx.sign`, `trx.multiSign`, or `trx.signMessageV2`, the promise rejects with the **plain string** `'Confirmation declined by user'` — not an `Error` object, and without a numeric `code`. The `{ code: 4001, message: 'User rejected the request.' }` object is returned only by `window.tron.request(...)` methods such as `eth_requestAccounts`. Other failures (locked wallet, invalid payload, watch-only account) use other values — see [Handling rejections](#handling-rejections). Do not automatically retry signing.

| Business meaning | DApp provider ([EIP-1474][provider]) | DeepLink ([5-digit][deeplink]) | MCP ([`TL_*`][mcp]) | CLI v1.0.1 ([exit status][cli]) | Retryable? |
| --- | :---: | :---: | :---: | :---: | :---: |
| **User rejected** the signing or connection prompt | `4001` from `window.tron.request(...)`; the string `'Confirmation declined by user'` from `tronWeb.trx.sign` / `multiSign` / `signMessageV2` | `300` (Transaction canceled) | — (HITL — re-prompt only on a fresh tool call) | `1` | **No** |
| **Invalid input** / malformed params | thrown by `tronWeb` builder | `10001`–`10020`, `10024`, `10025` | `TL_INVALID_INPUT` | `1` | **No** — fix the payload |
| **Method / capability not supported** | `4200` | `10003`, `10008`, `10009`, `10011`, `10023` | `TL_CAPABILITY_NOT_AVAILABLE` | — | **No** |
| **Wallet authorization mismatch** (initiator ≠ current wallet) | provider returns empty `accounts[]` | `10021`, `10022` | — | — | **No** — re-authorize |
| **No wallet / no session** | provider not injected (`window.tron` undefined) | `10016` | `TL_NO_ACTIVE_SESSION` | — | **No** — initialize / `tl_launch` first |
| **Rate-limited / wallet locked** | `-32000` (`eth_requestAccounts` within 20 s while locked) | — | — | — | **Yes** — wait and retry |
| **Network / RPC transient** (TronGrid, RPC error) | TronGrid HTTP error in `tronWeb` call | — | `TL_CHAIN_QUERY_FAILED`, `TL_GASFREE_QUERY_FAILED`, `TL_MULTISIG_QUERY_FAILED` | `1` | **Yes** |
| **On-chain execution failed** (post-broadcast: `REVERT`, `OUT_OF_ENERGY`, `FAILED`) | thrown by `sendRawTransaction` or surfaces via `getTransactionInfo` | — | `TL_CHAIN_SEND_FAILED`, `TL_CHAIN_SWAP_FAILED`, `TL_GASFREE_SEND_FAILED`, `TL_MULTISIG_SUBMIT_FAILED` | `1` | **No** — the tx is final; fix the root cause; never auto-retry writes |
| **Timeout** (user didn't sign in time, element not found) | call resolves slowly; no canonical code | — | `TL_WAIT_TIMEOUT`, `TL_NAVIGATION_FAILED` | `1` | **Maybe** — safe for reads; for writes that may have been broadcast, reconcile via `tronWeb.trx.getTransactionInfo` / `tl_chain_get_tx` before retrying |
| **Internal / unexpected** | `-32603` (Internal error) | — | `TL_INTERNAL_ERROR`, `TL_LAUNCH_FAILED` | — | **Yes once** — retry once then escalate with logs |

[provider]: ../dapp/getting-started.md#request-authorization
[deeplink]: ../mobile/deeplink.md#result-code
[mcp]: ../ai-support/tronlink-mcp-core.md#error-codes
[cli]: ../ai-support/tronlink-cli.md#exit-codes

## Handling rejections

Besides the user-rejection values described above, other values a DApp can receive from the signing methods include `'User has not unlocked wallet'` (wallet locked, or the DApp was disconnected after authorization), `'Invalid transaction provided'` (invalid payload, or signing failed inside the wallet), `'Transaction integrity check failed'` (4.11.1 and later; the payload failed TronLink's integrity check, e.g. a non-string message — returned after the user closes TronLink's warning popup), and `{ code: 4100, message: 'Watch accounts cannot sign' }` (watch-only account; 4.10.0 and later). Treat anything you do not recognize as an unexpected error, not as a user rejection.

```javascript
function isUserRejection(err) {
  if (typeof err === 'string') return err === 'Confirmation declined by user';
  return err != null && err.code === 4001;
}

try {
  const signed = await window.tron.tronWeb.trx.sign(tx);
} catch (err) {
  if (isUserRejection(err)) {
    // user declined — do not retry automatically
  } else {
    // locked, invalid payload, watch-only account, or unexpected — inspect `err`
  }
}
```

## How to use this map

1. Receive an error from any surface, look up its row, and read across to find the corresponding code (or absence) on the other surfaces.
2. The **Retryable?** column is the agent-safety hint:
    - **No** — auto-retry will fail or do harm. The most dangerous case is "On-chain execution failed", where the tx is already final on-chain.
    - **Yes** — transient; back off (exponential, max 3 retries) and retry the original call.
    - **Maybe** — read-only retry is OK; **never auto-retry writes** without first reconciling with on-chain state.
3. The DeepLink and CLI columns have many gaps because those surfaces only cover a slice of the lifecycle — DeepLink is mobile-only and lives on a separate trust boundary; CLI v1.0.1 exits with `1` for every failure class, so its column cannot distinguish them — read the string `error` on stderr instead (`—` means the CLI has no dedicated condition for it; any failure still exits `1`). For CLI write commands, an exit `1` is never safe to auto-retry, even in rows marked **Yes** — confirm on chain first. Use the most specific surface available.

## Notes for downstream MCP servers

Downstream MCP servers built on TronLink MCP Core (for example custom Skills) **must reuse** the `TL_*` codes from this map rather than minting new strings. If a new business meaning emerges, add a new row here and a new `TL_*` constant in `tronlink-mcp-core` (the SSOT) before shipping; do not invent codes in the consuming server.
