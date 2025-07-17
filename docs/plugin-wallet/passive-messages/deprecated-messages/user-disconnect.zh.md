# 用户断连网站消息

<span class="deprecated">DEPRECATED</span>

消息标识： `disconnectWeb`

以下情况会产生此消息

  1. 用户主动断接网站

![image](../../../images/zh_cha-jian-qian-bao_bei-dong-jie-shou-tronlink-cha-jian-de-xiao-xi_ji-jiang-fei-qi-de-xiao-xi_yong-hu-duan-lian-wang-zhan-xiao-xi_img_0.jpg)

开发者可以监听此消息来获取用户主动断连消息

```shell

    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "disconnectWeb") {
          // handler logic
          console.log('got disconnectWeb event', e.data)
      }
    })
```

