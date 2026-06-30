---
tags:
- cybersecurity
- programming
- security
---

# 01 Cryptography Basics

Cryptography is the math that keeps secrets secret. You don't need to implement ciphers — you need to know which algorithms to use, when, and how not to misuse them.

---

## Hashing

One-way function. Same input → same output. Can't reverse. Used for passwords, integrity checks.

| Algorithm | Output | Status |
|-----------|:------:|--------|
| **MD5** | 128-bit | ❌ Broken — never use |
| **SHA-1** | 160-bit | ❌ Broken — migrate away |
| **SHA-256** | 256-bit | ✅ Safe |
| **SHA-512** | 512-bit | ✅ Safe |
| **bcrypt** | Variable | ✅ Password hashing (slow by design) |
| **Argon2** | Variable | ✅ Best for passwords (2024+) |

```java
// Password hashing — always use bcrypt/argon2, never SHA
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));  // 12 = cost factor
boolean match = BCrypt.checkpw(attempt, hash);
```

### Salt & Pepper

| Term | What | Why |
|------|------|-----|
| **Salt** | Random value per password, stored with hash | Prevents rainbow table attacks. Each hash is unique even for same password. |
| **Pepper** | Secret value, NOT stored with hash (app config) | Extra layer. If DB is breached, pepper still unknown. |

---

## Encryption

Two-way. Can encrypt and decrypt with the right key.

### Symmetric (One Key)

Same key encrypts and decrypts. Fast. Used for bulk data.

| Algorithm | Key Size | Status |
|-----------|:------:|--------|
| **AES-256-GCM** | 256-bit | ✅ Best choice (authenticated encryption) |
| **AES-128-CBC** | 128-bit | ⚠️ OK but prefer GCM |
| **ChaCha20-Poly1305** | 256-bit | ✅ Alternative to AES |

```java
// AES-GCM encryption — Java
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec gcmSpec = new GCMParameterSpec(128, iv);  // 128-bit auth tag
cipher.init(Cipher.ENCRYPT_MODE, key, gcmSpec);
byte[] encrypted = cipher.doFinal(plaintext);
```

### Asymmetric (Key Pair)

Public key encrypts, private key decrypts. Slow. Used for key exchange, signatures.

| Algorithm | Use |
|-----------|-----|
| **RSA-2048/4096** | Legacy key exchange, signatures |
| **ECDSA (P-256)** | Modern signatures (faster, smaller keys) |
| **Ed25519** | Modern signatures (best, simplest) |
| **X25519** | Key exchange (ECDH) |

---

## TLS — Transport Layer Security

Encrypts data in transit between client and server.

```
TLS 1.3 Handshake (simplified):
  Client → Server: "Hello, I support these ciphers"
  Server → Client: "Let's use this cipher" + certificate
  Client: verifies certificate against trusted CA
  ← Encrypted channel established →
```

### Minimum TLS Configuration

```nginx
ssl_protocols TLSv1.2 TLSv1.3;        # No TLS 1.0/1.1
ssl_ciphers HIGH:!aNULL:!MD5;          # Strong ciphers only
ssl_prefer_server_ciphers on;
```

---

## Certificates

| Concept | What |
|---------|------|
| **Certificate** | Binds a public key to an identity (domain, org) |
| **CA** (Certificate Authority) | Trusted third party that signs certificates |
| **Self-signed** | Signed by yourself — fine for internal, never for public |
| **Let's Encrypt** | Free, automated TLS certificates |

---

## Never Roll Your Own Crypto

| ❌ Don't | ✅ Do |
|----------|------|
| Invent your own cipher | Use AES-GCM, ChaCha20 |
| Implement RSA from scratch | Use Java `Cipher`, `KeyPairGenerator` |
| Hardcode keys | Use Vault, K8s Secrets, env vars |
| Use ECB mode | Use GCM (authenticated, prevents tampering) |

---

## Sources

- OWASP Cryptographic Storage Cheat Sheet
- Java Crypto API — https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html
