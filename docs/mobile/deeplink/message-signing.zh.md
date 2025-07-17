# 消息签名

```shell 
    // Tronlink-v4.11.0
    // 链接
    <a href='tronlinkoutside://pull.activity?param={}'>Sign message</a>
```
```shell 
    // request parameter
    {
      "url": "https://justlend.org/#/home",
      "callbackUrl": "http://3.12.131.175:7777/api/tron/v1/callback",
      "dappIcon": "https://test/icon.png",
      "dappName": "Test demo",
      "protocol": "TronLink",
      "version": "1.0",
      "chainId": "0x2b6653dc",
      "loginAddress": "TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig",
      "signType": "signStr",
      "message": "abc",
      "action": "sign",
      "actionId": "50554861-4861-41c4-adf3-abf36213f843"
    }
```
```shell 
    // callback parameter
    {
      "actionId": "50554861-4861-41c4-adf3-abf36213f843",
      "code": 0,
      "id": 2001871012,
      "message": "success",
      "signedData": "0xffcac5731d9f70a58e5126f44c34b9356ccb9bef53331e33ddab84bb829adc1b77df24362348f8d46e506b489b4af4496600799b173e708faf1b9db99da9d13c1b"
    }
```

