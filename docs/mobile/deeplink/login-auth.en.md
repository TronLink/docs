
# Login by TronLink

```shell  
    // Tronlink-v4.11.0
    // Link
    <a href='tronlinkoutside://pull.activity?param={}'>Login/Request Address</a>
```
```shell 
    
    //  The parameter of param is the protocol data in json format
    //  Note: json.toString needs to be encoded with urlencode
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
