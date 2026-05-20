# TronLink Skills

## 概述

**GitHub**: [https://github.com/TronLink/tronlink-skills](https://github.com/TronLink/tronlink-skills)

**TronLink Wallet Skills** 是一套 AI Agent 技能集，通过自然语言提供完整的 TRON 区块链钱包和 DeFi 功能。专为 Claude Code、Cursor、OpenCode、Codex CLI 及其他 AI 代理设计。

**核心亮点：**
- **6 大技能，33 个命令**，涵盖钱包、代币研究、市场数据、兑换、资源和质押
- **零 npm 依赖**：使用原生 Node.js 18+ `fetch` 和 `crypto`，无需 `npm install`
- **TRON 专属领域知识** — 专门处理能量 + 带宽资源模型
- **多平台支持** — Claude Code、Cursor、OpenCode、Codex CLI、LangChain/CrewAI
- **纯只读安全设计**：所有命令均为查询操作，不涉及私钥或签名
- **MCP 服务封装**：为结构化 AI 代理集成提供标准接口

---

## 为什么需要 TronLink Skills？

TRON 的费用模型与 EVM 链有根本性不同。TRON 不使用统一的 Gas，而是使用**能量**（用于智能合约）和**带宽**（用于所有交易）。现有的 AI Agent 技能集均未覆盖：

- TRON 独特的资源模型和成本优化策略
- Stake 2.0（冻结 TRX 获取资源并赚取奖励）
- 超级代表（SR）投票机制
- 跨 SunSwap V2/V3 和 Sun.io 的 DEX 聚合
- 14 天解冻等待期及其影响

TronLink Skills 以深度 TRON 领域知识填补了这一空白。

---

## 架构设计

```
自然语言输入
         |
         v
AI 代理 (Claude Code / Cursor / OpenCode / 自定义)
         |
         v
tron_api.mjs (Node.js 18+, 原生 fetch, 零依赖)
    ├── 零 npm 依赖
    ├── TronGrid HTTP API（公共或带 API Key）
    └── Tronscan API 用于代币元数据
         |
         v
结构化 JSON → Agent 解读 → 自然语言回复
```

---

## 6 大技能详解

### 1. tron-wallet（6 个命令）

钱包查询与账户信息。

| 命令 | 说明 |
|------|------|
| `wallet-balance` | TRX 余额和冻结金额 |
| `token-balance` | 查询 TRC-20 代币余额 |
| `wallet-tokens` | 列出所有代币持仓 |
| `tx-history` | 最近交易历史 |
| `account-info` | 完整账户详情 |
| `validate-address` | 地址格式验证 |

**特点：** 同时支持 Base58Check（T...）和 hex 地址格式，内置常用代币符号，自动转换精度。

**何时不要用：** 发送 TRX / 代币——这些命令是只读的，请走 [signer SDK](tronlink-signer.md) 或 [MCP Server TronLink](mcp-server-tronlink.md)。代币层面的深度分析（rug-pull / 流动性锁定）请用 `tron-token`。

### 2. tron-token（7 个命令）

代币研究与安全分析。

| 命令 | 说明 |
|------|------|
| `token-info` | 元数据、发行量、发行方、社交链接 |
| `token-search` | 按名称/符号搜索代币 |
| `contract-info` | ABI、字节码、验证状态 |
| `token-holders` | 顶级持有者和持有者分析 |
| `trending-tokens` | 24 小时最高交易量代币 |
| `token-rankings` | 按市值、交易量、持有者、涨跌幅排序 |
| `token-security` | 安全审计（蜜罐、代理、所有者权限） |

**特点：** 检测 Rug Pull、分析持有者集中度、检查流动性锁定。

**何时不要用：** 单账户余额或交易历史——那是 `tron-wallet` 的活；实时价格/成交量——那是 `tron-market` 的活。

### 3. tron-market（8 个命令）

实时市场数据和巨鲸监控。

| 命令 | 说明 |
|------|------|
| `token-price` | 当前 USD/TRX 价格，24 小时变化 |
| `kline` | OHLCV K 线数据（1 分钟到 1 周） |
| `trade-history` | 最近 DEX 交易 |
| `dex-volume` | 买卖量、交易笔数 |
| `whale-transfers` | 大额转账（可配置阈值） |
| `large-transfers` | TRX 巨鲸活动 |
| `pool-info` | 流动性池（SunSwap V2/V3 TVL、APY） |
| `market-overview` | TRON 网络统计（价格、市值、交易量、活跃账户） |

**特点：** 多 DEX 聚合、智能资金信号检测、K 线分析。

**何时不要用：** 立刻执行 swap 报价或路径——那是 `tron-swap`（会算上滑点）；静态代币元数据——`tron-token`。

### 4. tron-swap（3 个命令）

DEX 兑换报价与路由优化。

| 命令 | 说明 |
|------|------|
| `swap-quote` | 预期产出、价格影响、滑点 |
| `swap-route` | 跨 SunSwap V2/V3、Sun.io 的最优路径（含多跳） |
| `tx-status` | 追踪交易状态 |

**特点：** 聚合多源流动性、估算能量成本、处理多跳路由。

**何时不要用：** 真正执行 swap——报价是只读的，实际兑换走 [MCP Server TronLink](mcp-server-tronlink.md)（`tl_chain_swap_v3`）或 signer SDK；历史成交数据——`tron-market`。

### 5. tron-resource（6 个命令）

能量与带宽管理 — TRON 专属。

| 命令 | 说明 |
|------|------|
| `resource-info` | 当前可用能量/带宽及已质押量 |
| `estimate-energy` | 智能合约调用的能量成本 |
| `estimate-bandwidth` | 带宽成本（每日免费额度：600） |
| `energy-price` | 当前每单位能量的 SUN 成本 |
| `energy-rental` | 查询租赁市场选项 |
| `optimize-cost` | 个性化建议（冻结 vs. 租赁 vs. 燃烧） |

**特点：** 成本优化决策树逻辑、追踪每日免费带宽、计算 TRX 燃烧等值。

**何时不要用：** 真正冻结 TRX 获取能量/带宽——那是 Remote Write，请走 signer SDK / MCP Server；冻结后的 SR 投票策略——见 `tron-staking`。

### 6. tron-staking（3 个命令）

Stake 2.0 查询与 SR 信息。

| 命令 | 说明 |
|------|------|
| `sr-list` | SR 列表，含投票数、出块率、APY |
| `staking-info` | 冻结金额、投票、未领奖励、待解冻 |
| `staking-apy` | 计算预估年化收益率 |

**特点：** Stake 2.0 状态查询、APY 计算、SR 佣金追踪。

**何时不要用：** 执行 freeze / 投票 / 解冻动作——这些是 Remote Write，请走 signer SDK / MCP Server；单次操作能量成本——`tron-resource`。

---

## 推荐技能组合工作流

### 余额与代币查询
```
tron-wallet（查余额）→ tron-wallet（列出代币）→ tron-resource（检查能量状态）
```

### 研究与兑换报价
```
tron-token（搜索）→ tron-market（价格/K线）→ tron-resource（检查能量）→ tron-swap（获取报价）
```

### 质押分析
```
tron-wallet（查余额）→ tron-staking（质押信息）→ tron-staking（APY 估算）→ tron-staking（SR 列表）
```

### 资源优化
```
tron-resource（检查状态）→ tron-resource（估算成本）→ tron-resource（optimize-cost）
```

---

## TRON 资源模型参考

### 能量 vs. 带宽

| 资源 | 消耗场景 | 免费额度 | 获取方式 |
|------|----------|----------|----------|
| **带宽** | 所有交易 | 600/天 | 冻结 TRX 或燃烧 TRX |
| **能量** | 仅智能合约 | 无 | 冻结 TRX、租赁或燃烧 TRX |

### 成本示例

> **数据截至 2026-05。** 能量数字会随合约升级（尤其是 USDT TRC-20）和网络参数变化；TRX 燃烧列用到的带宽/能量单价也会变。**仅作量级参考**，不是契约值。数据来源：TronGrid / Tronscan 交易采样与 TRON 网络参数。需要实时数值请用 `tron-resource` 的 `estimate-energy` / `estimate-bandwidth` 命令。

| 操作 | 带宽 | 能量 | TRX 燃烧量（无资源时） |
|------|------|------|------------------------|
| TRX 转账 | ~267 | 0 | 0（在免费额度内） |
| USDT 转账 | ~345 | ~65,000 | ~13-27 TRX |
| SunSwap 兑换 | ~345 | ~65,000-200,000 | ~13-40 TRX |
| 代币授权 | ~345 | ~30,000 | ~6-12 TRX |

### Stake 2.0 要点
- 冻结 TRX → 获取能量或带宽 → 投票给 SR → 赚取奖励
- 解冻需 **14 天等待期** 才能提取
- 解冻后投票重置；重新冻结后需重新投票
- 1 冻结 TRX ≈ 每天 4.5 能量——**动态值**：取决于全网总质押量；实时数请用 `tron-resource estimate-energy`。数据截至 2026-05。
- 投票奖励每 6 小时可领取一次

---

## 集成方式

### 方式一：Claude Code（推荐）

```bash
# 克隆后直接使用
git clone <repo>
cd tronlink-skills
claude   # 自动发现 SKILL.md 文件
```

只读操作无需 `npm install`。

### 方式二：MCP 服务器

```bash
# 注册为 MCP 服务器
claude mcp add tronlink -- node ~/.tronlink-skills/scripts/mcp_server.mjs

# 提供 25 个 MCP 工具，可被 Claude Desktop / Claude Code 直接调用
```

### 方式三：命令行直接使用

```bash
# 直接执行命令
node scripts/tron_api.mjs wallet-balance --address T地址...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs swap-quote --from TRX --to USDT --amount 100
```

### 方式四：其他 AI 平台

| 平台 | 集成方式 |
|------|----------|
| **Cursor / Windsurf** | 克隆仓库，使用 MCP 或直接读取技能文件 |
| **Codex CLI** | 软链接到 `~/.agents/skills/tronlink-skills` |
| **OpenCode** | 注册插件，软链接技能 |
| **LangChain / CrewAI** | 将 `tron_api.mjs` 封装为 Tool |

#### Cursor（Windsurf 配置同构）

`~/.cursor/mcp.json`:

```jsonc
{
  "mcpServers": {
    "tronlink-skills": {
      "command": "node",
      "args": ["/absolute/path/to/tronlink-skills/scripts/mcp_server.mjs"]
    }
  }
}
```

#### Codex CLI

```bash
# 将 skills 目录软链到 agent 发现路径
ln -s "$(pwd)/tronlink-skills" ~/.agents/skills/tronlink-skills
# 验证识别
codex skills list | grep tron
```

#### OpenCode

`~/.config/opencode/config.json`:

```jsonc
{
  "plugins": {
    "tronlink-skills": { "path": "/absolute/path/to/tronlink-skills" }
  }
}
```

#### LangChain / CrewAI（Python）

```python
from langchain_core.tools import Tool
import subprocess, json

def tron_call(cmd: str) -> dict:
    out = subprocess.check_output(
        ["node", "scripts/tron_api.mjs", *cmd.split()],
        cwd="/absolute/path/to/tronlink-skills",
    )
    return json.loads(out)

tron_wallet_balance = Tool.from_function(
    func=lambda addr: tron_call(f"wallet-balance --address {addr}"),
    name="tron_wallet_balance",
    description="TRX 余额与冻结量，地址为 TRON Base58（T...）字符串。",
)
```

### 快速安装脚本

```bash
# 自动安装到所有 AI 环境
bash install.sh

# 清洁卸载
bash uninstall.sh
```

---

## 配置说明

### 环境变量

```bash
# 可选：TronGrid API Key，获取更高请求频率
export TRONGRID_API_KEY="your-api-key"

# 可选：切换网络（默认：mainnet）
export TRON_NETWORK="mainnet"    # 或 "shasta" / "nile"
```

### 网络支持

| 网络 | 地址 | 用途 |
|------|------|------|
| 主网 | https://api.trongrid.io | 生产环境 |
| Shasta 测试网 | https://api.shasta.trongrid.io | 测试 |
| Nile 测试网 | https://nile.trongrid.io | 测试 |

### 内置代币快捷符号

| 符号 | 合约地址 |
|------|----------|
| TRX | 原生代币（无合约） |
| USDT | TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t |
| USDC | TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8 |
| WTRX | TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR |
| BTT | TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4 |
| JST | TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9 |
| SUN | TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S |
| WIN | TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7 |

---

## 项目结构

```
tronlink-skills/
├── README.md                          # 主文档
├── package.json                       # Node.js 配置文件
├── install.sh                         # 全环境自动安装脚本
├── uninstall.sh                       # 清洁卸载脚本
│
├── scripts/
│   ├── tron_api.mjs                   # 主 CLI（33 个命令，零依赖）
│   └── mcp_server.mjs                 # MCP 协议服务封装
│
├── skills/                            # 技能定义（自动发现）
│   ├── tron-wallet/SKILL.md
│   ├── tron-token/SKILL.md
│   ├── tron-market/SKILL.md
│   ├── tron-swap/SKILL.md
│   ├── tron-resource/SKILL.md
│   └── tron-staking/SKILL.md
│
├── docs/
│   ├── claude-integration-guide.md    # 3 种集成方式
│   ├── resource-model.md              # 能量与带宽深度解析
│   ├── staking-guide.md               # Stake 2.0 与 APY 说明
│   └── integration-guide.sh
│
├── .claude-plugin/                    # Claude Code 插件配置
├── .cursor-plugin/                    # Cursor IDE 插件配置
├── .opencode/                         # OpenCode 配置
├── .codex/                            # Codex CLI 安装说明
├── .claude/                           # 预配置测试命令
├── _meta.json                         # 技能注册元数据
└── LICENSE                            # MIT
```

---

## 依赖项

| 依赖 | 是否必需？ | 用途 |
|------|-----------|------|
| Node.js >= 18 | 是 | 运行时（原生 fetch、crypto） |
| npm install | 不需要 | 所有操作均无需安装任何 npm 依赖 |

---

## 安全模型

| 方面 | 实现方式 |
|------|----------|
| 纯只读设计 | 所有命令均为查询操作——不涉及私钥、签名或资金移动 |
| 副作用 | 每个命令都是 **Network Read**：调用公共 API,但不改变任何状态。所有命令均可安全重试,无需人工确认（HITL） |
| 无需密钥 | 仅可选 TRONGRID_API_KEY 用于提高请求频率 |
| 频率限制 | 公共 TronGrid API；使用 TRONGRID_API_KEY 获取更高限额 |
| 错误处理 | 失败均为查询类错误：限流（可重试,需退避）、网络错误（可重试）、地址/参数非法（不可重试——修正输入）。如需执行交易（转账、兑换、质押）,请使用 [signer SDK](tronlink-signer.md) 或 [MCP Server TronLink](mcp-server-tronlink.md)——这些技能本身从不签名或广播 |

---

## 地址格式支持

所有命令均支持并自动归一化两种格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| Base58Check | `T...`（34 字符） | 标准显示格式 |
| Hex | `41...`（42 个十六进制字符） | 内部表示格式 |

---

## 关键设计决策

1. **零依赖** — 无需 npm install，对 AI Agent 而言轻量且即时
2. **纯只读安全设计** — 所有命令均为查询操作，不涉及私钥或签名
3. **TRON 专属领域知识** — 为能量/带宽和 Stake 2.0 提供专门技能，尊重 TRON 独特架构
4. **多格式地址支持** — 透明处理 Base58Check 和 hex 两种格式
5. **代币符号解析** — 常用代币有内置快捷方式；未知合约可直接使用地址
6. **成本优化建议** — `optimize-cost` 命令提供个性化策略
7. **MCP 服务封装** — 为 Claude Desktop 和现代 AI Agent 提供结构化集成

---

## 快速开始

```bash
# 1. 克隆
git clone <repo>
cd tronlink-skills

# 2. 配合 Claude Code 使用（只读操作无需安装）
claude
> "查一下 T地址... 的 TRX 余额"
> "展示 TRON 上最热门的代币"
> "发送 USDT 需要多少能量？"
> "获取能量最好的方式是什么——冻结、租赁还是燃烧？"

# 3. 或直接使用命令行
node scripts/tron_api.mjs wallet-balance --address T地址...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs optimize-cost --address T地址...
```

## 版本与许可证

- **包：** `tronlink-skills` v1.0.1
- **许可证：** MIT —— `SPDX-License-Identifier: MIT`
- **变更记录 / 发布：** [https://github.com/TronLink/tronlink-skills/releases](https://github.com/TronLink/tronlink-skills/releases)
