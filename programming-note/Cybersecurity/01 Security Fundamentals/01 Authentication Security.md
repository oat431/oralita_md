---
tags:
- cybersecurity
- programming
- security
---

# 01 Authentication Security

Authentication is the most attacked surface. Get it wrong and everything else is irrelevant.

---

## Password Storage — NEVER Plaintext

```java
// ❌ NEVER do this
user.setPassword(password);  // Stored as-is — breach = all passwords exposed

// ❌ Even hashing with SHA isn't enough
String hash = DigestUtils.sha256Hex(password);  // Too fast — brute-forceable

// ✅ bcrypt with salt and cost factor
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));

// ✅ Argon2id (2024+ best practice)
Argon2 argon2 = Argon2Factory.create(Argon2Factory.Argon2Types.ARGON2id);
String hash = argon2.hash(10, 65536, 1, password.toCharArray());
```

---

## Session Security

```java
// Cookie configuration
http
    .sessionManagement(session -> session
        .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
        .maximumSessions(1)                      // One session per user
        .maxSessionsPreventsLogin(true)           // Block new login, don't expire old
    );

// Session cookie flags
server:
  servlet:
    session:
      cookie:
        http-only: true     // Not accessible via JavaScript
        secure: true        // HTTPS only
        same-site: Lax       // CSRF protection
```

| Flag | What It Does |
|------|-------------|
| **HttpOnly** | JavaScript can't read the cookie (XSS protection) |
| **Secure** | Cookie sent only over HTTPS |
| **SameSite** | Cookie not sent on cross-site requests (CSRF protection) |

---

## JWT Best Practices

| Rule | Why |
|------|-----|
| **Short expiration** (15 min) | Limit damage if token is stolen |
| **Use refresh tokens** | Longer-lived, stored securely, revocable |
| **RS256 (asymmetric)** | Only auth server has private key. Services verify with public key. |
| **Never store in localStorage** | Vulnerable to XSS. HttpOnly cookie or memory. |
| **Validate EVERYTHING** | Signature, expiration, issuer, audience |

```java
// JWT validation
JwtDecoder decoder = NimbusJwtDecoder.withPublicKey(publicKey).build();
Jwt jwt = decoder.decode(token);

// Verify claims
if (jwt.getExpiresAt().isBefore(Instant.now())) {
    throw new JwtException("Token expired");
}
if (!"my-auth-server".equals(jwt.getIssuer().toString())) {
    throw new JwtException("Invalid issuer");
}
```

---

## Multi-Factor Authentication (MFA)

| Factor | Example |
|--------|---------|
| **Something you know** | Password, PIN |
| **Something you have** | Phone (TOTP), hardware key (WebAuthn) |
| **Something you are** | Fingerprint, face |

> MFA blocks 99.9% of automated account attacks. Implement it for all privileged operations.

---

## Rate Limiting Login

```java
// Prevent brute force — 5 attempts per username per 15 minutes
@PostMapping("/login")
@RateLimiter(name = "loginLimiter", fallbackMethod = "loginRateLimited")
public Token login(@RequestBody LoginRequest request) {
    // Authenticate
}

public Token loginRateLimited(LoginRequest request, Exception e) {
    throw new ResponseStatusException(HttpStatus.TOO_MANY_REQUESTS,
        "Too many login attempts. Try again in 15 minutes.");
}
```

---

## Auth Checklist

- [ ] Passwords hashed with bcrypt/argon2 (cost ≥ 12)
- [ ] All auth endpoints rate-limited
- [ ] Session cookies: HttpOnly, Secure, SameSite
- [ ] JWT: short expiry, RS256, refresh tokens
- [ ] MFA for admin/sensitive operations
- [ ] Failed login logging and alerting
- [ ] Password reset tokens: single-use, short expiry, tied to user

---

## Sources

- OWASP Authentication Cheat Sheet
- JWT Best Practices — https://datatracker.ietf.org/doc/html/rfc8725
