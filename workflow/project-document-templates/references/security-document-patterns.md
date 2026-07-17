# Security Document Patterns

Reference for Section 14: Security templates (CyBOK, ISO 27001, OWASP).

## Document Categories

| Category | Documents | Key Standards |
|----------|----------|--------------|
| Governance | ISMS Documentation, Security Policy, Compliance Assessment | ISO 27001 |
| Risk | Risk Assessment, Risk Treatment Plan, Threat Model | ISO 27005, STRIDE |
| Requirements | Security Requirements, Secure Design Review, Secure Coding Guidelines | OWASP, CERT |
| Testing | SAST, SCA, DAST, Penetration Test, Abuse/Misuse Cases | OWASP Testing Guide |
| Operations | Incident Response, BCP, Vulnerability Management, DevSecOps | ISO 27035, NIST 800-61 |
| Architecture | Security Architecture, Network Security, Access Control, Authentication | CyBOK |
| Metrics | Security Metrics Dashboard, Compliance Assessment | CyBOK |
| Forensics | Digital Forensics, Adversary Emulation | CyBOK |

## STRIDE Analysis Pattern

| Threat | Description | Mitigation Pattern |
|--------|-----------|-------------------|
| Spoofing | Impersonate user | MFA, JWT validation |
| Tampering | Modify data | TLS, integrity checks |
| Repudiation | Deny action | Audit logging |
| Information Disclosure | Expose data | Encryption, access controls |
| Denial of Service | Overwhelm system | Rate limiting, WAF |
| Elevation of Privilege | Gain unauthorized access | RBAC, least privilege |

## Risk Heat Map (5×5)

```markdown
| Likelihood \ Impact | Negligible (1) | Minor (2) | Moderate (3) | Major (4) | Critical (5) |
|-------------------|---------------|-----------|-------------|-----------|-------------|
| **Very Likely (5)** | 🟡 | 🟡 | 🟠 | 🔴 | 🔴 |
| **Likely (4)** | 🟢 | 🟡 | 🟠 | 🔴 | 🔴 |
| **Possible (3)** | 🟢 | 🟡 | 🟡 | 🟠 | 🔴 |
| **Unlikely (2)** | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |
| **Rare (1)** | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 |
```

## OWASP Top 10 Reference

| # | Category | Key Mitigation |
|---|---------|---------------|
| A01 | Broken Access Control | RBAC, least privilege |
| A02 | Cryptographic Failures | AES-256, TLS 1.3, bcrypt |
| A03 | Injection | Parameterized queries |
| A04 | Insecure Design | Threat modeling |
| A05 | Security Misconfiguration | Security headers, no defaults |
| A06 | Vulnerable Components | SCA scanning |
| A07 | Auth Failures | MFA, rate limiting |
| A08 | Data Integrity Failures | Input validation |
| A09 | Logging Failures | Audit logging |
| A10 | SSRF | URL validation |

## Defense in Depth Layers

| Layer | Controls | Mermaid Color |
|-------|---------|-------------|
| Perimeter | CDN, WAF, LB | #e3f2fd (light blue) |
| Application | API Gateway, Input Validation | #e8f5e9 (light green) |
| Data | Encryption, Masking | #fff3e0 (light orange) |
| Infrastructure | Network Segmentation, Container Security | #fce4ec (light pink) |
| Monitoring | SIEM, IDS/IPS | #f3e5f5 (light purple) |

## SSDLC Gate Pattern

| Gate | Phase | Criteria | Blocking |
|------|-------|---------|---------|
| Security Requirements Review | Requirements | All security reqs defined | Yes |
| Threat Model Review | Design | Threat model complete | Yes |
| SAST Gate | Build | No critical/high findings | Yes |
| SCA Gate | Build | No critical/high vulns | Yes |
| DAST Gate | Pre-release | No critical findings | Yes |
| Pen Test Gate | Pre-release | No critical findings | Yes |
