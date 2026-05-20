# 网络与地址

汇总本文档各处用到的网络参数与常用地址。

## 网络

| 网络 | `chainId`（十六进制） | EVM chainId（十进制） | RPC 端点 | 浏览器 |
|---|---|---|---|---|
| 主网 | `0x2b6653dc` | `728126428` | `https://api.trongrid.io` | [tronscan.org](https://tronscan.org) |
| Shasta 测试网 | `0x94a9059e` | `2494104990` | `https://api.shasta.trongrid.io` | [shasta.tronscan.org](https://shasta.tronscan.org) |
| Nile 测试网 | `0xcd8690dc` | `3448148188` | `https://nile.trongrid.io` | [nile.tronscan.org](https://nile.tronscan.org) |

- 十六进制 `chainId` 用于 `wallet_switchEthereumChain`（TIP-3326）和 `chainChanged` 事件。**`chainId` 区分大小写。**
- EVM（十进制）chainId 用于 EIP-712 类型化数据签名的 `domain.chainId` 字段。

## 测试网水龙头

- Shasta：在 [Shasta 水龙头](https://www.trongrid.io/shasta)领取测试 TRX。
- Nile：在 [Nile 水龙头](https://nileex.io/join/getJoinPage)领取测试 TRX。

## 地址格式

TRON 地址有两种可互转的编码：

- **Base58** —— 以 `T` 开头，例如 `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`，是面向用户的形式。
- **Hex** —— 以 `41` 开头，例如 `41...`，是链上/原始形式（`41` 是 TRON 的地址前缀字节）。

`tronWeb.address.toHex()` / `tronWeb.address.fromHex()` 可在两者间转换。

## 单位

- `1 TRX = 1,000,000 SUN`。`tronWeb` 交易构造器（如 `sendTrx`）中的金额以 **SUN** 为单位。

## 常用代币合约（主网）

| 代币 | 标准 | 合约地址 |
|---|---|---|
| USDT | TRC-20 | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` |

其他代币请在 [TronScan](https://tronscan.org/#/tokens) 查询其合约地址。集成前务必核对代币合约地址——不同网络上的地址不同。
