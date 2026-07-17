# SWEBOK Template Structure

Standard template structure for software specification documents based on SWEBOK v4.

## Folder Structure

```
01_requirement/     — What to build (requirements)
02_design/          — How to build it (architecture)
03_construction/    — How to code it (developer guide)
04_testing/         — How to verify it (test plan)
05_devops/          — How to deploy it (CI/CD)
06_security/        — How to secure it (security)
07_pm/              — How to manage it (project management)
```

## Document Naming Convention

Two-digit folder prefix + two-digit document prefix:
- `011_business_objective.md` — folder 01, doc 01
- `022_API_specification.md` — folder 02, doc 02

## Required Frontmatter

```yaml
---
document_type: [Type Name]
version: "1.0"
status: Draft | Under Review | Approved | Baselined
author: "[Author Name]"
created: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
project_name: "[Project Name]"
project_id: "[Project-ID]"
classification: "Internal"
tags: [tag1, tag2, tag3]
standard_ref:
  - SWEBOK v4 — [Section]
  - ISO/IEC/IEEE 29148 — Requirements Engineering
---
```

## Document Types by Folder

### 01_requirement
| File | Document Type | Purpose |
|------|---------------|---------|
| 011 | Business Objectives | SMART goals, KPI framework |
| 012 | User Stories | As a/I want/So that format |
| 013 | Acceptance Criteria | Given/When/Then (BDD) |
| 014 | Stakeholder Analysis | Influence/interest matrix |

### 02_design
| File | Document Type | Purpose |
|------|---------------|---------|
| 021 | ADR | Architecture Decision Records |
| 022 | API Specification | REST endpoints, request/response |
| 023 | Database Schema DDL | PostgreSQL CREATE TABLE |
| 024 | ERD | Mermaid erDiagram |
| 025 | Software Architecture | High-level architecture diagram |

### 03_construction
| File | Document Type | Purpose |
|------|---------------|---------|
| 031 | Developer Guide | Setup, prerequisites, running |
| 032 | Build Scripts | Build commands |
| 033 | Dependency Manifest | Package versions |
| 034 | Commit Messages & Changelog | PR/commit log |
| 035 | Coding Standards | Style rules, linting |
| 036 | Code Review Records | Review log |

### 04_testing
| File | Document Type | Purpose |
|------|---------------|---------|
| 041 | Test Plan | Strategy, scope, environment |
| 042 | Test Cases | TC-ID, Given/When/Then |
| 043 | Defect Report | Bug log |
| 044 | Regression Test Suite | Regression tests |
| 045 | Coverage Report | Coverage metrics |

### 05_devops
| File | Document Type | Purpose |
|------|---------------|---------|
| 051 | CI/CD Pipeline | GitHub Actions config |
| 052 | Deployment Plan | Docker, infrastructure |
| 053 | Release Notes | Version changelog |
| 054 | Operations Manual | Runbook, health checks |

### 06_security
| File | Document Type | Purpose |
|------|---------------|---------|
| 061 | Security Test Report | Security testing results |
| 062 | Security Coding Standards | Security rules |

### 07_pm
| File | Document Type | Purpose |
|------|---------------|---------|
| 071 | Risk Register | Risk log |
| 072 | Meeting Minutes | Daily logs |

## Key Formatting Rules

1. **Tables over prose** — structured data is easier to maintain
2. **Wikilinks** — `[[022_API_specification]]` for cross-references
3. **Mermaid diagrams** — ERD, architecture, flowcharts
4. **Status badges** — ✅ Approved, ⬜ Not Started, ⏳ In Progress
5. **Priority markers** — 🔴 Must Have, 🟡 Should Have, 🟢 Could Have
