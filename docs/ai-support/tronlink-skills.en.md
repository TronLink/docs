# TronLink Skills 

## Overview

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

## Why TronLink Skills?

TRON has a fundamentally different fee model than EVM chains. Instead of unified gas, TRON uses **Energy** (for smart contracts) and **Bandwidth** (for all transactions). No existing AI agent skill properly covers:

- TRON's unique resource model and cost optimization strategies
- Stake 2.0 (freezing TRX to obtain resources and earn rewards)
- Super Representative (SR) voting mechanics
- DEX aggregation across SunSwap V2/V3 and Sun.io
- The 14-day unfreezing wait period and its implications

TronLink Skills fills this gap with deep TRON-specific domain knowledge.

---

## Architecture

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

## The 6 Skills

### 1. tron-wallet (8 commands)

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

### 2. tron-token (7 commands)

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

### 3. tron-market (8 commands)

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

### 4. tron-swap (5 commands)

DEX trading and swap execution.

| Command | Description |
|---------|-------------|
| `swap-quote` | Expected output, price impact, slippage |
| `swap-route` | Optimal route across SunSwap V2/V3, Sun.io (multi-hop) |
| `swap-approve` | ERC20-style approve for token spending |
| `swap-execute` | Execute swap with user confirmation |
| `tx-status` | Track swap transaction status |

**Features:** Aggregates liquidity from multiple sources, estimates Energy cost, handles multi-hop routes, enforces human-in-the-loop confirmation.

### 5. tron-resource (7 commands)

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

### 6. tron-staking (8 commands)

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

## Recommended Skill Workflows

### Check & Transfer
```
tron-wallet (check balance) → tron-resource (estimate energy) → tron-wallet (send)
```

### Research & Buy
```
tron-token (search) → tron-market (price/chart) → tron-resource (check energy) → tron-swap (execute)
```

### Staking Flow
```
tron-wallet (check balance) → tron-staking (freeze) → tron-staking (vote) → tron-staking (claim)
```

### Resource Optimization
```
tron-resource (check status) → tron-resource (estimate cost) → tron-staking (freeze) OR tron-resource (rent)
```

---

## TRON Resource Model Reference

### Energy vs. Bandwidth

| Resource | Consumed By | Free Allowance | How to Get |
|----------|-------------|----------------|------------|
| **Bandwidth** | ALL transactions | 600/day | Freeze TRX or burn TRX |
| **Energy** | Smart contracts only | None | Freeze TRX, rent, or burn TRX |

### Cost Examples

| Operation | Bandwidth | Energy | TRX Burned (no resources) |
|-----------|-----------|--------|---------------------------|
| TRX transfer | ~267 | 0 | 0 (within free limit) |
| USDT transfer | ~345 | ~65,000 | ~13-27 TRX |
| SunSwap swap | ~345 | ~65,000-200,000 | ~13-40 TRX |
| Token approve | ~345 | ~30,000 | ~6-12 TRX |

### Stake 2.0 Key Facts
- Freeze TRX → Get Energy or Bandwidth → Vote for SR → Earn rewards
- Unfreezing has **14-day wait** before withdrawal
- Votes reset if you unfreeze; must re-vote after re-freezing
- 1 frozen TRX ≈ 4.5 Energy/day
- Voting rewards claimable every 6 hours

---

## Integration Methods

### Method 1: Claude Code (Recommended)

```bash
# Clone and use directly
git clone <repo>
cd tronlink-skills
claude   # Auto-discovers SKILL.md files
```

No `npm install` needed for read-only operations.

### Method 2: MCP Server

```bash
# Register as MCP server
claude mcp add tronlink -- node ~/.tronlink-skills/scripts/mcp_server.mjs

# Provides 25 MCP tools callable by Claude Desktop / Claude Code
```

### Method 3: Manual CLI

```bash
# Direct command execution
node scripts/tron_api.mjs wallet-balance --address TAddress...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs swap-quote --from TRX --to USDT --amount 100
```

### Method 4: Other AI Platforms

| Platform | Integration |
|----------|-------------|
| **Cursor / Windsurf** | Clone repo, use MCP or direct skill reading |
| **Codex CLI** | Symlink to `~/.agents/skills/tronlink-skills` |
| **OpenCode** | Register plugin, symlink skills |
| **LangChain / CrewAI** | Wrap `tron_api.mjs` as a Tool |

### Quick Setup Script

```bash
# Auto-install for all AI environments
bash install.sh

# Clean uninstall
bash uninstall.sh
```

---

## Configuration

### Environment Variables

```bash
# Optional: TronGrid API key for higher rate limits
export TRONGRID_API_KEY="your-api-key"

# Optional: Switch network (default: mainnet)
export TRON_NETWORK="mainnet"    # or "shasta" / "nile"

# For signing operations (choose one):
export TRON_PRIVATE_KEY="your-hex-private-key"
# or
export TRON_PRIVATE_KEY_FILE="/path/to/keyfile.txt"
```

### Network Support

| Network | URL | Use Case |
|---------|-----|----------|
| Mainnet | https://api.trongrid.io | Production |
| Shasta | https://api.shasta.trongrid.io | Testing |
| Nile | https://nile.trongrid.io | Testing |

### Built-In Token Shortcuts

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

## Project Structure

```
tronlink-skills/
├── README.md                          # Main documentation
├── package.json                       # Node.js manifest
├── install.sh                         # Auto-install for all AI environments
├── uninstall.sh                       # Clean uninstall
│
├── scripts/
│   ├── tron_api.mjs                   # Main CLI (1,248 lines, 41 commands)
│   └── mcp_server.mjs                 # MCP protocol server wrapper
│
├── skills/                            # Skill definitions (auto-discovered)
│   ├── tron-wallet/SKILL.md
│   ├── tron-token/SKILL.md
│   ├── tron-market/SKILL.md
│   ├── tron-swap/SKILL.md
│   ├── tron-resource/SKILL.md
│   └── tron-staking/SKILL.md
│
├── docs/
│   ├── claude-integration-guide.md    # 3 integration methods
│   ├── resource-model.md              # Energy & Bandwidth deep dive
│   ├── staking-guide.md               # Stake 2.0 & APY explanation
│   └── integration-guide.sh
│
├── .claude-plugin/                    # Claude Code plugin config
├── .cursor-plugin/                    # Cursor IDE plugin config
├── .opencode/                         # OpenCode config
├── .codex/                            # Codex CLI setup
├── .claude/                           # Pre-configured test commands
├── _meta.json                         # Metadata for skill registries
└── LICENSE                            # MIT
```

---

## Dependencies

| Dependency | Required? | Purpose |
|------------|-----------|---------|
| Node.js >= 18 | Yes | Runtime (native fetch, crypto) |
| tronweb ^6.0.0 | Only for signing | send-trx, send-token, staking ops |
| npm install | Not needed | Read-only operations work without it |

---

## Security Model

| Aspect | Implementation |
|--------|----------------|
| Private key handling | Environment variables only — never CLI arguments |
| Key exposure | Never passed as CLI args (visible in `ps`, shell history) |
| Signing | All signing is local via TronWeb — keys never sent to network |
| Fund movements | Human-in-the-loop confirmation required |
| Read operations | Safe — no state changes, no key needed |
| Rate limits | Public TronGrid API; use TRONGRID_API_KEY for higher limits |

---

## Address Format Support

Both formats are supported and auto-normalized across all commands:

| Format | Example | Description |
|--------|---------|-------------|
| Base58Check | `T...` (34 chars) | Standard display format |
| Hex | `41...` (42 hex chars) | Internal representation |

---

## Key Design Decisions

1. **Zero Dependencies by Default** — Read-only operations don't require npm install, making it lightweight and instant for AI agents
2. **Human-in-the-Loop for Fund Movements** — All transactions that move funds require explicit user confirmation
3. **TRON-Specific Domain Knowledge** — Dedicated skills for Energy/Bandwidth and Stake 2.0, acknowledging TRON's unique architecture
4. **Multi-Format Address Support** — Handles both Base58Check and hex formats transparently
5. **Token Symbol Resolution** — Common tokens have built-in shortcuts; unknown contracts work by address
6. **Cost Optimization Recommendations** — The `optimize-cost` command provides personalized strategies
7. **MCP Server Wrapper** — Provides structured integration for Claude Desktop and modern AI agents

---

## Quick Start

```bash
# 1. Clone
git clone <repo>
cd tronlink-skills

# 2. Use with Claude Code (no install needed for reads)
claude
> "What's the TRX balance of TAddress...?"
> "Show me the top trending tokens on TRON"
> "How much Energy do I need to send USDT?"
> "What's the best way to get Energy — freeze, rent, or burn?"

# 3. Or use directly
node scripts/tron_api.mjs wallet-balance --address TAddress...
node scripts/tron_api.mjs token-price --token USDT
node scripts/tron_api.mjs optimize-cost --address TAddress...
```
