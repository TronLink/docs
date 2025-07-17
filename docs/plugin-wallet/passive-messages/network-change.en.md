# Network Change Message

Message ID: `setNode`

**Overview**

Developers can monitor this message to know network changes 

This message is generated when:

  1. When the user changes the network




**Specification**

**Example**

```shell
    
    
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action == "setNode") {
        // handler logic
        console.log('got setNode event', e.data)
      }
    })
```
**Returns**

```shell
    
    
    {
      "node": {
        // Information about the current network
      },
      "connectNode": {
        // Node information of DApp chain
      }
    }
```