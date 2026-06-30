---
tags:
- cybersecurity
- overview
- programming
- security
---

# Cybersecurity for Backend Engineers — Overview

Security is not a feature. It's a property of every line of code you write. This vault focuses on what matters for building safer backends — from cryptography basics to incident response. Not a CISSP study guide. A practical defense toolkit.

> Roadmap reference: https://roadmap.sh/cyber-security

---

## Topics

### 01 Security Fundamentals

> [[01 Cryptography Basics]] — Hashing, encryption (symmetric/asymmetric), TLS, certificates, JWT signing
> [[01 Common Web Attacks]] — OWASP Top 10: SQLi, XSS, CSRF, SSRF, IDOR, injection
> [[01 Authentication Security]] — Password storage, MFA, session management, OAuth2 pitfalls

### 02 Secure Development

> [[02 Secure Coding Practices]] — Input validation, output encoding, parameterized queries, file upload safety
> [[02 Dependency & Supply Chain]] — SCA, CVE tracking, SBOM, supply chain attacks, dependency pinning
> [[02 Secrets Management]] — Vault, K8s secrets, .gitignore, environment variables, secret rotation

### 03 Infrastructure Security

> [[03 Network & TLS]] — TLS 1.3, mTLS, certificate pinning, firewalls, WAF, zero-trust
> [[03 Container & Cloud Security]] — Docker security, K8s RBAC, IAM, cloud security groups
> [[03 API Security]] — Rate limiting, CORS, API keys, gateway auth, GraphQL-specific attacks

### 04 Security Operations

> [[04 Monitoring & Incident Response]] — SIEM, alerting, incident playbooks, post-mortems
> [[04 Vulnerability Management]] — SAST, DAST, dependency scanning, pen testing, bug bounty
> [[04 Compliance & Frameworks]] — OWASP ASVS, NIST, ISO 27001, SOC2, GDPR basics

---

## Defense in Depth — The Layers

```
Perimeter   → Firewall, WAF, DDoS protection
Network     → TLS, mTLS, network segmentation
Application → Input validation, auth, authz, rate limiting
Data        → Encryption at rest, hashing, masking
Operations  → Monitoring, alerting, incident response
```

> An attacker must breach ALL layers. A defender only needs ONE layer to hold.

---

## Quick Routes

| Goal | Path |
|------|------|
| **Securing a new API** | 01 Common Attacks → 03 API Security → 02 Secure Coding |
| **Preparing for an audit** | 04 Compliance → 01 Cryptography → 02 Secrets |
| **Incident just happened** | 04 Monitoring → 01 Common Attacks (identify the attack) |
| **DevOps security** | 03 Infrastructure → 02 Dependency → 04 Vulnerability |

---

## Sources

- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets — https://cheatsheetseries.owasp.org/
- roadmap.sh — https://roadmap.sh/cyber-security
