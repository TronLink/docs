# 登陆授权

使用Deeplink方式唤起钱包，并在钱包中选择获取钱包地址

```shell 
    // Tronlink-v4.11.0
    // 链接
    <a href='tronlinkoutside://pull.activity?param={}'>Login/Request Address</a>
```

```shell 
    // param的参数为json格式的协议数据
    // 注意：json.toString后需要进行urlencode编码
    {
      "url": "https://justlend.org/#/home",
      "callbackUrl": "http://xxx/api/tron/v1/callback",
      "dappIcon": "https://test/icon.png",
      "dappName": "Test demo",
      "protocol": "TronLink",
      "version": "1.0",
      "chainId": "0x2b6653dc",
      "action": "login",
      "actionId": "e5471a9c-b0f1-418b-8634-3de60d68a288"
    }
```
```shell 
    {
      "actionId": "e5471a9c-b0f1-418b-8634-3de60d68a288",
      "address": "TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig",
      "code": 0,
      "id": 1780812177,
      "message": "success"
    }
```    