---
tags:
- cybersecurity
- programming
- security
---

# 04 Compliance & Frameworks

Security frameworks turn "be secure" from a vague goal into a checklist. Compliance proves you're following the checklist to auditors, customers, and regulators.

---

## Key Frameworks

| Framework | What It Is | Who Needs It |
|-----------|-----------|-------------|
| **OWASP Top 10** | Top web app risks | Every web developer |
| **OWASP ASVS** | Detailed verification standard | Security-conscious dev teams |
| **NIST CSF** | Risk management framework | US gov, enterprises |
| **ISO 27001** | Information security management | Enterprises, certification |
| **SOC 2** | Service org controls (trust criteria) | SaaS companies |
| **PCI DSS** | Payment card security | Anyone handling credit cards |
| **GDPR** | EU data protection | Anyone with EU user data |

---

## OWASP ASVS (Application Security Verification Standard)

Three levels of verification:

| Level | What | For |
|:-----:|------|-----|
| **L1** | Basic. Automated scans + manual review of key controls. | All apps |
| **L2** | Standard. Most apps. Penetration testing required. | Apps with sensitive data |
| **L3** | Advanced. For critical systems. | Banking, healthcare, military |

### ASVS Categories (L1 Highlights)

| # | Category | Key Requirement |
|---|----------|----------------|
| V1 | Architecture | Threat model exists |
| V2 | Authentication | bcrypt/argon2, MFA, secure password recovery |
| V3 | Session | HttpOnly, Secure, SameSite cookies |
| V4 | Access Control | Server-side enforcement on every endpoint |
| V5 | Input Validation | Parameterized queries, output encoding |
| V6 | Cryptography | TLS 1.2+, no deprecated algorithms |

---

## SOC 2 — The Five Trust Criteria

| Criteria | What It Means |
|----------|--------------|
| **Security** | Systems are protected against unauthorized access |
| **Availability** | Systems are operational and usable |
| **Processing Integrity** | Data processing is complete, accurate, timely |
| **Confidentiality** | Confidential data is protected |
| **Privacy** | Personal data is handled per privacy notice |

> SOC 2 Type I = design of controls at a point in time. Type II = effectiveness over 6–12 months.

---

## GDPR — Quick Compliance Checklist

| Requirement | Implementation |
|------------|---------------|
| **Consent** | Opt-in, not pre-checked. Easy to withdraw. |
| **Right to access** | User can request all their data |
| **Right to deletion** | "Delete my account" actually deletes data |
| **Data breach notification** | Notify authorities within 72 hours |
| **Data Protection Officer** | Required for large-scale processing |
| **DPA** (Data Processing Agreement) | Contract with every third-party that touches user data |

```java
// GDPR-compliant account deletion
@DeleteMapping("/account")
public void deleteAccount(Authentication auth) {
    String userId = auth.getName();
    
    // 1. Delete/Anonymize personal data
    userService.anonymizeUser(userId);
    
    // 2. Delete associated data
    orderService.deleteByUserId(userId);
    
    // 3. Log for audit
    auditLog.info("Account deleted: userId={}, timestamp={}", userId, Instant.now());
}
```

---

## Compliance != Security

> **Compliance is a snapshot. Security is continuous.** You can be compliant and still get breached. Frameworks are the minimum — go beyond them.

---

## Sources

- OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
- NIST CSF — https://www.nist.gov/cyberframework
- GDPR — https://gdpr.eu/
