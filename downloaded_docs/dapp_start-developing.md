  1. [DApp](/dapp)



# Start Developing

This document will guide you to connect your DApp with the TronLink application in the easiest way. After the DApp is loaded, TronLink will inject the “window.tronLink” object into it.

  1. A user who has connected to this DApp can directly get tronLink.tronWeb.

  2. If the user has not been connected to this DApp before, a request can be invoked to establish the connection before getting tronLink.tronWeb.




Copy
    
    
    async function getTronWeb() {
      let tronWeb;
      if (window.tronLink.ready) {
        tronWeb = tronLink.tronWeb;
      } else {
        const res = await tronLink.request({ method: 'tron_requestAccounts' });
        if (res.code === 200) {
          tronWeb = tronLink.tronWeb;
        }
      }
      return tronWeb;
    }

After getting the tronWeb instance, you can perform on-chain interactive actions such as signing transfers, multi-signature transactions, and messages. For use cases of the tronWeb instance, please refer to the following document: <https://tronweb.network/docu/docs/intro/>[](https://tronweb.network/docu/docs/intro/)

Reference: <https://developers.tron.network/docs/introduction>[](https://developers.tron.network/docs/introduction)

[PreviousUser requests to connect to the website](/tronlink-wallet-extension/receive-messages-from-tronlink/messages-to-be-deprecated/user-requests-to-connect-to-the-website)[NextMulti-Signature Transfer](/dapp/multi-signature-transfer)

Last updated 2 months ago
