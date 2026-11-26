# Android Core (Open Source)

**GitHub**: [https://github.com/TronLink/tronlink-android-core](https://github.com/TronLink/tronlink-android-core)

Integrate the wallet functions used by TronLink Android to create a TRON wallet, read its address, and sign transactions or messages.

## Installation

The library requires Android API level 21 or later and Java 8 or later. Add JitPack to the repositories Gradle uses to resolve dependencies (Groovy DSL).

```groovy
repositories {
    maven { url "https://jitpack.io" }
}
```

Add the AAR to the app module’s dependencies.

```groovy
dependencies {
    implementation 'com.github.TronLink:tronlink-android-core:1.0.2@aar'
}
```

## Create a wallet

Create a wallet in your app and read its TRON address.

```java
import org.tron.walletserver.Wallet;

// Inside an application method
Wallet wallet = new Wallet(true);
String address = wallet.getAddress();
```

The wallet tests also show how to restore an address from a mnemonic or private key. For transaction and message signing, see the signing tests. [Wallet examples](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/WalletCoreUnitTest.java) · [Signing examples](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/TransactionCoreUnitTest.java)

## Verify the AAR

The release signing key fingerprint is `7B910EA80207596075E6D7BA5D34F7A6550473BA`. With the public key imported, run this command in the directory containing the AAR and its detached signature. Use the filenames from your release.

```bash
gpg --verify tronlink-android-core-VERSION.aar.asc tronlink-android-core-VERSION.aar
```

## Privacy

TronLink Android aggregates usage on the device using per-address UUIDs and amount ranges. Enabling Basic Mode in the app settings disables report creation and upload. [Android privacy policy](https://github.com/TronLink/tronlink-android-core/blob/main/PRIVACY-POLICY.md)

## Version & License

The upstream installation example uses `1.0.2`. [Apache License 2.0](https://github.com/TronLink/tronlink-android-core/blob/main/LICENSE)
