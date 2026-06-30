---
tags:
- cybersecurity
- programming
- security
---

# 02 Dependency & Supply Chain Security

Your code is only as secure as your dependencies. A single vulnerable library can expose everything. Supply chain attacks inject malware through the tools you trust.

---

## The Problem

```
Your App
  ├── Spring Boot (200+ transitive deps)
  ├── Jackson (parses untrusted JSON)
  ├── Log4j (remember December 2021?)
  ├── PostgreSQL driver
  └── ... hundreds more
```

A CVE in ANY of these = your app is vulnerable.

---

## Software Composition Analysis (SCA)

| Tool | What It Does |
|------|-------------|
| **Snyk** | Scans dependencies for CVEs. Fix PRs. |
| **Dependabot** (GitHub) | Auto-PRs for vulnerable deps. Free. |
| **OWASP Dependency-Check** | CLI/plugin. Maps deps to NVD. |
| **Trivy** | Container + dependency scanning. |

```yaml
# GitHub Dependabot — auto-update vulnerable deps
version: 2
updates:
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

---

## CVE Lifecycle

```
CVE Published → NVD scores severity (CVSS) → Scanner flags your project → You update
```

| CVSS Score | Severity | Response Time |
|:----------:|----------|:------------:|
| 9.0–10.0 | 🔴 Critical | < 24 hours |
| 7.0–8.9 | 🟠 High | < 72 hours |
| 4.0–6.9 | 🟡 Medium | Next sprint |
| 0.1–3.9 | 🟢 Low | Next release |

---

## SBOM (Software Bill of Materials)

A list of every component in your software. Becoming mandatory (US Executive Order 14028).

```bash
# Generate SBOM with CycloneDX Maven plugin
mvn cyclonedx:makeAggregateBom
# Output: target/bom.xml — machine-readable inventory
```

---

## Supply Chain Attacks

| Attack | How | Defense |
|--------|-----|---------|
| **Typosquatting** | Malicious package with similar name (e.g., `sping-boot`) | Verify package names. Use internal registry. |
| **Dependency confusion** | Public package with same name as private | Scoped packages. Internal registry priority. |
| **Compromised maintainer** | Legit package gets malicious update | Pin versions. Review diffs before upgrading. |
| **Build tool compromise** | Malicious plugin/action | Pin action versions. Review workflow changes. |

---

## Dependency Hygiene

| Rule | How |
|------|-----|
| **Pin versions, not ranges** | `2.4.1` not `^2.4.0` |
| **Minimize dependencies** | If you only need 1 function, copy it (with attribution) |
| **Regular updates** | Auto-merge patch updates. Review minor/major. |
| **Audit periodically** | `mvn dependency:analyze` — find unused deps |
| **Private registry** | Proxy/cache Maven Central. Block known-bad packages. |

```xml
<!-- ✅ Pin exact version -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.17.1</version>  <!-- Exact, not range -->
</dependency>
```

---

## Sources

- OWASP Dependency-Check — https://owasp.org/www-project-dependency-check/
- Snyk — https://snyk.io/
- CycloneDX SBOM — https://cyclonedx.org/
