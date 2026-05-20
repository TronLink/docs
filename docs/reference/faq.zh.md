# 常见问题

将 DApp 接入 TronLink 时的常见问题。

## `window.tron` 是 undefined / 检测不到钱包

可能是 provider 尚未注入，或未安装 TronLink。请用 TIP-6963 检测，而不要直接读 `window.tron`：监听 `TIP6963:announceProvider`，再派发 `TIP6963:requestProvider`。若无 provider 应答，则说明未安装 TronLink，提示用户安装。参见[开始开发](../dapp/getting-started.md)。

## `eth_requestAccounts` 被拒绝（错误码 `4001`）

用户拒绝了连接（点击【拒绝】、关闭弹窗，或请求不是来自当前活动标签页）。这是正常情况——捕获该错误并允许用户重试。参见[错误码](../plugin-wallet/active-requests.md)。

## 调用 `eth_requestAccounts` 返回 `-32000`

同一来源在钱包锁定期间 20 秒内重复发起了 `eth_requestAccounts`（被限流）。请稍候重试，避免反复触发请求。

## `tronWeb` 是 `false` / 未就绪

`window.tron.tronWeb` 在用户授权前为 `false`。先调用 `eth_requestAccounts`，再读取 `tronWeb`。稳妥的写法是检查 `tronProvider.tronWeb?.ready`。参见[获取 tronWeb 实例](../dapp/getting-started.md)。

## DApp 感知不到账户或网络变化

`eth_requestAccounts` 只负责初次授权。之后的变化——用户切换账户、锁定钱包、切换网络——需订阅被动事件 `accountsChanged` 与 `chainChanged`。参见[被动接收 TronLink 插件的消息](../plugin-wallet/passive-messages.md)。

## DApp 需要特定网络

用 `wallet_switchEthereumChain`（TIP-3326）请求切换，传入目标十六进制 `chainId`。参见 [chainId 取值](networks.md)与[切换网络](../plugin-wallet/active-requests.md)。通过 `chainChanged` 确认当前网络。

## 交易因资源不足而失败

链上操作会消耗 **Energy（能量）**（合约执行）与 **Bandwidth（带宽）**（交易体积）。请确保签名账户有足够资源——通过质押 TRX（Stake 2.0）或燃烧 TRX 获得。参见[术语表](glossary.md)与 [Stake 2.0](../dapp/stake2.md)。

## Ledger 签名看起来不一样（`v` 字节）

TronLink 会规范化 Ledger 签名的末尾字节（`01`→`1c`，`00`→`1b`），使 Ledger 与普通账户签名一致。参见[对 Ledger 签名后的 v 字段兼容](../plugin-wallet/ledger-signing-update.md)。

## 如何与移动端集成？

使用 DeepLink（`tronlinkoutside://`）协议拉起 TronLink App 进行登录、转账与签名。参见 [DeepLink](../mobile/deeplink.md)。

## 如何构建使用 TronLink 的 AI 智能体？

可使用 MCP 服务、智能体技能集、签名 SDK 或 CLI。从 [AI 支持](../ai-support/ai-llms.md)开始。
