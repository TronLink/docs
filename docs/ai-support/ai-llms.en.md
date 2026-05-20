# AI Support

TronLink ships first-class tooling for AI agents and LLM-based applications: MCP servers, an agent skill set, a command-line tool, and a standalone signer SDK. This page is the entry point — start here, then open the specific tool you need.

## Machine-Readable Resources

For LLMs and AI agents that ingest documentation directly:

- [llms.txt](/docs/llms.txt) — a curated index of this documentation, following the [llmstxt.org](https://llmstxt.org/) standard
- [llms-full.txt](/docs/llms-full.txt) — the full text of every English page, bundled for single-fetch ingestion

## Tooling

- [MCP Server TronLink](mcp-server-tronlink.md) — MCP server exposing on-chain, multi-signature, and GasFree tools (Playwright + Direct API modes)
- [TronLink MCP Core](tronlink-mcp-core.md) — the framework library behind the MCP servers: session manager, capability interfaces, tool definitions, and flow recipes
- [TronLink Skills](tronlink-skills.md) — an agent skill set covering wallet, token, market, swap, resource, and staking commands
- [MCP TronLink Signer](mcp-tronlink-signer.md) — a lightweight MCP server wrapping the signer SDK for signing and broadcasting
- [TronLink Signer](tronlink-signer.md) — the standalone signer SDK (`connect`, `sendTrx`, `sendTrc20`, `signMessage`, `signTypedData`)
- [TronLink CLI](tronlink-cli.md) — command-line tool for queries, transfers, staking, delegation, and voting

## Choosing a Tool

- Building an autonomous agent that reads and writes on-chain → start with [MCP Server TronLink](mcp-server-tronlink.md) or the [Skills](tronlink-skills.md).
- Embedding signing into your own service → use the [Signer SDK](tronlink-signer.md) or its [MCP wrapper](mcp-tronlink-signer.md).
- Scripting one-off operations from a terminal → use the [CLI](tronlink-cli.md).
- Extending or building your own MCP server → build on [TronLink MCP Core](tronlink-mcp-core.md).
