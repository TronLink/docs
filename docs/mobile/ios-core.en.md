# iOS Core (Open Source)

Use TronLink’s native iOS wallet module to create a TRON wallet, read its address, and sign transactions or messages.

[Upstream README](https://github.com/TronLink/tronlink-iOS-core/blob/main/README.md)

## Installation

The pod targets iOS 15.1 or later and declares Swift 4.2. Add the dependency to your app target in the Podfile.

```ruby
pod 'tronlink-iOS-core', '2.0.1'
```

Run `pod install`, open the generated `.xcworkspace` in Xcode, and import the module in Swift.

```swift
import TLCore
```

## Run the example project

To explore the wallet APIs in the upstream Xcode project, install its pods from the example directory.

```bash
git clone https://github.com/TronLink/tronlink-iOS-core.git
cd tronlink-iOS-core/Example
pod install
```

Open the workspace in `Example/`. The Swift tests show wallet creation, transaction and message signing, and how to export a private key or mnemonic. [Swift wallet examples](https://github.com/TronLink/tronlink-iOS-core/blob/main/Example/Tests/Tests.swift)

## Privacy

TronLink iOS aggregates usage on the device. Basic Mode disables report creation and upload. Watch-only wallets and Shasta activity are also excluded. In both Debug and Release builds, the host must report an online or pre-release environment for uploads to occur. [iOS privacy policy](https://github.com/TronLink/tronlink-iOS-core/blob/main/PRIVACY-POLICY.md)

## Version & License

Version `2.0.1`. [Podspec](https://github.com/TronLink/tronlink-iOS-core/blob/main/tronlink-iOS-core.podspec) · [Apache License 2.0](https://github.com/TronLink/tronlink-iOS-core/blob/main/LICENSE)
