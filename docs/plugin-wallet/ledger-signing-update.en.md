
# Upcoming implementation: compatibility adaptation for the v field in the signature returned after Ledger signing

> **Current status — planned, not yet released:** Today, Ledger signatures (transaction, message, and EIP-712) are returned exactly as the device produces them and end in `00` / `01`; the same value goes into the broadcast transaction. Regular (non-Ledger) accounts end in `1b` / `1c`. Until the change ships, DApps that verify signatures should accept both forms — treat a trailing `00` / `01` as `1b` / `1c` (v + 27) before recovering the signer or passing the signature to a contract that expects `v` = 27 / 28.

For Ledger signing (including all transaction signatures, message signatures, and EIP-712 signatures), a new technical measure is planned: the trailing `01` in the `signature` field will be replaced with `1c`, and `00` will be replaced with `1b`.

This change ensures that the final byte (two hexadecimal characters) of Ledger account signatures is consistent with those of regular account signatures.

### Transaction Signing

The following is a successfully signed Ledger transaction body:
```text
{
    "txID": "......",
    .....other property,
    "signature": [
        "......01"
    ]
}
```
It will become:
```text
{
    "txID": "......",
    .....other property,
    "signature": [
        "......1c"
    ]
}
```
When broadcasting, the DApp will use the modified transaction body.

### Message Signing

The DApp sends a message signing request:
```javascript
tron.tronWeb.trx.sign('.....unsign_string');
```
or
```javascript
tron.tronWeb.trx.signMessageV2('.....unsign_string');
```

Actual signature hash returned by Ledger:
```text
......50f400
```

Modified hash:
```text
......50f41b
```

### EIP-712 Signing

The DApp sends an EIP-712 signing request:
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

Actual signature hash returned by Ledger:
```text
.....7ee700
```

Modified hash:
```text
......7ee71b
```
