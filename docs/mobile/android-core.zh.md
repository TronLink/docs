# Android 开源核心库

在 Android 应用中集成 TronLink 的钱包功能，可以创建 TRON 钱包、读取地址，并对交易或消息签名。

[上游 README](https://github.com/TronLink/tronlink-android-core/blob/main/README.md)

## 安装

环境要求为 Android API 21 及以上、Java 8 及以上。在 Gradle 解析依赖的仓库列表中加入 JitPack。以下示例使用 Groovy DSL。

```groovy
repositories {
    maven { url "https://jitpack.io" }
}
```

在应用模块中声明 AAR 依赖。

```groovy
dependencies {
    implementation 'com.github.TronLink:tronlink-android-core:1.0.2@aar'
}
```

## 创建钱包

在应用中创建钱包并读取 TRON 地址。

```java
import org.tron.walletserver.Wallet;

// 在应用的方法中执行
Wallet wallet = new Wallet(true);
String address = wallet.getAddress();
```

钱包测试还演示了如何通过助记词或私钥恢复地址。交易签名和消息签名的用法见签名测试。[钱包示例](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/WalletCoreUnitTest.java) · [签名示例](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/TransactionCoreUnitTest.java)

## 验证 AAR 签名

发布签名公钥的指纹为 `7B910EA80207596075E6D7BA5D34F7A6550473BA`。导入公钥后，在 AAR 和签名文件所在目录运行以下命令，并将文件名替换为实际下载的名称。

```bash
gpg --verify tronlink-android-core-VERSION.aar.asc tronlink-android-core-VERSION.aar
```

## 隐私

TronLink Android 在设备上为地址分配 UUID，按金额区间汇总使用数据。在 App 设置中开启基础模式（Basic Mode）后，应用会停止生成和上传统计报告。[Android 隐私说明](https://github.com/TronLink/tronlink-android-core/blob/main/PRIVACY-POLICY.md)

## 版本与许可证

上游安装示例使用 `1.0.2`。[Apache License 2.0](https://github.com/TronLink/tronlink-android-core/blob/main/LICENSE)
