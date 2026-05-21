# AI / LLMs

TronLink 的开发者文档以机器可读形式发布，便于 AI 智能体和基于 LLM 的工具直接发现、读取与集成。

## 可用端点

| 端点 | 说明 |
| --- | --- |
| [/docs/llms.txt](/docs/llms.txt) | 关键页面的精选索引,每条带一句话描述（[llmstxt.org](https://llmstxt.org/) 规范） |
| [/docs/llms-full.txt](/docs/llms-full.txt) | 所有英文页面的全文聚合,便于单次抓取 |

生产地址：`https://docs.tronlink.org/docs/llms.txt` 与 `https://docs.tronlink.org/docs/llms-full.txt`。

## 该用哪个文件？

| 场景 | 文件 |
| --- | --- |
| 导航 / 找到正确页面 | `llms.txt` —— 简短的纯链接地图 |
| 单次抓取整份文档 | `llms-full.txt` —— 每页全文 |

先用 `llms.txt` 并跟随其链接;需要一次性获取全部内容时再抓 `llms-full.txt`。

## 添加到你的 AI 工具

- **Cursor** —— Settings → Features → Docs → *Add new doc*,粘贴 `https://docs.tronlink.org/docs/llms.txt`。
- **Claude / 支持 MCP 的智能体** —— TronLink 提供 MCP 服务以实现实时钱包与链上访问,host 配置见 [MCP Server TronLink](mcp-server-tronlink.md) 与 [MCP TronLink Signer](mcp-tronlink-signer.md)。仅作文档上下文时,把工具指向上面的 `llms.txt` 地址即可。
- **其他工具** —— 任何支持自定义文档 URL 的工具都可使用 `llms.txt` / `llms-full.txt` 端点。

## 覆盖范围

该聚合覆盖完整文档,包括 AI/智能体工具链：

- [MCP Server TronLink](mcp-server-tronlink.md) —— 链上、多签、GasFree 工具（Playwright + Direct API）
- [TronLink MCP Core](tronlink-mcp-core.md) —— 框架库：schema、工具定义、流程配方
- [TronLink Skills](tronlink-skills.md) —— 只读智能体技能集（钱包、代币、行情、兑换、资源、质押）
- [MCP TronLink Signer](mcp-tronlink-signer.md) —— 封装签名 SDK 的 MCP 服务
- [TronLink Signer](tronlink-signer.md) —— 独立签名 SDK
- [TronLink CLI](tronlink-cli.md) —— 命令行工具

以及 DApp 集成、移动端（DeepLink）和参考（网络、术语表、FAQ）章节。

## 给智能体的说明

- 从 `llms.txt` 开始——它是权威地图。不要盲目枚举站点文件。
- 工具调用请基于结构化的 `error.code` / `error.retryable` 分支,**不要**解析人类可读的 `message`。
- 读操作可安全重试;签名 / 远程写操作需要用户审批（HITL）,且不得自动重试——见各工具的「安全」一节。
- 实验时默认用测试网（`nile` / `shasta`）;只有动用真实资金时才用 `mainnet`。
