# Connect Website

<span class="deprecated">DEPRECATED</span>

The methods in this section are deprecated and are expected to be removed in a few releases. The TRON community is discussing new specifications, you can go to [TRON-TIP](https://github.com/tronprotocol/tips/issues/463) to participate in the discussion.

**Connect Website**

**Overview**

TronLink supports TRX transfers, contract signature, authorization, etc. initiated by DApps. For security considerations, users are required to authorize the DApp to “connect website”. They can take further actions only after successful authorization. The DApp must first connect to the website, and wait for the user's permission before it can initiate a request for authorization.

**Specification**

**Example**

```shell
    const res = await tronWeb.request(
      {
        method: 'tron_requestAccounts',
        params: {
          websiteIcon: '<WEBSITE ICON URI>',
          websiteName: '<WEBSITE NAME>',
        },
      }
    )
```
**Parameters**

```shell
    interface RequestAccountsParams {
      websiteIcon?: string;
      websiteName?: string;
    }
```

**Returns**

```shell
    interface ReqestAccountsResponse {
      code: 200 | 4000 | 4001,
      message: string
    }
```
| Error Code | Description | Message |
|:-------|:-------|:-------|
| null  | Wallet is locked   | Empty string  |
| 200  | The site has previously been allowed to connect   | The site is already in the whitelist  |
| 200  | The user approved the connection   | User allowed the request.  |
| 4000  | The same DApp has already initiated a request to connect to the website, and the pop-up window has not been closed   | Authorization requests are being processed, please do not resubmit  |
| 4001  | The user rejected connection   | User rejected the request  |

**Interaction**

After triggering ‘tron_requestAccounts‘, there will be a pop-up window asking for confirmation: 

![image](../../images/tronlink-wallet-extension_request-tronlink-extension_connect-website_img_0.jpg)
