# /plugin-wallet 推荐用法迁移方案

> **状态：** 方案已锁版，可执行。决策汇总见 §三；中文标题锚点对策见 §4.2。

## 背景

`window.tron`（TIP-1193 provider）已成为 TronLink 的推荐接入入口，旧的 `window.tronLink` / `tronLink.tronWeb` / `tronLink.request` 仍作为兼容别名保留但不再推荐。

`/dapp` 子站已在前一轮改造中完成切换（commit `fb3cc8b`）。本方案处理 `/plugin-wallet` 下的文档对齐。

## 范围

- `docs/plugin-wallet/active-requests.zh.md`
- `docs/plugin-wallet/active-requests.en.md`
- `docs/plugin-wallet/passive-messages.zh.md`
- `docs/plugin-wallet/passive-messages.en.md`

`ledger-signing-update.{zh,en}.md` 不涉及 provider，不动。

## 总体原则

1. **每篇文档主体只展示推荐用法（`window.tron`）。**
2. **每篇文档底部统一新增"旧版用法（不推荐）"区，集中放置 `window.tronLink` 等兼容用法。**
3. **新版的每个具体接口小节，末尾以一行 blockquote callout 链接到底部对应的旧版条目。**
4. **不删除任何旧 API 文档信息，只是搬位 + 重新组织。**

---

## 一、active-requests 改造

### 1.1 当前结构与处理对照

| # | 当前小节 | 当前 API | 处理动作 |
|---|---|---|---|
| 1 | 连接网站 TIP-1102 | 新 `tron.request` | 保留为主版，末尾加旧版链接 |
| 2 | 连接网站（旧版）`tron_requestAccounts` | 旧 | **整段移到底部"旧版用法"区** |
| 3 | 获取 provider TIP-6963 | 新 | 保留，不动 |
| 4 | 普通转账 | 旧 `window.tronLink.ready` | **重写为新版**；原旧版代码片段拆出搬到底部 |
| 5 | 多签转账 | 旧 | 同上 |
| 6 | 消息签名 | 旧 | 同上 |
| 7 | 添加资产 | 主示例新 / 三个子例旧 | 子例改为 `window.tron.request`；原旧代码搬到底部 |
| 8 | 切换网络 TIP-3326 | 旧 `tronLink.request` | 改为 `window.tron.request`；旧版搬到底部 |

### 1.2 目标骨架

```
# 主动请求TronLink插件功能

### 连接网站 TIP-1102
… 现有内容 …
> **旧版用法（不推荐）：** [兼容用法：tron_requestAccounts](#tron_requestaccounts)

### 获取TronLink的provider TIP-6963
（不动）

### 普通转账
> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见上方 [连接网站 TIP-1102](#tip-1102)）。
（代码改为 `const tronweb = window.tron.tronWeb; …`，去掉 `if (window.tronLink.ready)` 包裹）
> **旧版用法（不推荐）：** [兼容用法：sendTrx（window.tronLink）](#sendtrx-window-tronlink)

### 多签转账
（前提条件 + 新代码 + 链接到旧版）

### 消息签名
（同上）

### 添加资产
（主示例已是新 API；TRC10/20/721 三个子例去掉 if 包裹，改 `window.tron.request`）
> **旧版用法（不推荐）：** [兼容用法：wallet_watchAsset（window.tronLink）](#wallet_watchasset-window-tronlink)

### 切换网络 TIP-3326
（代码改为 `await window.tron.request(...)`）
> **旧版用法（不推荐）：** [兼容用法：wallet_switchEthereumChain（tronLink.request）](#wallet_switchethereumchain-tronlinkrequest)

---

## 旧版用法（不推荐）

下列接口作为兼容别名保留，新接入请使用上方推荐用法。`window.tronLink` 与 `window.tron` 在功能上等价，但前者将逐步不再维护。

### 兼容用法：tron_requestAccounts
（搬自原"连接网站（旧版）"整段）

### 兼容用法：sendTrx（window.tronLink）
（搬自原"普通转账"代码示例）

### 兼容用法：multiSign（window.tronLink）
…

### 兼容用法：signMessageV2（window.tronLink）
…

### 兼容用法：wallet_watchAsset（window.tronLink）
（搬自原"交互流程"下三个 TRC 子例）

### 兼容用法：wallet_switchEthereumChain（tronLink.request）
（搬自原"切换网络"代码示例）
```

### 1.3 锚点策略

MkDocs 默认 slug 会剥掉中文，保留 ASCII token 用 `-` 拼接、转小写、保留下划线。可在标题里以"兼容用法：<ASCII 方法名>"形式预埋稳定锚点：

| 中文标题 | 生成 slug |
|---|---|
| `### 兼容用法：tron_requestAccounts` | `tron_requestaccounts` |
| `### 兼容用法：sendTrx（window.tronLink）` | `sendtrx-window-tronlink` |
| `### 兼容用法：multiSign（window.tronLink）` | `multisign-window-tronlink` |
| `### 兼容用法：signMessageV2（window.tronLink）` | `signmessagev2-window-tronlink` |
| `### 兼容用法：wallet_watchAsset（window.tronLink）` | `wallet_watchasset-window-tronlink` |
| `### 兼容用法：wallet_switchEthereumChain（tronLink.request）` | `wallet_switchethereumchain-tronlinkrequest` |

英文版用 `### Legacy: <method>` 形式，slug 形如 `legacy-tron_requestaccounts`、`legacy-sendtrx-via-windowtronlink` 等。

### 1.4 callout 文案

新版小节末尾统一插入：

**中文：**
```markdown
> **旧版用法（不推荐）：** [兼容用法：sendTrx（window.tronLink）](#sendtrx-window-tronlink)
```

**英文：**
```markdown
> **Legacy (not recommended):** [Legacy: sendTrx via window.tronLink](#legacy-sendtrx-via-windowtronlink)
```

前提条件 callout（覆盖普通转账 / 多签转账 / 消息签名 / 添加资产，共 4 节；切换网络不加）：

**中文：**
```markdown
> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见上方 [连接网站 TIP-1102](#tip-1102)）。
```

**英文：**
```markdown
> **Prerequisite:** The DApp connection has been authorized via `eth_requestAccounts` (see [Request to connect website TIP-1102](#request-to-connect-website-tip-1102) above).
```

> 切换网络不需要预先授权，**不加**"前提条件"callout。

---

## 二、passive-messages 改造

### 2.1 现状

主体已基于 `window.tron`，底部已有两块旧版区域：

- **历史遗留问题**：postMessage 派发的 `connectWeb` / `acceptWeb` / `rejectWeb` / `disconnectWeb`（3.x 兼容事件，未来会废弃）。
- **已废弃的 3.x 事件**：`tabReply` / `setAccount` / `setNode`（主链 / 侧链检测）。

### 2.2 两种处理方案

**方案 A（推荐 · 最小变更）**

- 保留现有两个旧版区结构（4.x postMessage 兼容 vs 3.x 主侧链）。
- 在新版的 `accountsChanged` / `chainChanged` / `connect` / `disconnect` 四个小节末尾各加一行 callout，链接到对应的旧版条目。
- 顶部 demo 代码块（HTML 示例）保持不动。

新→旧映射建议：

| 新版事件 | 旧版对应（链接目标） |
|---|---|
| `accountsChanged` | `setAccount`（3.x） |
| `chainChanged` | `setNode` / `tabReply`（3.x） |
| `connect` | `connectWeb` / `acceptWeb`（postMessage） |
| `disconnect` | `disconnectWeb` / `rejectWeb`（postMessage） |

**方案 B（彻底对齐 active-requests）**

把两个旧版区合并成单一"## 旧版用法（不推荐）"大区，内部再分子小节。

**结论：选 A。** 现有两个旧版区主题不同（兼容事件 vs 3.x 主侧链），强行合并反而模糊。结构基本不动，只补 callout 链接。

---

## 三、确认事项（已锁定）

| # | 项 | 决定 |
|---|---|---|
| 1 | 前提条件 callout 覆盖范围 | 转账 / 多签 / 消息签名 / **添加资产**（共 4 节）；切换网络不加 |
| 2 | callout 措辞 | `**旧版用法（不推荐）：**` |
| 3 | passive-messages | 方案 A（保留两块旧版区，新版小节补链接） |
| 4 | TIP-1102 是否链旧版 | 链到 `兼容用法：tron_requestAccounts` |
| 5 | 旧版区开篇说明 | 一两句简短说明（"作为兼容别名保留，新接入请使用上方推荐用法。`window.tronLink` 与 `window.tron` 在功能上等价，但前者将逐步不再维护。"） |

---

## 四、已知风险与对策（执行前必读）

### 4.1 风险：纯中文 `###` 标题的锚点不可靠

`普通转账` / `多签转账` / `消息签名` / `添加资产` 这 4 个小节标题全是中文，mkdocs 默认 slug 会剥到空串，被自动加上 `_1`、`_2` 等位置 fallback。现有文件里的 `[普通转账](#_13)` 就是这种情况 —— 数字 `13` 是页面内累计的空 slug 计数器，**不能在文件重排后稳定预测**。

这会影响：

- 新版小节里"参见上方 [普通转账]" / "参见上方 [多签转账]" 等回链
- 底部"旧版用法"区的"新接入请使用上方 [普通转账]"等回链
- TIP-1102 顶部如果想链到任何一节，同样有问题

> 注：`TIP-1102` / `TIP-6963` / `TIP-3326` 这几节标题混了 ASCII，slug 可稳定预测为 `#tip-1102` / `#tronlinkprovider-tip-6963` / `#tip-3326`，不受影响。

### 4.2 对策（三选一，请挑选）

**对策 A：给纯中文小节标题加 ASCII 方法名后缀（推荐）**

改为：
- `### 普通转账 sendTrx` → slug `sendtrx`
- `### 多签转账 multiSign` → slug `multisign`
- `### 消息签名 signMessageV2` → slug `signmessagev2`
- `### 添加资产 wallet_watchAsset` → slug `wallet_watchasset`

优点：slug 完全可控；标题里直接显示方法名对开发者也是好事；跟既有 `获取TronLink的provider TIP-6963` 这种"中英混合标题"风格一致。  
缺点：每个小节标题变长一截，视觉略变化。

**对策 B：不在新版小节之间互链，纯中文方位词描述**

如"参见上方「普通转账」"，不写 markdown 链接。

优点：标题不动。  
缺点：放弃了点击跳转的便利；侧栏 / 目录里的"普通转账"虽然可点击，但行文中没有热区。

**对策 C：跑一次 mkdocs build，把生成的真实 slug 反写回链**

优点：保留中文标题。  
缺点：必须先 build 一遍；任何后续小节顺序变化都会让 `_N` 编号漂移，长期维护成本高；放弃了"自描述性"。

**已确认：对策 A。** 4 个纯中文小节标题改为：

- `### 普通转账 sendTrx`（slug `sendtrx`）
- `### 多签转账 multiSign`（slug `multisign`）
- `### 消息签名 signMessageV2`（slug `signmessagev2`）
- `### 添加资产 wallet_watchAsset`（slug `wallet_watchasset`）

### 4.3 旧版区标题的锚点

旧版区的标题都预埋了 ASCII 方法名（`### 兼容用法：tron_requestAccounts` 等），slug 可控（见 §1.3 表）。**不受 4.1 影响。**

### 4.4 跨页引用检查

仓库内只有 2 处对 `active-requests.md#xxx` 锚点的跨页引用，且都指向 TIP-6963 小节（slug `tronlinkprovider-tip-6963` / `get-tronlink-provider-via-tip-6963`），本次方案 **不动这个小节**，不会断链：

```
docs/plugin-wallet/passive-messages.zh.md:93  → #tronlinkprovider-tip-6963
docs/plugin-wallet/passive-messages.en.md:93  → #get-tronlink-provider-via-tip-6963
```

---

## 五、执行步骤（确认对策 A/B/C 后开工）

1. `active-requests.zh.md` 重排：
   - 删除原"连接网站（旧版）"小节，整段搬到底部"旧版用法"区
   - 4 个业务小节（普通转账 / 多签转账 / 消息签名 / 添加资产）：
     - 按对策 A/B/C 处理小节标题
     - 顶部插入"前提条件" callout
     - 代码改为 `const tronweb = window.tron.tronWeb; …`，去 `if (window.tronLink.ready)` 包裹
     - 末尾插入"旧版用法（不推荐）"链接 callout
   - 切换网络小节：代码改为 `window.tron.request(...)`；末尾加旧版链接；不加前提条件
   - TIP-1102 小节末尾加旧版链接（指向 `兼容用法：tron_requestAccounts`）
   - 文末新增 `## 旧版用法（不推荐）` 大区，下设 6 个 `###` 兼容用法子节
2. `active-requests.en.md` 同步以上改动（英文标题天然有 ASCII slug，不涉及对策 A/B/C 取舍）
3. `passive-messages.zh.md` 4 个事件小节（accountsChanged / chainChanged / connect / disconnect）末尾各加一行旧版 callout，链接到对应 postMessage / 3.x 子节
4. `passive-messages.en.md` 同步
5. 本地 `mkdocs serve` 校验全部站内锚点跳转可用，无 404
6. 一次性 commit：`migrate plugin-wallet docs to window.tron and isolate legacy usage`

## 六、影响面

- **不破坏现有接入**：旧 API 用法全部保留在底部"旧版用法"区，搜索引擎与现有外链可继续命中。
- **mkdocs.yml 不需要改**：导航条目数量不变；不引入 admonition 等新扩展。
- **跨页引用**：见 §4.4，无断链风险。
- **未涉及 mobile 端**：移动端 DApp 注入逻辑不同，本次不动。
