---
tags:
- software-engineering
- swebok
---

# Software Configuration Management

> **Purpose:** Software Configuration Management (SCM) is the discipline of identifying, controlling, and tracking the evolution of software artifacts throughout the entire life cycle. It ensures integrity and traceability of configuration items through version control, baseline establishment, formal change control, status accounting, auditing, and release management — providing the backbone for collaborative development and quality assurance.

## Knowledge Areas

- **Management of the SCM Process** — Planning, organizing, and monitoring SCM activities within the organizational context. Covers constraints, tool selection, vendor/subcontractor control, interface control, and the SCM Plan (SCMP) as a living document.
- **Software Configuration Identification** — Determining which artifacts are Configuration Items (CIs), establishing unique identifiers and attributes, defining baselines, tracking CI relationships (dependencies, derivation, succession, variants), and maintaining software libraries.
- **Software Configuration Change Control** — Formal processes for requesting, evaluating, approving, and implementing changes to CIs via a Configuration Control Board (CCB/SCCB), Change Requests (CRs/SCRs), and handling deviations and waivers.
- **Software Configuration Status Accounting (SCSA)** — Recording and reporting information about CIs, baselines, and relationships throughout the life cycle. Provides current implementation status, change traffic metrics, and evidence for governance and compliance.
- **Software Configuration Auditing** — Independent examinations to verify CIs conform to specifications and documentation. Includes Functional Configuration Audit (FCA), Physical Configuration Audit (PCA), and in-process audits conducted throughout development.
- **Software Release Management and Delivery** — Building the correct versions of SCIs, packaging artifacts, producing version description documents (VDD), and delivering releases — including continuous integration/continuous delivery pipelines.
- **Software Configuration Management Tools** — Covers version control tools, build automation, change control tools, CMDBs, and integrated workbenches. Tool selection depends on organizational scale, certification needs, and branching/merging strategies.

## Essential Concepts

- **Configuration Item (CI):** Any artifact (code, documents, plans, tools, data) designated for formal configuration control — an aggregation managed as a single entity.
- **Software Configuration Item (SCI):** A CI that is specifically a software entity (source code, libraries, executables, documentation, test materials).
- **Baseline:** A formally approved, fixed version of a CI at a specific point in the life cycle; can only be changed through formal change control procedures.
- **Configuration Control Board (CCB/SCCB):** The authority body (or individual in smaller projects) that evaluates, approves, rejects, or defers change requests. Multiple levels may exist based on criticality and life-cycle phase.
- **Change Request (CR/SCR):** A formal request to modify CIs — can originate from anyone, at any life-cycle stage. Requires technical evaluation (impact analysis), approval, implementation tracking, and verification.
- **Software Bill of Materials (SBOM):** A formal record detailing the components and supply-chain relationships of CIs used in building software — critical for security, compliance, and vulnerability tracking.
- **CI Relationships:** Dependencies (mutual), derivation (sequential), succession (version evolution), and variants (engineered alternatives) — tracked to understand change impact across the configuration.
- **Version Control & Branching/Merging:** Foundational SCM mechanisms — branches represent evolving source file versions; merging combines parallel changes. Strategies must be planned and communicated.
- **Status Accounting (SCSA):** The activity of capturing, verifying, and reporting CI status — who changed what, when, and what relationships exist. Supports audits, compliance, and process measurement.
- **Functional Configuration Audit (FCA):** Ensures the audited software item is consistent with its governing specifications (uses V&V outputs).
- **Physical Configuration Audit (PCA):** Ensures design and reference documentation are consistent with the as-built software product.
- **Deviation vs. Waiver:** A *deviation* is pre-approved departure from requirements before production; a *waiver* permits use of a nonconforming item discovered during/after production.
- **SCM Plan (SCMP):** The "living document" recording SCM planning — covers organization, responsibilities, activities, schedules, resources, and maintenance procedures.
- **Software Libraries:** Controlled collections of artifacts — source in version control, binaries in repositories with cryptographic hashes, release baselines in a definitive media library.
- **Continuous Integration/Delivery:** Automated build-test-deploy pipelines triggered by commits — requires SCM to track which changes are incorporated into releases and to reproduce prior builds exactly.

## Tools & Techniques Mentioned

- **Version Control Systems** (e.g., Git, SVN) — track and document source code changes; support branching, merging, parallel/distributed development
- **Build Automation Tools** — compile, link, run static analysis, execute tests, extract documentation; critical for reproducible builds and CI/CD pipelines
- **Change Control / Issue Tracking Tools** — manage CR workflows, CCB decisions, event notifications, and link to problem-reporting systems
- **Configuration Management System (CMS) / Workbench** — integrated tool sets providing CM logic, artifact identification, structuring, validation, and release
- **Configuration Management Database (CMDB)** — persistent store for configuration data and relationships
- **Release/Deployment Tools** — package artifacts, generate VDDs, track distribution, support digital signatures for integrity
- **SBOM Tools** — capture and maintain Software Bill of Materials for compliance and security
- **Impact Analysis** — technical evaluation of a proposed change's extent and consequences using CI relationship data
- **SCM Metrics** — change traffic, breakage, time-to-implement CRs, number of CRs per SCI, baseline status
- **Cryptographic Hashing** (SHA-1, MD5, MAC) — used in PCAs and integrity verification of built artifacts

## Related SWEBOK Chapters

- [[04_Software_Construction]] — SCM tools directly support construction activities; version control and build automation are tightly integrated with coding workflows.
- [[06_Software_Engineering_Operations]] — SCM enables repeatable deployment pipelines, environment configuration management, and operational release management.
- [[07_Software_Maintenance]] — SCM provides the traceability and change control infrastructure essential for corrective, adaptive, and perfective maintenance.
- [[10_Software_Engineering_Process]] — SCM is a foundational software life cycle process (SLCP); process controls and audits govern configuration activities.
- [[09_Software_Quality]] — SQA activities (V&V, audits, reviews) depend on SCM for controlled baselines; FCA/PCA are closely related to quality reviews.
