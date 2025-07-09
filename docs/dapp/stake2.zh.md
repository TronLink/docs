---
title: Stake2.0
layout: docs
category: dapp
parent: dapp
---

DApp 生成质押2.0交易的时候，对于`DelegateResourceContract` 或者`UnDelegateResourceContract` 类型的交易，想要在签名时使用 tronlink 插件展示预估结果，需要向交易体添加 __options 字段。

__options 内部有两个值 `estimatedBandwidth，estimatedEnergy` ，分别对应代理和回收预估的能量和带宽。

通过非 tronlink 插件注入的 tronweb 生成质押2.0交易的时候，对于`DelegateResourceContract` 或者`UnDelegateResourceContract` 类型的交易想要在签名时使用 tronlink 插件展示资源对应的类型，需要向交易体添加 resource 字段。(添加 resource 仅针对非 tronlink 插件注入的 tronweb ，使用 tronlink 插件注入的 tronweb 不需要添加)。

resource 对应 `'BANDWIDTH'，'ENERGY'`。

![](https://docs-zh.tronlink.org/~gitbook/image?url=https%3A%2F%2F1166523713-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FCXoQmcUHNY97twQ2Y2PY%252Fuploads%252FQEIMfPng69F1p3qKJwfu%252Fimage1.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=938407c6&sv=2)

代码示例：

```shell 
    const transaction = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'BANDWIDTH', 'ownerAddress', false);
    transaction.raw_data.contract[0].parameter.value.resource = "BANDWIDTH"
    transaction.__options = {"estimatedBandwidth": 1}
```

estimatedEnergy estimatedBandwidth 的具体计算逻辑见![](https://docs-zh.tronlink.org/~gitbook/image?url=https%3A%2F%2F1166523713-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FCXoQmcUHNY97twQ2Y2PY%252Fuploads%252FXBi2ghdtBKVhNXcAhoNV%252Fimage2.png%3Falt%3Dmedia&width=300&dpr=4&quality=100&sign=56a9a3dd&sv=2)[Stake 2.0 Adaption FAQ](https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb) 最后一个章节：How to convert resource share to amount?


