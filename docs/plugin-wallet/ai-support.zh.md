## MCP Server TronLink 

### 概述

**mcp-server-tronlink** 是一个生产级的 Model Context Protocol (MCP) 服务器，使 AI 代理（Claude、GPT 等）能够通过自然语言与 TRON 区块链交互。基于 `@tronlink/mcp-core` 构建，提供跨两种互补操作模式的 **56+ 工具**。

**核心亮点：**
- 双模架构：**Playwright**（浏览器自动化）+ **Direct API**（链上操作）
- 32 个内置 Flow Recipe，带预检查和依赖解析
- 基于 `@noble/curves` 的非托管本地交易签名
- 多签管理，支持实时 WebSocket 监控
- 通过 GasFree 服务集成实现零 Gas TRC20 转账

---

### 架构设计

```
AI 代理 (Claude Desktop / Claude Code)
         | (MCP 协议 — stdio / JSON-RPC 2.0)
         v
TronLink MCP 服务器
├── Playwright 模式 ─── TronLinkSessionManager
│   └── 浏览器自动化 + TronLink 扩展 UI 控制
├── Direct API 模式
│   ├── TronLinkOnChainCapability   (14 个工具)
│   ├── TronLinkMultiSigCapability  (5 个工具)
│   └── TronLinkGasFreeCapability   (3 个工具)
├── 实用能力
│   ├── TronLinkBuildCapability     (扩展构建)
│   ├── TronLinkStateSnapshotCapability (UI 状态提取)
│   └── TRON Crypto Utils           (地址派生、签名、Base58)
└── Flow Recipes (32 个内置流程配方)
         |
         v
TronGrid API / 多签服务 / GasFree 服务
         |
         v
TRON 区块链
```

两种模式可同时运行，工具根据配置自动启用。

---

### 双模运行机制

#### 模式一：Playwright（浏览器自动化）

通过 Playwright Chromium 控制 TronLink Chrome 扩展。适用于 **E2E 测试、UI 验证和 DApp 交互**。

**能力：**
- 使用 `--load-extension` 标志启动浏览器加载 TronLink
- 从 Chrome API 自动检测扩展 ID
- 多标签页跟踪，自动角色分类（扩展 / 通知 / DApp / 其他）
- 基于 DOM 的状态提取（TRON 地址、TRX 余额、网络检测）
- Base64 编码的截图捕获
- 自动处理浏览器对话框（alert、confirm、prompt）

**27 个 Playwright 工具包括：** `tl_launch`、`tl_cleanup`、`tl_navigate`、`tl_click`、`tl_type`、`tl_screenshot`、`tl_accessibility_snapshot`、`tl_describe_screen` 等。

#### 模式二：Direct API（链上操作）

直接调用 TronGrid REST API——无需浏览器。适用于 **账户查询、转账、兑换、质押和多签管理**。

**22 个 API 工具分组：**

| 分组 | 工具数 | 说明 |
|------|--------|------|
| 链上操作 | 14 | 转账、质押、兑换、查询、多签设置 |
| 多签管理 | 5 | 权限查询、交易提交、WebSocket 监控 |
| GasFree | 3 | 零 Gas TRC20 转账 |

---

### 核心组件

#### 1. TronLinkSessionManager

完整的浏览器生命周期管理：

| 方法 | 说明 |
|------|------|
| `launch()` | 使用 TronLink 扩展初始化浏览器 |
| `getExtensionState()` | 从 UI 提取钱包状态 |
| `navigateToUrl()` | 导航到指定 URL |
| `navigateToNotification()` | 打开 TronLink 通知弹窗 |
| `screenshot()` | 捕获当前 UI 状态 |
| `getTrackedPages()` | 列出所有打开的浏览器标签页 |
| `cleanup()` | 优雅地关闭所有资源 |

**页面检测：** 自动检测 15 种 TronLink 界面：`home`、`login`、`settings`、`send`、`receive`、`sign`、`broadcast`、`assets`、`address_book`、`node_management`、`dapp_list`、`create_wallet`、`import_wallet`、`notification`、`unknown`。

#### 2. TronLinkOnChainCapability（14 个工具）

TronGrid 的直接 API 封装：

**查询操作：**
- `getAddress()` — 从配置的私钥派生 TRON 地址
- `getAccount()` — 余额、带宽、能量、权限
- `getTokens()` — TRC10 和 TRC20 代币余额
- `getTransaction()` — 按 txID 获取交易详情
- `getHistory()` — 分页查询交易历史
- `getStakingInfo()` — 质押状态（冻结金额、投票、解冻）

**交易操作：**
- `send()` — 转账 TRX、TRC10 或 TRC20 代币
- `stake()` — 冻结/解冻 TRX 获取带宽或能量（Stake 2.0）
- `resource()` — 代理/取消代理带宽或能量
- `swap()` — 通过 SunSwap V2 代币兑换
- `swapV3()` — 通过 SunSwap V3 智能路由代币兑换

**多签操作：**
- `setupMultisig()` — 配置多签权限
- `createMultisigTx()` — 创建未签名的多签交易
- `signMultisigTx()` — 签署多签交易

#### 3. TronLinkMultiSigCapability（5 个工具）

TRON 多签服务的 REST + WebSocket API：

- `queryAuth()` — 查询多签权限（所有者/活跃权限、阈值、权重）
- `submitTransaction()` — 提交签名交易（达到阈值时自动广播）
- `queryTransactionList()` — 带过滤条件的交易列表
- `connectWebSocket()` — 实时交易监控
- `disconnectWebSocket()` — 停止监控

**实现细节：** HmacSHA256 签名生成用于 API 认证，基于 UUID 的请求签名，同时支持 Nile 测试网和主网凭证。

#### 4. TronLinkGasFreeCapability（3 个工具）

通过 GasFree 服务实现零 Gas TRC20 转账：

- `getAccount()` — 查询资格、支持的代币、每日配额
- `getTransactions()` — 查询免 Gas 交易历史
- `send()` — 零 Gas 费发送 TRC20

#### 5. TRON 密码学工具

纯密码学函数——无外部服务调用：

```
privateKeyToAddress()      64 字符十六进制 → TRON 地址（base58 + hex）
signTransaction()          raw_data_hex → 65 字节签名
base58CheckEncode()        有效载荷 → base58check 编码地址
base58CheckDecode()        TRON 地址 → 21 字节有效载荷
addressToHex()             T 地址 → 0x41... 十六进制
hexToAddress()             0x41... → T 地址
```

使用 `@noble/curves`（secp256k1 ECDSA）和 `@noble/hashes`（Keccak-256、SHA256）。

---

### Flow Recipes（32 个内置流程）

预配置的多步骤工作流，带依赖检查和参数模板。

#### Playwright 流程
| 流程 | 说明 |
|------|------|
| `importWalletFlow` | 使用助记词导入钱包 |
| `switchNetworkFlow` | 切换到主网/Nile/Shasta |
| `enableTestNetworksFlow` | 启用测试网可见性 |
| `transferTrxFlow` | 通过 UI 进行 TRX 转账 |
| `transferTokenFlow` | 通过 UI 进行代币转账 |

#### 链上流程（11 个）
| 流程 | 说明 |
|------|------|
| `chainCheckBalanceFlow` | 查询余额 |
| `chainTransferTrxFlow` | 带预检查的 TRX 转账 |
| `chainTransferTrc20Flow` | 带预检查的 TRC20 转账 |
| `chainStakeFlow` | 质押 TRX |
| `chainUnstakeFlow` | 解除质押 TRX |
| `chainGetStakingFlow` | 查询质押信息 |
| `chainDelegateResourceFlow` | 代理带宽/能量 |
| `chainUndelegateResourceFlow` | 取消代理资源 |
| `chainSetupMultisigFlow` | 设置多签权限 |
| `chainCreateMultisigTxFlow` | 创建未签名的多签交易 |
| `chainSwapV3Flow` | SunSwap V3 代币兑换 |

#### 多签流程（6 个）
| 流程 | 说明 |
|------|------|
| `multisigQueryAuthFlow` | 查询权限 |
| `multisigListTransactionsFlow` | 列出待处理交易 |
| `multisigMonitorFlow` | WebSocket 实时监控 |
| `multisigStopMonitorFlow` | 停止监控 |
| `multisigSubmitTxFlow` | 提交签名交易 |
| `multisigCheckFlow` | 完整状态检查 |

#### GasFree 流程（3 个）
| 流程 | 说明 |
|------|------|
| `gasfreeCheckAccountFlow` | 查询资格 |
| `gasfreeTransactionHistoryFlow` | 查询历史 |
| `gasfreeSendFlow` | 免 Gas TRC20 转账 |

---

### 配置说明

#### 环境变量

**Playwright 模式：**

| 变量 | 说明 |
|------|------|
| `TRONLINK_EXTENSION_PATH` | TronLink 扩展构建目录 |
| `TRONLINK_SOURCE_PATH` | 启用构建能力 |
| `TL_MODE` | `e2e`（测试）或 `prod`（生产） |
| `TL_HEADLESS` | 浏览器无头模式 |
| `TL_SLOW_MO` | Playwright 慢动作延迟（毫秒） |

**TronGrid API：**

| 变量 | 说明 |
|------|------|
| `TL_TRONGRID_URL` | 全节点 API 地址 |
| `TL_TRONGRID_API_KEY` | API 密钥（主网必需） |
| `TL_CHAIN_PRIVATE_KEY` | 64 字符十六进制私钥 |
| `TL_SUNSWAP_ROUTER` | SunSwap V2 路由地址 |
| `TL_SUNSWAP_V3_ROUTER` | SunSwap V3 智能路由地址 |
| `TL_WTRX_ADDRESS` | WTRX 合约地址 |

**多签服务：**

| 变量 | 说明 |
|------|------|
| `TL_MULTISIG_BASE_URL` | API 基础地址 |
| `TL_MULTISIG_SECRET_ID` | 项目凭证 |
| `TL_MULTISIG_SECRET_KEY` | HmacSHA256 签名密钥 |
| `TL_MULTISIG_CHANNEL` | 渠道/项目名称 |
| `TL_MULTISIG_OWNER_KEY` | 所有者私钥 |
| `TL_MULTISIG_COSIGNER_KEY` | 联合签名者私钥 |

**GasFree 服务：**

| 变量 | 说明 |
|------|------|
| `TL_GASFREE_BASE_URL` | 服务地址 |
| `TL_GASFREE_API_KEY` | API 密钥 |
| `TL_GASFREE_API_SECRET` | API 密钥 |

#### 集成方式

**1. 项目级 MCP 配置（`.mcp.json`）**

Claude Code 自动检测：
```json
{
  "mcpServers": {
    "tronlink": {
      "command": "node",
      "args": ["./dist/index.js"],
      "env": {
        "TL_TRONGRID_URL": "https://nile.trongrid.io",
        "TL_CHAIN_PRIVATE_KEY": "你的64字符十六进制私钥"
      }
    }
  }
}
```

**2. Claude Desktop**

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`。

**3. Claude Code 全局设置**

编辑 `~/.claude/settings.json` 或 `.claude/settings.json`。

**4. 任意 MCP 客户端**

支持 stdio 传输协议——兼容任何符合 MCP 标准的客户端。

---

### 项目结构

```
mcp-server-tronlink/
├── src/
│   ├── index.ts                    ## 服务入口、配置、能力注册
│   ├── session-manager.ts          ## 浏览器生命周期（TronLinkSessionManager）
│   ├── capabilities/
│   │   ├── on-chain.ts             ## 14 个链上操作（TronGrid）
│   │   ├── multisig.ts             ## 5 个多签操作（REST + WS）
│   │   ├── gasfree.ts              ## 3 个免 Gas 转账操作
│   │   ├── build.ts                ## 扩展 webpack 构建
│   │   ├── state-snapshot.ts       ## UI 状态提取
│   │   └── tron-crypto.ts          ## 地址派生、签名、Base58
│   └── flows/
│       ├── index.ts                ## 流程注册（32 个配方）
│       ├── import-wallet.ts        ## 钱包导入流程
│       ├── switch-network.ts       ## 网络切换流程
│       ├── transfer-trx.ts         ## 转账流程
│       ├── multisig.ts             ## 6 个多签流程
│       ├── onchain.ts              ## 11 个链上流程
│       └── gasfree.ts              ## 3 个免 Gas 流程
├── dist/                           ## 编译输出
├── .mcp.json                       ## MCP 配置
├── .env.example                    ## 环境变量参考
├── package.json
├── tsconfig.json
└── README.md
```

---

### 依赖项

| 包名 | 版本 | 用途 |
|------|------|------|
| `@noble/curves` | ^2.0.1 | secp256k1 ECDSA 签名 |
| `@noble/hashes` | ^2.0.1 | Keccak-256、SHA256 |
| `@tronlink/mcp-core` | 本地 | 核心 MCP 服务框架 |
| `playwright` | ^1.49.0 | 浏览器自动化 |
| `ws` | ^8.18.0 | WebSocket（多签监控） |

---

### 安全模型

| 方面 | 实现方式 |
|------|----------|
| 密钥存储 | 通过 MCP JSON `env` 字段注入，不使用 `.env` 文件 |
| 密钥暴露 | 不向 stderr 记录任何密钥信息 |
| 签名方式 | 本地交易签名——密钥不会被传输 |
| 预检查 | 所有交易在执行前验证 |
| Git 安全 | 配置文件在 `.gitignore` 中防止意外提交 |
| 默认网络 | Nile 测试网，安全默认值 |

---

### 典型使用场景

1. **钱包自动化** — 导入钱包、查询余额、发起转账
2. **DApp 测试** — 启动浏览器、连接钱包、签署交易、验证状态
3. **链上交易** — 直接 API 兑换、质押、无需浏览器的代币转账
4. **多签工作流** — 设置权限、提交/监控交易
5. **免 Gas 操作** — 无需 TRX 余额即可完成 TRC20 转账
6. **基础设施测试** — 合约部署、固件管理、Mock 服务

---

### 快速开始

```bash
## 1. 构建
npm install && npm run build

## 2. 配置（Nile 测试网示例）
export TL_TRONGRID_URL="https://nile.trongrid.io"
export TL_CHAIN_PRIVATE_KEY="你的64字符十六进制私钥"

## 3. 配合 Claude Code 使用
## 添加到 .mcp.json 后自然语言使用：
## "查看我的 TRX 余额"
## "给 TAddress... 转 10 个 TRX"
## "在 SunSwap V3 上用 100 TRX 兑换 USDT"
```


## TronLink MCP Core 

### 概述

**@tronlink/mcp-core** 是构建 TronLink MCP（Model Context Protocol）服务器的基础框架库。它不是独立应用——使用者必须实现 `ISessionManager` 接口并注入能力模块来创建可运行的服务器。

**核心亮点：**
- 接口驱动的可插拔架构，提供 **9 个能力接口**
- **56+ 预定义工具处理器**，使用 Zod 验证 Schema
- 内置 Knowledge Store，支持跨会话学习和步骤回放
- Flow Recipe 系统，将多步骤工作流程模板化
- 标准化响应格式，25+ 错误码
- 双模支持：Playwright（UI 自动化）+ Direct API（链上操作）

---

### 架构设计

```
┌─ AI 代理 (Claude, GPT 等)
│
├─ MCP 协议 (stdio / JSON-RPC 2.0)
│
├─ MCP 服务器实例 (createMcpServer)
│  ├─ 56+ tl_* 工具处理器
│  ├─ Knowledge Store（跨会话持久化）
│  ├─ Flow Registry（流程管理）
│  └─ Discovery 工具
│
├─ ISessionManager 接口（使用者实现）
│  ├─ 会话生命周期
│  ├─ 页面/标签管理
│  ├─ 能力注入（9 个接口）
│  └─ 环境模式 (e2e / prod)
│
├─ 能力系统（9 个可插拔接口）
│  ├─ BuildCapability
│  ├─ FixtureCapability
│  ├─ ChainCapability
│  ├─ ContractSeedingCapability
│  ├─ StateSnapshotCapability
│  ├─ MockServerCapability
│  ├─ OnChainCapability
│  ├─ MultiSigCapability
│  └─ GasFreeCapability
│
└─ 可选: Playwright（浏览器自动化）
```

**设计原则：**
1. **接口驱动** — 所有主要组件使用接口实现可扩展性
2. **组合优于继承** — 能力通过注入，而非继承
3. **单例模式** — SessionManager、KnowledgeStore、FlowRegistry 使用全局持有者
4. **预检查** — 链上工具在执行前验证
5. **数据脱敏** — Knowledge Store 自动屏蔽敏感字段

---

### 与 mcp-server-tronlink 的关系

| 维度 | tronlink-mcp-core | mcp-server-tronlink |
|------|-------------------|---------------------|
| 类型 | 核心库（框架） | 独立 MCP 服务器 |
| 角色 | 定义接口、工具、协议 | 具体实现 |
| 使用方式 | 通过 npm 导入并扩展 | 直接 CLI 调用 |
| 可扩展性 | 9 个可插拔能力接口 | 预配置能力 |
| 依赖关系 | 无（它本身就是依赖） | 依赖 @tronlink/mcp-core |

**mcp-server-tronlink 是 tronlink-mcp-core 的使用者。** 核心库定义了工具"是什么"；服务器提供了工具"怎么工作"。

---

### ISessionManager 接口

使用者必须实现的关键接口（25+ 方法）：

#### 会话生命周期
```typescript
hasActiveSession(): boolean
getSessionId(): string
getSessionState(): SessionState
getSessionMetadata(): SessionMetadata
launch(input: LaunchInput): Promise<LaunchResult>
cleanup(): Promise<void>
```

#### 页面管理
```typescript
getPage(): Page
setActivePage(page: Page): void
getTrackedPages(): TrackedPage[]
classifyPageRole(page: Page): PageRole
getContext(): ContextInfo
```

#### 扩展状态
```typescript
getExtensionState(): Promise<ExtensionState>
```

#### 无障碍引用
```typescript
setRefMap(map: Map<string, any>): void
getRefMap(): Map<string, any>
clearRefMap(): void
resolveA11yRef(ref: string): any
```

#### 导航
```typescript
navigateToHome(): Promise<void>
navigateToSettings(): Promise<void>
navigateToUrl(url: string): Promise<void>
navigateToNotification(): Promise<void>
waitForNotificationPage(timeoutMs?: number): Promise<Page>
```

#### 截图
```typescript
screenshot(options?: ScreenshotOptions): Promise<ScreenshotResult>
```

#### 能力获取器（9 个，均可选）
```typescript
getBuildCapability(): BuildCapability | undefined
getFixtureCapability(): FixtureCapability | undefined
getChainCapability(): ChainCapability | undefined
getContractSeedingCapability(): ContractSeedingCapability | undefined
getStateSnapshotCapability(): StateSnapshotCapability | undefined
getMockServerCapability(): MockServerCapability | undefined
getOnChainCapability(): OnChainCapability | undefined
getMultiSigCapability(): MultiSigCapability | undefined
getGasFreeCapability(): GasFreeCapability | undefined
```

#### 环境
```typescript
getEnvironmentMode(): 'e2e' | 'prod'
setContext(context: string, options?: any): Promise<void>
getContextInfo(): ContextInfo
```

---

### 9 个能力接口

每个能力都是可选的，可独立注入：

#### 1. BuildCapability
从源码构建 TronLink 扩展。

#### 2. FixtureCapability
管理钱包状态 JSON（default、onboarding、自定义预设）。

#### 3. ChainCapability
控制本地 TRON 节点（tron-quickstart 等）。

#### 4. ContractSeedingCapability
部署智能合约（TRC20/721/1155/10/multisig/staking/energy_rental）。

#### 5. StateSnapshotCapability
从 UI 提取钱包状态（界面、地址、余额、能量、带宽）。

#### 6. MockServerCapability
用于隔离测试的 Mock API 服务器。

#### 7. OnChainCapability
通过 TronGrid REST API 的直接链上操作（14 个方法）：
- 查询：`getAddress`、`getAccount`、`getTokens`、`getTransaction`、`getHistory`、`getStakingInfo`
- 交易：`send`、`stake`、`resource`、`swap`、`swapV3`
- 多签：`setupMultisig`、`createMultisigTx`、`signMultisigTx`

#### 8. MultiSigCapability
多签服务集成（REST + WebSocket，5 个方法）。

#### 9. GasFreeCapability
零 Gas TRC20 转账服务（3 个方法）。

---

### 56+ 工具定义

所有工具使用 `tl_` 前缀，分为 13 个类别：

#### 1. 会话管理（2 个）
| 工具 | 说明 |
|------|------|
| `tl_launch` | 启动带扩展的浏览器 |
| `tl_cleanup` | 关闭浏览器和服务 |

#### 2. 状态与发现（4 个）
| 工具 | 说明 |
|------|------|
| `tl_get_state` | 获取钱包状态 |
| `tl_describe_screen` | 包含状态 + testIds + a11y + 截图的界面描述 |
| `tl_list_testids` | 列出 data-testid 属性 |
| `tl_accessibility_snapshot` | 获取带引用的无障碍树 (e1, e2...) |

#### 3. 导航（4 个）
| 工具 | 说明 |
|------|------|
| `tl_navigate` | 导航到 TronLink 界面或 URL |
| `tl_switch_to_tab` | 按角色/URL 切换标签页 |
| `tl_close_tab` | 关闭标签页 |
| `tl_wait_for_notification` | 等待确认弹窗 |

#### 4. UI 交互（6 个）
| 工具 | 说明 |
|------|------|
| `tl_click` | 点击元素（a11yRef、testId、selector） |
| `tl_type` | 在输入框中输入文本 |
| `tl_wait_for` | 等待元素状态 |
| `tl_scroll` | 滚动页面/元素 |
| `tl_keyboard` | 发送键盘事件 |
| `tl_evaluate` | 执行 JavaScript |

#### 5. 截图与剪贴板（2 个）
| 工具 | 说明 |
|------|------|
| `tl_screenshot` | 捕获屏幕 |
| `tl_clipboard` | 读写剪贴板 |

#### 6. 合约部署 — 仅 e2e（4 个）
| 工具 | 说明 |
|------|------|
| `tl_seed_contract` | 部署单个合约 |
| `tl_seed_contracts` | 批量部署合约 |
| `tl_get_contract_address` | 查询合约地址 |
| `tl_list_contracts` | 列出已部署合约 |

#### 7. 上下文管理（2 个）
| 工具 | 说明 |
|------|------|
| `tl_set_context` | 切换 e2e/prod 模式 |
| `tl_get_context` | 获取上下文信息 |

#### 8. Knowledge Store（4 个）
| 工具 | 说明 |
|------|------|
| `tl_knowledge_last` | 获取最近 N 个步骤 |
| `tl_knowledge_search` | 搜索历史 |
| `tl_knowledge_summarize` | 生成配方 |
| `tl_knowledge_sessions` | 列出会话 |

#### 9. Flow Recipes（1 个）
| 工具 | 说明 |
|------|------|
| `tl_list_flows` | 列出/获取流程配方 |

#### 10. 批量执行（1 个）
| 工具 | 说明 |
|------|------|
| `tl_run_steps` | 顺序执行多个步骤 |

#### 11. 链上操作（14 个）
| 工具 | 说明 |
|------|------|
| `tl_chain_get_address` | 从私钥获取地址 |
| `tl_chain_get_account` | 查询账户详情 |
| `tl_chain_get_tokens` | 查询 TRC10/TRC20 余额 |
| `tl_chain_send` | 发送 TRX/TRC10/TRC20 |
| `tl_chain_get_tx` | 获取交易详情 |
| `tl_chain_get_history` | 查询交易历史 |
| `tl_chain_stake` | 冻结/解冻 TRX (Stake 2.0) |
| `tl_chain_get_staking` | 查询质押信息 |
| `tl_chain_resource` | 代理/取消代理资源 |
| `tl_chain_swap` | SunSwap V2 兑换 |
| `tl_chain_swap_v3` | SunSwap V3 兑换 |
| `tl_chain_setup_multisig` | 配置多签权限 |
| `tl_chain_create_multisig_tx` | 创建未签名多签交易 |
| `tl_chain_sign_multisig_tx` | 签署多签交易 |

#### 12. 多签管理（5 个）
| 工具 | 说明 |
|------|------|
| `tl_multisig_query_auth` | 查询多签权限 |
| `tl_multisig_submit_tx` | 提交签名交易 |
| `tl_multisig_list_tx` | 列出多签交易 |
| `tl_multisig_connect_ws` | 连接 WebSocket |
| `tl_multisig_disconnect_ws` | 断开 WebSocket |

#### 13. GasFree（3 个）
| 工具 | 说明 |
|------|------|
| `tl_gasfree_get_account` | 查询资格与配额 |
| `tl_gasfree_get_transactions` | 查询交易历史 |
| `tl_gasfree_send` | 零 Gas 发送 |

---

### 标准化响应格式

所有工具返回一致的结构：

```typescript
// 成功
{
  ok: true,
  result: { /* 工具特定数据 */ },
  meta: {
    timestamp: "2026-03-09T10:15:23.456Z",
    sessionId: "tl-1741504523",
    durationMs: 234
  }
}

// 错误
{
  ok: false,
  error: {
    code: "TL_CLICK_FAILED",       // 25+ 错误码之一
    message: "Element not found",
    details: { /* 可选 */ }
  },
  meta: { timestamp, sessionId, durationMs }
}
```

---

### Knowledge Store

跨会话学习和步骤回放系统。

#### 存储结构
```
test-artifacts/llm-knowledge/
├── tl-1741504523/
│   ├── session.json
│   └── steps/
│       ├── 2026-03-09T10-15-23-456Z-tl_click.json
│       └── ...
└── tl-1741504600/
    └── ...
```

#### 特性
- **自动记录：** 每次工具调用都被记录（时间戳、界面、目标、结果）
- **敏感数据脱敏：** 密码、助记词、私钥、种子自动屏蔽
- **搜索：** 按工具名、界面、testId、无障碍名称查询
- **摘要生成：** 从会话历史生成可复用的"配方"
- **会话管理：** 带元数据的会话列表

---

### Flow Recipe 系统

将常见多步骤工作流程模板化，支持参数替换。

#### FlowRecipe 结构
```typescript
{
  id: "transfer_trx",
  name: "发送 TRX",
  description: "向另一个地址转账 TRX",
  context: "both",                      // "playwright" | "api" | "both"
  preconditions: ["钱包已解锁"],
  params: [
    { name: "recipient", description: "目标 TRON 地址", required: true },
    { name: "amount", description: "TRX 金额", required: true }
  ],
  steps: [
    { tool: "navigate", input: { target: "send" } },
    { tool: "type", input: { testId: "address-input", text: "{{recipient}}" } },
    { tool: "type", input: { testId: "amount-input", text: "{{amount}}" } },
    { tool: "click", input: { a11yRef: "e5" } }
  ],
  tags: ["transfer", "basic"]
}
```

---

### 元素定位（3 种方式）

```typescript
// 1. 无障碍引用（推荐）
tl_click({ a11yRef: "e5" })

// 2. data-testid
tl_click({ testId: "send-button" })

// 3. CSS 选择器
tl_click({ selector: ".confirm-btn" })
```

无障碍引用来自 `tl_accessibility_snapshot` 输出——最可靠的定位方式。

---

### 安装与使用

#### 安装
```bash
npm install @tronlink/mcp-core
```

#### 基础使用
```typescript
import {
  createMcpServer,
  setSessionManager,
  type ISessionManager,
} from '@tronlink/mcp-core';

// 1. 实现 ISessionManager
class MySessionManager implements ISessionManager {
  // ... 实现全部 25+ 方法
}

// 2. 注册
setSessionManager(new MySessionManager());

// 3. 创建并启动服务器
const server = createMcpServer({
  name: 'My TronLink Server',
  version: '1.0.0',
});

await server.start();
```

---

### 项目结构

```
tronlink-mcp-core/
├── src/
│   ├── index.ts                           ## 公共 API 导出
│   ├── mcp-server/
│   │   ├── server.ts                      ## createMcpServer() 工厂函数
│   │   ├── session-manager.ts             ## ISessionManager 接口
│   │   ├── knowledge-store.ts             ## 持久化步骤记录
│   │   ├── discovery.ts                   ## 页面检查工具
│   │   ├── schemas.ts                     ## Zod 验证 Schema
│   │   ├── constants.ts                   ## 超时、限制、URL、界面常量
│   │   ├── tools/                         ## 56+ 工具处理器
│   │   ├── types/                         ## 类型定义
│   │   └── utils/                         ## 工具函数
│   ├── capabilities/
│   │   ├── types.ts                       ## 9 个能力接口
│   │   └── context.ts                     ## 环境配置类型
│   ├── flows/
│   │   ├── types.ts                       ## FlowRecipe 类型
│   │   └── registry.ts                    ## FlowRegistry 类
│   ├── launcher/
│   │   ├── extension-id-resolver.ts       ## 扩展 ID 提取
│   │   └── extension-readiness.ts         ## 扩展加载检测
│   └── utils/
│       └── index.ts                       ## 工具函数
├── dist/                                  ## 编译输出 + .d.ts
├── package.json
├── tsconfig.json
└── README.md
```

---

### 依赖项

| 包名 | 版本 | 用途 |
|------|------|------|
| `@modelcontextprotocol/sdk` | ^1.12.0 | MCP 协议实现 |
| `zod` | ^3.23.0 | 输入验证 Schema |

**可选对等依赖：**

| 包名 | 版本 | 用途 |
|------|------|------|
| `playwright` | ^1.49.0 | 浏览器自动化（仅 Playwright 模式） |
| `@playwright/test` | ^1.49.0 | 测试工具 |

---

### 构建与开发

```bash
npm run build      ## 编译 TypeScript 到 dist/
npm run dev        ## 监视模式
npm run test       ## 运行 Vitest 测试
npm run lint       ## ESLint
npm run clean      ## 删除 dist/
```

---

### 关键设计模式

1. **全局单例** — `setSessionManager()` / `getSessionManager()`，`setKnowledgeStore()` / `getKnowledgeStore()`，`FlowRegistry.getInstance()`
2. **组合优于继承** — 能力通过 getter 方法注入，而非类层次结构
3. **接口隔离** — 每个能力都有专注的最小接口
4. **预检查** — 链上工具在发送交易前验证余额、权限、配额
5. **数据脱敏** — Knowledge Store 自动屏蔽 password、mnemonic、private_key、seed 字段
6. **标准化响应** — 所有 56+ 工具使用一致的 `{ ok, result/error, meta }` 结构
7. **模板系统** — Flow Recipes 使用 `{{param}}` 占位符实现可复用工作流


## TronLink Skills 

### 概述

**TronLink Wallet Skills** 是一套 AI Agent 技能集，通过自然语言提供完整的 TRON 区块链钱包和 DeFi 功能。专为 Claude Code、Cursor、OpenCode、Codex CLI 及其他 AI 代理设计。

**核心亮点：**
- **6 大技能，41 个命令**，涵盖钱包、代币研究、市场数据、兑换、资源和质押
- **零 npm 依赖**：所有只读操作使用原生 Node.js 18+ `fetch` 和 `crypto`
- **TRON 专属领域知识** — 专门处理能量 + 带宽资源模型
- **多平台支持** — Claude Code、Cursor、OpenCode、Codex CLI、LangChain/CrewAI
- **人工确认机制**：所有涉及资金移动的操作需用户确认
- **MCP 服务封装**：为结构化 AI 代理集成提供标准接口

---

### 为什么需要 TronLink Skills？

TRON 的费用模型与 EVM 链有根本性不同。TRON 不使用统一的 Gas，而是使用**能量**（用于智能合约）和**带宽**（用于所有交易）。现有的 AI Agent 技能集均未覆盖：

- TRON 独特的资源模型和成本优化策略
- Stake 2.0（冻结 TRX 获取资源并赚取奖励）
- 超级代表（SR）投票机制
- 跨 SunSwap V2/V3 和 Sun.io 的 DEX 聚合
- 14 天解冻等待期及其影响

TronLink Skills 以深度 TRON 领域知识填补了这一空白。

---

### 架构设计

```
自然语言输入
         |
         v
AI 代理 (Claude Code / Cursor / OpenCode / 自定义)
         |
         v
tron_api.mjs (Node.js 18+, 原生 fetch, 1,248 行)
    ├── 只读操作零依赖
    ├── 可选: tronweb 用于签名
    ├── TronGrid HTTP API（公共或带 API Key）
    └── Tronscan API 用于代币元数据
         |
         v
结构化 JSON → Agent 解读 → 自然语言回复
```

---

### 6 大技能详解

#### 1. tron-wallet（8 个命令）

钱包管理与基础操作。

| 命令 | 说明 |
|------|------|
| `wallet-balance` | TRX 余额和冻结金额 |
| `token-balance` | 查询 TRC-20 代币余额 |
| `wallet-tokens` | 列出所有代币持仓 |
| `tx-history` | 最近交易历史 |
| `account-info` | 完整账户详情 |
| `validate-address` | 地址格式验证 |
| `send-trx` | 转账 TRX（需私钥） |
| `send-token` | 转账 TRC-20 代币（需私钥） |

**特点：** 同时支持 Base58Check（T...）和 hex 地址格式，内置常用代币符号，自动转换精度。

#### 2. tron-token（7 个命令）

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

#### 3. tron-market（8 个命令）

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

#### 4. tron-swap（5 个命令）

DEX 交易与兑换执行。

| 命令 | 说明 |
|------|------|
| `swap-quote` | 预期产出、价格影响、滑点 |
| `swap-route` | 跨 SunSwap V2/V3、Sun.io 的最优路径（含多跳） |
| `swap-approve` | ERC20 风格的代币授权 |
| `swap-execute` | 执行兑换（需用户确认） |
| `tx-status` | 追踪兑换交易状态 |

**特点：** 聚合多源流动性、估算能量成本、处理多跳路由、强制人工确认。

#### 5. tron-resource（7 个命令）

能量与带宽管理 — TRON 专属。

| 命令 | 说明 |
|------|------|
| `resource-info` | 当前可用能量/带宽及已质押量 |
| `estimate-energy` | 智能合约调用的能量成本 |
| `estimate-bandwidth` | 带宽成本（每日免费额度：600） |
| `energy-price` | 当前每单位能量的 SUN 成本 |
| `delegate-resource` | 不转账 TRX 即可发送资源给他人 |
| `energy-rental` | 查询租赁市场选项 |
| `optimize-cost` | 个性化建议（冻结 vs. 租赁 vs. 燃烧） |

**特点：** 成本优化决策树逻辑、追踪每日免费带宽、计算 TRX 燃烧等值。

#### 6. tron-staking（8 个命令）

Stake 2.0 和 SR 投票。

| 命令 | 说明 |
|------|------|
| `stake-freeze` | 冻结 TRX 获取能量或带宽 |
| `stake-unfreeze` | 开始 14 天解冻等待期 |
| `stake-withdraw` | 提取已解冻的 TRX |
| `vote` | 投票给超级代表（1 冻结 TRX = 1 票） |
| `claim-rewards` | 领取投票奖励（每 6 小时可领一次） |
| `sr-list` | SR 列表，含投票数、出块率、APY |
| `staking-info` | 冻结金额、投票、未领奖励、待解冻 |
| `staking-apy` | 计算预估年化收益率 |

**特点：** 完整 Stake 2.0 支持、14 天解锁管理、APY 计算、SR 佣金追踪。

---

### 推荐技能组合工作流

#### 查余额 & 转账
```
tron-wallet（查余额）→ tron-resource（估算能量）→ tron-wallet（发送）
```

#### 研究 & 买入
```
tron-token（搜索）→ tron-market（价格/K线）→ tron-resource（检查能量）→ tron-swap（执行）
```

#### 质押流程
```
tron-wallet（查余额）→ tron-staking（冻结）→ tron-staking（投票）→ tron-staking（领奖）
```

#### 资源优化
```
tron-resource（检查状态）→ tron-resource（估算成本）→ tron-staking（冻结）或 tron-resource（租赁）
```

---

### TRON 资源模型参考

#### 能量 vs. 带宽

| 资源 | 消耗场景 | 免费额度 | 获取方式 |
|------|----------|----------|----------|
| **带宽** | 所有交易 | 600/天 | 冻结 TRX 或燃烧 TRX |
| **能量** | 仅智能合约 | 无 | 冻结 TRX、租赁或燃烧 TRX |

#### 成本示例

| 操作 | 带宽 | 能量 | TRX 燃烧量（无资源时） |
|------|------|------|------------------------|
| TRX 转账 | ~267 | 0 | 0（在免费额度内） |
| USDT 转账 | ~345 | ~65,000 | ~13-27 TRX |
| SunSwap 兑换 | ~345 | ~65,000-200,000 | ~13-40 TRX |
| 代币授权 | ~345 | ~30,000 | ~6-12 TRX |

#### Stake 2.0 要点
- 冻结 TRX → 获取能量或带宽 → 投票给 SR → 赚取奖励
- 解冻需 **14 天等待期** 才能提取
- 解冻后投票重置；重新冻结后需重新投票
- 1 冻结 TRX ≈ 每天 4.5 能量
- 投票奖励每 6 小时可领取一次

---

### 集成方式

#### 方式一：Claude Code（推荐）

```bash
## 克隆后直接使用
git clone <repo>
cd tronlink-skills
claude   ## 自动发现 SKILL.md 文件
```

只读操作无需 `npm install`。

#### 方式二：MCP 服务器

```bash
## 注册为 MCP 服务器
claude mcp add tronlink -- node ~/.tronlink-skills/scripts/mcp_server.mjs

## 提供 25 个 MCP 工具，可被 Claude Desktop / Claude Code 直接调用
```

#### 方式三：命令行直接使用

```bash
## 直接执行命令
node scripts/tron_api.mjs wallet-balance --address T地址...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs swap-quote --from TRX --to USDT --amount 100
```

#### 方式四：其他 AI 平台

| 平台 | 集成方式 |
|------|----------|
| **Cursor / Windsurf** | 克隆仓库，使用 MCP 或直接读取技能文件 |
| **Codex CLI** | 软链接到 `~/.agents/skills/tronlink-skills` |
| **OpenCode** | 注册插件，软链接技能 |
| **LangChain / CrewAI** | 将 `tron_api.mjs` 封装为 Tool |

#### 快速安装脚本

```bash
## 自动安装到所有 AI 环境
bash install.sh

## 清洁卸载
bash uninstall.sh
```

---

### 配置说明

#### 环境变量

```bash
## 可选：TronGrid API Key，获取更高请求频率
export TRONGRID_API_KEY="your-api-key"

## 可选：切换网络（默认：mainnet）
export TRON_NETWORK="mainnet"    ## 或 "shasta" / "nile"

## 签名操作（二选一）：
export TRON_PRIVATE_KEY="你的十六进制私钥"
## 或
export TRON_PRIVATE_KEY_FILE="/path/to/keyfile.txt"
```

#### 网络支持

| 网络 | 地址 | 用途 |
|------|------|------|
| 主网 | https://api.trongrid.io | 生产环境 |
| Shasta 测试网 | https://api.shasta.trongrid.io | 测试 |
| Nile 测试网 | https://nile.trongrid.io | 测试 |

#### 内置代币快捷符号

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

### 项目结构

```
tronlink-skills/
├── README.md                          ## 主文档
├── package.json                       ## Node.js 配置文件
├── install.sh                         ## 全环境自动安装脚本
├── uninstall.sh                       ## 清洁卸载脚本
│
├── scripts/
│   ├── tron_api.mjs                   ## 主 CLI（1,248 行，41 个命令）
│   └── mcp_server.mjs                 ## MCP 协议服务封装
│
├── skills/                            ## 技能定义（自动发现）
│   ├── tron-wallet/SKILL.md
│   ├── tron-token/SKILL.md
│   ├── tron-market/SKILL.md
│   ├── tron-swap/SKILL.md
│   ├── tron-resource/SKILL.md
│   └── tron-staking/SKILL.md
│
├── docs/
│   ├── claude-integration-guide.md    ## 3 种集成方式
│   ├── resource-model.md              ## 能量与带宽深度解析
│   ├── staking-guide.md               ## Stake 2.0 与 APY 说明
│   └── integration-guide.sh
│
├── .claude-plugin/                    ## Claude Code 插件配置
├── .cursor-plugin/                    ## Cursor IDE 插件配置
├── .opencode/                         ## OpenCode 配置
├── .codex/                            ## Codex CLI 安装说明
├── .claude/                           ## 预配置测试命令
├── _meta.json                         ## 技能注册元数据
└── LICENSE                            ## MIT
```

---

### 依赖项

| 依赖 | 是否必需？ | 用途 |
|------|-----------|------|
| Node.js >= 18 | 是 | 运行时（原生 fetch、crypto） |
| tronweb ^6.0.0 | 仅签名操作需要 | send-trx、send-token、质押操作 |
| npm install | 不需要 | 只读操作无需安装任何依赖 |

---

### 安全模型

| 方面 | 实现方式 |
|------|----------|
| 私钥处理 | 仅通过环境变量传递——绝不作为 CLI 参数 |
| 密钥暴露 | 不作为 CLI 参数传递（`ps`、shell 历史可见） |
| 签名方式 | 所有签名通过 TronWeb 在本地完成——密钥不会发送到网络 |
| 资金操作 | 需人工确认后才执行 |
| 只读操作 | 安全——无状态变更，无需密钥 |
| 频率限制 | 公共 TronGrid API；使用 TRONGRID_API_KEY 获取更高限额 |

---

### 地址格式支持

所有命令均支持并自动归一化两种格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| Base58Check | `T...`（34 字符） | 标准显示格式 |
| Hex | `41...`（42 个十六进制字符） | 内部表示格式 |

---

### 关键设计决策

1. **默认零依赖** — 只读操作无需 npm install，对 AI Agent 而言轻量且即时
2. **资金操作人工确认** — 所有移动资金的交易需要明确的用户确认
3. **TRON 专属领域知识** — 为能量/带宽和 Stake 2.0 提供专门技能，尊重 TRON 独特架构
4. **多格式地址支持** — 透明处理 Base58Check 和 hex 两种格式
5. **代币符号解析** — 常用代币有内置快捷方式；未知合约可直接使用地址
6. **成本优化建议** — `optimize-cost` 命令提供个性化策略
7. **MCP 服务封装** — 为 Claude Desktop 和现代 AI Agent 提供结构化集成

---

### 快速开始

```bash
## 1. 克隆
git clone <repo>
cd tronlink-skills

## 2. 配合 Claude Code 使用（只读操作无需安装）
claude
> "查一下 T地址... 的 TRX 余额"
> "展示 TRON 上最热门的代币"
> "发送 USDT 需要多少能量？"
> "获取能量最好的方式是什么——冻结、租赁还是燃烧？"

## 3. 或直接使用命令行
node scripts/tron_api.mjs wallet-balance --address T地址...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs optimize-cost --address T地址...
```
