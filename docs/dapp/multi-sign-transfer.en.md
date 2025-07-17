# Multi-Signature Transfer

**Overview**

For this section, you may refer to [General Transfer](transfer.en.md)

**Specification**

**Example**

```shell 
    if (window.tronLink.ready) {
      const tronweb = tronLink.tronWeb;
      const toAddress = "TRKb2nAnCBfwxnLxgoKJro6VbyA6QmsuXq";
      const activePermissionId = 2;
      const tx = await tronweb.transactionBuilder.sendTrx(
        toAddress, 10,
        { permissionId: activePermissionId}
      ); // step 1
      try {
        const signedTx = await tronweb.trx.multiSign(tx, undefined, activePermissionId); // step 2
        await tronweb.trx.sendRawTransaction(signedTx); // step 3
      } catch (e) {}
    }
```

If the user chooses “Reject” in the pop-up window, an exception will be thrown, which the developer can catch for further processing. If the user chooses “Sign” in the pop-up window, the DApp receives and broadcasts the signed transaction.


