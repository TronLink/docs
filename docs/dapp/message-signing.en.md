# Message Signature

**Overview**

DApp requires users to sign a hex message. The signed message will be forwarded to the back-end to verify whether a user's login is legitimate.

**Prerequisite**

The DApp sends a request asking the user to connect the wallet to the website, and the user approves to the connection.

**Specification**

**Example**
```shell
    
    if (window.tronLink.ready) {
      const tronweb = tronLink.tronWeb;
      try {
        const message = "0x1e"; // any hex string
        const signedString = await tronweb.trx.sign(message);
      } catch (e) {}
    }
```
**Parameters**

“tronLink.tronWeb.trx.sign” accepts a hexadecimal string as the parameter. The string represents the content to be signed.

**Returns**

If the user chooses to sign in the pop-up window, the DApp will get the signed hexadecimal string. For example:

```shell 
    0xaa302ca153b10dff25b5f00a7e2f603c5916b8f6d78cdaf2122e24cab56ad39a79f60ff3916dde9761baaadea439b567475dde183ee3f8530b4cc76082b29c341c
```

If an error occurs, the following information will be returned:

```shell 
    
    Uncaught (in promise) Invalid transaction provided
```

**Interaction**

When “tronweb.trx.sign(message);” is executed, a pop-up window will show in the TronLink wallet asking the user to confirm, as shown below. The message content will be in hex: 

![image](../images/dapp_message-signature_img_0.jpg)

If the user chooses “Reject” in the pop-up window, an exception will be thrown, which the developer can catch for further processing.

