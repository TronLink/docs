# 多签转账

## 简介

此处可参考[普通转账](transfer.zh.md)

> **前提条件：** 已通过 `eth_requestAccounts` 完成 DApp 连接授权（参见[开始开发](getting-started.md)）。

## 查询账户的 active permissions

选择持有资金的账户。如果当前签名人就是 owner，可使用其地址；共同签名人应填写被控制账户的地址。在交易所属网络查询该 owner 的权限，选择包含签名人且允许 TRX 转账的活动权限，使用该条目自身的 `id`。

```javascript
const tronweb = window.tron.tronWeb;
const owner = "REPLACE_WITH_OWNER_ADDRESS";
const account = await tronweb.trx.getAccount(owner);
console.table(account.active_permission);
```

## 技术规范

### 签名并检查累计权重

在交易所用网络上，将已授权的 TronWeb 实例传给以下函数。广播前，由节点根据交易 owner 当前的权限检查签名。[GetSignWeight](https://developers.tron.network/reference/getsignweight)

```javascript
function validateSignWeight(check, permissionId) {
  const { permission, result, current_weight: weight } = check ?? {};
  if (result?.code === "PERMISSION_ERROR") throw new Error("请核对交易 owner 和权限");
  if (!result || typeof result !== "object" || Array.isArray(result) ||
      !permission || !Number.isSafeInteger(permission.threshold) ||
      permission.threshold <= 0 || !Number.isSafeInteger(weight) || weight < 0 ||
      !/^[0-9a-f]{64}$/i.test(permission.operations)) {
    throw new Error("无法确认权限或累计权重");
  }
  // 活动权限位图中的第 1 位对应 TransferContract。
  const allowsTransfer = (parseInt(permission.operations.slice(0, 2), 16) & 2) !== 0;
  if (permission.type !== "Active" || permission.id !== permissionId || !allowsTransfer) {
    throw new Error("请核对交易 owner 和权限");
  }
  return { code: result.code, weight, threshold: permission.threshold };
}

async function checkAndBroadcast(tronweb, signedTx, permissionId) {
  const check = await tronweb.trx.getSignWeight(signedTx);
  const { code, weight, threshold } = validateSignWeight(check, permissionId);
  if (code === "NOT_ENOUGH_PERMISSION" && weight < threshold) {
    return { status: "collect", signedTx };
  }

  // 节点可能省略默认的 ENOUGH_PERMISSION 状态码。
  if ((code !== undefined && code !== "ENOUGH_PERMISSION") || weight < threshold) {
    throw new Error("签名权重检查失败");
  }

  const receipt = await tronweb.trx.sendRawTransaction(signedTx);
  if (!receipt.result) {
    const message = receipt.message ? tronweb.toUtf8(receipt.message) : "";
    throw new Error([receipt.code, message].filter(Boolean).join(" ") || "广播被拒绝");
  }
  return { status: "submitted", txID: signedTx.txID };
}

async function signAndCheck(tronweb, tx) {
  const permissionId = tx.raw_data.contract[0].Permission_id;
  if (!Number.isSafeInteger(permissionId) || permissionId < 2) {
    throw new Error("请填写有效的活动权限 ID");
  }

  let signedTx;
  try {
    signedTx = await tronweb.trx.multiSign(tx, undefined, permissionId);
  } catch (error) {
    if (error === "Confirmation declined by user") return { status: "declined" };
    throw error;
  }

  return checkAndBroadcast(tronweb, signedTx, permissionId);
}
```

### 第一位签名人

替换收款地址，并填写上面从交易 owner 的活动权限中选出的 ID。

```javascript
const recipient = "REPLACE_WITH_RECIPIENT_ADDRESS";
const permissionId = 2; // 替换为所选活动权限的 ID。
if (!account.active_permission?.some(p => p.id === permissionId)) {
  throw new Error("请选择交易 owner 的活动权限");
}

// 构建一笔 10 SUN 的转账（1 TRX = 1_000_000 SUN）。
const tx = await tronweb.transactionBuilder.sendTrx(recipient, 10, owner, { permissionId });
const outcome = await signAndCheck(tronweb, tx);
```

### 后续共同签名人

结果为 `collect` 时，通过 DApp 的交接流程将其中的 `signedTx` 传给下一位有权限的共同签名人。每位共同签名人在同一网络连接钱包。签名前，先确认交易数据与其 `txID` 一致，再解析 owner、收款地址、金额和过期时间并展示给共同签名人，确认无误后再继续。调用 `coSignTransfer` 时传入收到的交易对象，以及一个在共同签名人确认后返回 `true` 的 `confirmTransfer` 回调。`signAndCheck` 会在该对象上调用 `multiSign`，保留已有签名和交易 ID。

```javascript
function describeTransfer(tronweb, tx) {
  // 签名针对 txID，展示前先确认 raw_data 的哈希与其一致。
  const txCheck = tronweb.utils?.transaction?.txCheck;
  if (!txCheck || !txCheck(tx)) throw new Error("交易数据与 txID 不一致");
  const contract = tx.raw_data.contract[0];
  if (contract.type !== "TransferContract") throw new Error("不是 TRX 转账");
  const { owner_address, to_address, amount } = contract.parameter.value;
  return {
    owner: tronweb.address.fromHex(owner_address),
    recipient: tronweb.address.fromHex(to_address),
    amount: `${tronweb.fromSun(amount)} TRX`,
    permissionId: contract.Permission_id,
    expires: new Date(tx.raw_data.expiration).toISOString(),
  };
}

async function coSignTransfer(partiallySignedTx, confirmTransfer) {
  const tronweb = window.tron.tronWeb;
  const details = describeTransfer(tronweb, partiallySignedTx);
  // 在 DApp 界面中展示这些信息，共同签名人确认后再签名。
  if (!(await confirmTransfer(details))) return { status: "declined" };
  return signAndCheck(tronweb, partiallySignedTx);
}
```

返回 `collect` 时继续交接，返回 `declined` 时停止本次签名。权重查询失败或缺少必要字段时暂停，恢复后重新执行完整权重检查。权限被撤销或已不允许本次操作时，核对交易 owner 和权限 ID，重建交易并重新收集全部签名。广播超时则先按交易 ID 查询结果。

## 错误码

**错误结构：** 在 TronLink 注入的 `tronWeb` 上（插件 4.0.0 起），用户拒绝 `trx.sign`、`trx.multiSign` 或 `trx.signMessageV2` 时，Promise 以**纯字符串** `'Confirmation declined by user'` reject——不是 `Error` 对象，也没有数字 `code`。`{ code: 4001, message: 'User rejected the request.' }` 对象只由 `window.tron.request(...)` 方法（如 `eth_requestAccounts`）返回。其他失败（钱包未解锁、载荷非法、观察钱包等）返回其他值——参见[处理拒签](../reference/error-code-map.md#handling-rejections)。不要自动重试签名。

| 码 | 含义 | 来源 | 可重试? |
| :---: | --- | --- | :---: |
| `'Confirmation declined by user'`（字符串） | 用户在签名弹窗里点【拒绝】 | `tronWeb.trx.multiSign(...)` | 否——用户拒绝 |
| `code: 'SIGERROR'`，`message` 解码为 `Validate signature error: permission isn't exit` | `owner` 上不存在该 `permissionId`（填错或已撤销）。`sendTrx` **不会**校验权限，由节点在广播时拒绝 | `sendRawTransaction(...)` 的返回值（不抛异常） | 否——重新查 `getAccount(owner).active_permission` 后重建交易 |
| `code: 'SIGERROR'`，其他 `Validate signature error: …` 信息 | 签名不满足该权限——如总权重低于 `threshold`，或签名人不在其 `keys[]` 中 | `sendRawTransaction(...)` 的返回值（不抛异常） | 否——补齐缺少的签名（每个 co-signer 一次 `multiSign`） |
| `REVERT` / `OUT_OF_ENERGY` / `FAILED` | 广播成功但链上执行失败 | `getTransactionInfo(txid)` | **否——交易已 final,永远不要自动重试** |

`sendRawTransaction` 返回结果里的 `message` 是 hex 编码，用 `tronweb.toUtf8(res.message)` 解码。若要在广播前检查，可调用 `tronweb.trx.getSignWeight(signedTx)`：权限不存在时 `result.code` 为 `PERMISSION_ERROR`，签名权重仍低于 `threshold` 时为 `NOT_ENOUGH_PERMISSION`。

跨 surface 的码对照见[错误码对照表](../reference/error-code-map.md)。
