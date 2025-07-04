---
title: 转账
layout: docs
category: mobile
parent: mobile/deeplink
---

使用DeepLink方式唤起TronLink，并发送转账数据，在钱包中转账并广播

Copy

    // Tronlink-v4.11.0
    // 链接
    Transfer

Copy

    {
      "url": "https://justlend.org/#/home",
      "callbackUrl": "http://3.12.131.175:7777/api/tron/v1/callback",
      "dappIcon": "https://test/icon.png",
      "dappName": "Test demo",
      "protocol": "TronLink",
      "version": "1.0",
      "chainId": "0x2b6653dc",
      "memo": "Reward",
      "from": "TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig",
      "to": "TXd9duqtcyyj4pBCKvXKNqmazxxDw5SdBa",
      "loginAddress": "TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig",
      "tokenId": "0",
      "contract": "",
      "amount": "20",
      "action": "transfer",
      "actionId": "408170fc-7919-4459-be5e-05a9d4b4065e"
    }

Copy

    {
      "actionId": "099482f0-ee12-4703-bb7b-2e9d8c7c61a1",
      "code": 0,
      "id": 1142367107,
      "message": "success",
      "transactionHash": "e8ffe9b92c771e66999732b810bf2493be389464191040d8666a26dc449fa5f0"
    }

[Previous登陆授权](https://docs-zh.tronlink.org/yi-dong-duan/deeplink/deng-lu-shou-quan)[Next交易签名](https://docs-zh.tronlink.org/yi-dong-duan/deeplink/jiao-yi-qian-ming)

Last updated 2 years ago