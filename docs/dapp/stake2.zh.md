# Stake2.0

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

DApp 请求 TronLink 对 `DelegateResourceContract` 或 `UnDelegateResourceContract` 交易签名时，签名弹窗会展示资源类型和预估的资源数量：

- **资源类型**——读取自 `raw_data.contract[0].parameter.value.resource`。`tronWeb.transactionBuilder.delegateResource` / `undelegateResource` 对能量交易已自动写入 `"ENERGY"`；带宽交易会省略该字段（它是 protobuf 默认值），TronLink（4.1.4 及以上）把缺失值按 `"BANDWIDTH"` 处理。DApp 无需自行添加。
- **预估数量**——读取自 DApp 在交易对象顶层添加的 `__options`：`estimatedBandwidth` 表示预估带宽，`estimatedEnergy` 表示预估能量。弹窗只展示与资源类型对应的那一项。缺少 `__options` 时弹窗显示 `0`，签名不受影响。

`__options` 不在 `raw_data` 内，添加它不会改变 `txID` 或 `raw_data_hex`。而 `parameter.value.resource` 属于被签名的协议数据，构建后不要再修改：修改后的值与 `raw_data_hex` / `txID` 不一致。`trx.sign` 会拒绝这样的交易（`'Invalid transaction provided'`；插件 4.4.3 起），`trx.multiSign` 则会按修改后的数据重新计算 `txID`，签出的交易与你构建的不同。需要更换资源类型时请重新构建交易。

![委托交易对象示意，标出 raw_data.contract[0].parameter.value.resource 与顶层的 __options.estimatedBandwidth](../images/dapp_stake2.0_img_0.jpg)
<style>
img {
  max-width: 100%!important;
}
</style>

代码示例：

```javascript
// 能量——tronWeb 会写入 parameter.value.resource = "ENERGY"
const energyTx = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'ENERGY', 'ownerAddress', false);
energyTx.__options = { estimatedEnergy: 1 }; // 占位值——按下方说明计算

// 带宽——省略 resource，按 BANDWIDTH 展示
const bandwidthTx = await tronWeb.transactionBuilder.delegateResource(10e6, 'receiverAddress', 'BANDWIDTH', 'ownerAddress', false);
bandwidthTx.__options = { estimatedBandwidth: 1 }; // 占位值——按下方说明计算

const signed = await tronWeb.trx.sign(energyTx);
```

`undelegateResource` 交易使用相同的 `__options` 字段。

estimatedEnergy estimatedBandwidth 的具体计算逻辑见![Stake 2.0 资源份额到具体数额换算公式示意图](../images/dapp_skake2.0_img_1.png)[<a class="tooltip" href="https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb" data-tooltip="https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb">Stake 2.0 Adaptation FAQ</a>](https://www.google.com/url?q=https://coredevs.medium.com/stake-2-0-adaption-faq-66bafdf53606&sa=D&source=editors&ust=1684151119972747&usg=AOvVaw0msvWulJZhW6xn5QU461cb) 最后一个章节：How to convert resource share to amount?

## 错误码

**错误结构：** 在 TronLink 注入的 `tronWeb` 上（插件 4.0.0 起），用户拒绝 `trx.sign`、`trx.multiSign` 或 `trx.signMessageV2` 时，Promise 以**纯字符串** `'Confirmation declined by user'` reject——不是 `Error` 对象，也没有数字 `code`。`{ code: 4001, message: 'User rejected the request.' }` 对象只由 `window.tron.request(...)` 方法（如 `eth_requestAccounts`）返回。其他失败（钱包未解锁、载荷非法、观察钱包等）返回其他值——参见[处理拒签](../reference/error-code-map.md#handling-rejections)。不要自动重试签名。

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'`（字符串） | 用户在签名弹窗里点【拒绝】 | 委托/取消委托交易的 `tronWeb.trx.sign(tx)` | 否——用户拒绝 |
| (抛出) | 质押的 TRX 不足 / 无可取消的代理 | `delegateResource` / `undelegateResource` 构造器 | 否——先修链上状态 |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | 广播成功但链上执行失败 | `sendRawTransaction` 返回或 `getTransactionInfo` | **否——交易已 final,永远不要自动重试** |

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。
