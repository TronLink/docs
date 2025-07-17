# 用户确定连接消息

<span class="deprecated">DEPRECATED</span>

消息标识： `acceptWeb`

以下情况会产生此消息

  1. 用户确定连接消息

 ![image](../../../images/zh_cha-jian-qian-bao_bei-dong-jie-shou-tronlink-cha-jian-de-xiao-xi_ji-jiang-fei-qi-de-xiao-xi_yong-hu-que-ding-lian-jie-xiao-xi_img_0.jpg)

开发者可以监听此消息来获取用户确定连接消息

```shell

    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "acceptWeb") {
          // handler logic
          console.log('got acceptWeb event', e.data)
      }
    })
```

