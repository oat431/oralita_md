# Template Skeleton — Copy & Customize

## YAML Frontmatter

```yaml
---
document_type: [Document Name]
version: "1.0"
status: Draft
author: "[Author Name]"
created: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
project_name: "[Project Name]"
project_id: "[Project-ID]"
sponsor: "[Sponsor Name]"
ba_owner: "[Business Analyst Name]"
classification: "Internal / Confidential"
tags: [tag1, tag2, tag3]
standard_ref:
  - BABOK v3 — [Section Name]
  - PMBOK v8 — [Focus Area]
  - ISO/IEC/IEEE XXXXX — [Title]
---
```

## Document Control Block

```markdown
## Document Control

| Field | Value |
|-------|-------|
| Document Owner | [Name / Role] |
| Sponsor | [Name / Role] |
| Business Analyst | [Name / Role] |

### Revision History

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |
| 1.0 | [YYYY-MM-DD] | [Name] | Approved version |

### Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | | | |
| Business Owner | | | |
| BA Lead | | | |
```

## Standard Sections by Document Type

### Plan Documents
1. Executive Summary
2. Objectives & Scope
3. Roles & Responsibilities
4. Processes / Activities
5. Tools & Resources
6. Metrics & KPIs
7. Review Cadence
8. Appendices

### Report Documents
1. Executive Summary
2. Scope & Methodology
3. Findings
4. Analysis
5. Recommendations
6. Appendices

### Specification Documents
1. Executive Summary
2. Overview / Context
3. Requirements (Functional)
4. Requirements (Non-Functional)
5. Constraints & Assumptions
6. Acceptance Criteria
7. Traceability Matrix
8. Appendices

### Register Documents
1. Purpose & Scope
2. Classification Scheme
3. Register (main table)
4. Summary Dashboard
5. Review Process

### Strategy Documents
1. Executive Summary
2. Context / Drivers
3. Current State
4. Options Analysis
5. Recommended Approach
6. Implementation Plan
7. Risk & Mitigation
8. Governance

## Placeholder Convention

- All fill-in values: `[brackets]`
- Dates: `[YYYY-MM-DD]`
- Names: `[Name / Role]`
- Money: `$[X]`
- Percentages: `[X%]`
- Repeatable sections: "> **Repeat this section for each [item]**"

## Related Documents Block

```markdown
## Related Documents

| Document | Relationship |
|----------|-------------|
| [[Document Name]] | [How it relates] |
```
