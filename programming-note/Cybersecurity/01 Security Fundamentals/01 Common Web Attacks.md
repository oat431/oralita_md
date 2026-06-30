---
tags:
- cybersecurity
- programming
- security
---

# 01 Common Web Attacks — OWASP Top 10

These are the attacks every backend developer must defend against. Each one has a specific fix. None are hard to prevent — you just need to know them.

---

## 1. Broken Access Control

User accesses data they shouldn't.

```java
// ❌ Broken — trusts client-provided ID
@GetMapping("/orders/{id}")
public Order getOrder(@PathVariable String id) {
    return orderRepo.findById(id);  // Any user can read any order!
}

// ✅ Fixed — verify ownership
@GetMapping("/orders/{id}")
public Order getOrder(@PathVariable String id, Authentication auth) {
    Order order = orderRepo.findById(id);
    if (!order.getUserId().equals(auth.getName())) {
        throw new AccessDeniedException("Not your order");
    }
    return order;
}
```

**Fix:** Server-side authorization on EVERY endpoint. Never trust client-provided IDs for access control.

---

## 2. Cryptographic Failures

Sensitive data exposed due to weak crypto or none at all.

```java
// ❌ Plaintext password in logs
log.info("User login: {}", password);

// ❌ Hardcoded key
String key = "my-secret-key-1234";

// ✅ Hashed password, key from Vault
log.info("User login: userId={}", userId);
String key = vaultClient.getSecret("encryption-key");
```

**Fix:** Hash passwords (bcrypt). Encrypt PII. Keys from secrets manager. TLS everywhere.

---

## 3. Injection (SQL, XSS, Command)

Attacker injects malicious code through user input.

### SQL Injection

```java
// ❌ String concatenation — SQLi possible
String query = "SELECT * FROM users WHERE name = '" + userName + "'";

// ✅ Parameterized query — immune to SQLi
String query = "SELECT * FROM users WHERE name = ?";
PreparedStatement ps = conn.prepareStatement(query);
ps.setString(1, userName);
```

### XSS (Cross-Site Scripting)

```java
// ❌ Rendering user input as HTML
return "<div>" + userComment + "</div>";  // <script>alert(1)</script>

// ✅ Encode output
return "<div>" + HtmlUtils.htmlEscape(userComment) + "</div>";
```

**Fix:** Parameterized queries for SQL. Output encoding for HTML. Input validation everywhere.

---

## 4. Insecure Design

Missing security controls by design. No threat modeling. No rate limiting.

**Fix:** Threat model before coding. Document security assumptions. Rate limit all public endpoints.

---

## 5. Security Misconfiguration

Default credentials. Verbose error messages. Unnecessary features enabled.

```yaml
# ❌ Spring Boot defaults expose too much
management:
  endpoints:
    web:
      exposure:
        include: "*"           # Exposes env, heapdump, threaddump...

# ✅ Minimal exposure
management:
  endpoints:
    web:
      exposure:
        include: health,info   # Only what's needed
```

**Fix:** Harden defaults. Disable unused features. Review configs regularly.

---

## 6-10 Quick Reference

| # | Vulnerability | Fix |
|---|-------------|-----|
| 6 | **Vulnerable Components** | Scan dependencies. Update promptly. Use Snyk/Dependabot. |
| 7 | **Auth Failures** | bcrypt passwords. Rate-limit login. MFA. Secure session cookies. |
| 8 | **Software & Data Integrity** | Verify checksums. Pin dependencies. Use signed commits. |
| 9 | **Logging & Monitoring Failures** | Log auth events. Alert on anomalies. Never log secrets. |
| 10 | **SSRF** (Server-Side Request Forgery) | Validate URLs. Block internal IPs. Use allow-lists. |

---

## SSRF Example

```java
// ❌ SSRF possible — user controls the URL
String url = request.getParameter("url");
String content = restTemplate.getForObject(url, String.class);
// Attacker passes: http://169.254.169.254/latest/meta-data/ (AWS metadata)

// ✅ Validate URL against allow-list
if (!url.startsWith("https://api.trusted-partner.com/")) {
    throw new SecurityException("URL not allowed");
}
```

---

## Sources

- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets — https://cheatsheetseries.owasp.org/
