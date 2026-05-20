# AI 支持

TronLink 为 AI 智能体与基于 LLM 的应用提供了完整的工具链：MCP 服务、智能体技能集、命令行工具，以及独立的签名 SDK。本页是入口——先看这里，再进入你需要的具体工具。

## 机器可读资源

供直接读取文档的 LLM / AI 智能体使用：

- [llms.txt](../../llms.txt) —— 本文档的精选索引，遵循 [llmstxt.org](https://llmstxt.org/) 规范
- [llms-full.txt](../../llms-full.txt) —— 所有英文页面的全文聚合，便于单次抓取

## 工具

- [MCP Server TronLink](mcp-server-tronlink.md) —— 提供链上、多签、GasFree 工具的 MCP 服务（Playwright + Direct API 两种模式）
- [TronLink MCP Core](tronlink-mcp-core.md) —— MCP 服务背后的框架库：会话管理、能力接口、工具定义、流程配方（flow recipe）
- [TronLink Skills](tronlink-skills.md) —— 覆盖钱包、代币、行情、兑换、资源、质押等命令的智能体技能集
- [MCP TronLink Signer](mcp-tronlink-signer.md) —— 封装签名 SDK、用于签名与广播的轻量 MCP 服务
- [TronLink Signer](tronlink-signer.md) —— 独立签名 SDK（`connect`、`sendTrx`、`sendTrc20`、`signMessage`、`signTypedData`）
- [TronLink CLI](tronlink-cli.md) —— 用于查询、转账、质押、代理、投票的命令行工具

## 如何选择

- 构建能读写链上的自治智能体 → 从 [MCP Server TronLink](mcp-server-tronlink.md) 或 [Skills](tronlink-skills.md) 入手。
- 把签名能力嵌入自己的服务 → 用 [Signer SDK](tronlink-signer.md) 或它的 [MCP 封装](mcp-tronlink-signer.md)。
- 在终端里脚本化执行一次性操作 → 用 [CLI](tronlink-cli.md)。
- 扩展或自建 MCP 服务 → 基于 [TronLink MCP Core](tronlink-mcp-core.md) 构建。
