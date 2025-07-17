# User disconnects from the website

<span class="deprecated">DEPRECATED</span>

Message ID: `disconnectWeb` 

This message is generated when:

  1. User actively disconnect from the website. 
  
  ![image](../../../images/tronlink-wallet-extension_receive-messages-from-tronlink_messages-to-be-deprecated_user-disconnects-from-the-website_img_0.jpg)




Developers can get the disconnection message by listening to it:

```shell
    
    
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "disconnectWeb") {
        // handler logic
        console.log('got disconnectWeb event', e.data)
      }
    })
```