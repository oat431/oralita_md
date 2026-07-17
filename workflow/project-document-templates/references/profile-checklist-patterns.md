# Profile Checklist Patterns

## Overview

Project-size-based checklists help teams right-size their documentation. Each profile maps documents to project characteristics (team size, timeline, regulatory exposure).

## Profile Definitions

### Small / Startup
- **Team:** 1–5 developers
- **Timeline:** Weeks to months
- **Methodology:** Agile / Lean
- **Regulatory:** Low / None
- **Key principle:** Just enough documentation to ship

### Medium / Enterprise
- **Team:** 10–50
- **Timeline:** 6–18 months
- **Methodology:** Hybrid (Agile + formal gates)
- **Regulatory:** Moderate
- **Key principle:** Structured enough for governance, flexible enough for delivery

### Large / Safety-Critical
- **Team:** 50+ members
- **Timeline:** 18+ months
- **Methodology:** V-Model / Waterfall with formal gates
- **Regulatory:** Heavy (aerospace, medical, defense, automotive)
- **Key principle:** If it's not documented, it didn't happen

## Profile Checklist Structure

```markdown
---
document_type: Project Profile Checklist — [Size] / [Type]
version: "1.0"
status: Active
tags: [profile, [size]-[type], checklist, essential-documents]
---

# Project Profile — [Size] / [Type] — Checklist

> **Team:** [size]
> **Timeline:** [range]
> **Methodology:** [approach]
> **Regulatory:** [level]
>
> **Key principle:** [principle]

---

## Priority Legend

| Symbol | Priority | Meaning |
|--------|---------|---------|
| 🔴 | **Must Have** | Essential — produce before or during the phase |
| 🟡 | **Nice to Have** | Recommended — add when capacity allows |
| 🟢 | **Optional** | Situational — produce only if context demands it |

---

## 1. [Category Name]

> **Owner:** [Role]

| Document | Priority | Template | Status |
|----------|---------|---------|--------|
| [[Document-Name]] | 🔴 | [Folder_Name] | ☐ |

---

## Summary

| Category | 🔴 | 🟡 | 🟢 | Total |
|---------|-----|-----|-----|-------|
| [Category] | [X] | [X] | [X] | [X] |
| **Total** | **[X]** | **[X]** | **[X]** | **[X]** |

---

## Quick-Start Checklist (🔴 Must Have Only)

| # | Document | ✓ |
|---|----------|---|
| 1 | [[Document-Name]] | ☐ |

---

## Related Profiles

- [[Profile-Other-Size-Checklist]]
```

## Backlink Convention

Each document entry uses:
- `[[Hyphenated-Name]]` — links to the template file
- `Template` column — references the folder name (e.g., `[01_Business_Analysis_and_strategy]`)
- `Status` column — ☐ for pending, ✅ for done

## Document Counts by Profile

| Category | Small | Medium | Large |
|---------|-------|--------|-------|
| Business Analysis | 4 | 9 | 11 |
| Requirements | 0 | 7 | 9 |
| Project Management | 2 | 11 | 15 |
| Architecture & Design | 5 | 12 | 13 |
| UX/UI Design | 3 | 12 | 20 |
| Construction | 6 | 9 | 10 |
| Testing | 5 | 15 | 19 |
| Security | 2 | 10 | 26 |
| Deployment & Operations | 4 | 6 | 8 |
| Maintenance & Support | 0 | 4 | 4 |
| Quality Assurance | 0 | 3 | 5 |
| Configuration Management | 0 | 0 | 6 |
| Data Management | 0 | 0 | 59 |
| SE Cross-Cutting | 0 | 0 | 18 |
| Domain-Specific | 0 | 0 | 4 |
| **Total** | **31** | **94** | **252** |

## Key Differences Between Profiles

| Aspect | Small | Medium | Large |
|--------|-------|--------|-------|
| [Formal reviews] | [Optional] | [Required] | [Mandatory with sign-off] |
| [Traceability] | [Nice to have] | [Required] | [Bidirectional, audited] |
| [Configuration mgmt] | [Git only] | [Git + branch strategy] | [Full CM plan + baselines] |
| [Testing rigor] | [Unit + basic] | [Full pyramid] | [V&V, formal verification] |
| [Security] | [Basic scan] | [OWASP compliance] | [Full security accreditation] |
| [Documentation] | [README + ADRs] | [Full specs] | [Every artifact documented] |
| [Data Management] | [Not included] | [Not included] | [Full DMBOK coverage] |
| [SE Cross-Cutting] | [Not included] | [Not included] | [Full SE lifecycle] |

## Profile File Locations

```
23_Project_Size/
├── Profile-Small-Startup-Checklist.md
├── Profile-Medium-Enterprise-Checklist.md
└── Profile-Large-Safety-Critical-Checklist.md
```

## Backlink Coverage

All profiles should have 100% backlink coverage after all sections are complete:
- Small: 51 backlinks
- Medium: 102 backlinks  
- Large: 251 backlinks

Verify with: `grep -c '\[\[' Profile-Name.md`
Verify no empty: `grep -c '| — |' Profile-Name.md`
