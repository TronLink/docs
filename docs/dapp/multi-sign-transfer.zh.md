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
const activePermissionId = 2; // 通过 tronWeb.trx.getAccount(...).active_permission 查出
const tx = await tronweb.transactionBuilder.sendTrx(
    toAddress, 10,
    { permissionId: activePermissionId }
); // 步骤1
try {
  const signedTx = await tronweb.trx.multiSign(tx, undefined, activePermissionId); // 步骤2
  await tronweb.trx.sendRawTransaction(signedTx); // 步骤3
} catch (e) {}
```

如果用户在弹窗中选择【拒绝】，则会抛出异常，开发者可捕获此异常进行业务处理。

如果用户在弹窗中选择【签名】，DApp 可以拿到签名后的交易，继续进行广播。

注意:此次调用只收集**一个**签名——完整的多签交易需要凑齐 `threshold`,通常对应**多次** `multiSign` 调用(每个 co-signer 一次)。在凑齐前应在链下(或通过 MCP 的 `tl_multisig_*` 工具)跟踪部分签名的交易,凑齐后再广播。

## 错误码

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| `4001` | 用户在签名弹窗里点【拒绝】 | `tronWeb.trx.multiSign(...)` | 否——用户拒绝 |
| (抛出) | `permission_id not active` / `permission_id not exist` | `transactionBuilder.sendTrx({permissionId})`——权限不存在或被撤销 | 否——重新 `getAccount(...).active_permission` 查 |
| (抛出) | 签名权重广播后仍低于 `threshold` | `sendRawTransaction` | 否——再凑签名(每个 co-signer 一次 `multiSign`) |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | 广播成功但链上执行失败 | `getTransactionInfo(txid)` | **否——交易已 final,永远不要自动重试** |

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。
