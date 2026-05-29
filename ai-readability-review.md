# TronLink 开发者文档 · AI 可读性评估与优化报告

- **评估对象**：https://docs.tronlink.org/ （EN/ZH 双语，mkdocs-material）
- **评估视角**：以「agent 能否稳定发现 / 解析 / 调用 / 判断失败」为标准的区块链开发者 AI
- **评估基线**：AI Agent 文档标准包 V1.0（项目级覆盖度 20% + 文档质量 80%）
- **评估日期**：2026-05-29 ｜ 文档快照：commit `e724781c635f`，生成于 `2026-05-21T14:08:15Z`

## 一句话结论

> 这是极少数「为 AI 而设计」而不是「顺便能被 AI 读」的钱包文档。综合评级 **A（8.3 / 10）**：AI 入口、MCP、错误码联表、安全披露均为范本级别。剩余问题集中在「最后一公里」工程化：**机器可读契约文件缺失、逐页 raw markdown 缺失、错误矩阵有空洞、License / 版本治理缺位**。补齐后可冲 S。

---

## 一、做得非常好的地方

| 维度 | 证据 | 为什么对 AI 重要 |
|---|---|---|
| AI 入口索引 | 根目录有 `llms.txt`（真·纯文本），含 commit SHA、UTC 时间戳、网络 chainId、「集成原理」摘要、按导航顺序的全站索引；并有 `llms-full.txt` 单次拉取全量（23 页 ≈ 57k tokens），EN/ZH 双份 | agent 一次 fetch 即可建立全局心智，无需爬 51 个 URL |
| 明确的 agent 立场 | `ai-support/ai-llms` 声明文档面向 "retrieval / RAG / inference-time grounding"，并给 "Notes for agents"：从 `llms.txt` 入手、按 error code 分支而非 message、签名需用户批准、优先 testnet | 教科书式 agent 引导，多数项目完全没有 |
| 错误码横向联表 | `reference/error-code-map` 把 DApp(EIP-1474) / DeepLink(5 位) / MCP(`TL_*`) / CLI(exit code) 按「业务含义」对齐，并标 `Retryable` | 让 agent 跨 4 个调用面用同一套语义分支，SSOT 思想到位 |
| MCP 文档深度 | stdio transport、55 个 tool、JSON Schema Draft-7 示例、Zod 运行时校验、`list_tools` 为权威源、统一 error 包络（`error.code/retryable/details` + `meta.schemaVersion`）、`.mcp.json` 配置、高危工具（`tl_evaluate`）禁用指引 | 达到 MCP 标准 9 分锚点 |
| 安全披露诚实 | 明确区分 Direct-API（本地签名直接广播，无 HITL）vs Playwright/Signer（浏览器内人工批准）；标注 swap 的 MEV/滑点风险、必须 bound minimum-output；多签密钥轮换/最小权限 | 副作用等级、确认机制、风险隔离全覆盖 |
| Provider 契约 | `window.tron` 给了 TypeScript interface；TIP-6963 发现、`eth_requestAccounts`(TIP-1102)、TIP-3326 切链、`chainChanged` 等都有 JSON Schema 入参 | 比多数 EVM 钱包文档严谨 |
| 网络参考可拷贝 | mainnet/Shasta/Nile 的 hex chainId + EVM 十进制 + RPC + explorer + faucet + USDT 合约 + TRX/SUN 单位，全部表格化 | agent 直接抽字段 |

---

## 二、扣分项与优化建议（按优先级）

### P0 — 影响 agent 稳定自动化

**P0-1　契约机器可读性分三个断层，provider RPC 是真缺口**

核实源码后，schema 并非笼统「埋在散文里」，而是三档成熟度断层：

| 调用面 | 机器可读性 | SSOT |
|---|---|---|
| MCP tools | 内联 JSON Schema，但仅镜像 **7/55** 个 tool、仅顶层字段 | 🟢 上游 Zod（`tronlink-mcp-core/src/mcp-server/schemas.ts`）+ CI 对账（`scripts/check_doc_schema_parity.py`） |
| Provider RPC（`window.tron`） | ❌ **无 per-method schema**：参数=JS 示例，返回=散文，错误=Markdown 表 | 🔴 无，手写 |
| 错误码 | 四方言联表，`Retryable` 独立列 | 🟡 `TL_*` 在 `tronlink-mcp-core` |

因此 P0-1 按调用面拆级：

- **Provider RPC = 真 P0**：DApp 开发者最高频的面，却零结构化契约，`request(): Promise<any>` + 散文返回（"an array is returned with a single element"），agent 只能靠英文句子推断 I/O。
- **MCP tools = P1（比初判轻）**：SSOT（Zod）与对账 CI 已就位，差的只是覆盖率（7/55）+ 把 schema 作为独立文件发布 + 嵌套全量。
- **错误码 = P1（最便宜）**：一张干净的表 → 一份 `error-codes.json`，近乎零成本。

关键：补契约是「顺手」而非「工程」，流水线与数据源都已就位：

- `error-codes.json`：`scripts/gen_llms_full.py` 已在 build 时按 nav 顺序遍历全部页面，顺带解析 error-code-map 那张表（行=业务含义，retryable 已是独立列）输出 JSON 即可。
- `mcp-tools.json`：**不要手写**，应由上游用 `zod-to-json-schema` 把 Zod SSOT 导出为 release artifact，docs 站点链接/代理它——一步同时解决「7/55 覆盖率」与「仅顶层字段」两个老问题。
- `provider-methods.json`：provider 侧目前零结构，最该补；可参考 MCP 那套对账思路新增可校验 schema，或至少把每个方法返回从散文升级成具体类型。

再评估「`list_tools` 才是权威」：对**已连 MCP** 的 agent 成立，但 `llms.txt` 宣称的受众是**读文档 / RAG** 的 agent，它调不到 `list_tools`、只能读到 7/55——**权威源恰好对宣称服务的人群不可达**。这正是覆盖度标准「OpenAPI / API 契约」项目前只能给 ~7 分（而非 9 分）的精确原因。

**P0-2　逐页没有 raw markdown 入口**

现状：每页是 HTML；想要单页纯文本，要么解析 HTML，要么下载 57k token 的整包 `llms-full.txt`。

- 建议：每页额外暴露 `*.md`（mkdocs 配 `?plain` 或部署 `.md` 镜像）。`llms-full.txt` 已用 `<!-- source: ... | url: ... -->` 分隔，把该 source 路径做成可直接拉取的 raw md 即闭环。

**P0-3　错误矩阵有空洞 + 重试语义含糊**

现状：联表大量 `—`（多数 DApp provider 行无 DeepLink/MCP/CLI 对应）；`active-requests` 中 `tronweb.trx.sign / multiSign / signMessageV2 / wallet_watchAsset` 的 Error Codes 列为空；`Timeout=Maybe`、`Internal=Yes(once)` 对 agent 不可执行。

- 建议：① 补全每个方法的错误码；② 把「Maybe/once」量化成可执行策略（max attempts、backoff、是否需先 `waitForTransaction` 对账再重试）——对应「有副作用操作不得自动重试，除非证明幂等」。

### P1 — 影响接入信任与可维护性

**P1-1　robots.txt 是「允许检索、拒绝训练」的合理姿态，但有两个实操坑**

现状（逐行核对）：`Content-Signal: search=yes,ai-train=no`；Disallow 了 `ClaudeBot, GPTBot, Google-Extended, CCBot, Bytespider, Amazonbot, Applebot-Extended, meta-externalagent, CloudflareBrowserRenderingCrawler`；而 `Claude-User / Claude-SearchBot / OAI-SearchBot / ChatGPT-User` 未被封。

- 该姿态逻辑自洽（封训练爬虫、放行实时检索 UA），与 `ai-llms` 页「面向 inference-time grounding 而非训练」一致，值得肯定。
- 坑 1：靠「没写 Disallow」放行检索 UA，而非显式 `Allow`。建议显式 `Allow` 关键检索 UA 并复核 `PerplexityBot / Googlebot / Bingbot / Applebot(非 Extended)` 未被误伤；注意 `Google-Extended` 被封会同时削弱 Gemini 的 grounding，不只训练。
- 坑 2：用通用/被封 UA 抓取的 RAG 管线会吃 403 且静默丢内容。建议把 UA 政策写进 `ai-llms` 页，并考虑 `llms.txt/llms-full.txt` 对所有 UA 放行。

**P1-2　Direct-API 的密钥默认路径偏危险**

现状：Direct-API 工具本地签名直接广播，仅靠 `AGENT_WALLET_PASSWORD` 把关；`tl_wallet_create` 自动路径会把明文密码写入 `~/.agent-wallet/runtime_secrets.json`。已有警告，但把「明文密钥落盘」作为一等公民路径披露，风险偏高。

- 建议：警告升级为显著 admonition；自动创建路径明确标 test-only；生产路径首选 `mcp-tronlink-signer`（浏览器批准）。

**P1-3　License / SPDX 缺失**

未见文档声明 license。standards 要求所有文档声明 license。

- 建议：`llms.txt` 头部与页脚加 SPDX（文档 `CC-BY-4.0`，SDK/CLI `MIT` 或 `Apache-2.0`）。

**P1-4　版本治理缺一页**

`llms.txt` 有 commit+时间戳（很好），但 pre-1.0 稳定性承诺散落在 MCP 页，没有统一 CHANGELOG / 版本兼容页，每页也未标「适用于扩展/SDK 哪个版本」。

- 建议：加 `reference/changelog`，并在每页 frontmatter 标注 `applies-to` 版本。

### P2 — 完整度 / 体验

- **P2-1　Provider 返回类型过松**：`request(): Promise<any>`、`tronWeb: TronWeb|false`。`any` 让 agent 只能靠 prose 推断返回形状。建议每方法给具体返回类型（提炼进 P0-1 的契约文件）。
- **P2-2　i18n 平价破例**：sitemap 显示 `zh/asset_filter_logic/` 无 EN 对应页，违背「同 slug 即翻译对」不变式。建议补 EN 或在 zh 索引说明这是中文专属。
- **P2-3　MCP 无 resources/prompts**：若不提供可在页面标 N/A（避免误判遗漏）。stdio-only 也建议显式声明「暂不提供 HTTP/SSE transport」。
- **P2-4　首页缺机器发现提示**：HTML `<head>` 加指向 `llms.txt` 的 `<link>`/meta，让未读约定的爬虫也能发现入口。

---

## 三、评分卡（对照 standards 项目级覆盖度）

| 评分项 | 权重 | 得分 | 主要依据 / 扣分点 |
|---|---:|---:|---|
| AI 入口索引 | 20% | 9.3 | `llms.txt`+`llms-full.txt`+双语+agent notes+commit/时间戳，范本级 |
| OpenAPI / API 契约 | 20% | 7.0 | provider RPC 无 per-method schema（P0）；MCP 仅 7/55 且未发布为独立文件（P1） |
| MCP 文档 | 20% | 9.0 | 极完整；扣分于无 resources/prompts 说明、stdio-only 未显式声明、全集靠 `list_tools` |
| Skills 文档 | 15% | 8.0 | 入口与能力齐全（未深读，按列示与联表推断） |
| CLI 文档 | 10% | 8.0 | 有命令面 + exit code 进联表 |
| 互链与 SSOT | 15% | 9.0 | 错误码联表 + `llms.txt` 全互链 + schemaVersion；扣分于矩阵空洞与 i18n 破例 |
| **项目级覆盖度** | 100% | **≈ 8.4 (A-)** | |
| 文档质量（安全/错误/示例/版本/License 综合） | — | **≈ 8.3 (A-)** | 强在安全披露与示例，弱在 License/版本/逐页 raw md |
| **综合** | — | **8.3 / A** | 距 S（9.0）差「机器可读契约 + raw md + 错误矩阵补全 + License/版本治理」 |

---

## 四、最小行动清单（按性价比排序）

1. 发 4 个机器可读文件并在 `llms.txt` 链接：`provider-methods.json`、`mcp-tools.json`、`error-codes.json`、`*.d.ts`。（解 P0-1，覆盖度 7→9）
2. 每页 raw `.md` 镜像，复用现有 `<!-- source -->` 路径。（解 P0-2）
3. 补全错误矩阵 + 量化重试（max attempts/backoff/对账）。（解 P0-3）
4. robots：显式 Allow 检索 UA + 在 ai-llms 页写明 UA 政策；复核 Perplexity/Google-Extended 影响。（解 P1-1）
5. 加 License/SPDX + CHANGELOG + 每页 applies-to 版本。（解 P1-3/P1-4）
6. 把明文密钥落盘路径降级为 test-only admonition。（解 P1-2）

---

## 附：数据可信度说明

具体取值（signer 端口 3386、57k token、各 schema 字段）来自对线上页面的抓取摘要；结构性结论已被多个页面（`llms.txt` ↔ 错误码表 ↔ MCP 页）交叉印证，可信度高。个别精确数值（重试次数、端口）建议落地前对照源仓库 `scripts/gen_llms_full.py` 与 `mkdocs.yml` 复核。

注：初版 P0-1 曾引用一段 `eth_requestAccounts` 的 JSON Schema，经核对源码 `docs/plugin-wallet/active-requests.en.md`，该 schema 实为 WebFetch 摘要模型臆造——真实页面只有 JS 示例 + 散文返回 + 错误码表。结论性判断一律以本地源文件为准，不采信二次摘要。

---

*评审基线：`/Users/tron/Downloads/standards`（AI Agent 文档标准包 V1.0）。本报告由挑剔视角的 AI 评审生成，仅覆盖「AI 可读性」维度。*
