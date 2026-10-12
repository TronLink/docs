# 消息签名

## 简介

DApp 可以请求用户对消息签名，再将消息与签名转发给后端验签，以此验证用户登录。

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

## 技术规范

### 代码示例

```javascript
const tronweb = window.tron.tronWeb;
try {
  const message = "0x01EF"; // UTF-8 文本，不是原始 hex 字节
  const signedString = await tronweb.trx.signMessageV2(message);
} catch (e) {}
```

### 参数

本例使用的是外观类似 hex 的**字符串**。TronWeb 的 `signMessageV2` 会将字符串按 UTF-8 编码：`"0x1234"` 表示六个文本字符（字节为 `30 78 31 32 33 34`），不等于两个原始字节 `12 34`。签名与验签必须使用相同的消息表示；V2 签名应使用 `verifyMessageV2` 验签。参见 [TronWeb 消息签名与验签说明](https://tronweb.network/docu/docs/Sign%20and%20Verify%20Message/)。

TronLink 注入的钱包桥接接口允许哪些输入类型，需要按所支持的 TronLink 与 TronWeb 版本验证。本例不构成钱包桥接支持任意 UTF-8 文本、数字数组或 `Uint8Array` 的承诺。

### 返回值

如果用户在弹窗中选择签名, DApp 可以得到签名后的十六进制字符串, 比如：

```text
    0xb0e0b150b9b10dc348f25c7f38fc87f16e18c0d230d23946aac519a5ad9e45937f656012d33c09e9d9dec00b03fbb304e797f8991bb823dce676ac91e03a55991b
```

如果报错，则会返回如下信息：

```text
    Uncaught (in promise) Invalid transaction provided
```

## 交互流程

当代码执行到`await tronweb.trx.signMessageV2(message);`时，TronLink 钱包会提示弹窗，需要用户进行确认， 如下图, 其中消息内容会以hex的方式展示：

![TronLink 消息签名审批弹窗，以 hex 形式展示待签消息与"拒绝"/"签名"按钮](../images/zh_plugin-wallet_sign_message.png)

如果用户在弹窗中选择【拒绝】，则会抛出异常，开发者可捕获此异常进行业务处理。

## 错误码

**接口区别：** `provider.request(...)` 文档中的错误码（例如用户拒绝时的 `4001`）不是 `tronWeb.trx.sign`、`multiSign` 或 `signMessageV2` 的通用契约。请捕获签名异常，数字 `code` 可能不存在。分类前应验证所支持的 TronLink/TronWeb 版本的异常结构；未知异常不能直接认定为用户拒绝。不要自动重试签名。

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| (抛出；结构取决于版本) | 用户在签名弹窗里点【拒绝】 | `tronWeb.trx.signMessageV2(message)` | 否——用户拒绝 |
| (抛出) | 输入非法，例如 `Invalid transaction provided` | `signMessageV2(...)` / 钱包桥接校验 | 否——核对所支持版本的输入规则 |
| (抛出) | provider 未注入 / 钱包未授权 | `window.tron.tronWeb` 未定义 | 否——先通过 `eth_requestAccounts` 连接 |

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。

