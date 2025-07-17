# 打开钱包

### 使用 DeepLink 方式唤起钱包
```shell 
    // Tronlink-v4.10.0
    // 链接
    <a href='tronlinkoutside://pull.activity?param={}'>Open Tronlink</a>
```
```shell 
    // param的参数为json格式的协议数据
    // 注意：json.toString后需要进行urlencode编码
    {
    	"action": "open",
    	"protocol": "tronlink",
    	"version": "1.0"
    }
```

