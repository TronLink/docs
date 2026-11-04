# 多签转账

## 简介

此处可参考[普通转账](transfer.zh.md)

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

## 查询账户的 active permissions

`multiSign` 需要传入一个**有效的** `permissionId`。账户的 active permissions 通过 `tronWeb.trx.getAccount(address)` 返回的 `active_permission[]` 数组取得,每个 entry 暴露 `id`、`permission_name`、`threshold` 以及 `keys[]`(地址 + 权重)。owner 权限 id 固定为 `0`,在 `owner_permission` 字段下单独返回。

```javascript
const tronweb = window.tron.tronWeb;
const account = await tronweb.trx.getAccount(tronweb.defaultAddress.base58);
// account.active_permission 是数组——挑选 keys[] 里包含你要签名地址、
// 且 weight + threshold 足够覆盖本次交易的 id。
const activePermissions = account.active_permission ?? [];
console.log(activePermissions.map(p => ({ id: p.id, name: p.permission_name, threshold: p.threshold })));
```

把查出来的 `id` 作为下面的 `permissionId` 传入。

## 技术规范

### 代码示例

```javascript
const tronweb = window.tron.tronWeb;
const toAddress = "TRKb2nAnCBfwxnLxgoKJro6VbyA6QmsuXq";
// fromAddress = 资金所在、由该 active 权限控制的账户（交易 owner）。
// 它不一定是当前连接的签名账户：若当前账户只是该权限 keys[] 里的共同签名人，
// 请把 fromAddress 改成被控制的账户地址。
const fromAddress = tronweb.defaultAddress.base58;
const activePermissionId = 2; // 通过 tronWeb.trx.getAccount(fromAddress).active_permission 查出
const tx = await tronweb.transactionBuilder.sendTrx(
    toAddress, 10, fromAddress,
    { permissionId: activePermissionId }
); // 步骤1
try {
  const signedTx = await tronweb.trx.multiSign(tx, undefined, activePermissionId); // 步骤2
  const res = await tronweb.trx.sendRawTransaction(signedTx); // 步骤3
  if (!res.result) {
    // 节点拒绝以返回值给出，不会抛异常——见下方错误码。
    console.error(res.code, tronweb.toUtf8(res.message));
  }
} catch (e) {}
```

如果用户在弹窗中选择【拒绝】，则会抛出异常，开发者可捕获此异常进行业务处理。

如果用户在弹窗中选择【签名】，DApp 可以拿到签名后的交易，继续进行广播。

注意:此次调用只收集**一个**签名——完整的多签交易需要凑齐 `threshold`,通常对应**多次** `multiSign` 调用(每个 co-signer 一次)。在凑齐前应在链下(或通过 MCP 的 `tl_multisig_*` 工具)跟踪部分签名的交易,凑齐后再广播。

## 错误码

**错误结构：** 在 TronLink 注入的 `tronWeb` 上（插件 4.0.0 起），用户拒绝 `trx.sign`、`trx.multiSign` 或 `trx.signMessageV2` 时，Promise 以**纯字符串** `'Confirmation declined by user'` reject——不是 `Error` 对象，也没有数字 `code`。`{ code: 4001, message: 'User rejected the request.' }` 对象只由 `window.tron.request(...)` 方法（如 `eth_requestAccounts`）返回。其他失败（钱包未解锁、载荷非法、观察钱包等）返回其他值——参见[处理拒签](../reference/error-code-map.md#handling-rejections)。不要自动重试签名。

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'`（字符串） | 用户在签名弹窗里点【拒绝】 | `tronWeb.trx.multiSign(...)` | 否——用户拒绝 |
| `code: 'SIGERROR'`，`message` 解码为 `Validate signature error: permission isn't exit` | `fromAddress` 上不存在该 `permissionId`（填错或已撤销）。`sendTrx` **不会**校验权限，由节点在广播时拒绝 | `sendRawTransaction(...)` 的返回值（不抛异常） | 否——重新查 `getAccount(fromAddress).active_permission` 后重建交易 |
| `code: 'SIGERROR'`，其他 `Validate signature error: …` 信息 | 签名不满足该权限——如总权重低于 `threshold`，或签名人不在其 `keys[]` 中 | `sendRawTransaction(...)` 的返回值（不抛异常） | 否——补齐缺少的签名（每个 co-signer 一次 `multiSign`） |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | 广播成功但链上执行失败 | `getTransactionInfo(txid)` | **否——交易已 final,永远不要自动重试** |

`sendRawTransaction` 返回结果里的 `message` 是 hex 编码，用 `tronweb.toUtf8(res.message)` 解码。若要在广播前检查，可调用 `tronweb.trx.getSignWeight(signedTx)`：权限不存在时 `result.code` 为 `PERMISSION_ERROR`，签名权重仍低于 `threshold` 时为 `NOT_ENOUGH_PERMISSION`。

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。
