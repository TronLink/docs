# Android Core (Open Source)

**GitHub**: [https://github.com/TronLink/tronlink-android-core](https://github.com/TronLink/tronlink-android-core)

Integrate the wallet functions used by TronLink Android to create a TRON wallet, read its address, and sign transactions or messages.

## Installation

The library requires Android API level 21 or later; the Java version is set in the upstream [build configuration](https://github.com/TronLink/tronlink-android-core/blob/main/core/build.gradle). Add JitPack to the repositories Gradle uses to resolve dependencies (Groovy DSL).

```groovy
repositories {
    maven { url "https://jitpack.io" }
}
```

Add the AAR to the app module’s dependencies. Replace `<VERSION>` with a tag from the [releases](https://github.com/TronLink/tronlink-android-core/releases), normally the latest.

```groovy
dependencies {
    implementation 'com.github.TronLink:tronlink-android-core:<VERSION>@aar'
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

The wallet tests also show how to restore an address from a mnemonic or private key. For transaction signing, see the transaction tests. The tests include no message-signing example; the library implements it in `org.tron.common.bip32.Sign` (`signPrefixedMessage`, `signPrefixedMessageV2`). [Wallet examples](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/WalletCoreUnitTest.java) · [Transaction signing examples](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/test/java/org/tron/TransactionCoreUnitTest.java) · [`Sign.java`](https://github.com/TronLink/tronlink-android-core/blob/main/core/src/main/java/org/tron/common/bip32/Sign.java)

## Verify the AAR

Verification requires the exact AAR signed by TronLink and its matching detached `.asc` signature. JitPack and the GitHub releases do not provide signature files, so obtain the signed AAR and matching signature from the maintainers. See the [upstream verification instructions](https://github.com/TronLink/tronlink-android-core#integrity-check).

Download the [public key](https://keys.openpgp.org/vks/v1/by-fingerprint/7B910EA80207596075E6D7BA5D34F7A6550473BA) as `tronlink-build.asc`. Check the signing subkey fingerprint against the one in the upstream instructions, `7B910EA80207596075E6D7BA5D34F7A6550473BA`. Once it matches, import the key and verify the two files supplied by the maintainers, substituting their filenames below.

```bash
gpg --show-keys --with-subkey-fingerprint tronlink-build.asc
gpg --import tronlink-build.asc
gpg --verify release.aar.asc release.aar
```

## Privacy

Embedding the library does not start usage reporting. The reporting code in `org.tron.metrics` records and uploads data only after the host app wires up its repositories and calls `DataUploader.init(...)` and `upload(...)`. Read the upstream [privacy policy](https://github.com/TronLink/tronlink-android-core/blob/main/PRIVACY-POLICY.md) before enabling it.

## Version & License

The examples and links on this page follow the upstream `main` branch. When you pin an older tag, check that its APIs match. [Apache License 2.0](https://github.com/TronLink/tronlink-android-core/blob/main/LICENSE)
