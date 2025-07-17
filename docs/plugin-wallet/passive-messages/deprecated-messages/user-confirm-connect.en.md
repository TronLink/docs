# User accepts connection

<span class="deprecated">DEPRECATED</span>

Message ID: `acceptWeb` 

This message is generated when:

  1. The user accepts connection. 
  
  ![image](../../../images/tronlink-wallet-extension_receive-messages-from-tronlink_messages-to-be-deprecated_user-accepts-connection_img_0.jpg)




Developers can get the connection acceptance message by listening to it:

```shell 
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "acceptWeb") {
        // handler logic
        console.log('got acceptWeb event', e.data)
      }
    })
```