# HD 钱包
### 什么是 HD 钱包

HD 钱包是在 BIP32 中提出的为了避免管理一堆私钥的麻烦提出的分层推导方案。 钱包的生成是从单一个seed 产生一个树状结构存储多组 keypairs(私钥和公钥)，为了方便记忆，将 seed 用方便记忆和书写的单词表示，由12个单词组成，称为 mnemonic code(phrase)。

### TronLink 钱包-HD 钱包

TronLink 钱包支持 BIP32、BIP44 协议，并依据 BIP44 的分层路径方案，生成对应的 TRON 地址。


