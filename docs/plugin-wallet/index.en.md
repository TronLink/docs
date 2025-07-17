# 插件钱包开发

TronLink 插件钱包为浏览器环境提供了完整的开发者集成方案，支持主动请求功能和被动消息接收。

## 主要功能

### 主动请求功能
- [主动请求概述](active-requests.md) - 主动请求功能总览
- [连接网站](active-requests/connect-website.md) - 连接网站功能
- [添加Token](active-requests/add-token.md) - 添加 Token 功能

### 被动接收消息
- [被动消息概述](passive-messages.md) - 被动接收消息总览
- [账户改变消息](passive-messages/account-change.md) - 账户改变消息处理
- [网络改变消息](passive-messages/network-change.md) - 网络改变消息处理
- [连接网站成功消息](passive-messages/connect-success.md) - 连接成功消息处理
- [断开连接网站消息](passive-messages/disconnect.md) - 断开连接消息处理
- [即将废弃的消息](passive-messages/deprecated-messages.md) - 即将废弃的消息说明

## 快速开始

1. 阅读 [主动请求概述](active-requests.md) 了解基本概念
2. 按照 [连接网站](active-requests/connect-website.md) 进行集成
3. 实现 [被动消息处理](passive-messages.md) 功能
4. 测试各种功能，确保正常工作

## 开发注意事项

- 确保正确处理所有消息类型
- 注意即将废弃的消息，及时更新代码
- 遵循安全最佳实践
- 测试不同网络环境下的兼容性

## 技术支持

如有问题，请参考相关文档或联系技术支持团队。 