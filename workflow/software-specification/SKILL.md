---
name: software-specification
description: Spec-driven development workflow — requirements elicitation, SWEBOK-structured specs, template migration, spec validation against codebase.
tags: [specification, requirements, swebok, ba, grilling, template-migration]
---

# Software Specification

Spec-driven development: write requirements before code, validate specs against implementation.

## When to Use

- User wants to define requirements for a new project
- User has old specs that need restructuring into a standard template
- User wants to validate specs against actual codebase
- User mentions "spec-driven development" or "requirements first"

## Workflow

### Phase 1: Requirements Elicitation (Grilling)

Run structured interview rounds to extract requirements. Use `grill-me` skill methodology:

**Round 1 — Core Problem:**
- What does "done" look like? (3-5 core actions)
- Who is the user/persona?
- Why not existing solutions?
- What's the MVP line?

**Round 2 — Stress-Test Design:**
- Find contradictions in answers
- Challenge naming/semantics
- Identify gaps between vision and MVP

**Round 3 — Architecture:**
- API contract / interface design
- Data ownership / isolation
- Where it fits in existing stack
- Why this architecture vs alternatives

**Round 4 — Data Model:**
- Review for redundancy (can fields be derived/computed?)
- Naming consistency
- Enum vs string trade-offs

**Round 5 — API Contract:**
- Propose endpoints
- Pagination / filtering
- Response format
- Error handling

**Round 6 — Decisions:**
- Consolidate all decisions
- Set development order: spec → test → code

### Phase 2: Spec Document Creation

Create structured spec documents using SWEBOK template format:

```
project-specs/
├── 01_requirement/
│   ├── 011_business_objective.md    — SMART objectives
│   ├── 012_user_stories.md          — User stories with ACs
│   ├── 013_acceptance_criteria.md   — Given/When/Then format
│   └── 014_stakeholder_analysis.md  — Stakeholder matrix
├── 02_design/
│   ├── 021_architecture_decision_records.md  — ADRs
│   ├── 022_API_specification.md              — REST endpoints
│   ├── 023_database_schema_DDL.md            — PostgreSQL DDL
│   ├── 024_ERD.md                            — Mermaid ERD
│   └── 025_software_architecture_document.md — Architecture
├── 03_construction/
│   ├── 031_README_developer_guide.md    — Setup instructions
│   ├── 033_dependency_manifest.md       — Package versions
│   ├── 034_commit_messages_changelog.md — PR/commit log
│   └── 035_coding_standards_development.md — Code style
├── 04_testing/
│   ├── 041_test_plan.md     — Strategy + scope
│   └── 042_test_cases.md    — Test cases from ACs
├── 05_devops/
│   └── 053_release_notes.md — Release notes
└── 07_pm/
    ├── 071_risk_register.md      — Risk log
    └── 072_meeting_minutes.md    — Daily logs
```

**Key format rules:**
- YAML frontmatter with document_type, version, status, tags, standard_ref
- Tables for structured data (not prose)
- Wikilinks for cross-references
- Mermaid for diagrams (ERD, architecture, flowcharts)

### Phase 3: Template Migration

When user has old specs in non-standard format:

1. Read old specs to understand content
2. Read new template to understand structure
3. Map old content to new structure
4. Transform with proper frontmatter and formatting
5. Create placeholder sections for TODO items

**Mapping strategy:**
| Old Content | New Location |
|-------------|--------------|
| Project overview | 011_business_objective + 021_ADR |
| Data model | 023_database_schema_DDL + 024_ERD |
| API spec | 022_API_specification |
| Business logic | 013_acceptance_criteria |
| Daily logs | 072_meeting_minutes |

### Phase 4: Spec Validation

After implementation exists, validate specs against actual codebase:

1. Read GitHub repo structure (mcp__github__get_file_contents)
2. Check actual dependencies (go.mod, package.json)
3. Verify data model matches code structs
4. Confirm API endpoints match handler code
5. Update specs with actual versions and findings

**What to check:**
- Dependency versions (go.mod, package.json)
- Data model structs (model/*.go, types/*.ts)
- Handler implementations (handler/*.go, pages/*.tsx)
- Test coverage (test files)
- Configuration (ports, env vars)

## Pitfalls

- **Don't over-spec for MVP** — placeholder files are fine for future work
- **Don't assume tech stack** — read actual code before updating specs
- **Don't skip validation** — specs that don't match code are worse than no specs
- **Use tables, not prose** — structured data is easier to maintain and reference
- **Frontmatter matters** — consistent YAML enables tooling and filtering

## Related Skills

- `grill-me` — Requirements elicitation methodology
- `plan` — Planning mode for implementation
- `test-driven-development` — Test-first development
