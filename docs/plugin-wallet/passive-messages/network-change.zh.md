# 网络改变消息

消息标识： `setNode`

**简介**

开发者可以监听此消息来获取网络的改变

以下情况会产生此消息

  1. 用户改变网络的时候

**技术规范**

**代码示例**

```shell

    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "setNode") {
          // handler logic
          console.log('got setNode event', e.data)
      }
    })
```
**返回值**

```shell

    {
      "node": {
        // 当前网络的信息
      },
      "connectNode": {
        // dapp chain 的节点信息
      }
    }
```

