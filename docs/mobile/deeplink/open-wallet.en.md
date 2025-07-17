# Open Wallet

### Launch TronLink wallet via DeepLink

```shell  
    // Tronlink-v4.10.0
    // Link
    <a href='tronlinkoutside://pull.activity?param={}'>Open Tronlink</a>
```
```shell  
    // The parameter of param is the protocol data in json format
    // Note: json.toString needs to be encoded with urlencode
    {
    	"action": "open",
    	"protocol": "tronlink",
    	"version": "1.0"
    }
```