# DApp支持

提供流畅的 DApp 浏览器，支持运行 TRON DApp。


## 集成TronLink

TronLink App 内置 DApp 浏览器，对于在其上运行的 TRON DApp，TronLink 会自动将 tronWeb 及 tronLink 对象注入到该 DApp。从而允许 DApp 与 TronLink App，以及TRON 网络交互。

App 内置浏览器支持通过 TIP-6963 发现 Provider，并通过 `eth_requestAccounts` 请求连接授权。可参考[开始开发](../dapp/getting-started.md)中的发现和授权步骤，再用授权后的 TronWeb 实例构建交易。如果 DApp 依赖 `accountsChanged` 或 `chainChanged`，请在目标 App 版本上验证这些事件。

从外部移动浏览器唤起 TronLink 请参考 [DeepLink](deeplink.md)。

## Dapp 浏览器

### 基本功能

DApp 浏览器支持运行 TRON DApp，并自动注入 tronWeb 及 tronLink 对象

### 扩展

在 DApp 浏览器中运行的 Tron DApp，会自动注入 iTron 对象，并提供 App 端定制化功能

  * 切换屏幕方向

```java
        // url: DApp page url
        // screenModel: "1" -> 竖屏；"2" -> 横屏
        public void setScreenModel(String url, String screenModel)
```

