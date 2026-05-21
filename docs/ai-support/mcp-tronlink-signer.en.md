# mcp-tronlink-signer

**GitHub**: https://github.com/TronLink/mcp-tronlink-signer

MCP Server that exposes [tronlink-signer](https://github.com/TronLink/mcp-tronlink-signer/tree/main/packages/tronlink-signer) as MCP tools for Claude and other AI clients. Sign TRON transactions via TronLink browser wallet with user approval — private keys never leave the wallet.

## Setup

### Claude Code

```bash
claude mcp add -s user tronlink-signer -- npx mcp-tronlink-signer
```

### Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "tronlink-signer": {
      "command": "npx",
      "args": ["mcp-tronlink-signer"]
    }
  }
}
```

### From Source

```bash
git clone https://github.com/TronLink/mcp-tronlink-signer.git
cd mcp-tronlink-signer
pnpm install && pnpm build
```

Then point to the built CLI:

```bash
claude mcp add -s user tronlink-signer -- node /path/to/packages/mcp-tronlink-signer/dist/cli.js
```

## MCP Tools

| Tool | Description | Parameters | Side effect | Auto-retry safe? |
| ---- | ----------- | ---------- | --- | :---: |
| `connect_wallet` | Connect TronLink wallet | `network?` | Local Write (caches session) | Yes — user re-approves if needed |
| `send_trx` | Send TRX to an address | `to`, `amount`, `network?` | **Remote Write** | **No** — verify on-chain before re-issuing |
| `send_trc20` | Send TRC20 tokens | `contractAddress`, `to`, `amount`, `decimals?`, `network?` | **Remote Write** | **No** — same as `send_trx` |
| `sign_message` | Sign a message | `message`, `network?` | Local Write (signs only; no broadcast) | Yes — re-prompts the user |
| `sign_typed_data` | Sign EIP-712 typed data | `typedData`, `network?` | Local Write (signs only) | Yes — re-prompts the user |
| `sign_transaction` (`broadcast=false`) | Sign a raw transaction | `transaction`, `broadcast=false`, `network?` | Local Write | Yes — re-prompts the user |
| `sign_transaction` (`broadcast=true`) | Sign + broadcast | `transaction`, `broadcast=true`, `network?` | **Remote Write** | **No** — verify on-chain before re-issuing |
| `get_balance` | Get TRX balance | `address`, `network?` | Network Read | Yes |

All tools support an optional `network` parameter (`mainnet` / `nile` / `shasta`), defaulting to `mainnet`.

**Human-in-the-loop.** Every tool that signs (`send_trx`, `send_trc20`, `sign_message`, `sign_typed_data`, `sign_transaction`) opens the TronLink approval page in the browser. The AI agent **cannot** sign without the user clicking Approve. Treat Remote Write tools as requiring confirmation in production.

## MCP Resources

| URI | Description |
| --- | ----------- |
| `wallet://networks` | Available networks and their configurations |
| `wallet://config` | Current signer configuration |

## MCP Prompts

| Prompt | Description |
| ------ | ----------- |
| `send-trx` | Guided workflow for sending TRX |
| `check-balance` | Guided workflow for checking balance |
| `send-token` | Guided workflow for sending TRC20 tokens |

## How It Works

1. AI agent calls an MCP tool (e.g., `send_trx`) — a signing notice is shown in the CLI
2. The server delegates to `tronlink-signer`, which opens a **single browser tab** for approval (reuses existing tab if open)
3. The approval page discovers TronLink via **TIP-6963** protocol
4. Auto-unlocks wallet and switches network if needed
5. `connect_wallet` auto-completes if the wallet is already connected
6. Transaction details are parsed into human-readable format (TRX transfer, TRC20, TRC721 NFT, stake, delegate, vote, etc.)
7. User reviews and approves in the browser
8. TronLink signs the transaction — private keys never leave the wallet
9. Result is returned to the AI agent — the page stays open for the next operation

## End-to-End Example

A typical `send_trx` flow, from the user's prompt to the on-chain result:

**1. User → agent**

> "Send 5 TRX to TJRabc…xyz on nile."

**2. Agent → MCP tool call**

```json
{
  "name": "send_trx",
  "arguments": { "to": "TJRabc...xyz", "amount": 5, "network": "nile" }
}
```

**3. Approval (human-in-the-loop)** — the server opens the TronLink approval page; the user reviews "Send 5 TRX → TJRabc…xyz (Nile)" and clicks **Approve**. Clicking Reject returns `USER_REJECTED` (not retryable).

**4. MCP tool → agent (result)**

```json
{
  "txId": "0a1b2c...",
  "status": "success"
}
```

**5. Agent → user**

> "Sent 5 TRX — confirmed on-chain (tx `0a1b2c…`)."

> Branch on `status` / `error.code`, never on prose. `status: "pending"` means the broadcast succeeded but confirmation timed out — reconcile with `get_balance` or an explorer lookup rather than resending (see [Errors](#errors)).

## Cancellation

All signing tools support MCP cancellation. If the AI client cancels a pending tool call (e.g., user presses Ctrl+C in Claude Code), the in-flight request is automatically aborted and the browser approval page is not opened for already-cancelled requests.

## Transaction Confirmation

When `sign_transaction` is called with `broadcast: true`, the server automatically polls for on-chain confirmation after broadcast and returns the execution status (`success` or `pending`). If the transaction fails on-chain (e.g., `OUT_OF_ENERGY`, Solidity revert), the error is returned to the AI agent with a decoded reason.

## Errors

The server returns errors in the standard MCP shape. Each error carries a stable `code` and a `retryable` hint so an agent can branch without parsing prose. Framework-level codes follow the SSOT table in [TronLink MCP Core — Error Codes](tronlink-mcp-core.md#error-codes). Server-specific conditions are:

| Condition | Retryable | When |
| --- | :---: | --- |
| `USER_REJECTED` | No | User clicked Reject on the TronLink approval page. |
| `TIMEOUT` | Yes | No approval within the request timeout (default 5 min). Re-issuing re-opens the prompt; do **not** auto-retry a broadcast that may already be in flight. |
| `BROWSER_DISCONNECTED` | Yes (signing only) | Approval page was closed or lost heartbeat. Reconnect by re-issuing the call. Never re-issue a broadcast that may have already landed. |
| `NETWORK_ERROR` | Yes | A TronGrid / RPC request failed. Transient. |
| `BROADCAST_FAILED` | No | Signing succeeded but submission was rejected by the node. Inspect the message; **do not** auto-retry — the signature may already have been accepted by another node. |
| `ON_CHAIN_FAILED` | No | Broadcast OK but on-chain execution failed (`OUT_OF_ENERGY`, Solidity revert, `FAILED`). The transaction is final; address the root cause and submit a new tx. |
| `INVALID_INPUT` | No | The tool input failed validation. Fix the payload. |
| `CANCELLED` | No | The MCP client cancelled the call (e.g., user pressed Ctrl+C). |

**Retry policy.** Read calls (`get_balance`) and pre-sign failures (`USER_REJECTED`, `INVALID_INPUT`, `CANCELLED`) are agent-safe to re-issue with corrected input. For any sign + broadcast path, treat the outcome as unknown the moment the request leaves the server — confirm with `get_balance` or an explorer lookup before re-issuing.

## Security Boundaries

| Boundary | Guarantee | Agent / operator obligation |
|---|---|---|
| **Prompt injection** | Tool inputs are consumed verbatim as call arguments; the server does not re-prompt an LLM with them. The TronLink approval page renders parsed transaction fields, not the agent's free-text. | Treat any on-chain string returned (memos, revert reasons) as untrusted; branch on `txId` / `status` / `code`, not on prose. |
| **Local HTTP listener** | The local approval server **binds to `127.0.0.1` only** (port `TRON_HTTP_PORT`, default 3386, auto-increments on conflict). It never accepts off-host connections. Each server session has a unique ID; old browser tabs from previous sessions are invalidated automatically. | Do not port-forward 3386 over a network. Do not run two copies of this server with the same `TRON_HTTP_PORT` on a shared box. |
| **Outbound host allowlist (SSRF)** | The signer only talks to TronGrid endpoints listed in [Networks](#environment-variables) and to the local browser. Tools do not accept user-supplied URLs that get fetched. | Pin `TRON_NETWORK` and (optionally) `TRON_API_KEY` to known values in production. |
| **API key handling (token passthrough)** | `TRON_API_KEY` is read from env at startup and used only on the outbound leg to TronGrid. It is **not** returned in any tool response, error `details`, or MCP resource. The server does not accept Authorization headers from MCP clients and forward them upstream. | Store the key in the MCP host's secret manager, not in plain `mcpServers` config committed to git. |
| **HITL is mandatory for signing** | Every signing tool (`send_trx`, `send_trc20`, `sign_message`, `sign_typed_data`, `sign_transaction`) opens the TronLink approval page. **There is no programmatic bypass.** Private keys never leave TronLink. | Operators do not need to enforce HITL — it is structural. Do not attempt to harden by removing the browser layer. |
| **Browser tab hijacking** | The approval page authenticates each request against the server session ID and ignores stale tabs. Heartbeat detection closes the session on browser disconnect. | If the same user runs multiple agents, ensure each spawns its own signer instance; cross-instance request mixing is prevented by session ID, but UI confusion is not. |
| **Confused deputy** | The signer acts under the connected TronLink account; there is no per-call authorization scope from the MCP client. | One signer instance = one TronLink account; do not multiplex multiple end users through the same instance. |

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `TRON_NETWORK` | Default network (mainnet/nile/shasta) | `mainnet` |
| `TRON_HTTP_PORT` | Local HTTP server port | `3386` |
| `TRON_API_KEY` | TronGrid API key (optional) | - |

## Version & License

- **Package:** `mcp-tronlink-signer` v0.1.4
- **License:** MIT — `SPDX-License-Identifier: MIT`
- **Changelog / releases:** [https://github.com/TronLink/mcp-tronlink-signer/releases](https://github.com/TronLink/mcp-tronlink-signer/releases)
