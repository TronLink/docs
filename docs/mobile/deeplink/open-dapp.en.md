# Open DApp

### Use DeepLink to launch TronLink and open DApp in the DApp Explorer

```shell  
    // Tronlink-v4.10.0
    // Link
    <a href='tronlinkoutside://pull.activity?param={}'>Open DApp</a>
```
```shell 
    
    //  The parameter of param is the protocol data in json format
    //  Note: json.toString needs to be encoded with urlencode
    {
    	"url": "https://www.tronlink.org/", //target DApp
    	"action": "open",
    	"protocol": "tronlink",
    	"version": "1.0"
    }
```