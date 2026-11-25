# iOS 开源核心库

在 iOS 应用中使用 TronLink 的原生钱包模块，可以创建 TRON 钱包、读取地址，并对交易或消息签名。

[上游 README](https://github.com/TronLink/tronlink-iOS-core/blob/main/README.md)

## 安装

该 Pod 支持 iOS 15.1 及以上，声明的 Swift 版本为 4.2。在 Podfile 中为应用 target 添加依赖。

```ruby
pod 'tronlink-iOS-core', '2.0.1'
```

运行 `pod install`，用 Xcode 打开生成的 `.xcworkspace`，然后在 Swift 文件中导入模块。

```swift
import TLCore
```

## 运行示例工程

要在上游 Xcode 示例工程中查看钱包 API 的用法，请先进入示例目录安装依赖。

```bash
git clone https://github.com/TronLink/tronlink-iOS-core.git
cd tronlink-iOS-core/Example
pod install
```

在 Xcode 中打开 `Example/` 下的工作区。Swift 测试展示了创建钱包、签署交易和消息，以及导出私钥或助记词的用法。[Swift 钱包示例](https://github.com/TronLink/tronlink-iOS-core/blob/main/Example/Tests/Tests.swift)

## 隐私

TronLink iOS 在设备上汇总使用数据。开启基础模式（Basic Mode）后，应用会停止生成和上传统计报告。观察钱包和 Shasta 测试网也不参与上报。Debug 与 Release 构建都只允许在宿主标记为线上或预发布的环境中上传。[iOS 隐私说明](https://github.com/TronLink/tronlink-iOS-core/blob/main/PRIVACY-POLICY.md)

## 版本与许可证

版本为 `2.0.1`。[Podspec](https://github.com/TronLink/tronlink-iOS-core/blob/main/tronlink-iOS-core.podspec) · [Apache License 2.0](https://github.com/TronLink/tronlink-iOS-core/blob/main/LICENSE)
