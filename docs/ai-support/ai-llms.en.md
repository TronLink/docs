# AI / LLMs

TronLink's developer documentation is published in machine-readable form so AI agents and LLM-based tools can discover, read, and integrate it directly.

## Available endpoints

| Endpoint | Description |
| --- | --- |
| [/docs/llms.txt](/docs/llms.txt) | Curated English index of key pages with one-line descriptions ([llmstxt.org](https://llmstxt.org/) format) |
| [/docs/llms.zh.txt](/docs/llms.zh.txt) | Curated Chinese index — same layout, links into `/docs/zh/` pages |
| [/docs/llms-full.en.txt](/docs/llms-full.en.txt) | Every English page concatenated for single-fetch ingestion |
| [/docs/llms-full.zh.txt](/docs/llms-full.zh.txt) | Every Chinese page concatenated for single-fetch ingestion |
| [/docs/llms-full.txt](/docs/llms-full.txt) | Alias of `llms-full.en.txt` (kept for back-compat) |

Production URLs: `https://docs.tronlink.org/docs/llms.txt`, `https://docs.tronlink.org/docs/llms.zh.txt`, and the matching `llms-full.*.txt` bundles.

## Which file should I use?

| Use case | File |
| --- | --- |
| Navigate / find the right English page | `llms.txt` — short, link-only map |
| Navigate / find the right Chinese page | `llms.zh.txt` — same layout, Chinese descriptions |
| Ingest the whole documentation in one request | `llms-full.en.txt` / `llms-full.zh.txt` — full text per language |

Start with the index for your language and follow its links; fetch a `llms-full.*` bundle when you need everything at once. The Chinese index points at `/docs/zh/` slugs; the English index points at `/docs/` slugs.

## Add to your AI tool

- **Cursor** — Settings → Features → Docs → *Add new doc*, paste `https://docs.tronlink.org/docs/llms.txt`.
- **Claude / MCP-capable agents** — TronLink ships MCP servers for live wallet and chain access; see [MCP Server TronLink](mcp-server-tronlink.md) and [MCP TronLink Signer](mcp-tronlink-signer.md) for host configuration. For documentation context, point the tool at the `llms.txt` URL above.
- **Other tools** — any tool that accepts a custom documentation URL can use the `llms.txt` / `llms-full.txt` endpoints.

## Coverage

The bundle covers the full documentation, including the AI/agent tooling:

- [MCP Server TronLink](mcp-server-tronlink.md) — on-chain, multi-sig, and GasFree tools (Playwright + Direct API)
- [TronLink MCP Core](tronlink-mcp-core.md) — framework library: schemas, tool definitions, flow recipes
- [TronLink Skills](tronlink-skills.md) — read-only agent skill set (wallet, token, market, swap, resource, staking)
- [MCP TronLink Signer](mcp-tronlink-signer.md) — MCP server wrapping the signer SDK
- [TronLink Signer](tronlink-signer.md) — standalone signer SDK
- [TronLink CLI](tronlink-cli.md) — command-line tool

Plus the DApp integration, mobile (DeepLink), and Reference (networks, glossary, FAQ) sections.

## Notes for agents

- Start from `llms.txt` — it is the authoritative map. Don't enumerate the site blindly.
- For tool calls, branch on the structured `error.code` / `error.retryable`, never on the human-readable `message`.
- Read operations are safe to retry; signing / Remote Write operations require user approval (HITL) and must not be auto-retried — see each tool's Safety section.
- Default to testnets (`nile` / `shasta`) when experimenting; use `mainnet` only for real funds.
