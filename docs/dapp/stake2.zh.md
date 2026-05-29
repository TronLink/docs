# Stake2.0

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

DApp 生成质押2.0交易的时候，对于`DelegateResourceContract` 或者`UnDelegateResourceContract` 类型的交易，想要在签名时使用 tronlink 插件展示预估结果，需要向交易体添加 __options 字段。

__options 内部有两个值 `estimatedBandwidth，estimatedEnergy` ，分别对应代理和回收预估的能量和带宽。

通过非 tronlink 插件注入的 tronweb 生成质押2.0交易的时候，对于`DelegateResourceContract` 或者`UnDelegateResourceContract` 类型的交易想要在签名时使用 tronlink 插件展示资源对应的类型，需要向交易体添加 resource 字段。(添加 resource 仅针对非 tronlink 插件注入的 tronweb ，使用 tronlink 插件注入的 tronweb 不需要添加)。

resource 对应 `'BANDWIDTH'，'ENERGY'`。

![Stake 2.0 委托/取消委托签名界面示意，标注了 __resource（"BANDWIDTH" 或 "ENERGY"）与 __options.estimatedBandwidth / estimatedEnergy 字段——TronLink 据此在签名页渲染资源类型](../images/dapp_stake2.0_img_0.jpg)
<style>
img {
  max-width: 100%!important;
}
</style>
代码示例：

```javascript
    const transaction = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'BANDWIDTH', 'ownerAddress', false);
    transaction.raw_data.contract[0].parameter.value.resource = "BANDWIDTH"
    transaction.__options = {"estimatedBandwidth": 1}
```

estimatedEnergy estimatedBandwidth 的具体计算逻辑见![Stake 2.0 资源份额到具体数额换算公式示意图](../images/dapp_skake2.0_img_1.png)[<a class="tooltip" href="https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb" data-tooltip="https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb">Stake 2.0 Adaptation FAQ</a>](https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb) 最后一个章节：How to convert resource share to amount?

## 错误码

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| `4001` | 用户在签名弹窗里点【拒绝】 | 委托/取消委托交易的 `tronWeb.trx.sign(tx)` | 否——用户拒绝 |
| (抛出) | 缺 `__options` 或 `__resource`——签名页无法渲染预估 | `tronWeb.trx.sign(tx)` | 否——按上文规则补全两个字段 |
| (抛出) | 质押的 TRX 不足 / 无可取消的代理 | `delegateResource` / `undelegateResource` 构造器 | 否——先修链上状态 |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | 广播成功但链上执行失败 | `sendRawTransaction` 返回或 `getTransactionInfo` | **否——交易已 final,永远不要自动重试** |

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。
