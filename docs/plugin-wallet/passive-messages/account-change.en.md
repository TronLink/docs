# Account Change Message

Message ID: `accountsChanged`

**Overview**

This message is generated when:

  1. Users log in

  2. Users switch accounts

  3. Users lock accounts

  4. The wallet is automatically locked after timeout




**Specification**

**Example**

```shell
    
    
    window.addEventListener('message', function (e) {
      if (e.data.message && e.data.message.action === "accountsChanged") {
        // handler logic
        console.log('got accountsChanged event', e.data)
      }
    })
```
**Returns**

```shell
    
    
    interface MessageEventAccountsChangedData {
      isTronLink: boolean;
      message: {
        action: string;
        data: {
          address: string | boolean;
        }
      }
    }
```
**Return value example**

  1. When users log in, the content of the message body is:




```shell
    
    
    {
      "data": {
        "address": "TZ5XixnRyraxJJy996Q1sip85PHWuj4793" // Last selected account address
      }
    }
```
  1. When users switch accounts, the content of the message body is:




```shell
    {
      "data": {
        "address": "TRKb2nAnCBfwxnLxgoKJro6VbyA6QmsuXq" // Newly selected account address
      }
    }
```
  1. When users lock accounts and the wallet is automatically locked due to timeout, the message body content is:




```shell
    {
      "data": {
        "address": false
      }
    }
```