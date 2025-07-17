# User requests to connect to the website

<span class="deprecated">DEPRECATED</span>

Message ID: `connectWeb` 

This message is generated when:

  1. The user requests to connect to the website. 
  
  ![image](../../../images/tronlink-wallet-extension_receive-messages-from-tronlink_messages-to-be-deprecated_user-requests-to-connect-to-the-website_img_0.jpg)




Developers can get the connection request message by listening to it:

```shell
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "connectWeb") {
        // handler logic
        console.log('got connectWeb event', e.data)
      }
    })
```
