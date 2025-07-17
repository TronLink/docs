# 打开DApp
### 使用 DeepLink 方式唤起钱包，并在 DApp 浏览器中打开 DApp
```shell 
    // Tronlink-v4.10.0
    // 链接
    <a href='tronlinkoutside://pull.activity?param={}'>Open DApp</a>
```
```shell 
    // param的参数为json格式的协议数据
    // 注意：json.toString后需要进行urlencode编码
    {
    	"url": "https://www.tronlink.org/", //目标DApp
    	"action": "open",
    	"protocol": "tronlink",
    	"version": "1.0"
    }
```

