# 错误码对照表

TronLink 智能体在一次用户请求里跨 DApp provider → DeepLink → MCP → CLI 时,会先后碰到三四套错误码方言。本页是以**业务含义**为主轴的横向对照,用来把任一方言里的错误码翻译到其他方言,并判断重试是否安全。

> 各列表头链接的"每个 surface 自己的错误表"仍然是 SSOT,本页只是导航工具——遇到歧义时,以**你实际调用的那个 surface 的结构化字段**为准(MCP Server TronLink 看 `error.code`;MCP TronLink Signer 看 `Error: <message>` 文本;CLI 看退出状态和 stderr 的 `error` 字符串;`window.tron.request` 看 `code` 字段(`tronWeb.trx.*` 签名看拒签字符串);DeepLink 看回调里的 `code`)。

**错误结构：** 在 TronLink 注入的 `tronWeb` 上（插件 4.0.0 起），用户拒绝 `trx.sign`、`trx.multiSign` 或 `trx.signMessageV2` 时，Promise 以**纯字符串** `'Confirmation declined by user'` reject——不是 `Error` 对象，也没有数字 `code`。`{ code: 4001, message: 'User rejected the request.' }` 对象只由 `window.tron.request(...)` 方法（如 `eth_requestAccounts`）返回。其他失败（钱包未解锁、载荷非法、观察钱包等）返回其他值——参见[处理拒签](#handling-rejections)。不要自动重试签名。

| 业务含义 | DApp provider([EIP-1474][provider]) | DeepLink([5 位码][deeplink]) | MCP([`TL_*`][mcp]) | CLI v1.0.1([退出状态][cli]) | 可重试? |
| --- | :---: | :---: | :---: | :---: | :---: |
| **用户拒绝**签名或连接弹窗 | `window.tron.request(...)` 为 `4001`；`tronWeb.trx.sign` / `multiSign` / `signMessageV2` 为字符串 `'Confirmation declined by user'` | `300`(交易取消) | —(HITL——只能在新的 tool 调用里再次唤起) | `1` | **否** |
| **参数非法** / payload 错 | `tronWeb` 构造器抛错 | `10001`–`10020`、`10024`、`10025` | `TL_INVALID_INPUT` | `1` | **否**——修参数 |
| **方法 / capability 不支持** | `4200` | `10003`、`10008`、`10009`、`10011`、`10023` | `TL_CAPABILITY_NOT_AVAILABLE` | — | **否** |
| **钱包授权不匹配**(发起地址 ≠ 当前钱包) | provider 返回空 `accounts[]` | `10021`、`10022` | — | — | **否**——重新授权 |
| **没有钱包 / 无会话** | provider 未注入(`window.tron` 不存在) | `10016` | `TL_NO_ACTIVE_SESSION` | — | **否**——先初始化 / `tl_launch` |
| **限流 / 钱包锁定** | `-32000`(20 秒内重复 `eth_requestAccounts` 且钱包锁定) | — | — | — | **是**——等一会儿再试 |
| **网络 / RPC 抖动**(TronGrid、RPC 错) | `tronWeb` 调用里的 TronGrid HTTP 错 | — | `TL_CHAIN_QUERY_FAILED`、`TL_GASFREE_QUERY_FAILED`、`TL_MULTISIG_QUERY_FAILED` | `1` | **是** |
| **链上执行失败**(广播后:`REVERT`、`OUT_OF_ENERGY`、`FAILED`) | `sendRawTransaction` 抛错或经 `getTransactionInfo` 暴露 | — | `TL_CHAIN_SEND_FAILED`、`TL_CHAIN_SWAP_FAILED`、`TL_GASFREE_SEND_FAILED`、`TL_MULTISIG_SUBMIT_FAILED` | `1` | **否**——交易已 final;查根因;**永远不要**自动重试写操作 |
| **超时**(用户没及时签 / 元素找不到) | 调用解析慢,无规范化的码 | — | `TL_WAIT_TIMEOUT`、`TL_NAVIGATION_FAILED` | `1` | **视情况**——读操作可以;**可能已被广播的写操作**先用 `tronWeb.trx.getTransactionInfo` / `tl_chain_get_tx` 对账后再决定 |
| **内部 / 未知** | `-32603`(Internal error) | — | `TL_INTERNAL_ERROR`、`TL_LAUNCH_FAILED` | — | **可重试一次**——再失败带 log 上报 |

[provider]: ../dapp/getting-started.md
[deeplink]: ../mobile/deeplink.md
[mcp]: ../ai-support/tronlink-mcp-core.md
[cli]: ../ai-support/tronlink-cli.md

<a id="handling-rejections"></a>

## 处理拒签

除上文所述的用户拒绝值外，签名方法还可能返回：`'User has not unlocked wallet'`（钱包未解锁，或 DApp 授权后已断开连接）、`'Invalid transaction provided'`（载荷非法，或钱包内部签名失败）、`'Transaction integrity check failed'`（4.11.1 起；载荷未通过 TronLink 完整性校验，如非字符串消息——在用户关闭 TronLink 警告弹窗后返回）、`{ code: 4100, message: 'Watch accounts cannot sign' }`（观察钱包；4.10.0 起）。无法识别的值应按意外错误处理，不要当作用户拒绝。

```javascript
function isUserRejection(err) {
  if (typeof err === 'string') return err === 'Confirmation declined by user';
  return err != null && err.code === 4001;
}

try {
  const signed = await window.tron.tronWeb.trx.sign(tx);
} catch (err) {
  if (isUserRejection(err)) {
    // 用户拒绝——不要自动重试
  } else {
    // 未解锁、载荷非法、观察钱包或其他意外错误——检查 err
  }
}
```

## 使用方式

1. 在任一 surface 收到错误后,在表里找到对应的业务含义行,横向读出其他 surface 的对应码(或空白)。
2. **可重试?** 列是给智能体的安全提示:
    - **否**——自动重试会失败甚至有害。最危险的是"链上执行失败",此时交易已上链,无法撤回。
    - **是**——临时性问题,退避(指数,最多 3 次)后重试原调用。
    - **视情况**——读操作可以重试;**写操作不要在没对账的情况下自动重试**。
3. DeepLink 和 CLI 两列有很多空白,是因为这两个 surface 只覆盖了生命周期的一段——DeepLink 仅限移动端且跨信任边界;CLI v1.0.1 所有失败都退出 `1`，该列无法区分失败类别，请改读 stderr 中的 `error` 字符串（`—` 表示 CLI 没有对应的专门情况，任何失败仍退出 `1`）。CLI 写命令退出 `1` 时，即使该行标为**是**也不能自动重试——先在链上确认。**用得到哪个 surface 就以哪个 surface 为准**。

## 给下游 MCP 服务的约束

基于 TronLink MCP Core 的下游 MCP 服务(如自定义 Skills)**必须复用**本表里的 `TL_*` 码,不要自创新字符串。如果出现了新的业务含义,先在本页加行 + 在 `tronlink-mcp-core`(SSOT)加新的 `TL_*` 常量,再在消费端引用——**不要在消费端临时造码**。
