# 断开连接网站消息

消息标识： `disconnect`

**简介**

开发者可以监听此消息来获取网络的改变。

以下情况会产生此消息：

  1. DApp 请求连接，用户在弹窗中拒绝连接后

  2. 用户主动断开连接网站

**技术规范**

**代码示例**

```shell

    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "disconnect") {
          // handler logic
          console.log('got connect event', e.data)
      }
    })
```

