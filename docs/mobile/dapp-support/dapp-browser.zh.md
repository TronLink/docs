# Dapp 浏览器

### 基本功能

DApp 浏览器支持运行 TRON DApp，并自动注入 tronWeb 及 tronLink 对象

### 扩展

在 DApp 浏览器中运行的 Tron DApp，会自动注入 iTron 对象，并提供 App 端定制化功能

  * 切换屏幕方向

```shell   
        // url: DApp page url
        // screenModel: "1" -> 竖屏；"2" -> 横屏
        public void setScreenModel(String url, String screenModel)
```

