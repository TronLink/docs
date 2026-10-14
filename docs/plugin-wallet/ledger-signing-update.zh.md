
# 即将实施：对ledger签名后signature的v字段进行兼容改造

> **当前状态——计划中，尚未上线：** 目前 Ledger 签名（交易、消息、EIP-712）均按设备原样返回，末尾为 `00` / `01`，广播的交易中也是同一个值。普通（非 Ledger）账户签名末尾为 `1b` / `1c`。在该改动上线前，验签的 DApp 应同时兼容两种形式：在恢复签名地址、或把签名传给要求 `v` = 27 / 28 的合约之前，把末尾的 `00` / `01` 按 `1b` / `1c`（v + 27）处理。

针对ledger签名（包括所有交易签名、消息签名、712签名），计划更新一项新的技术措施，会将签名后的 `signature` 字段中末尾的`01`替换成`1c`，`00`替换成`1b`。

这个改动，是为了保证ledger账户签名和普通账户签名的末尾两位十六进制字符（即一个字节）一致。

### 普通交易签名

以下是签名成功的 ledger 交易体：
```text
{
    "txID": "......",
    .....other property,
    "signature": [
        "......01"
    ]
}
```
会变成:
```text
{
    "txID": "......",
    .....other property,
    "signature": [
        "......1c"
    ]
}
```
如果需要广播，DApp会使用修改后的交易体进行广播

### 消息签名

DApp发送消息签名
```javascript
tron.tronWeb.trx.sign('.....unsign_string');
```
或者
```javascript
tron.tronWeb.trx.signMessageV2('.....unsign_string');
```

ledger返回的实际签名hash：
```text
......50f400
```

经过修改后的hash：
```text
......50f41b
```

### 712签名

DApp发送712签名
```javascript
const types = {
  Person: [
    {
      name: 'name',
      type: 'string',
    },
    {
      name: 'wallet',
      type: 'address',
    },
  ],
  Mail: [
    {
      name: 'from',
      type: 'Person',
    },
    {
      name: 'to',
      type: 'Person',
    },
    {
      name: 'contents',
      type: 'string',
    },
  ],
};

const primaryType = 'Mail';

const domain = {
  name: 'Ether Mail',
  version: '1',
  chainId: '0x2b6653dc',
  verifyingContract: '0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC',
};

const message = {
  from: {
    name: 'Cow',
    wallet: '0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826',
  },
  to: {
    name: 'Bob',
    wallet: '0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB',
  },
  contents: 'Hello, Bob!',
};

await tron.tronWeb.trx._signTypedData(domain, types, message);
```

ledger返回的实际签名hash：
```text
.....7ee700
```

经过修改后的hash：
```text
......7ee71b
```