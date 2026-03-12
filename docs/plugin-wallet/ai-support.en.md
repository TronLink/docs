## MCP Server TronLink 

### Overview

**GitHub**: [https://github.com/TronLink/mcp-server-tronlink](https://github.com/TronLink/mcp-server-tronlink)

**mcp-server-tronlink** is a production-ready Model Context Protocol (MCP) server that enables AI agents (Claude, GPT, etc.) to interact with the TRON blockchain through natural language. Built on `@tronlink/mcp-core`, it provides **56+ tools** across two complementary operation modes.

**Key Highlights:**
- Dual-mode architecture: **Playwright** (browser automation) + **Direct API** (on-chain operations)
- 32 built-in Flow Recipes with pre-checks and dependency resolution
- Non-custodial local transaction signing via `@noble/curves`
- Multi-signature management with real-time WebSocket monitoring
- Gas-free TRC20 transfers via GasFree service integration

---

### Architecture

```
AI Agent (Claude Desktop / Claude Code)
         | (MCP Protocol — stdio / JSON-RPC 2.0)
         v
TronLink MCP Server
├── Playwright Mode ─── TronLinkSessionManager
│   └── Browser automation + TronLink extension UI control
├── Direct API Mode
│   ├── TronLinkOnChainCapability   (14 tools)
│   ├── TronLinkMultiSigCapability  (5 tools)
│   └── TronLinkGasFreeCapability   (3 tools)
├── Utility Capabilities
│   ├── TronLinkBuildCapability     (extension build)
│   ├── TronLinkStateSnapshotCapability (UI state extraction)
│   └── TRON Crypto Utils           (address derivation, signing, Base58)
└── Flow Recipes (32 built-in recipes with pre-checks)
         |
         v
TronGrid API / Multi-Sig Service / GasFree Service
         |
         v
TRON Blockchain
```

Both modes can run simultaneously and tools are auto-enabled based on configuration.

---

### Dual-Mode Operation

#### Mode 1: Playwright (Browser Automation)

Controls the TronLink Chrome extension via Playwright Chromium. Ideal for **E2E testing, UI validation, and DApp interaction**.

**Capabilities:**
- Launch browser with `--load-extension` flag for TronLink
- Auto-detect extension ID from Chrome API
- Multi-tab tracking with automatic role classification (extension / notification / dapp / other)
- DOM-based state extraction (TRON address, TRX balance, network detection)
- Screenshot capture with base64 encoding
- Automatic browser dialog handling (alerts, confirms, prompts)

**27 Playwright tools include:** `tl_launch`, `tl_cleanup`, `tl_navigate`, `tl_click`, `tl_type`, `tl_screenshot`, `tl_accessibility_snapshot`, `tl_describe_screen`, etc.

#### Mode 2: Direct API (On-Chain)

Operates directly against TronGrid REST API — no browser required. Ideal for **account queries, transfers, swaps, staking, and multi-sig management**.

**22 API tools grouped into:**

| Group | Tools | Description |
|-------|-------|-------------|
| On-Chain | 14 | Transfer, stake, swap, query, multisig setup |
| Multi-Signature | 5 | Permission query, tx submit, WebSocket monitoring |
| GasFree | 3 | Zero-gas TRC20 transfers |

---

### Core Components

#### 1. TronLinkSessionManager

Full browser lifecycle management:

| Method | Description |
|--------|-------------|
| `launch()` | Initialize browser with TronLink extension |
| `getExtensionState()` | Extract wallet state from UI |
| `navigateToUrl()` | Navigate to a specific URL |
| `navigateToNotification()` | Open TronLink notification popup |
| `screenshot()` | Capture current UI state |
| `getTrackedPages()` | List all open browser tabs |
| `cleanup()` | Graceful shutdown of all resources |

**Screen Detection:** Auto-detects 15 TronLink screens: `home`, `login`, `settings`, `send`, `receive`, `sign`, `broadcast`, `assets`, `address_book`, `node_management`, `dapp_list`, `create_wallet`, `import_wallet`, `notification`, `unknown`.

#### 2. TronLinkOnChainCapability (14 Tools)

Direct API wrapper for TronGrid:

**Query Operations:**
- `getAddress()` — Derive TRON address from configured private key
- `getAccount()` — Balance, bandwidth, energy, permissions
- `getTokens()` — TRC10 and TRC20 token balances
- `getTransaction()` — Transaction details by txID
- `getHistory()` — Transaction history with pagination
- `getStakingInfo()` — Staking status (frozen amounts, votes, unfreezing)

**Transaction Operations:**
- `send()` — Transfer TRX, TRC10, or TRC20 tokens
- `stake()` — Freeze/unfreeze TRX for bandwidth or energy (Stake 2.0)
- `resource()` — Delegate/undelegate bandwidth or energy
- `swap()` — Token swap via SunSwap V2
- `swapV3()` — Token swap via SunSwap V3 Smart Router

**Multi-Sig Operations:**
- `setupMultisig()` — Configure multi-sig permissions
- `createMultisigTx()` — Create unsigned multi-sig transaction
- `signMultisigTx()` — Sign multi-sig transaction

#### 3. TronLinkMultiSigCapability (5 Tools)

REST + WebSocket API for TRON multi-signature service:

- `queryAuth()` — Query multi-sig permissions (owner/active, thresholds, weights)
- `submitTransaction()` — Submit signed transaction (auto-broadcast when threshold reached)
- `queryTransactionList()` — List transactions with filtering
- `connectWebSocket()` — Real-time transaction monitoring
- `disconnectWebSocket()` — Stop monitoring

**Implementation:** HmacSHA256 signature generation for API auth, UUID-based request signing, supports both Nile testnet and Mainnet credentials.

#### 4. TronLinkGasFreeCapability (3 Tools)

Zero-gas TRC20 transfers via GasFree service:

- `getAccount()` — Query eligibility, supported tokens, daily quota
- `getTransactions()` — Query gas-free transaction history
- `send()` — Send TRC20 with zero gas fee

#### 5. TRON Cryptography Utils

Pure cryptographic functions — no external service calls:

```
privateKeyToAddress()      64-char hex → TRON address (base58 + hex)
signTransaction()          raw_data_hex → 65-byte signature
base58CheckEncode()        Payload → base58check address
base58CheckDecode()        TRON address → 21-byte payload
addressToHex()             T-address → 0x41... hex
hexToAddress()             0x41... → T-address
```

Uses `@noble/curves` (secp256k1 ECDSA) and `@noble/hashes` (Keccak-256, SHA256).

---

### Flow Recipes (32 Built-In)

Pre-configured multi-step workflows with dependency checks and parameter templates.

#### Playwright Flows
| Flow | Description |
|------|-------------|
| `importWalletFlow` | Import wallet with seed phrase |
| `switchNetworkFlow` | Switch to Mainnet/Nile/Shasta |
| `enableTestNetworksFlow` | Enable testnet visibility |
| `transferTrxFlow` | TRX transfer via UI |
| `transferTokenFlow` | Token transfer via UI |

#### On-Chain Flows (11)
| Flow | Description |
|------|-------------|
| `chainCheckBalanceFlow` | Query balance |
| `chainTransferTrxFlow` | TRX transfer with pre-checks |
| `chainTransferTrc20Flow` | TRC20 transfer with pre-checks |
| `chainStakeFlow` | Stake TRX |
| `chainUnstakeFlow` | Unstake TRX |
| `chainGetStakingFlow` | Query staking info |
| `chainDelegateResourceFlow` | Delegate bandwidth/energy |
| `chainUndelegateResourceFlow` | Undelegate resources |
| `chainSetupMultisigFlow` | Setup multi-sig permissions |
| `chainCreateMultisigTxFlow` | Create unsigned multi-sig tx |
| `chainSwapV3Flow` | SunSwap V3 token swap |

#### Multi-Sig Flows (6)
| Flow | Description |
|------|-------------|
| `multisigQueryAuthFlow` | Query permissions |
| `multisigListTransactionsFlow` | List pending transactions |
| `multisigMonitorFlow` | WebSocket real-time monitoring |
| `multisigStopMonitorFlow` | Stop monitoring |
| `multisigSubmitTxFlow` | Submit signed transaction |
| `multisigCheckFlow` | Full status check |

#### GasFree Flows (3)
| Flow | Description |
|------|-------------|
| `gasfreeCheckAccountFlow` | Query eligibility |
| `gasfreeTransactionHistoryFlow` | Query history |
| `gasfreeSendFlow` | Gas-free TRC20 transfer |

---

### Configuration

#### Environment Variables

**Playwright Mode:**

| Variable | Description |
|----------|-------------|
| `TRONLINK_EXTENSION_PATH` | TronLink extension build directory |
| `TRONLINK_SOURCE_PATH` | Enable build capability |
| `TL_MODE` | `e2e` (test) or `prod` (production) |
| `TL_HEADLESS` | Browser headless mode |
| `TL_SLOW_MO` | Playwright slow-motion delay (ms) |

**TronGrid API:**

| Variable | Description |
|----------|-------------|
| `TL_TRONGRID_URL` | Full-node API URL |
| `TL_TRONGRID_API_KEY` | API key (required for Mainnet) |
| `TL_CHAIN_PRIVATE_KEY` | 64-char hex private key |
| `TL_SUNSWAP_ROUTER` | SunSwap V2 router address |
| `TL_SUNSWAP_V3_ROUTER` | SunSwap V3 smart router address |
| `TL_WTRX_ADDRESS` | WTRX contract address |

**Multi-Signature Service:**

| Variable | Description |
|----------|-------------|
| `TL_MULTISIG_BASE_URL` | API base URL |
| `TL_MULTISIG_SECRET_ID` | Project credential |
| `TL_MULTISIG_SECRET_KEY` | HmacSHA256 signing key |
| `TL_MULTISIG_CHANNEL` | Channel/project name |
| `TL_MULTISIG_OWNER_KEY` | Owner private key |
| `TL_MULTISIG_COSIGNER_KEY` | Co-signer private key |

**GasFree Service:**

| Variable | Description |
|----------|-------------|
| `TL_GASFREE_BASE_URL` | Service URL |
| `TL_GASFREE_API_KEY` | API key |
| `TL_GASFREE_API_SECRET` | API secret |

#### Integration Options

**1. Project-Level MCP Config (`.mcp.json`)**

Auto-detected by Claude Code:
```json
{
  "mcpServers": {
    "tronlink": {
      "command": "node",
      "args": ["./dist/index.js"],
      "env": {
        "TL_TRONGRID_URL": "https://nile.trongrid.io",
        "TL_CHAIN_PRIVATE_KEY": "your-64-char-hex-key"
      }
    }
  }
}
```

**2. Claude Desktop**

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "tronlink": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"],
      "env": { ... }
    }
  }
}
```

**3. Claude Code Global Settings**

Edit `~/.claude/settings.json` or `.claude/settings.json`.

**4. Any MCP Client**

Supports stdio transport protocol — compatible with any MCP-compliant client.

---

### Project Structure

```
mcp-server-tronlink/
├── src/
│   ├── index.ts                    ## Server entry, config, capability registration
│   ├── session-manager.ts          ## Browser lifecycle (TronLinkSessionManager)
│   ├── capabilities/
│   │   ├── on-chain.ts             ## 14 on-chain operations (TronGrid)
│   │   ├── multisig.ts             ## 5 multi-sig operations (REST + WS)
│   │   ├── gasfree.ts              ## 3 gas-free transfer operations
│   │   ├── build.ts                ## Extension webpack build
│   │   ├── state-snapshot.ts       ## UI state extraction
│   │   └── tron-crypto.ts          ## Address derivation, signing, Base58
│   └── flows/
│       ├── index.ts                ## Flow registry (32 recipes)
│       ├── import-wallet.ts        ## Wallet import flow
│       ├── switch-network.ts       ## Network switching flows
│       ├── transfer-trx.ts         ## Transfer flows
│       ├── multisig.ts             ## 6 multi-sig flows
│       ├── onchain.ts              ## 11 on-chain flows
│       └── gasfree.ts              ## 3 gas-free flows
├── dist/                           ## Compiled output
├── .mcp.json                       ## MCP configuration
├── .env.example                    ## Environment variable reference
├── package.json
├── tsconfig.json
└── README.md
```

---

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@noble/curves` | ^2.0.1 | secp256k1 ECDSA signing |
| `@noble/hashes` | ^2.0.1 | Keccak-256, SHA256 |
| `@tronlink/mcp-core` | local | Core MCP server framework |
| `playwright` | ^1.49.0 | Browser automation |
| `ws` | ^8.18.0 | WebSocket (multi-sig monitoring) |

---

### Security Model

| Aspect | Implementation |
|--------|----------------|
| Key storage | Injected via MCP JSON `env` field, never in `.env` files |
| Key exposure | No key material logged to stderr |
| Signing | Local transaction signing — keys never transmitted |
| Pre-checks | All transactions validate before execution |
| Git safety | Config files in `.gitignore` prevent accidental commits |
| Default network | Nile testnet with safe defaults |

---

### Typical Usage Scenarios

1. **Wallet Automation** — Import wallet, check balance, send transfers
2. **DApp Testing** — Launch browser, connect wallet, sign transactions, verify state
3. **On-Chain Trading** — Direct API swaps, staking, token transfers without browser
4. **Multi-Sig Workflows** — Set up permissions, submit/monitor transactions
5. **Gas-Free Operations** — TRC20 transfers without TRX balance requirements
6. **Infrastructure Testing** — Contract deployment, fixture management, mock servers

---

### Quick Start

```bash
## 1. Build
npm install && npm run build

## 2. Configure (Nile testnet example)
export TL_TRONGRID_URL="https://nile.trongrid.io"
export TL_CHAIN_PRIVATE_KEY="your-64-char-hex-private-key"

## 3. Run with Claude Code
## Add to .mcp.json and use naturally:
## "Check my TRX balance"
## "Send 10 TRX to TAddress..."
## "Swap 100 TRX for USDT on SunSwap V3"
```


## TronLink MCP Core 

### Overview

**GitHub**: [https://github.com/TronLink/tronlink-mcp-core](https://github.com/TronLink/tronlink-mcp-core)

**@tronlink/mcp-core** is the foundational framework library for building TronLink MCP (Model Context Protocol) servers. It is not a standalone application — consumers must implement the `ISessionManager` interface and inject capabilities to create a working server.

**Key Highlights:**
- Interface-driven, pluggable architecture with **9 capability interfaces**
- **56+ pre-defined tool handlers** with Zod-validated schemas
- Built-in Knowledge Store for cross-session learning and step replay
- Flow Recipe system for codifying multi-step workflows
- Standardized response format with 25+ error codes
- Dual-mode support: Playwright (UI automation) + Direct API (on-chain)

---

### Architecture

```
┌─ AI Agent (Claude, GPT, etc.)
│
├─ MCP Protocol (stdio / JSON-RPC 2.0)
│
├─ MCP Server Instance (createMcpServer)
│  ├─ 56+ tl_* tool handlers
│  ├─ Knowledge Store (cross-session persistence)
│  ├─ Flow Registry (recipe management)
│  └─ Discovery utilities
│
├─ ISessionManager Interface (consumer implements)
│  ├─ Session lifecycle
│  ├─ Page/tab management
│  ├─ Capability injection (9 interfaces)
│  └─ Environment mode (e2e / prod)
│
├─ Capability System (9 pluggable interfaces)
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
└─ Optional: Playwright (browser automation)
```

**Design Principles:**
1. **Interface-driven** — All major components use interfaces for extensibility
2. **Composition over inheritance** — Capabilities are injected, not inherited
3. **Singleton patterns** — SessionManager, KnowledgeStore, FlowRegistry use global holders
4. **Pre-checks** — On-chain tools validate before execution
5. **Data redaction** — Knowledge store automatically masks sensitive fields

---

### Relationship to mcp-server-tronlink

| Aspect | tronlink-mcp-core | mcp-server-tronlink |
|--------|-------------------|---------------------|
| Type | Core library (framework) | Standalone MCP server |
| Role | Defines interfaces, tools, protocol | Concrete implementation |
| Usage | Import via npm, extend | Direct CLI invocation |
| Extensibility | 9 pluggable capability interfaces | Pre-configured capabilities |
| Dependency | None (it IS the dependency) | Depends on @tronlink/mcp-core |

**mcp-server-tronlink is a consumer of tronlink-mcp-core.** The core defines WHAT tools exist; the server provides HOW they work.

---

### ISessionManager Interface

The critical interface that consumers must implement (25+ methods):

#### Session Lifecycle
```typescript
hasActiveSession(): boolean
getSessionId(): string
getSessionState(): SessionState
getSessionMetadata(): SessionMetadata
launch(input: LaunchInput): Promise<LaunchResult>
cleanup(): Promise<void>
```

#### Page Management
```typescript
getPage(): Page
setActivePage(page: Page): void
getTrackedPages(): TrackedPage[]
classifyPageRole(page: Page): PageRole
getContext(): ContextInfo
```

#### Extension State
```typescript
getExtensionState(): Promise<ExtensionState>
```

#### Accessibility References
```typescript
setRefMap(map: Map<string, any>): void
getRefMap(): Map<string, any>
clearRefMap(): void
resolveA11yRef(ref: string): any
```

#### Navigation
```typescript
navigateToHome(): Promise<void>
navigateToSettings(): Promise<void>
navigateToUrl(url: string): Promise<void>
navigateToNotification(): Promise<void>
waitForNotificationPage(timeoutMs?: number): Promise<Page>
```

#### Screenshots
```typescript
screenshot(options?: ScreenshotOptions): Promise<ScreenshotResult>
```

#### Capability Getters (9 optional)
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

#### Environment
```typescript
getEnvironmentMode(): 'e2e' | 'prod'
setContext(context: string, options?: any): Promise<void>
getContextInfo(): ContextInfo
```

---

### 9 Capability Interfaces

Each capability is optional and independently injectable:

#### 1. BuildCapability
Build TronLink extension from source.
```typescript
interface BuildCapability {
  build(options?: BuildOptions): Promise<BuildResult>
}
```

#### 2. FixtureCapability
Manage wallet state JSON (default, onboarding, custom presets).
```typescript
interface FixtureCapability {
  applyPreset(preset: string): Promise<void>
  getAvailablePresets(): string[]
  exportState(): Promise<WalletState>
  importState(state: WalletState): Promise<void>
}
```

#### 3. ChainCapability
Control local TRON node (tron-quickstart, etc.).
```typescript
interface ChainCapability {
  startNode(): Promise<void>
  stopNode(): Promise<void>
  getNodeStatus(): Promise<NodeStatus>
  fundAccount(address: string, amount: number): Promise<string>
}
```

#### 4. ContractSeedingCapability
Deploy smart contracts (TRC20/721/1155/10/multisig/staking/energy_rental).
```typescript
interface ContractSeedingCapability {
  seedContract(type: string, options?: any): Promise<ContractInfo>
  seedContracts(specs: ContractSpec[]): Promise<ContractInfo[]>
  getContractAddress(name: string): string | undefined
  listContracts(): ContractInfo[]
}
```

#### 5. StateSnapshotCapability
Extract wallet state from UI.
```typescript
interface StateSnapshotCapability {
  getSnapshot(): Promise<StateSnapshot>  // screen, address, balance, energy, bandwidth
}
```

#### 6. MockServerCapability
Mock API server for isolated testing.
```typescript
interface MockServerCapability {
  start(config?: MockConfig): Promise<void>
  stop(): Promise<void>
  addRoute(route: MockRoute): void
  getRequests(): MockRequest[]
}
```

#### 7. OnChainCapability
Direct on-chain operations via TronGrid REST API.
```typescript
interface OnChainCapability {
  getAddress(): Promise<AddressResult>
  getAccount(address?: string): Promise<AccountResult>
  getTokens(address?: string): Promise<TokensResult>
  send(params: SendParams): Promise<SendResult>
  getTransaction(txId: string): Promise<TxResult>
  getHistory(params?: HistoryParams): Promise<HistoryResult>
  stake(params: StakeParams): Promise<StakeResult>
  getStakingInfo(address?: string): Promise<StakingResult>
  resource(params: ResourceParams): Promise<ResourceResult>
  swap(params: SwapParams): Promise<SwapResult>
  swapV3(params: SwapV3Params): Promise<SwapResult>
  setupMultisig(params: MultisigSetupParams): Promise<MultisigResult>
  createMultisigTx(params: MultisigTxParams): Promise<MultisigTxResult>
  signMultisigTx(params: SignMultisigParams): Promise<SignResult>
}
```

#### 8. MultiSigCapability
Multi-signature service integration (REST + WebSocket).
```typescript
interface MultiSigCapability {
  queryAuth(address: string): Promise<AuthResult>
  submitTransaction(params: SubmitParams): Promise<SubmitResult>
  queryTransactionList(params: ListParams): Promise<TxListResult>
  connectWebSocket(params: WsParams): Promise<void>
  disconnectWebSocket(): Promise<void>
}
```

#### 9. GasFreeCapability
Gas-free TRC20 transfer service.
```typescript
interface GasFreeCapability {
  getAccount(address: string): Promise<GasFreeAccountResult>
  getTransactions(params: GasFreeTxParams): Promise<GasFreeTxResult>
  send(params: GasFreeSendParams): Promise<GasFreeSendResult>
}
```

---

### 56+ Tool Definitions

All tools use the `tl_` prefix. Organized into 13 categories:

#### 1. Session Management (2)
| Tool | Description |
|------|-------------|
| `tl_launch` | Launch browser with extension |
| `tl_cleanup` | Close browser and services |

#### 2. State & Discovery (4)
| Tool | Description |
|------|-------------|
| `tl_get_state` | Get wallet state |
| `tl_describe_screen` | Screen description with state + testIds + a11y + screenshot |
| `tl_list_testids` | List data-testid attributes |
| `tl_accessibility_snapshot` | Get accessibility tree with refs (e1, e2...) |

#### 3. Navigation (4)
| Tool | Description |
|------|-------------|
| `tl_navigate` | Navigate to TronLink screen or URL |
| `tl_switch_to_tab` | Switch tabs by role/URL |
| `tl_close_tab` | Close tabs |
| `tl_wait_for_notification` | Wait for confirmation popups |

#### 4. UI Interaction (6)
| Tool | Description |
|------|-------------|
| `tl_click` | Click elements (a11yRef, testId, selector) |
| `tl_type` | Type text into inputs |
| `tl_wait_for` | Wait for element state |
| `tl_scroll` | Scroll page/element |
| `tl_keyboard` | Send keyboard events |
| `tl_evaluate` | Execute JavaScript |

#### 5. Screenshots & Clipboard (2)
| Tool | Description |
|------|-------------|
| `tl_screenshot` | Capture screen |
| `tl_clipboard` | Read/write clipboard |

#### 6. Contract Deployment — e2e only (4)
| Tool | Description |
|------|-------------|
| `tl_seed_contract` | Deploy single contract |
| `tl_seed_contracts` | Deploy multiple contracts |
| `tl_get_contract_address` | Query contract address |
| `tl_list_contracts` | List deployed contracts |

#### 7. Context Management (2)
| Tool | Description |
|------|-------------|
| `tl_set_context` | Switch e2e/prod mode |
| `tl_get_context` | Get context info |

#### 8. Knowledge Store (4)
| Tool | Description |
|------|-------------|
| `tl_knowledge_last` | Get last N steps |
| `tl_knowledge_search` | Search history |
| `tl_knowledge_summarize` | Generate recipe |
| `tl_knowledge_sessions` | List sessions |

#### 9. Flow Recipes (1)
| Tool | Description |
|------|-------------|
| `tl_list_flows` | List/get flow recipes |

#### 10. Batch Execution (1)
| Tool | Description |
|------|-------------|
| `tl_run_steps` | Execute multiple steps sequentially |

#### 11. On-Chain Operations (14)
| Tool | Description |
|------|-------------|
| `tl_chain_get_address` | Get address from private key |
| `tl_chain_get_account` | Query account details |
| `tl_chain_get_tokens` | Query TRC10/TRC20 balances |
| `tl_chain_send` | Send TRX/TRC10/TRC20 |
| `tl_chain_get_tx` | Get transaction details |
| `tl_chain_get_history` | Query tx history |
| `tl_chain_stake` | Freeze/unfreeze TRX (Stake 2.0) |
| `tl_chain_get_staking` | Query staking info |
| `tl_chain_resource` | Delegate/undelegate resources |
| `tl_chain_swap` | SunSwap V2 swap |
| `tl_chain_swap_v3` | SunSwap V3 swap |
| `tl_chain_setup_multisig` | Configure multisig permissions |
| `tl_chain_create_multisig_tx` | Create unsigned multisig tx |
| `tl_chain_sign_multisig_tx` | Sign multisig transaction |

#### 12. Multi-Signature (5)
| Tool | Description |
|------|-------------|
| `tl_multisig_query_auth` | Query multisig permissions |
| `tl_multisig_submit_tx` | Submit signed tx |
| `tl_multisig_list_tx` | List multisig transactions |
| `tl_multisig_connect_ws` | Connect WebSocket |
| `tl_multisig_disconnect_ws` | Disconnect WebSocket |

#### 13. GasFree (3)
| Tool | Description |
|------|-------------|
| `tl_gasfree_get_account` | Query eligibility & quota |
| `tl_gasfree_get_transactions` | Query tx history |
| `tl_gasfree_send` | Send with zero gas |

---

### Standardized Response Format

All tools return a consistent structure:

```typescript
// Success
{
  ok: true,
  result: { /* tool-specific data */ },
  meta: {
    timestamp: "2026-03-09T10:15:23.456Z",
    sessionId: "tl-1741504523",
    durationMs: 234
  }
}

// Error
{
  ok: false,
  error: {
    code: "TL_CLICK_FAILED",       // One of 25+ error codes
    message: "Element not found",
    details: { /* optional */ }
  },
  meta: { timestamp, sessionId, durationMs }
}
```

**25+ Error Codes:** `TL_BUILD_FAILED`, `TL_SESSION_ALREADY_RUNNING`, `TL_NO_ACTIVE_SESSION`, `TL_LAUNCH_FAILED`, `TL_INVALID_INPUT`, `TL_NAVIGATION_FAILED`, `TL_TARGET_NOT_FOUND`, `TL_CLICK_FAILED`, `TL_TYPE_FAILED`, `TL_WAIT_TIMEOUT`, `TL_SCREENSHOT_FAILED`, `TL_CAPABILITY_NOT_AVAILABLE`, `TL_CHAIN_QUERY_FAILED`, `TL_CHAIN_SEND_FAILED`, `TL_CHAIN_SWAP_FAILED`, `TL_GASFREE_QUERY_FAILED`, `TL_GASFREE_SEND_FAILED`, `TL_MULTISIG_QUERY_FAILED`, `TL_MULTISIG_SUBMIT_FAILED`, `TL_MULTISIG_WS_FAILED`, `TL_INTERNAL_ERROR`, etc.

---

### Knowledge Store

Cross-session learning and step replay system.

#### Storage Structure
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

#### Features
- **Auto-recording:** Every tool invocation is logged (timestamp, screen, target, result)
- **Sensitive data redaction:** Passwords, mnemonics, private keys, seeds are automatically masked
- **Search:** Query by tool name, screen, testId, accessibility name
- **Summarization:** Generate reusable "recipes" from session history
- **Session management:** List sessions with metadata

---

### Flow Recipe System

Codifies common multi-step workflows with template parameters.

#### FlowRecipe Structure
```typescript
{
  id: "transfer_trx",
  name: "Send TRX",
  description: "Transfer TRX to another address",
  context: "both",                      // "playwright" | "api" | "both"
  preconditions: ["wallet unlocked"],
  params: [
    { name: "recipient", description: "Target TRON address", required: true },
    { name: "amount", description: "TRX amount", required: true }
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

#### FlowRegistry
- `register(recipe)` — Register a new flow recipe
- `get(id)` — Get recipe by ID
- `list(filter?)` — List recipes by tag, context, or search
- Singleton pattern via global holder

---

### Element Targeting (3 Methods)

```typescript
// 1. Accessibility Reference (recommended)
tl_click({ a11yRef: "e5" })

// 2. data-testid
tl_click({ testId: "send-button" })

// 3. CSS Selector
tl_click({ selector: ".confirm-btn" })
```

Accessibility references come from `tl_accessibility_snapshot` output — the most reliable targeting method.

---

### Installation & Usage

#### Install
```bash
npm install @tronlink/mcp-core
```

#### Basic Setup
```typescript
import {
  createMcpServer,
  setSessionManager,
  type ISessionManager,
} from '@tronlink/mcp-core';

// 1. Implement ISessionManager
class MySessionManager implements ISessionManager {
  // ... implement all 25+ methods
}

// 2. Register
setSessionManager(new MySessionManager());

// 3. Create and start server
const server = createMcpServer({
  name: 'My TronLink Server',
  version: '1.0.0',
});

await server.start();
```

---

### Project Structure

```
tronlink-mcp-core/
├── src/
│   ├── index.ts                           ## Public API exports
│   ├── mcp-server/
│   │   ├── server.ts                      ## createMcpServer() factory
│   │   ├── session-manager.ts             ## ISessionManager interface
│   │   ├── knowledge-store.ts             ## Persistent step recording
│   │   ├── discovery.ts                   ## Page inspection utilities
│   │   ├── schemas.ts                     ## Zod validation schemas
│   │   ├── constants.ts                   ## TIMEOUTS, LIMITS, URLs, SCREENS
│   │   ├── tools/
│   │   │   ├── definitions.ts             ## Tool registry & routing
│   │   │   ├── run-tool.ts                ## Execution wrapper (auto-logs)
│   │   │   ├── launch.ts                  ## tl_launch
│   │   │   ├── cleanup.ts                 ## tl_cleanup
│   │   │   ├── state.ts                   ## tl_get_state
│   │   │   ├── navigation.ts              ## Navigation tools
│   │   │   ├── interaction.ts             ## UI interaction tools
│   │   │   ├── discovery-tools.ts         ## Element discovery
│   │   │   ├── screenshot.ts              ## Screenshot capture
│   │   │   ├── on-chain.ts                ## 14 on-chain tools
│   │   │   ├── multisig.ts                ## 5 multisig tools
│   │   │   ├── gasfree.ts                 ## 3 gasfree tools
│   │   │   ├── knowledge.ts               ## Knowledge store tools
│   │   │   ├── flows.ts                   ## Flow listing
│   │   │   ├── batch.ts                   ## Batch execution
│   │   │   └── helpers.ts                 ## Shared utilities
│   │   ├── types/
│   │   │   ├── responses.ts               ## McpResponse types
│   │   │   ├── errors.ts                  ## ErrorCodes enum
│   │   │   ├── session.ts                 ## Session types
│   │   │   ├── step-record.ts             ## Step recording types
│   │   │   ├── tool-inputs.ts             ## All tool input types
│   │   │   └── tool-outputs.ts            ## All tool output types
│   │   └── utils/
│   │       ├── response.ts                ## createSuccessResponse / createErrorResponse
│   │       ├── errors.ts                  ## extractErrorMessage
│   │       └── zod-to-json-schema.ts      ## Zod → JSON Schema conversion
│   ├── capabilities/
│   │   ├── types.ts                       ## 9 capability interfaces
│   │   └── context.ts                     ## Environment config types
│   ├── flows/
│   │   ├── types.ts                       ## FlowRecipe, FlowParam types
│   │   └── registry.ts                    ## FlowRegistry class
│   ├── launcher/
│   │   ├── extension-id-resolver.ts       ## Extension ID extraction
│   │   └── extension-readiness.ts         ## Extension load detection
│   └── utils/
│       └── index.ts                       ## generateSessionId, etc.
├── dist/                                  ## Compiled output + .d.ts
├── package.json
├── tsconfig.json
└── README.md
```

---

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@modelcontextprotocol/sdk` | ^1.12.0 | MCP protocol implementation |
| `zod` | ^3.23.0 | Input validation schemas |

**Peer Dependencies (optional):**

| Package | Version | Purpose |
|---------|---------|---------|
| `playwright` | ^1.49.0 | Browser automation (Playwright mode only) |
| `@playwright/test` | ^1.49.0 | Test utilities |

---

### Build & Development

```bash
npm run build      ## Compile TypeScript to dist/
npm run dev        ## Watch mode
npm run test       ## Run Vitest tests
npm run lint       ## ESLint
npm run clean      ## Remove dist/
```

**Output:** Compiled JavaScript + type definitions in `dist/`.

---

### Key Design Patterns

1. **Global Singletons** — `setSessionManager()` / `getSessionManager()`, `setKnowledgeStore()` / `getKnowledgeStore()`, `FlowRegistry.getInstance()`
2. **Composition over Inheritance** — Capabilities injected via getter methods, not class hierarchy
3. **Interface Segregation** — Each capability has a focused, minimal interface
4. **Pre-checks** — On-chain tools validate balances, permissions, quotas before sending transactions
5. **Data Redaction** — Knowledge store auto-masks password, mnemonic, private_key, seed fields
6. **Standardized Responses** — Consistent `{ ok, result/error, meta }` structure across all 56+ tools
7. **Template System** — Flow recipes use `{{param}}` placeholders for reusable workflows


## TronLink Skills 

### Overview

**GitHub**: [https://github.com/TronLink/tronlink-skills](https://github.com/TronLink/tronlink-skills)

**TronLink Wallet Skills** is an AI Agent skill set that provides complete TRON blockchain wallet and DeFi functionality through natural language. Designed for Claude Code, Cursor, OpenCode, Codex CLI, and other AI agents.

**Key Highlights:**
- **6 skills, 41 commands** covering wallet, token research, market data, swaps, resources, and staking
- **Zero npm dependencies** for all read-only operations (uses native Node.js 18+ `fetch` and `crypto`)
- **TRON-specific domain knowledge** — dedicated handling of Energy + Bandwidth resource model
- **Multi-platform support** — Claude Code, Cursor, OpenCode, Codex CLI, LangChain/CrewAI
- **Human-in-the-loop** confirmation for all fund-moving operations
- **MCP server wrapper** for structured AI agent integration

---

### Why TronLink Skills?

TRON has a fundamentally different fee model than EVM chains. Instead of unified gas, TRON uses **Energy** (for smart contracts) and **Bandwidth** (for all transactions). No existing AI agent skill properly covers:

- TRON's unique resource model and cost optimization strategies
- Stake 2.0 (freezing TRX to obtain resources and earn rewards)
- Super Representative (SR) voting mechanics
- DEX aggregation across SunSwap V2/V3 and Sun.io
- The 14-day unfreezing wait period and its implications

TronLink Skills fills this gap with deep TRON-specific domain knowledge.

---

### Architecture

```
Natural Language Input
         |
         v
AI Agent (Claude Code / Cursor / OpenCode / Custom)
         |
         v
tron_api.mjs (Node.js 18+, native fetch, 1,248 lines)
    ├── Zero dependencies for read operations
    ├── Optional: tronweb for signing
    ├── TronGrid HTTP API (public or with API key)
    └── Tronscan API for token metadata
         |
         v
Structured JSON → Agent interprets → Natural language response
```

---

### The 6 Skills

#### 1. tron-wallet (8 commands)

Wallet management and basic operations.

| Command | Description |
|---------|-------------|
| `wallet-balance` | TRX balance and frozen amounts |
| `token-balance` | Check TRC-20 token balance |
| `wallet-tokens` | List all token holdings |
| `tx-history` | Recent transaction history |
| `account-info` | Full account details |
| `validate-address` | Address format validation |
| `send-trx` | Transfer TRX (requires private key) |
| `send-token` | Transfer TRC-20 tokens (requires private key) |

**Features:** Handles both Base58Check (T...) and hex address formats, supports known token symbols, auto-converts decimals.

#### 2. tron-token (7 commands)

Token research and security analysis.

| Command | Description |
|---------|-------------|
| `token-info` | Metadata, supply, issuer, socials |
| `token-search` | Find tokens by name/symbol |
| `contract-info` | ABI, bytecode, verification status |
| `token-holders` | Top holders and holder analysis |
| `trending-tokens` | Highest volume tokens (24h) |
| `token-rankings` | Sort by market cap, volume, holders, gainers/losers |
| `token-security` | Security audit (honeypot, proxy, owner permissions) |

**Features:** Detects rug pulls, analyzes holder concentration, checks liquidity locks.

#### 3. tron-market (8 commands)

Real-time market data and whale monitoring.

| Command | Description |
|---------|-------------|
| `token-price` | Current price USD/TRX, 24h change |
| `kline` | OHLCV candlestick data (1m to 1w intervals) |
| `trade-history` | Recent DEX trades |
| `dex-volume` | Buy/sell volume, trade count |
| `whale-transfers` | Large transfers (configurable threshold) |
| `large-transfers` | TRX whale activity |
| `pool-info` | Liquidity pools (SunSwap V2/V3 TVL, APY) |
| `market-overview` | TRON network stats (price, cap, volume, active accounts) |

**Features:** Multi-DEX aggregation, smart money signal detection, K-line analysis.

#### 4. tron-swap (5 commands)

DEX trading and swap execution.

| Command | Description |
|---------|-------------|
| `swap-quote` | Expected output, price impact, slippage |
| `swap-route` | Optimal route across SunSwap V2/V3, Sun.io (multi-hop) |
| `swap-approve` | ERC20-style approve for token spending |
| `swap-execute` | Execute swap with user confirmation |
| `tx-status` | Track swap transaction status |

**Features:** Aggregates liquidity from multiple sources, estimates Energy cost, handles multi-hop routes, enforces human-in-the-loop confirmation.

#### 5. tron-resource (7 commands)

Energy & Bandwidth management — TRON-specific.

| Command | Description |
|---------|-------------|
| `resource-info` | Current Energy/Bandwidth available and staked |
| `estimate-energy` | Energy cost for smart contract calls |
| `estimate-bandwidth` | Bandwidth cost (free daily allowance: 600) |
| `energy-price` | Current SUN cost per Energy unit |
| `delegate-resource` | Send resources to another address without transferring TRX |
| `energy-rental` | Query rental marketplace options |
| `optimize-cost` | Personalized recommendation (freeze vs. rent vs. burn) |

**Features:** Decision tree logic for cost optimization, tracks daily free bandwidth, calculates TRX burn equivalent.

#### 6. tron-staking (8 commands)

Stake 2.0 and SR voting.

| Command | Description |
|---------|-------------|
| `stake-freeze` | Freeze TRX for Energy or Bandwidth |
| `stake-unfreeze` | Start 14-day unfreezing period |
| `stake-withdraw` | Withdraw unfrozen TRX |
| `vote` | Vote for Super Representatives (1 frozen TRX = 1 vote) |
| `claim-rewards` | Claim voting rewards (every 6 hours) |
| `sr-list` | List SRs with votes, block rate, APY |
| `staking-info` | Frozen amount, votes, unclaimed rewards, pending unfreezes |
| `staking-apy` | Calculate estimated annual yield |

**Features:** Full Stake 2.0 support, 14-day unlock management, APY calculation, SR commission tracking.

---

### Recommended Skill Workflows

#### Check & Transfer
```
tron-wallet (check balance) → tron-resource (estimate energy) → tron-wallet (send)
```

#### Research & Buy
```
tron-token (search) → tron-market (price/chart) → tron-resource (check energy) → tron-swap (execute)
```

#### Staking Flow
```
tron-wallet (check balance) → tron-staking (freeze) → tron-staking (vote) → tron-staking (claim)
```

#### Resource Optimization
```
tron-resource (check status) → tron-resource (estimate cost) → tron-staking (freeze) OR tron-resource (rent)
```

---

### TRON Resource Model Reference

#### Energy vs. Bandwidth

| Resource | Consumed By | Free Allowance | How to Get |
|----------|-------------|----------------|------------|
| **Bandwidth** | ALL transactions | 600/day | Freeze TRX or burn TRX |
| **Energy** | Smart contracts only | None | Freeze TRX, rent, or burn TRX |

#### Cost Examples

| Operation | Bandwidth | Energy | TRX Burned (no resources) |
|-----------|-----------|--------|---------------------------|
| TRX transfer | ~267 | 0 | 0 (within free limit) |
| USDT transfer | ~345 | ~65,000 | ~13-27 TRX |
| SunSwap swap | ~345 | ~65,000-200,000 | ~13-40 TRX |
| Token approve | ~345 | ~30,000 | ~6-12 TRX |

#### Stake 2.0 Key Facts
- Freeze TRX → Get Energy or Bandwidth → Vote for SR → Earn rewards
- Unfreezing has **14-day wait** before withdrawal
- Votes reset if you unfreeze; must re-vote after re-freezing
- 1 frozen TRX ≈ 4.5 Energy/day
- Voting rewards claimable every 6 hours

---

### Integration Methods

#### Method 1: Claude Code (Recommended)

```bash
## Clone and use directly
git clone <repo>
cd tronlink-skills
claude   ## Auto-discovers SKILL.md files
```

No `npm install` needed for read-only operations.

#### Method 2: MCP Server

```bash
## Register as MCP server
claude mcp add tronlink -- node ~/.tronlink-skills/scripts/mcp_server.mjs

## Provides 25 MCP tools callable by Claude Desktop / Claude Code
```

#### Method 3: Manual CLI

```bash
## Direct command execution
node scripts/tron_api.mjs wallet-balance --address TAddress...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs swap-quote --from TRX --to USDT --amount 100
```

#### Method 4: Other AI Platforms

| Platform | Integration |
|----------|-------------|
| **Cursor / Windsurf** | Clone repo, use MCP or direct skill reading |
| **Codex CLI** | Symlink to `~/.agents/skills/tronlink-skills` |
| **OpenCode** | Register plugin, symlink skills |
| **LangChain / CrewAI** | Wrap `tron_api.mjs` as a Tool |

#### Quick Setup Script

```bash
## Auto-install for all AI environments
bash install.sh

## Clean uninstall
bash uninstall.sh
```

---

### Configuration

#### Environment Variables

```bash
## Optional: TronGrid API key for higher rate limits
export TRONGRID_API_KEY="your-api-key"

## Optional: Switch network (default: mainnet)
export TRON_NETWORK="mainnet"    ## or "shasta" / "nile"

## For signing operations (choose one):
export TRON_PRIVATE_KEY="your-hex-private-key"
## or
export TRON_PRIVATE_KEY_FILE="/path/to/keyfile.txt"
```

#### Network Support

| Network | URL | Use Case |
|---------|-----|----------|
| Mainnet | https://api.trongrid.io | Production |
| Shasta | https://api.shasta.trongrid.io | Testing |
| Nile | https://nile.trongrid.io | Testing |

#### Built-In Token Shortcuts

| Symbol | Contract Address |
|--------|------------------|
| TRX | Native (no contract) |
| USDT | TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t |
| USDC | TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8 |
| WTRX | TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR |
| BTT | TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4 |
| JST | TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9 |
| SUN | TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S |
| WIN | TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7 |

---

### Project Structure

```
tronlink-skills/
├── README.md                          ## Main documentation
├── package.json                       ## Node.js manifest
├── install.sh                         ## Auto-install for all AI environments
├── uninstall.sh                       ## Clean uninstall
│
├── scripts/
│   ├── tron_api.mjs                   ## Main CLI (1,248 lines, 41 commands)
│   └── mcp_server.mjs                 ## MCP protocol server wrapper
│
├── skills/                            ## Skill definitions (auto-discovered)
│   ├── tron-wallet/SKILL.md
│   ├── tron-token/SKILL.md
│   ├── tron-market/SKILL.md
│   ├── tron-swap/SKILL.md
│   ├── tron-resource/SKILL.md
│   └── tron-staking/SKILL.md
│
├── docs/
│   ├── claude-integration-guide.md    ## 3 integration methods
│   ├── resource-model.md              ## Energy & Bandwidth deep dive
│   ├── staking-guide.md               ## Stake 2.0 & APY explanation
│   └── integration-guide.sh
│
├── .claude-plugin/                    ## Claude Code plugin config
├── .cursor-plugin/                    ## Cursor IDE plugin config
├── .opencode/                         ## OpenCode config
├── .codex/                            ## Codex CLI setup
├── .claude/                           ## Pre-configured test commands
├── _meta.json                         ## Metadata for skill registries
└── LICENSE                            ## MIT
```

---

### Dependencies

| Dependency | Required? | Purpose |
|------------|-----------|---------|
| Node.js >= 18 | Yes | Runtime (native fetch, crypto) |
| tronweb ^6.0.0 | Only for signing | send-trx, send-token, staking ops |
| npm install | Not needed | Read-only operations work without it |

---

### Security Model

| Aspect | Implementation |
|--------|----------------|
| Private key handling | Environment variables only — never CLI arguments |
| Key exposure | Never passed as CLI args (visible in `ps`, shell history) |
| Signing | All signing is local via TronWeb — keys never sent to network |
| Fund movements | Human-in-the-loop confirmation required |
| Read operations | Safe — no state changes, no key needed |
| Rate limits | Public TronGrid API; use TRONGRID_API_KEY for higher limits |

---

### Address Format Support

Both formats are supported and auto-normalized across all commands:

| Format | Example | Description |
|--------|---------|-------------|
| Base58Check | `T...` (34 chars) | Standard display format |
| Hex | `41...` (42 hex chars) | Internal representation |

---

### Key Design Decisions

1. **Zero Dependencies by Default** — Read-only operations don't require npm install, making it lightweight and instant for AI agents
2. **Human-in-the-Loop for Fund Movements** — All transactions that move funds require explicit user confirmation
3. **TRON-Specific Domain Knowledge** — Dedicated skills for Energy/Bandwidth and Stake 2.0, acknowledging TRON's unique architecture
4. **Multi-Format Address Support** — Handles both Base58Check and hex formats transparently
5. **Token Symbol Resolution** — Common tokens have built-in shortcuts; unknown contracts work by address
6. **Cost Optimization Recommendations** — The `optimize-cost` command provides personalized strategies
7. **MCP Server Wrapper** — Provides structured integration for Claude Desktop and modern AI agents

---

### Quick Start

```bash
## 1. Clone
git clone <repo>
cd tronlink-skills

## 2. Use with Claude Code (no install needed for reads)
claude
> "What's the TRX balance of TAddress...?"
> "Show me the top trending tokens on TRON"
> "How much Energy do I need to send USDT?"
> "What's the best way to get Energy — freeze, rent, or burn?"

## 3. Or use directly
node scripts/tron_api.mjs wallet-balance --address TAddress...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs optimize-cost --address TAddress...
```
