# TronLink 开发者文档评审报告（MCP + CLI + Skill + AI 入口）

**评审日期**：2026-05-27  
**评审依据**：
- [`MCP 文档标准 V1.0`](https://drive.google.com/drive/folders/1FhYGmYyKuRBcpSVhm82VuK2uceQ4w0uv)
- [`CLI 文档标准 V1.0`](https://drive.google.com/drive/folders/1FhYGmYyKuRBcpSVhm82VuK2uceQ4w0uv)
- [`Skill 产品文档标准 V1.0`](https://drive.google.com/drive/folders/1FhYGmYyKuRBcpSVhm82VuK2uceQ4w0uv)
- [`公共安全与错误码基线 V1.0`](https://drive.google.com/drive/folders/1FhYGmYyKuRBcpSVhm82VuK2uceQ4w0uv)
- [`项目级覆盖度评分标准 V1.7`](https://drive.google.com/drive/folders/1FhYGmYyKuRBcpSVhm82VuK2uceQ4w0uv)

**评审对象**：[docs.tronlink.org/zh/](https://docs.tronlink.org/zh/)「AI 支持」章节 6 篇文档  
**文档基线**：Updated 2026-05-21T14:08:15Z · Commit `e724781c635f`（docs 源码托管在 [`xueyuanying/docs`](https://github.com/xueyuanying/docs)）

| # | 文档 | 适用标准 |
|:-:|------|---------|
| 1 | [MCP Server TronLink](https://docs.tronlink.org/zh/ai-support/mcp-server-tronlink/) | MCP V1.0 |
| 2 | [TronLink MCP Core](https://docs.tronlink.org/zh/ai-support/tronlink-mcp-core/) | MCP V1.0 |
| 3 | [MCP TronLink Signer](https://docs.tronlink.org/zh/ai-support/mcp-tronlink-signer/) | MCP V1.0 |
| 4 | [TronLink CLI](https://docs.tronlink.org/zh/ai-support/tronlink-cli/) | CLI V1.0 |
| 5 | [TronLink Skills](https://docs.tronlink.org/zh/ai-support/tronlink-skills/) | Skill V1.0 |
| 6 | [AI / LLMs 入口页](https://docs.tronlink.org/zh/ai-support/ai-llms/) | 覆盖度 V1.7 + 跨标准 |

> **维护方说明**：本报告覆盖 6 篇文档。1–4 + 6 由 Leon 团队维护；**Skills（#5）由产品组维护**——请协助转发给对应 owner，或内部对齐后统一回应。Skills 部分的 P2 改进项与 Leon 的 P1-3 / P1-9 联动，建议两边协调整改。

---

## 一、总评

| # | 文档 | 类型判定 | 内容 | Agent | 安全 | 加权 | 整改后预期 | 等级 |
|:-:|------|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | MCP Server TronLink | High-risk / Mutative（30/40/30） | 8 | 9 | 9 | **87.0** | 98 | A |
| 2 | TronLink MCP Core | General / Agent-first（25/60/15） | 7 | 8 | 8 | **77.8** | 95 | B+ |
| 3 | MCP TronLink Signer | High-risk / Mutative（30/40/30） | 8 | 8 | 10 | **88.0** | 96 | A |
| 4 | TronLink CLI | High-risk CLI（30/40/30） | 9 | 10 | 9 | **94.0** | 99 | A+ |
| 5 | TronLink Skills | Read-only Data Skills（35/50/15） | 10 | 10 | 9 | **98.5** | 100 | A+ |
| 6 | AI / LLMs 入口页 | 覆盖度 + 跨标准入口 | 10 | 10 | 10 | **100.0** | 100 | A+ |
| **平均** | — | — | — | — | — | **90.9** | **98.0** | **A** |

**整体结论**：

- **TRON 生态当前 4 类文档（API / MCP / CLI / Skill）中标杆级别**——6 篇全部 A 级以上，3 套标准 P0 gate（MCP 6 + CLI 6 + Skill 6 = 18 项）全部通过
- **差距来源不在内容深度，而在三类硬伤**：跨文档死链（如 `tronlink-mcp-core.md#错误码` 锚点 3 处死链）、文档与代码漂移（Flow Recipes 文档 32 / 实际 23 / 含 2 个不存在 flow 名）、发布工程缺失（5 个 npm 包全部 0 GitHub releases）
- **三类硬伤都有清晰整改路径**——下文按优先级展开，整改后可达 98 分（A）

**亮点**（保留上一轮认知，下文 §二 详述）：CI schema parity、错误码 SSOT 设计意图、Content-Signal robots、退出码 6 档 retryable、多签凭证 5 维管理、`tl_evaluate` 三 host 禁用示例、依赖钉版 + 数据截至时间戳、Skills 反例表与判断口诀——均超 V1.0 标准明文要求。

---

## 二、20 条亮点汇总（建议回流标准 V1.1）

按标准维度分类，提议作为 V1.1 评分锚点 / P0 加项的素材，按价值排序。

### 2.1 Agent 可用性维度（10 条）

| # | 亮点 | 出处 | 标准对应 |
|:-:|------|------|---------|
| 1 | **「❌ 不要走这里（反例）」专节 + 判断口诀** | Skills | Skill §4.1「发现选择」10 分锚点「有路由表和负向触发」的极致实现 |
| 2 | **Skill ↔ MCP 工具映射表 + 子集关系明示**（25/33 + minor 内只增不减） | Skills | Skill §4.1 客户端兼容 + 版本契约创新 |
| 3 | **用户提问 → Skill → 工具三层路由表**（21 行常见提问对照） | Skills | Skill §4.1 发现选择 10 分 |
| 4 | **每个 skill 内置「何时不要用」写到命令粒度** | Skills | Skill §4.1 负向触发 10 分 |
| 5 | **CI 强制 schema parity 检查**（`scripts/check_doc_schema_parity.py`，文档侧 schema ↔ 上游 schemas.ts 自动 diff） | MCP Server | MCP §6 P0「缺 inputSchema」加分实践 |
| 6 | **错误码 SSOT 跨文档共享**：CLI / MCP Server / MCP Signer 共用 `tronlink-mcp-core#错误码`，含 `code / retryable / hint / 典型触发` | MCP Core | MCP §3 错误契约 10 分 |
| 7 | **HTTP / EVM / DeepLink / MCP / CLI 五通道错误码对照表**（[`reference/error-code-map`](https://docs.tronlink.org/zh/reference/error-code-map/)）以业务含义为主轴横向 join | 全站 | 跨标准创新 |
| 8 | **input schema 文档侧镜像**（MCP Server 镜像 `tl_chain_send` / `tl_chain_swap_v3` / `tl_chain_stake` / `tl_multisig_submit_tx` / `tl_gasfree_send` / `tl_chain_get_account` / `tl_evaluate` 7 个），明示 list_tools 是权威源 | MCP Server | MCP §3 Schema 完整度 10 分 |
| 9 | **副作用 4 分级**（Network Read / Local Write / Remote Write / Destructive）+ 逐工具表标注 | 全站 | MCP §4 / CLI §4 副作用 10 分 |
| 10 | **CLI `--json` 是自动化契约的明文承诺**（minor 加不减、改名属 major） | CLI | CLI §3 机器输出 10 分 |

### 2.2 安全与权限维度（6 条）

| # | 亮点 | 出处 | 标准对应 |
|:-:|------|------|---------|
| 11 | **`tl_evaluate` 三种 host 禁用配置示例**（Claude Code / Claude Desktop / 通用 MCP 客户端） | MCP Server | MCP §6 P0「远程 MCP 无 SSRF」加分实践 |
| 12 | **多签凭证 5 维管理**（按环境隔离 / 存储 / 轮换 / 撤销 / 最小权限） | MCP Server | MCP §5.1 权限授权 10 分 |
| 13 | **钱包密钥两路径对比表**（手动 vs 自动创建），含「待解决（代码侧）」字段明示文档级方案与代码 PR 关系 | MCP Server | MCP §5.1 安全规则 10 分 |
| 14 | **兑换安全专章**（minOut / 滑点上限 / 钉死 router / 不可自动重试） | MCP Server | MCP §5.1 风险防护 10 分 |
| 15 | **7 大安全边界逐条给 agent 与运维方义务**（Prompt 注入 / SSRF / token passthrough / 浏览器 JS / HITL 绕过 / confused deputy / 传输） | MCP Server | MCP §5.1 全维 10 分 |
| 16 | **robots.txt 用 Content-Signal 协议区分 inference vs training**（`search=yes, ai-train=no` + 显式 Disallow GPTBot / ClaudeBot / CCBot）；把 `llms.txt` / `llms-full.txt` 标为 inference 入口 | 全站 | 公共基线 §2 原则 11 机器可抓取的前沿做法 |

### 2.3 人读维度（4 条）

| # | 亮点 | 出处 | 标准对应 |
|:-:|------|------|---------|
| 17 | **双层 llms.txt**（精选索引 + 全文聚合，中英双版，源带 commit hash + UTC 时间戳） | 入口页 | 项目级覆盖度 §0 + 公共基线 §6 自发现入口 |
| 18 | **CLI 退出码 6 档 + 每档 retryable 列**（`0/1/2/3/4/5` + 「已提交但结果未知」不得自动重试） | CLI | CLI §3 错误契约 10 分 |
| 19 | **依赖钉版 + 数据带「截至 2026-05」标注**（`tronweb 6.2.2` / `tronlink-signer 0.1.4` / `mcp-server-tronlink@0.1.1` 全部钉版） | 全站 | MCP §5 / CLI §3 版本与兼容性 10 分 |
| 20 | **零依赖 / 零 npm install + `install.sh` / `uninstall.sh` 全生命周期脚本** | Skills | Skill §3.1 安装接入 10 分锚点 |

> **回流建议**：前 4 条（Agent 可用性）建议升级为 V1.1 的「10 分新锚点」；中间 5 条（安全）建议补入 P0 检查项；后 4 条（人读 + 版本）作 V1.1 加分项写入正文。

---

## 三、单文档详评

### 3.1 MCP Server TronLink — A，87/100

**类型判定**：High-risk / Mutative MCP（含 `tl_chain_send`、`tl_chain_swap_v3`、`tl_evaluate` 等 Remote Write 与 Destructive 原语）

| 维度 | 分 | 主要依据 |
|------|:---:|---|
| 人读 (30%) | **8** | 概述 / 双模架构图（mermaid）/ 双模运行机制 / 6 大核心组件 / 4 集成方式 / 项目结构 完整；扣 2 分：Flow Recipes 三方计数矛盾 + 含 2 个不存在 flow 名（详见 P0-2） |
| Agent 可用性 (40%) | **9** | 工具发现走 list_tools 权威源；input schema 精选镜像 + CI parity；副作用 4 分级；错误契约用 `error.code`；扣 1 分：`tronlink-mcp-core.md#错误码` 锚点死链（详见 P0-1） |
| 安全与权限 (30%) | **9** | 7 大安全边界、兑换安全专章、多签凭证 5 维、钱包路径 A/B 对比、`tl_evaluate` 三 host 禁用示例；扣 1 分：`@bankofai/agent-wallet` 版本管理问题（GitHub 404 + 文档版本落后 npm，详见 P0-3） |

### 3.2 TronLink MCP Core — B+，77.8/100

**类型判定**：Agent-first MCP（框架库，给上层 server 复用）

| 维度 | 分 | 主要依据 |
|------|:---:|---|
| 人读 (25%) | **7** | 完整覆盖架构 / ISessionManager / 9 个能力接口 / 52 工具定义 / Knowledge Store / Flow Recipe 系统 / 元素定位 3 方式；扣 3 分：错误码节标题缺失（应在「标准化响应格式」节下加 `## 错误码` 二级标题响应下游 3 文档引用，详见 P0-1）+ 缺「何时用 mcp-core / 何时用 mcp-server-tronlink」决策矩阵（P1-4） |
| Agent 可用性 (60%) | **8** | 错误码 SSOT 实质在本文档；标准化响应格式；52 工具完整定义；Flow Recipe 含依赖解析；扣 2 分：SSOT 身份未明示 + 下游 3 文档死链（P0-6） |
| 安全与权限 (15%) | **8** | 由上层 server 实现具体边界，本文档只定义抽象能力；扣 2 分：缺「具体安全边界由实现 server 提供，参考 mcp-server-tronlink §安全模型」交叉引用 |

### 3.3 MCP TronLink Signer — A，88/100

**类型判定**：High-risk / Mutative MCP（签名 + 广播）

| 维度 | 分 | 主要依据 |
|------|:---:|---|
| 人读 (30%) | **8** | 完整覆盖配置（Claude Code / Claude Desktop / Cursor / 源码）/ MCP 工具 / 资源 / 提示词 / 工作原理 / 端到端示例 / 取消 / 交易确认 / 错误 / 安全边界 / 环境变量 / 版本 + 内联 changelog；扣 2 分：缺「该用哪个」三选一对照表（P1-1）+ 与 SDK 版本对应关系不明（P1-7） |
| Agent 可用性 (40%) | **8** | 工具表含 7 列 + 副作用 + 可自动重试列；HITL 明确不可绕过；扣 2 分：input schema 没像 mcp-server-tronlink 那样镜像精选示例，全靠 list_tools（P1-2） |
| 安全与权限 (30%) | **10** | HITL 必经浏览器审批；私钥不离开 TronLink；明示哪些是 Remote Write 且不可自动重试；签名类只 Local Write 可重试 |

### 3.4 TronLink CLI — A+，94/100

**类型判定**：High-risk CLI（HITL 写操作 + 远程广播）

| 维度 | 分 | 主要依据 |
|------|:---:|---|
| 人读 (30%) | **9** | Overview / 环境要求（依赖钉版 + 数据截至时间）/ 全局选项 / 命令分类 / 交易签名 / 预览 / 广播双路径 / 输出格式 / 退出码 / 错误 / 安全 / 工作原理 / **AI 智能体使用专章** / 版本与兼容性；扣 1 分：常用代币合约表只列 3 个（与 Skills 8 个不一致，P1-3） |
| Agent 可用性 (40%) | **10** | `--json` 机器输出契约；`error.code` 跨文档 SSOT 引用；退出码 6 档 + retryable；ABI v2 完整支持（tuple / 嵌套数组 / tuple 数组）；pre-flight 模拟在签名前；AI 智能体专章含端到端转账流程示例 |
| 安全与权限 (30%) | **9** | 副作用分级表；HITL 必经浏览器；写操作不自动重试；私钥不离开 TronLink；输入校验 14 条；本地广播与签名器广播的双广播去重机制说明；扣 1 分：退出码 5「网络错误」缺「如何确认上一笔未上链」指引（P2-5） |

### 3.5 TronLink Skills — A+，98.5/100

**类型判定**：Read-only Data Skills（35/50/15）+ Skills/MCP/CLI Hybrid 特征

| 维度 | 分 | 主要依据 |
|------|:---:|---|
| 人读 (35%) | **10** | Overview / Why / 架构图 / 6 大 skill 详解 / 4 集成方式 / 配置 / TRON 资源模型 / 快速开始 / 版本与许可证 全覆盖 |
| Agent 可用性 (50%) | **10** | Skill ↔ MCP 工具映射表 + 用户提问路由表 + 反例表 + 子集关系明示（25/33）+ 5 个客户端配置 + 兼容性与迁移策略 |
| 安全与权限 (15%) | **9** | 纯只读 + 副作用统一 Network Read + 每个 skill「何时不要用」+ 反例表；扣 1 分：TronGrid API Key 的最小权限 / 轮换 / 泄漏处置无明文（Skills P2-3） |

**§7 P0 gate 6/6 全过；§6 推荐结构 10.5/11 覆盖**（Troubleshooting 散在「安全模型」表，未独立成节，Skills P2-1）

**数据 vs 代码核对（全部对齐）** — Skills 是 6 篇文档中唯一一份「重审无新发现」的样板：

| 文档声明 | 实测来源 | 实测值 | 状态 |
|---------|---------|:---:|:---:|
| 33 个 CLI 命令 | `scripts/tron_api.mjs` 实际 `"<cmd>":` 定义数 | **33** | ✅ |
| 25 个 MCP 工具 | `scripts/mcp_server.mjs` 实际 `name: "tron_*"` 数 | **25** | ✅ |
| 8 个 CLI-only | 33 − 25 = 8 + 文档明确列出 | **8** | ✅ |
| 6 大技能 | `skills/` 目录子文件夹数 | **6** | ✅ |
| 子集关系 MCP ⊂ CLI | 25 个 `tron_*` 全部对应到 CLI 命令 | **完美对应** | ✅ |

### 3.6 AI / LLMs 入口页 — A+，100/100

不在 MCP / CLI / Skill 标准评分清单（属导流入口页），整体质量极高：

- ✅ 4 个端点表（中英 × 索引 / 全文）
- ✅ 「该用哪个文件」场景表
- ✅ Cursor / Claude / 其他工具的添加指引
- ✅ 覆盖范围（指向 6 个 AI 工具链文档）
- ✅ 给智能体的 4 条明文说明
- ✅ allowed-use vs robots.txt 与 Content-Signal 的关系澄清

仅 1 条 P2：缺版本契约引用（P2-7）

---

## 四、必改清单（P0：相关标准 gate 失败）

### P0-1 ⚠️ 死链：`tronlink-mcp-core.md#错误码` 锚点在目标文档不存在

**标准依据**：MCP §6 P0「缺错误结构 → Agent 无法分支处理」+ CLI §6 P0「缺 error code / exit code」+ 公共基线「全站无事实自相矛盾」

**现状**：3 个文档引用同一个死锚点：

| 引用方 | 行号 | 引用形式 |
|--------|------|----------|
| mcp-server-tronlink | §「工具契约与副作用」L422 | `[TronLink MCP Core](tronlink-mcp-core.md#错误码) 的 SSOT 错误码表` |
| mcp-server-tronlink | §「兼容性与迁移策略」L729 | `error.code 枚举（SSOT：[TronLink MCP Core 错误码](tronlink-mcp-core.md#错误码)）` |
| tronlink-cli | §「兼容性与迁移策略」L475 | `error.code 枚举（与 [TronLink MCP Core](tronlink-mcp-core.md#错误码) 共享 SSOT）` |

**但 tronlink-mcp-core 文档没有 `## 错误码` 章节**。它的章节是：概述 / 架构设计 / 与 mcp-server-tronlink 的关系 / ISessionManager 接口 / 9 个能力接口 / 52 工具定义 / **标准化响应格式** / Knowledge Store / Flow Recipe 系统 / 元素定位 / 安装与使用 / 项目结构 / 依赖项 / 构建与开发 / 关键设计模式 / 版本与许可证。错误码表实际位于「标准化响应格式」节内的子段，渲染后**没有 `#错误码` 锚点**。

**Agent / 开发者影响**：跟链接 → 落到文档顶部或抛 404 锚点，**拿不到错误码 SSOT 表**。这违反了文档明示的「Agent 应基于 `error.code` 与 `error.retryable` 分支」。

**整改方案**（任选其一）：

- **方案 A**（推荐）：在 tronlink-mcp-core 文档「标准化响应格式」节下显式增加 `## 错误码` 二级标题，把现有错误码表移到该节下。锚点变为 `tronlink-mcp-core.md#错误码`，与 3 处引用对齐
- **方案 B**：把 3 处引用统一改为存在的锚点（如 `tronlink-mcp-core.md#标准化响应格式`），但需要保证错误码表在该节下且足够独立

**附加建议**：错误码表头加一行明示 SSOT 身份：

```
> SSOT for: mcp-server-tronlink, mcp-tronlink-signer, tronlink-cli — 任何下游文档变更需先在此更新。
```

**验收**：3 处跨文档引用全部跳转到包含错误码表的实际位置；mkdocs build 不报 broken anchor warning。

---

### P0-2 ⚠️ Flow Recipes 三方数据矛盾，并含 2 个不存在的 flow 名

**标准依据**：MCP §3 Schema 完整度 + 公共基线「全站无事实自相矛盾」+ §2 原则 3 稳定字段契约

**现状**：mcp-server-tronlink §「Flow Recipes（32 个内置流程）」三处计数互相矛盾：

| 来源 | 计数 |
|------|------|
| 节标题 | **32 个** |
| 子类型表加总（Playwright 4 + 链上 11 + 多签 6 + GasFree 3） | **24 个** |
| `src/flows/*.ts` 实际 `export const ...Flow` 数 | **23 个**（GasFree 3 + import-wallet 1 + multisig 6 + onchain **9** + switch-network 2 + transfer-trx 2） |

**文档列了但代码不存在的 flow**（即死链 flow 名）：

| 文档列出 | 代码核对 |
|---------|---------|
| `chainTransferTrc20Flow` | ❌ 不存在于 `src/flows/onchain.ts` |
| `chainSwapV3Flow` | ❌ 不存在于 `src/flows/onchain.ts` |

**文档遗漏的 flow**（代码有但表里没列）：

| 代码存在 | 文档核对 |
|---------|---------|
| `src/flows/import-wallet.ts` 内的 import wallet flow | ❌ 整个文件 / flow 在文档中未提及 |

**Agent / 开发者影响**：基于文档调 `tl_run_steps --flow chainTransferTrc20Flow` 会得到「flow not found」错误；同时不知道有 import-wallet flow 可用。

**整改**：

1. 重新统计实际 flow，更新节标题（如「Flow Recipes（**23 个内置流程**）」）
2. 子类型表与代码逐项对齐：
   - **链上类**：删除 `chainTransferTrc20Flow` / `chainSwapV3Flow`，改为 9 个；或在 onchain.ts 补这 2 个 flow 实现
   - **新增 Wallet 类**：列出 `importWallet*Flow`
3. 加 CI parity 检查（参考已有的 `scripts/check_doc_schema_parity.py` 模式）：扫 `src/flows/*.ts` 的 `export const ...Flow` 与文档表逐项 diff，CI 失败时阻塞 merge

**验收**：文档总数 = 子类型加总 = 代码实际数；CI parity 检查覆盖 flow 名集合。

---

### P0-3 ⚠️ `bankofai/agent-wallet` GitHub 404 + 文档钉版 `^2.3.0` 已落后 npm 的 `2.4.0`

**标准依据**：MCP §3 版本与兼容性 10 分锚点「有 breaking change / migration」+ 公共基线 §9 通用安全底线

**现状**：

- mcp-server-tronlink §「依赖项」表写：`@bankofai/agent-wallet | ^2.3.0 | 加密本地钱包管理（local_secure）——已钉版本，不用 latest，确保钱包行为可复现`
- npm 实测：`@bankofai/agent-wallet@latest = 2.4.0`（2026-05 已发，维护者 = TRON 团队成员 parson.hu / hades.ye / leo.wu @tron.network）
- GitHub `bankofai/agent-wallet` repo **HTTP 404**

**Agent / 开发者影响**：

1. 钉版 `^2.3.0` 在 npm semver 下允许 2.3.x ~ 2.4.0 之前的所有版本，**实际锁不住 2.4.0**。文档"已钉版本"的承诺与实际不符
2. GitHub 404 让开发者无法看源码 / 提 issue / 核对依赖透明性
3. `agent-wallet` 持有钱包密码（`AGENT_WALLET_PASSWORD`），其源码不可见对安全敏感场景是 deal-breaker

**整改**：

1. 钉死到准确版本：`"@bankofai/agent-wallet": "2.3.0"`（无 caret），或显式声明「kept on 2.3.0; 2.4.0 待评估」
2. 补一行：「GitHub 仓库当前未公开，源码透明性由 npm publish 提供。可通过 `npm pack @bankofai/agent-wallet@2.3.0 && tar -xzf ...` 解包审计。」
3. 评估升级到 2.4.0（若 breaking 则 CHANGELOG 说明，若不 breaking 则升级减少漂移风险）

**验收**：依赖版本与 npm 实际锁定一致；文档明示 GitHub 404 状态 + 源码审计路径；2 周内决策是否升级到 2.4.0。

---

### P0-4 ⚠️ 5 个 TronLink npm 包全部 0 GitHub releases / 0 tags

**标准依据**：MCP §3 版本与兼容性 9 分锚点「有协议/server/schema 版本」+ CLI §3 版本/更新 10 分锚点「SPDX、changelog、deprecated、migration」+ 公共基线 §2.6 原则 10 一致性

**现状**：

| Repo | npm latest | GitHub releases | GitHub tags |
|------|-----------|:---:|:---:|
| TronLink/mcp-server-tronlink | v0.1.1 | **0** | **0** |
| TronLink/tronlink-mcp-core | v0.1.0 | **0** | **0** |
| TronLink/mcp-tronlink-signer | (在子目录) | **0** | **0** |
| TronLink/tronlink-cli | v1.0.1 | **0** | **0** |
| TronLink/tronlink-skills | v1.0.1 | **0** | **0** |

文档已明示「截至当前 v1.0.x / 0.1.x 尚无 GitHub tag 发布；打 tag 之前请直接看 commit 历史」——已知缺陷，但这是**5 个 repo 全部** 0 发布的系统性问题。

**Agent / 开发者影响**：

1. npm 版本号无法对应到 GitHub commit hash，agent 无法基于 git tag 复现「v1.0.1 时的代码状态」
2. 「Releases」是 GitHub 标准发布通知机制，0 releases = 订阅者收不到新版通知
3. 文档说「兼容性与迁移策略」承诺「废弃窗口至少一个 minor 周期」，但没有 minor 边界（tag）参考点，策略落地不了

**整改**：

1. 5 个 repo 一次性把当前 npm 版本回溯打 tag：`git tag v0.1.1 <commit-hash>` + `git push --tags` + `gh release create v0.1.1 --notes "$(npm view <pkg> dist.shasum)"`
2. 加 npm publish CI workflow：每次 publish 自动打 tag + 创建 GitHub Release（含 npm shasum + dist tarball）
3. 文档兼容性节移除「打 tag 之前请直接看 commit 历史」（变成默认有 tag）

**验收**：5 repo 每个 npm 版本对应一个 git tag + GitHub Release；Releases 页可订阅。

---

### P0-5 ⚠️ docs.tronlink.org 源码托管在 `xueyuanying/docs` 个人 repo（所有权 / 单点风险）

**标准依据**：公共基线 §8 License + §9 通用安全底线 + 项目级覆盖度 §0「AI 入口索引层 = 帮 AI / Agent 找到权威文档」

**现状**：

- mcp-server-tronlink §「精选工具 schema」L441 引用：`[check-doc-schema-parity.yml](https://github.com/xueyuanying/docs/blob/main/.github/workflows/check-doc-schema-parity.yml)`
- gh api 实测：`xueyuanying/docs` 是个人 repo，pushed 2026-05-21（与文档站 Updated 时间戳一致 → 强烈暗示这是 docs.tronlink.org 的源码 repo）
- TronLink org 下没有看到对应的 docs repo

**Agent / 开发者影响**：

1. 开发者看到 CI 配置在个人 repo 会困惑（这是 TronLink 官方维护吗？）
2. 单点风险：维护者离职 / 转岗 / repo 删除 / 转 private → docs.tronlink.org 失去更新管道
3. 公开引用个人 repo URL 暴露了维护者身份信息

**整改**：

1. 把 docs 源码 repo 转移到 TronLink org（如 `TronLink/docs` 或 `TronLink/developer-docs`），保留 git history
2. 转移后更新 mcp-server-tronlink 文档里的 CI 引用 URL
3. 在 docs repo README 明示所有权 / 维护者 / contributor 流程

**验收**：docs 源码在 TronLink org 下可见；文档内所有引用 URL 更新到 org repo；GitHub URL `xueyuanying/docs` 可保留为 redirect 或归档。

---

### P0-6 ⚠️ MCP Core 错误码 SSOT 身份未明示

**标准依据**：MCP §3 错误契约 10 分锚点「可用于 agent 自动分支」+ 公共基线「跨文档错误码 SSOT 必须明示下游引用方」

**现状**：tronlink-mcp-core「标准化响应格式」节包含错误码表（实际 SSOT），但**未明示**它是 mcp-server-tronlink / mcp-tronlink-signer / tronlink-cli 三个下游文档共用的 SSOT。读者首次进入 mcp-core 文档无法判断错误码表的权威性。

**整改**：错误码表头加：

```markdown
## 错误码

> **SSOT**：本表是 [mcp-server-tronlink](mcp-server-tronlink.md)、[mcp-tronlink-signer](mcp-tronlink-signer.md)、[tronlink-cli](tronlink-cli.md) 三个下游文档共用的错误码权威源。任何错误码新增 / 修改 / 删除均需先在本表更新，下游同步引用。变更需在 CHANGELOG 标注 breaking / non-breaking。

| Code | Retryable | Hint | Typical Trigger |
| ---- | :---: | ---- | ---- |
| TL_CLICK_FAILED | true | 重试前先 screenshot 确认 UI 状态 | ... |
| ...
```

**验收**：mcp-core 错误码表头部含 SSOT 声明；下游 3 文档的「error.code 枚举」段落改为「引用 mcp-core 错误码（SSOT），不在此重复」。

---

## 五、强建议整改（P1）

### P1-1 MCP Signer 头部缺「该用哪个」三选一对照表

**现状**：mcp-server-tronlink 多处提到「生产环境涉及资金转移的工具，优先用 `mcp-tronlink-signer`（浏览器审批），而非 Direct-API」（L570 / L651），但 mcp-tronlink-signer 文档头部**没有反向对照表**，新读者无法快速判断三者差异。

**整改**：在 mcp-tronlink-signer §「配置」之前加：

```markdown
## 该用哪个

| 选项 | HITL | 凭证 | 适用场景 |
|------|:---:|------|---------|
| `mcp-tronlink-signer`（本服务） | ✅ 浏览器审批 | 无（钱包在 TronLink 扩展） | 生产环境真实资金转移、需要用户每笔确认 |
| `mcp-server-tronlink` Direct-API 模式 | ❌ 无 | `AGENT_WALLET_PASSWORD` | CI / 自动化批量操作、非真实资金（测试网） |
| `tronlink-cli` | ✅ 浏览器审批 | 无 | Shell 脚本、终端工作流 |

如不确定，优先选 `mcp-tronlink-signer`（最安全的默认值）。
```

---

### P1-2 MCP Signer 缺 input schema 精选镜像

**现状**：mcp-server-tronlink 文档侧镜像了 7 个工具 input schema（`tl_chain_send` / `tl_chain_swap_v3` / `tl_chain_stake` 等）并 CI parity；mcp-tronlink-signer 完全不镜像，全依赖 `list_tools`。Agent 在没有 MCP 会话时无法离线编写工具调用。

**整改**：至少镜像 `send_trx` / `send_trc20` / `sign_typed_data` 3 个核心写工具的 input schema；加入同套 CI parity 检查覆盖范围。

---

### P1-3 跨文档代币 symbol 表不一致

**现状**：

| 文档 | 内置代币 symbol 表内容 |
|------|------|
| `tronlink-cli` AI 智能体使用一节 | USDT / USDD / USDC（3 个） |
| `tronlink-skills` §「内置代币快捷符号」 | TRX / USDT / USDC / WTRX / BTT / JST / SUN / WIN（8 个） |
| `reference/networks`（公共参考） | 当前不明（待核） |

差异：CLI 缺 BTT/JST/SUN/WIN/WTRX；Skills 缺 USDD。

**整改**：在 `reference/networks` 集中维护一份「常用代币合约 SSOT」（建议 ≥10 个：含 TRX / USDT / USDD / USDC / WTRX / BTT / JST / SUN / WIN 等），CLI / Skills / 其他文档统一引用，避免维护漂移。

---

### P1-4 MCP Core「与 mcp-server-tronlink 的关系」节缺决策矩阵

**现状**：mcp-core §「与 mcp-server-tronlink 的关系」存在，但未提供「何时用 mcp-core / 何时直接用 mcp-server-tronlink」的决策表。开发者拿到两个包不知道该选哪个。

**整改**：在该节加：

```markdown
| 场景 | 选 mcp-core | 选 mcp-server-tronlink |
|------|:---:|:---:|
| 自建定制 MCP server（嵌入业务逻辑） | ✅ | ❌ |
| 直接给 agent 用 | ❌ | ✅ |
| 扩展能力（自定义 Capability） | ✅ | ❌ |
| 测试 / mock | ✅ | ✅（带 e2e 模式） |
| 学习 MCP 框架 | ✅ | ❌ |
```

---

### P1-5 onchain.ts 缺 `chainTransferTrc20Flow` / `chainSwapV3Flow` 实现（同步 P0-2）

**现状**：见 P0-2。文档列了这两个但代码缺。

**整改方案**（任选其一）：

- **方案 A**：补实现（如果产品确实需要）—— 参考 `chainTransferTrxFlow` / 现有 swap 工具 `tl_chain_swap_v3` 写 flow 包装
- **方案 B**：文档删除这两行（如果产品决策不做 flow，只暴露原子工具）

---

### P1-6 MCP Server 文档头「快速开始」步骤 3 钱包路径 A/B 选择不直观

**现状**：钱包密码是高敏感凭证，路径 B 自动创建会**明文写入 `~/.agent-wallet/runtime_secrets.json`**（文档已明示）。新用户照默认走 A/B 任一即开搞，没有「场景 → 路径」决策表，agent 容易选错路径。

**整改**：在快速开始步骤 3 加：

```markdown
| 场景 | 推荐路径 | 原因 |
|------|---------|------|
| 生产环境（真实资金） | A — 手动创建 + secret manager | 路径 B 会明文落盘密码 |
| CI / 自动化（测试网） | A — 手动创建 + env injection | 同上 |
| 本地开发（一次性体验） | B — 自动创建 | 无需预配置，密码自动生成 |
| 临时 demo 演示 | B + tmpfs 目录 | 任务结束即销毁 |
```

---

### P1-7 mcp-tronlink-signer 与 tronlink-signer SDK 的版本对应关系不明

**现状**：mcp-tronlink-signer 文档说「将 [tronlink-signer](https://github.com/TronLink/mcp-tronlink-signer/tree/main/packages/tronlink-signer) 封装为 MCP 工具」—— 暗示 `tronlink-signer` 是 monorepo 子包。但：

1. 独立的 [tronlink-signer 文档页](https://docs.tronlink.org/zh/ai-support/tronlink-signer/) 存在
2. CLI 文档说 `tronlink-signer 0.1.4` 是依赖（暗示是独立 npm 包）
3. mcp-tronlink-signer 文档没说「我用的 tronlink-signer 版本是 N，与独立 SDK 文档对齐到 commit X」

读者不知道这 3 处的 `tronlink-signer` 是不是同一份代码。

**整改**：mcp-tronlink-signer 头部加：

```markdown
> **关系澄清**：本服务 = 把 [`tronlink-signer` SDK](tronlink-signer.md) v0.1.4 封装为 MCP server。SDK 与 wrapper 同 monorepo 维护，版本同步发布。直接用 SDK 见 [tronlink-signer](tronlink-signer.md)；用 MCP wrapper 见本页。
```

---

### P1-8 「依赖项」表的「数据截至 2026-05」需要定期更新机制

**现状**：mcp-server-tronlink / CLI / Skills 都有「数据截至 2026-05」标注（好）。但没有更新机制 —— 6 月、7 月数据漂移后谁来改？

**整改**：

1. 加 CI 任务：每月扫所有 `数据截至 YYYY-MM` 字样，超过 N 个月触发文档 issue 提醒
2. 或改为「Last verified: 2026-05-21」+ commit hash 引用，让 reader 知道这是固定快照

---

### P1-9 Skills 反例表的「正确路由」工具名应做 CI parity 检查

**现状**：mcp-server-tronlink 已经有 CI parity 检查工具名；Skills 反例表里的 `tl_chain_send` / `tl_chain_stake` / `tl_chain_swap_v3` 等工具名引用 mcp-server-tronlink，但跨文档的工具名引用没纳入 parity 检查。如果 mcp-server 改名 `tl_chain_send` → `tl_send_trx`，Skills 反例表会变成死引用。

**整改**：parity 脚本扩到扫 Skills 文档对 `tl_*` 名字的引用，与 mcp-server 实际 list_tools 输出 diff。

---

## 六、锦上添花（P2）

### MCP / CLI / 入口（8 条）

| # | 文档 | 问题 | 建议 |
|:-:|------|------|------|
| P2-1 | MCP Server | Use Cases 6 条概括，缺端到端 agent 对话示例 | 补 1-2 个对话示例（如 SunSwap V3 swap 端到端） |
| P2-2 | MCP Server | Flow Recipes 子类型表与 src/flows/ 文件名不直观对应 | 表格加 `Source File` 列（如 `chainCheckBalanceFlow → src/flows/onchain.ts`） |
| P2-3 | MCP Core | 52 工具定义节按数字分组（1-13）阅读时跳跃 | 加目录跳转或合并为表 |
| P2-4 | MCP Signer | 内联 changelog 与 GitHub releases 双源 | 加同步策略说明（如「内联 SSOT，GitHub release 滞后 7 天」） |
| P2-5 | CLI | 退出码 5「网络错误」缺「如何确认上一笔未上链」指引 | 加「查 `tronscan.org/#/transaction/<txID>` 或 `tronlink balance --address` 对账」 |
| P2-6 | CLI | 常用代币合约表 3 个（同 P1-3） | 扩到 ≥8 个或引用 reference/networks SSOT |
| P2-7 | AI/LLMs 入口 | 「给智能体的说明」缺版本契约引用 | 加一条「版本契约见各工具页 §兼容性与迁移策略」 |
| P2-8 | 全站 | 引用 GitHub commit hash 时缺「截至日期」 | 引用 commit 时加 `(as of YYYY-MM-DD)` |

### Skills（5 条，需协调产品组 owner）

| # | 文档 | 问题 | 建议 |
|:-:|------|------|------|
| Skill-P2-1 | Skills | 缺独立 Troubleshooting 章节 | 错误处理散在「安全模型」表里。独立成节覆盖 5 类：① agent 未识别 skill ② TronGrid 限流 ③ CLI-only 命令被 MCP 调用 ④ install.sh 故障路径 ⑤ 多 host 命令名冲突 |
| Skill-P2-2 | Skills | 内置代币 symbol 表与 CLI 不一致（同 P1-3） | 合到 `reference/networks` SSOT，Skills / CLI 引用 |
| Skill-P2-3 | Skills | TronGrid API Key 凭证管理一笔带过 | 补 5 维（存储 / 最小权限 / 轮换 / 泄漏检测 / 撤销） |
| Skill-P2-4 | Skills | 推荐工作流是流程图式路径 | 补 1-2 个端到端 agent 对话示例（如「100 TRX 换 USDT 划算吗？」串 token-price → kline → resource-info → swap-quote） |
| Skill-P2-5 | Skills | `mcp_server.mjs ↔ tron_api.mjs` 等价性靠人盯 | 加 CI parity 检查（参考 mcp-server-tronlink 的 `check_doc_schema_parity.py`） |

> **协调建议**：Skill-P2-2 / P2-5 与 P1-3 / P1-9 联动，建议两边一起整改一次性解决。

---

## 七、跨文档一致性 grep 清单

> 团队可逐项 grep 全站核对，建议加入 CI parity 检查。

| 检查项 | grep 命令 | 期望结果 |
|--------|-----------|----------|
| 错误码锚点存在 | `grep -rn "tronlink-mcp-core.md#错误码" docs/` | 引用方 3 处，目标节存在 |
| Flow Recipes 计数一致 | 对比文档表与 `src/flows/*.ts` 实际 export | 三方一致 |
| `chainTransferTrc20Flow` 不出现在文档（或代码补实现） | `grep -rn "chainTransferTrc20Flow\|chainSwapV3Flow" .` | 文档与代码同步 |
| 工具名 `tl_*` 引用统一 | 跨 mcp-server / mcp-signer / cli / skills grep `tl_chain_send` 等 | 全站命名一致 |
| 网络命名（mainnet / nile / shasta） | `grep -rn -iE "mainnet\|nile\|shasta\|niletest\|testnet" docs/` | 全站统一三档 |
| `@bankofai/agent-wallet` 版本 | `grep -rn "agent-wallet.*[0-9]\.[0-9]" docs/` | 文档版本与 npm 实际锁定一致 |
| 代币 symbol 表 SSOT | `grep -rn "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" docs/` | 仅在 reference/networks 出现一次 |
| GitHub 0 releases | `gh api repos/TronLink/{mcp-server-tronlink,...}/releases --jq 'length'` | 全部 > 0 |
| 个人 repo 引用 | `grep -rn "xueyuanying/docs" docs/` | 0（已迁到 org repo） |

---

## 八、整改 checklist

### P0（必改，6 项）

- [ ] **P0-1** mcp-core 加 `## 错误码` 二级标题，与 3 处死锚点对齐
- [ ] **P0-2** Flow Recipes：核对 23 实际 flow + 删除 / 补全 `chainTransferTrc20Flow` / `chainSwapV3Flow` + 文档加 `import-wallet` flow + 节标题计数更新
- [ ] **P0-3** `@bankofai/agent-wallet` 改为精确版本 + 决策是否升级 2.4.0 + 文档明示 GitHub 404 状态
- [ ] **P0-4** 5 个 TronLink npm 包回溯打 git tag + 创建 GitHub Release + npm publish CI 自动化
- [ ] **P0-5** docs 源码 repo 从 `xueyuanying/docs` 迁移到 `TronLink/docs` 或 `TronLink/developer-docs`
- [ ] **P0-6** mcp-core 错误码表加 SSOT 声明 + 下游 3 文档改为引用而非重复

### P1（强建议，9 项）

- [ ] **P1-1** mcp-tronlink-signer 头部加「该用哪个」三选一对照表
- [ ] **P1-2** mcp-tronlink-signer 补 input schema 镜像 3 个 + CI parity
- [ ] **P1-3** 代币 symbol 表合到 reference/networks SSOT
- [ ] **P1-4** mcp-core 加「与 mcp-server-tronlink」决策矩阵
- [ ] **P1-5** onchain.ts 补 chainTransferTrc20Flow / chainSwapV3Flow 实现（或文档删除）
- [ ] **P1-6** mcp-server 快速开始钱包路径 A/B 加「场景→路径」决策表
- [ ] **P1-7** mcp-tronlink-signer 头部澄清与 SDK 版本对应关系
- [ ] **P1-8** 「数据截至 YYYY-MM」改为「Last verified + commit」+ CI 提醒
- [ ] **P1-9** Skills `tl_*` 引用纳入 CI parity 检查

### P2（锦上添花，8 项 + 5 项 Skills）

#### MCP / CLI / 入口（8 项）

- [ ] **P2-1** MCP Server Use Cases 补端到端对话示例
- [ ] **P2-2** Flow Recipes 表加 Source File 列
- [ ] **P2-3** MCP Core 52 工具定义合并为表
- [ ] **P2-4** MCP Signer 内联 changelog 加同步策略
- [ ] **P2-5** CLI 退出码 5 加「如何确认上一笔未上链」指引
- [ ] **P2-6** CLI 常用代币合约表扩到 ≥8 个
- [ ] **P2-7** AI/LLMs 入口加版本契约引用
- [ ] **P2-8** GitHub commit hash 引用加「截至日期」

#### Skills（5 项，需协调产品组 owner）

- [ ] **Skill-P2-1** 加独立 §Troubleshooting 章节
- [ ] **Skill-P2-2** 代币 symbol 表合到 reference/networks SSOT
- [ ] **Skill-P2-3** 加 TronGrid API Key 凭证管理 5 维
- [ ] **Skill-P2-4** 推荐工作流至少 2 个配端到端 agent 对话示例
- [ ] **Skill-P2-5** 加 `mcp_server.mjs ↔ tron_api.mjs` CI parity workflow

---

## 九、标准锚点对照表

| 整改项 | 标准章节 / 锚点 |
|--------|----------------|
| 错误结构（code / retryable / hint） | MCP §3 / CLI §3 / 公共基线 §3 + §4 |
| 副作用 5 级（Safe / Network Read / Local Write / Remote Write / Destructive） | 公共基线 §2 |
| 错误码 SSOT 跨文档共享 | 公共基线 §4 + 项目级覆盖度 §0「串联关系」9 分锚点 |
| Schema 完整度（input/output + version） | MCP §3 |
| 机器可读输出（`--json` + schema） | CLI §3 |
| 退出码契约 + retryable | CLI §3 + §4 |
| 副作用分级标记 | MCP §6 P0 + CLI §6 P0 + 公共基线 §2 |
| 版本契约 / changelog | MCP §3 + CLI §3 + 公共基线 §8 |
| 风险隔离（dry-run / preview） | CLI §4 + 公共基线 §9 |
| 自发现入口（`--help` / `list_tools` / llms.txt） | 公共基线 §6 |
| AI 入口索引（llms.txt） | 项目级覆盖度 §0 + §0.2 |
| 跨文档引用 SSOT 不割裂 | 项目级覆盖度 §0「Schema / Error / Examples 串联」15% 权重 |
| Skill 反例表 + 判断口诀 | Skill §4.1「发现选择」10 分锚点 |
| Skill ↔ MCP 子集关系明示 | Skill §4.1 客户端兼容 + 版本契约 |

---

## 十、整改前后预期对比

| 文档 | 当前 | 整改 P0 后 | 整改 P0+P1 后 |
|------|:---:|:---:|:---:|
| MCP Server | 87.0 | 94 | 98 |
| MCP Core | 77.8 | 90 | 95 |
| MCP Signer | 88.0 | 92 | 96 |
| CLI | 94.0 | 97 | 99 |
| Skills | 98.5 | 98.5 | 100 |
| AI/LLMs 入口 | 100.0 | 100 | 100 |
| **平均** | **90.9** | **95.3** | **98.0** |

---

## 十一、与上一轮评审差距说明

上一轮（2026-05-22 首轮 review）我给出的评分是 6 文档平均 **97.8**（MCP Server 100 / CLI 100 / MCP Core 95.4 / MCP Signer 93 / Skills 98.5 / AI 入口 100）。本次重审下调到 **90.9**，差距 −6.9 分。**差距不是因为文档质量退步，而是评分深度提升**：

| 重审挖出的问题 | 上一轮是否漏 | 本轮发现路径 |
|----------------|:---:|------|
| `tronlink-mcp-core.md#错误码` 死锚点（3 处） | ❌ 漏 | grep 跨文档锚点 + 核对 mcp-core 章节 |
| Flow Recipes 文档 32 / 加总 24 / 代码 23 三方矛盾 | ⚠️ 仅指出 32 vs 24 | gh api 取 `src/flows/*.ts` 实际 export 计数 |
| `chainTransferTrc20Flow` / `chainSwapV3Flow` 文档列了但代码不存在 | ❌ 漏 | grep onchain.ts 实际 flow 名 |
| `bankofai/agent-wallet` GitHub 404 + 文档版本落后 | ❌ 漏 | gh api repo + curl npm registry 双向核对 |
| 5 个 repo 0 releases / 0 tags | ❌ 漏 | gh api releases / tags 系统性扫描 |
| docs.tronlink.org 源码托管在 `xueyuanying/docs` 个人 repo | ❌ 漏 | gh api 个人 repo + pushed_at 时间戳对齐 |
| 错误码 SSOT 身份未明示 | ⚠️ 仅 P1 | 重审升级，跨文档引用关系 |

**这一轮按更扎实的深度做**：grep 死链 + 核对源码 + npm registry 实测 + GitHub repo 活性 + 跨文档术语一致性。

**Skills 是 6 篇文档中唯一一份「重审无新发现」的样板** — 33/25/8 数字与代码完美对齐，`mcp_server.mjs ↔ tron_api.mjs` 同源 SSOT。

---

**评审完成。** 如对评分逻辑、整改优先级、参考实现有疑问可直接联系 PM。整改完成后可申请复评。

附：参考实现样板（按本标准达 A+ 级）：

- [`ai-support/mcp-server-tronlink`](https://docs.tronlink.org/zh/ai-support/mcp-server-tronlink/) 自身（整改 P0/P1 后）
- [`reference/error-code-map`](https://docs.tronlink.org/zh/reference/error-code-map/) — 五通道错误码对照表（含 retryable 列）
- [`zh/llms.txt`](https://docs.tronlink.org/zh/llms.txt) — `llms.txt` 实现样板
- [`scripts/check_doc_schema_parity.py`](https://github.com/xueyuanying/docs/blob/main/.github/workflows/check-doc-schema-parity.yml) — CI parity 实现样板（建议迁移到 TronLink org，见 P0-5）
