# General Transfer

**Overview**

DApp requires users to initiate a TRX transfer.

**Prerequisite**

The DApp developer completes the request to connect to the website, and the user approves to the connection. The DApp sends a request asking the user to connect the wallet to the website, and the user approves to the connection.

It takes 3 steps to initiate a transfer on the TRON network:

  1. Create a transfer transaction

  2. Sign the transaction

  3. Broadcast the signed transaction




In this process, Step 2 requires TronLink while both Step 1 and 3 happen on tronWeb.

**Specification**

**Example**

```shell  
    
    if (window.tronLink.ready) {
      const tronweb = tronLink.tronWeb;
      const fromAddress = tronweb.defaultAddress.base58;
      const toAddress = "TAHQdDiZajMMP26STUnfsiRMNyXdxAJakZ";
      const tx = await tronweb.transactionBuilder.sendTrx(toAddress, 10, fromAddress); // Step1
      try {
        const signedTx = await tronweb.trx.sign(tx); // Step2
        await tronweb.trx.sendRawTransaction(signedTx); // Step3
      } catch (e) {
        // error handling
      }
    }
```

When “await tronweb.trx.sign(tx);” is executed, a pop-up window will show in the TronLink wallet asking the user to confirm, as shown below: 

![image](../images/dapp_general-transfer_img_0.jpg)

If the user chooses on “Reject” in the pop-up window, an exception will be thrown, which the developer can catch for further processing.

If the user chooses “Sign” in the pop-up window, the DApp receives and broadcasts the signed transaction.
