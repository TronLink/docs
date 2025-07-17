# Sign Transaction

```shell
  // Tronlink-v4.11.0
  // Link
  <a href='tronlinkoutside://pull.activity?param={}'>Sign transaction</a>
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
    "action": "sign",
    "loginAddress": "TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig",
    "method": "transfer(address,uint256)",
    "signType": "signTransaction",
    "data": "{\"visible\":false,\"txID\":\"dcfaf2c2d75d91994f9a23623e905eaa7d74bc804fa5821640111ada3441376a\",\"raw_data\":{\"contract\":[{\"parameter\":{\"value\":{\"data\":\"a9059cbb000000000000000000000000ed87a3ae2bf2ab8b95486a23f224487ad75c60200000000000000000000000000000000000000000000000000000000000000014\",\"owner_address\":\"41b42b84bad413dde093e27d01bb02ed9eede52c43\",\"contract_address\":\"41eca9bc828a3005b9a3b909f2cc5c2a54794de05f\"},\"type_url\":\"type.googleapis.com/protocol.TriggerSmartContract\"},\"type\":\"TriggerSmartContract\"}],\"ref_block_bytes\":\"84e1\",\"ref_block_hash\":\"1731d6450e11a03f\",\"expiration\":1670168865000,\"fee_limit\":100000000,\"timestamp\":1670168805340},\"raw_data_hex\":\"0a0284e122081731d6450e11a03f40e8d1c9eecd305aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a1541b42b84bad413dde093e27d01bb02ed9eede52c43121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f2244a9059cbb000000000000000000000000ed87a3ae2bf2ab8b95486a23f224487ad75c6020000000000000000000000000000000000000000000000000000000000000001470dcffc5eecd30900180c2d72f\"}",
    "actionId": "64fcdb39-2cfa-47f2-85bd-d7e8409809ed"
  }
```
```shell 
  // callback parameter
  {
    "actionId": "f5d9791a-c774-4684-805a-83784c0c86ff",
    "code": 0,
    "id": -799302342,
    "message": "success",
    "successful": true,
    "transactionHash": "2fc49e560f648e5ecb455955d8778267ec1f257436425f62393b632c9a7a55ad"
  }
```
