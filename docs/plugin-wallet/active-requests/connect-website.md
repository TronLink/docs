---
title: 连接网站
layout: docs
category: plugin
parent: plugin-wallet/active-requests
---

#### **DEPRECATED**

本小节的方法已废弃，预计将在几个版本后移除。TRON 社区正在讨论新的规范，可以到 [TRON-TIP](https://github.com/tronprotocol/tips/issues/463) 参与讨论。

#### 连接网站

**简介**

TronLink 提供外部发起 TRX 转账，合约签名，授权等功能，基于安全的考虑， 需要用户在关键操作前先对发起请求的 DApp 进行【连接网站】授权，在授权成功后才允许操作。 所以 DApp 要先进行【连接网站】操作，等待用户允许后，方能发起需要授权的请求。

**技术规范**

**代码示例**

Copy

    const res = await tronWeb.request(
      {
        method: 'tron_requestAccounts',
        params: {
          websiteIcon: '',
          websiteName: '',
        },
      }
    );

**参数**

Copy

    interface RequestAccountsParams {
      websiteIcon?: string;
      websiteName?: string;
    }

  * method: tron_requestAccounts 固定的字符串

  * params: RequestAccountParams类型，具体参数如下：

    * websiteIcon: DApp 网站的图标的网址, 具体会展示在用户已连接网站列表中

    * websiteName: DApp 网站名称

**返回值**

类型说明

Copy

    interface ReqestAccountsResponse {
      code: 200 | 4000 | 4001,
      message: string
    }

返回码

描述

返回消息

无

钱包处于锁定状态

空字符串

200

网站此前已被用户允许连接

The site is already in the whitelist

200

用户同意连接

User allowed the request.

4000

当前请求前已经有同一个 DApp 发起了连接网站请求，并且弹窗仍未关闭

Authorization requests are being processed, please do not resubmit

4001

用户拒绝连接

User rejected the request

**交互流程**

触发`tron_requestAccounts`之后，会打开连接确认的弹窗：

![](https://docs-zh.tronlink.org/~gitbook/image?url=https%3A%2F%2F1166523713-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FCXoQmcUHNY97twQ2Y2PY%252Fuploads%252FjhP6f0i4r8nlcP3f8YJP%252FrequestAccounts.png%3Falt%3Dmedia%26token%3Dc03e5e28-c640-43fa-ab15-0e343181d3c0&width=300&dpr=4&quality=100&sign=2ae53deb&sv=2)

[Previous主动请求TronLink插件功能](https://docs-zh.tronlink.org/cha-jian-qian-bao/zhu-dong-qing-qiu-tronlink-cha-jian-gong-neng)[Next添加Token](https://docs-zh.tronlink.org/cha-jian-qian-bao/zhu-dong-qing-qiu-tronlink-cha-jian-gong-neng/tian-jia-token)

Last updated 2 years ago