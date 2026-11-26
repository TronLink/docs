# iOS Core (Open Source)

**GitHub**: [https://github.com/TronLink/tronlink-iOS-core](https://github.com/TronLink/tronlink-iOS-core)

Use TronLink’s native iOS wallet module to create a TRON wallet, read its address, and sign transactions or messages.

## Installation

Add the dependency to your app target in the Podfile. The minimum iOS version and the Swift version are declared in the [podspec](https://github.com/TronLink/tronlink-iOS-core/blob/main/tronlink-iOS-core.podspec).

```ruby
pod 'tronlink-iOS-core'
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

Installing the pod or creating a wallet does not start a statistics upload. The host app must invoke the reporter and implement the upload callback in `TRXMetricsDataSource`. To enable uploads, the app must also identify its environment as production or pre-release. The same check applies to Debug and Release builds. In TronLink iOS, Basic Mode suppresses reporting, as do watch-only wallets and Shasta activity. [iOS privacy policy](https://github.com/TronLink/tronlink-iOS-core/blob/main/PRIVACY-POLICY.md)

## Version & License

For the current version, see the [podspec](https://github.com/TronLink/tronlink-iOS-core/blob/main/tronlink-iOS-core.podspec). [Apache License 2.0](https://github.com/TronLink/tronlink-iOS-core/blob/main/LICENSE)
