---
tags:
- software-engineering
- swebok
---

# Software Security

> **Purpose:** Covers the engineering discipline of building security into software throughout the entire development life cycle — from requirements and design through construction, testing, and maintenance. Introduced new in SWEBOK v4, this KA addresses threat modeling, vulnerability management, secure coding practices, security testing methodologies, and domain-specific concerns like cloud, IoT, and machine learning security.

## Knowledge Areas

- **Software Security Fundamentals** — Defines software security as a product quality characteristic (per ISO/IEC 25010:2023), establishes the CIA triad (Confidentiality, Integrity, Availability) from information security, and scopes cybersecurity as safeguarding people and organizations from cyber risks including social engineering, hacking, malware, and spyware.

- **Security Management and Organization** — Covers organizational governance: the Systems Security Engineering Capability Maturity Model (SSE-CMM) for measuring process capability, ISO/IEC 27001:2022 for establishing an Information Security Management System (ISMS), and adapting security practices to Agile development so security becomes an enabler rather than a blocker.

- **Software Security Engineering and Processes** — Introduces the Secure Development Life Cycle (SDLC) as a spiral model that treats security holistically across all lifecycle phases, and the DevSecOps movement integrating security into CI/CD culture. Also covers Common Criteria (ISO/IEC 15408:2022) for evaluating security functionality and assurance of IT products.

- **Security Engineering for Software Systems** — The core engineering practices: security requirements elicitation (misuse/abuse cases, threat actors, risk assessment), security design (access control, cryptography, threat modeling), security patterns (recurring proven solutions), secure construction (CERT Top 10 practices including input validation, least privilege, defense in depth), security testing (static analysis of source/binaries, dynamic testing via penetration testing and fuzzing), and vulnerability management using CVE, CWE, CAPEC, and CVSS databases.

- **Software Security Tools** — Two categories: vulnerability checking tools (source code analyzers for injection flaws, buffer overflows, insecure libraries; binary analysis tools for compiler-introduced or hidden vulnerabilities) and penetration testing tools (controlled attacks, fuzzing with malformed/random data to uncover operational weaknesses).

- **Domain-Specific Software Security** — Addresses emerging areas: container and cloud security (forgotten assets, outsourced physical controls), IoT software security (massive endpoint attack surface, device-to-device communication hardening), and machine learning security (model poisoning attacks on training data, evasion attacks on trained model inputs).

## Essential Concepts

- **Build security in, don't bolt it on** — Security must be designed from the start across all SDLC phases; retrofitting is far more expensive and less effective.
- **CIA Triad** — Confidentiality (no unauthorized disclosure), Integrity (accuracy and completeness), Availability (accessible on demand by authorized entities). Additional properties include authenticity, accountability, non-repudiation, and reliability.
- **Secure Development Life Cycle (SDLC)** — A spiral lifecycle model that ensures security is inherent in design and development, reducing maintenance costs and increasing reliability against security faults.
- **DevSecOps** — Integration of development, security, and operations into an Agile culture emphasizing automation, platform design, and continuous integration with security baked in.
- **Threat Modeling** — Illustrating how a system may be attacked to inform security design decisions and specify mitigations.
- **Defense in Depth** — Layering multiple security controls so that if one fails, others still provide protection.
- **Principle of Least Privilege** — Every module and process should operate with the minimum privileges necessary to perform its function.
- **Input Validation** — Validate all input; the #1 CERT secure coding practice to prevent injection flaws and buffer overflows.
- **Static vs. Dynamic Security Testing** — Static analysis examines source code or binaries for vulnerability patterns without execution; dynamic testing (penetration testing, fuzzing) evaluates running software behavior.
- **Vulnerability Databases** — CVE (Common Vulnerabilities and Exposures), CWE (Common Weakness Enumeration), CAPEC (Common Attack Pattern Enumeration and Classification), and CVSS (Common Vulnerability Scoring System) form the shared taxonomy for vulnerability management.
- **Common Criteria (ISO/IEC 15408:2022)** — International standard for evaluating security functionality and assurance of IT products, helping consumers assess whether products meet their security needs.
- **ISMS (ISO/IEC 27001:2022)** — A documented, systematic plan for managing organizational technology security, including risk assessments, protective measures, and continuous monitoring.
- **Agile Security** — Security teams must work iteratively, automate, and become enablers rather than blockers; keys are involvement of security + developers, enablement, automation, and agility.
- **ML Security Threats** — Two attack categories: model poisoning (corrupting training data) and evasion (crafting inputs that deceive trained models).
- **IoT Security Challenges** — Massive endpoint proliferation creates a broad attack surface; hardening endpoints, securing device-to-device communications, and ensuring device/information credibility in formerly closed homogeneous systems.

## Tools & Techniques Mentioned

- **Source Code Analyzers** — Static analysis tools detecting injection flaws, buffer overflows, insecure library usage through code patterns
- **Binary Analysis Tools** — Examine compiled code and third-party libraries for vulnerabilities not visible in source
- **Fuzzing Tools** — Submit malformed, malicious, or random data to system entry points to detect faults
- **Penetration Testing Tools** — Controlled attacks evaluating operational security; also called ethical hacking
- **Web Application Scanners** — Automated dynamic testing for web applications
- **SSE-CMM** — Systems Security Engineering Capability Maturity Model for measuring organizational process capability
- **CERT Secure Coding Standards** — Guidelines and standards (e.g., CERT C, CERT Java) for secure software construction
- **CVSS v4.0** — Scoring system expressing characteristics and severity of software vulnerabilities
- **MITRE Databases** — CVE, CWE, CAPEC for cataloguing vulnerabilities, weaknesses, and attack patterns
- **ISO/IEC 27001:2022** — ISMS requirements framework
- **ISO/IEC 15408:2022 (Common Criteria)** — IT security evaluation criteria

## Related SWEBOK Chapters

- [[01_Software_Requirements]]: Security requirements engineering — elicitation, misuse/abuse cases, threat actors, risk assessment
- [[03_Software_Design]]: Security design — access control, cryptography, threat modeling, security patterns
- [[04_Software_Construction]]: Secure coding practices — CERT guidelines, input validation, least privilege, defense in depth
- [[05_Software_Testing]]: Security testing — static analysis, penetration testing, fuzzing, vulnerability assessment
- [[06_Software_Engineering_Operations]]: DevSecOps — integrating security into CI/CD culture and automation
- [[11_Software_Quality]]: Product quality model (ISO/IEC 25010:2023) — security as a quality characteristic
