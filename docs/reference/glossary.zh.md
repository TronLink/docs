# 术语表

本文档各处用到的术语、标准与标识符释义。

## TRON 与代币

- **TRX** —— TRON 网络的原生代币。
- **SUN** —— TRX 的最小单位，`1 TRX = 1,000,000 SUN`。交易金额以 SUN 表示。
- **TRC-10** —— TRON 原生代币标准，在协议层管理（用数字 token id 标识）。
- **TRC-20** —— TRON 的智能合约同质化代币标准（类比以太坊 ERC-20）。
- **TRC-721** —— TRON 的非同质化代币（NFT）标准（类比 ERC-721）。
- **Energy（能量）** —— 执行智能合约操作时消耗的资源，通过质押 TRX（Stake 2.0）或燃烧 TRX 获得。
- **Bandwidth（带宽）** —— 按交易字节大小消耗的资源，通过质押或燃烧 TRX 获得；每个账户每天有少量免费额度。
- **Stake 2.0** —— TRON 的资源质押模型。质押 TRX 产出能量或带宽，资源可代理给其他账户（`DelegateResourceContract` / `UnDelegateResourceContract`）。参见 [Stake 2.0](../dapp/stake2.md)。

## 钱包对象与 SDK

- **TronWeb** —— 用于构造、签名、广播 TRON 交易的 JavaScript SDK。参见 [TronWeb 文档](https://tronweb.network/docu/docs/intro)。
- **`window.tron`** —— TronLink 注入到页面的 provider 对象，暴露 `request`、`tronWeb`、`on` / `removeListener`。
- **`tronWeb`（实例）** —— 绑定到用户账户/网络的 `TronWeb` SDK 实例，授权后通过 `window.tron.tronWeb` 获取；授权前为 `false`。
- **`window.tronLink`** —— 旧版 provider 对象（已不推荐，由 `window.tron` 取代）。
- **`iTron`** —— 仅在 TronLink 移动端内置 DApp 浏览器中注入的对象，暴露 App 端原生能力。参见 [DApp 支持](../mobile/dapp-support.md)。
- **HD 钱包** —— 分层确定性钱包（BIP-32），由单一种子派生出多个密钥对；**BIP-44** 定义派生路径结构；种子以**助记词**表示。参见 [HD 钱包](../hd-wallets.md)。

## 标准与提案

- **TIP** —— TRON Improvement Proposal（TRON 改进提案），索引见 [github.com/tronprotocol/tips](https://github.com/tronprotocol/tips)。
- **EIP** —— Ethereum Improvement Proposal（以太坊改进提案）。TronLink 复用了若干 EIP 方法名以保持兼容。
- **TIP-1102 / EIP-1102** —— 钱包连接请求（`eth_requestAccounts`）。参见[主动请求 TronLink 插件功能](../plugin-wallet/active-requests.md)。
- **TIP-1193 / EIP-1193** —— provider 接口及其事件（`connect`、`disconnect` 等），含 `ProviderRpcError` 结构。
- **TIP-3326 / EIP-3326** —— 切换网络请求（`wallet_switchEthereumChain`）。
- **TIP-6963 / EIP-6963** —— 通过 `announceProvider` / `requestProvider` 事件做多钱包 provider 发现，使 DApp 无需抢占 `window.tron` 即可选定特定钱包。

## 类型与标识符

- **ABI** —— Application Binary Interface，合约可调用方法与事件的 JSON 描述。若代币合约的 ABI 缺少可识别的方法（如 `transfer`、`approve`），TronLink 可能无法提供相应操作。
- **`chainId`** —— 网络标识。TronLink 在 `wallet_switchEthereumChain` 和 `chainChanged` 用十六进制形式（如 `0x2b6653dc`），在 EIP-712 的 `domain.chainId` 用十进制 EVM 形式（如 `728126428`）。参见[网络与地址](networks.md)。
- **`ProviderRpcError`** —— EIP-1193 在 `disconnect` 时抛出的错误对象，结构为 `{ code: number; message: string; data?: unknown }`。
- **permission id** —— 多签交易使用的活动权限索引（传给 `tronWeb.trx.multiSign`）。参见[多签转账](../dapp/multi-sign-transfer.md)。
- **base58 / hex 地址** —— TRON 地址的两种编码（`T...` 与 `41...`）。参见[网络与地址](networks.md)。

## AI 工具

- **MCP** —— Model Context Protocol，TronLink 的 AI 服务实现的标准，使智能体可调用钱包工具。参见 [AI 支持](../ai-support/ai-llms.md)。
- **DeepLink** —— `tronlinkoutside://` URL 协议，用于从 DApp 或 H5 页面驱动 TronLink 移动端。参见 [DeepLink](../mobile/deeplink.md)。
