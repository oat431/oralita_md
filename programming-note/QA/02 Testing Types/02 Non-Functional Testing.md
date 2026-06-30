---
tags:
- programming
- qa
- testing
---

# 02 Non-Functional Testing

Functional testing checks WHAT the system does. Non-functional testing checks HOW WELL it does it — speed, security, usability, reliability.

---

## The "-ilities"

| Quality Attribute | Testing Type | Key Question |
|------------------|-------------|-------------|
| **Performance** | Load, Stress, Spike, Endurance | How fast? How many users? |
| **Security** | Penetration, Vulnerability scan, SAST/DAST | Can it be broken into? |
| **Usability** | Heuristic evaluation, User testing | Can people actually use it? |
| **Accessibility** | a11y audit, Screen reader testing | Can everyone use it? |
| **Reliability** | Soak testing, Chaos engineering | Does it stay up? |
| **Compatibility** | Cross-browser, Cross-device | Does it work everywhere? |

---

## Performance Testing

| Type | What It Tests | Example |
|------|--------------|---------|
| **Load** | Expected user load | 1000 concurrent users → response time? error rate? |
| **Stress** | Breaking point | Ramp up until it crashes. Where? How does it recover? |
| **Spike** | Sudden traffic burst | Flash sale: 100 → 10,000 users in 60 seconds |
| **Endurance (Soak)** | Memory leaks over time | Run at 80% load for 24 hours. Does memory grow unbounded? |

### Performance Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Response time** (p95) | 95% of requests faster than this | < 500ms |
| **Throughput** | Requests per second | Based on SLA |
| **Error rate** | % of failed requests | < 1% |
| **CPU / Memory** | Resource usage under load | < 80% |

### Tools

| Tool | Type |
|------|------|
| **JMeter** | Java, GUI-based load testing |
| **k6** (Grafana) | Script-based (JavaScript), CI-friendly |
| **Gatling** | Scala-based, high-performance |
| **Locust** | Python-based, distributed |

---

## Security Testing

| Type | What It Does |
|------|-------------|
| **SAST** (Static) | Analyzes source code for vulnerabilities (SonarQube, Checkmarx) |
| **DAST** (Dynamic) | Attacks running app (OWASP ZAP, Burp Suite) |
| **Penetration Testing** | Human expert tries to break in |
| **Dependency Scan** | Checks libraries for known CVEs (Snyk, Dependabot) |
| **Secret Scan** | Detects keys/passwords in code (TruffleHog, GitGuardian) |

### OWASP Top 10 (Quick Reference)

| # | Vulnerability |
|---|-------------|
| 1 | Broken Access Control |
| 2 | Cryptographic Failures |
| 3 | Injection (SQL, XSS) |
| 4 | Insecure Design |
| 5 | Security Misconfiguration |
| 6 | Vulnerable Components |
| 7 | Auth Failures |
| 8 | Software & Data Integrity |
| 9 | Logging & Monitoring Failures |
| 10 | SSRF |

---

## Accessibility Testing (a11y)

| Tool | What It Checks |
|------|---------------|
| **axe DevTools** | Automated WCAG violations in browser |
| **Lighthouse** | Built into Chrome DevTools |
| **WAVE** | Visual overlay of accessibility issues |
| **Screen reader** (NVDA, VoiceOver) | Manual test — can a blind user navigate? |

> Deep dive: **[[28 Accessibility]]** in HCI vault.

---

## Sources

- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- k6 — https://k6.io/
