# 账户改变消息

消息标识： `accountsChanged`

**简介**

以下情况会产生此消息

  1. 用户登陆

  2. 用户切换账号

  3. 用户锁定账号

  4. 钱包超时自动锁定

**技术规范**

**代码示例**

```shell

    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action === "accountsChanged") {
          // handler logic
          console.log('got accountsChanged event', e.data)
      }
    })
```
**返回值**

```shell

    interface MessageEventAccountsChangedData {
      isTronLink: boolean;
      message: {
        action: string;
        data: {
          address: string | boolean;
        }
      }
    }
```
**返回值示例**

  1. 用户登陆时，消息体内容为：

```shell

    {
      "data": {
        "address": "TZ5XixnRyraxJJy996Q1sip85PHWuj4793" // 上次选择的账号地址
      }
    }
```
  1. 用户切换账号时，消息体内容为：

```shell

    {
      "data": {
        "address": "TRKb2nAnCBfwxnLxgoKJro6VbyA6QmsuXq" // 新选择的账号地址
      }
    }
```
  1. 用户锁定和钱包超时自动锁定时，消息体内容为：

```shell

    {
      "data": {
        "address": false
      }
    }
```

