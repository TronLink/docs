# 多签转账

## 简介

此处可参考[普通转账](transfer.zh.md)

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

## 查询账户的 active permissions

选择持有资金的账户。如果当前签名人就是 owner，可使用其地址；共同签名人应填写被控制账户的地址。在交易所属网络查询该 owner 的权限，选择包含签名人且允许 TRX 转账的活动权限，使用该条目自身的 `id`。

```javascript
const tronweb = window.tron.tronWeb;
const owner = window.prompt("Transaction owner", tronweb.defaultAddress.base58);
const account = await tronweb.trx.getAccount(owner);
console.table(account.active_permission);
```

## 技术规范

### 签名并检查累计权重

接着使用上面的变量，填写收款人和选定的权限 ID。每次收集新签名后，在同一网络上将更新后的交易传给 `checkAndBroadcast`。节点会按交易 owner 当前的权限验证签名。[GetSignWeight](https://developers.tron.network/reference/getsignweight)

```javascript
async function checkAndBroadcast(signedTx) {
  const contract = signedTx.raw_data.contract[0];
  const check = await tronweb.trx.getSignWeight(signedTx);
  if (!check) throw new Error("Sign-weight response unavailable");
  const { permission, result, current_weight: weight } = check;
  if (result?.code === "PERMISSION_ERROR") throw new Error("Recheck owner and permission");
  if (!result || typeof result !== "object" || Array.isArray(result) ||
      !permission || !Number.isSafeInteger(permission.id) ||
      !Number.isSafeInteger(permission.threshold) ||
      permission.threshold <= 0 || !Number.isSafeInteger(weight) || weight < 0 ||
      !/^[0-9a-f]{64}$/i.test(permission.operations)) {
    throw new Error("Permission or weight unavailable");
  }
  // TransferContract is operation 1 in the active permission bitmap.
  const allowsTransfer = (parseInt(permission.operations.slice(0, 2), 16) & 2) !== 0;
  if (permission.type !== "Active" || permission.id !== contract.Permission_id || !allowsTransfer) {
    throw new Error("Recheck owner and permission");
  }
  if (result.code === "NOT_ENOUGH_PERMISSION" && weight < permission.threshold) {
    return { status: "collect", signedTx };
  }
  // The node may omit the default ENOUGH_PERMISSION code in a successful result.
  if ((result.code !== undefined && result.code !== "ENOUGH_PERMISSION") ||
      weight < permission.threshold) throw new Error("Weight check failed");
  const receipt = await tronweb.trx.sendRawTransaction(signedTx);
  if (!receipt.result) throw new Error([receipt.code, receipt.message].join(" "));
  return { status: "submitted", txID: signedTx.txID };
}

const recipient = window.prompt("Recipient address");
const permissionId = Number(window.prompt("Active permission ID"));
if (!account.active_permission?.some(p => p.id === permissionId)) {
  throw new Error("Select an active permission of the transaction owner");
}
const tx = await tronweb.transactionBuilder.sendTrx(recipient, 10, owner, { permissionId });
let signedTx;
try {
  signedTx = await tronweb.trx.multiSign(tx, undefined, permissionId);
} catch (error) {
  if (error === "Confirmation declined by user") console.info("Signing declined");
  else console.error(tx.txID, error);
}
if (signedTx) {
  try {
    console.log(await checkAndBroadcast(signedTx));
  } catch (error) {
    console.error(signedTx.txID, error);
  }
}
```

返回 `collect` 时，保留部分签名交易并交给下一位有权限的共同签名人。查询失败或缺少必要字段时暂停，恢复后重新执行完整检查。权限已撤销或不再允许本次操作时，停止收集签名，核对 owner、权限 ID 和当前权限后重建交易，重新收集全部签名。广播超时则先按交易 ID 查询结果。

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
