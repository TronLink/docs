# Successful connection message

Message ID: `connect`

**Overview**

Developers can monitor this message for connection changes. 

This message is generated when:

  1. The DApp requests a connection, and the user confirms the connection in the pop-up window

  2. Users connect to the website




**Specification**

**Example**

```shell
    
    
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "connect") {
        // handler logic
        console.log('got connect event', e.data)
      }
    })
```