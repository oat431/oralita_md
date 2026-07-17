---
name: md-project-document-templates
description: Create markdown (.md) project document templates from Body of Knowledge (BOK) standards. Covers BABOK, PMBOK, SWEBOK, SEBOK, CyBOK, DMBOK, UX/UI. Use when building structured project documentation in markdown instead of docx/xlsx.
triggers:
  - project document template
  - markdown template
  - BOK document
  - business case template
  - SRS template
  - project charter template
  - essential documents
---

# Markdown Project Document Templates

## When to Use

When the user asks to create project document templates in `.md` format — business cases, requirements specs, architecture docs, test plans, etc. — sourced from Body of Knowledge standards.

## Workflow

### 1. Understand the Source

- Identify which BOK(s) the document belongs to (BABOK, PMBOK, SWEBOK, SEBOK, CyBOK, DMBOK, UX/UI)
- Check if a checklist exists (e.g., `TEMPLATE-CHECKLIST.md`) — read it to understand context and dependencies
- Read the BOK source file for the specific document's definition, priority, and ISO/IEEE references

### 2. Research (if needed)

- Web search for best-practice structures, industry templates, standard sections
- Cross-reference multiple BOKs — many documents appear in several (e.g., Risk Register in PMBOK + SEBOK)
- Note which BOKs define the document for traceability

### 3. Template Structure

Every template MUST include:

**YAML Frontmatter:**
```yaml
---
document_type: [Name]
version: "1.0"
status: Draft
author: "[Author Name]"
created: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
project_name: "[Project Name]"
project_id: "[Project-ID]"
classification: "Internal / Confidential"
tags: [relevant, tags]
standard_ref:
  - BABOK v3 — [Section]
  - ISO/IEC/IEEE XXXXX — [Title]
---
```

**Document Control Block:**
- Revision History table (Version, Date, Author, Change Description)
- Approvals table (Role, Name, Signature, Date)

**Table of Contents:**
- Linked section headers

**Body Sections:**
- Use tables as primary layout for structured data
- Use `[placeholder brackets]` for all fill-in values
- Include emoji priority indicators (🔴 Must Have, 🟡 Nice to Have, 🟢 Optional)
- Add `> blockquote` guidance notes where users need context

**Related Documents:**
- `[[Hyphenated-Name]]` cross-references to related templates (NEVER spaces — `[[Business-Case]]` not `[[Business Case]]`)

**Footer:**
- Template Standard reference (BOK + ISO/IEEE)
- Usage guidance

### 4. Diagram Rules (CRITICAL)

**ALWAYS use Mermaid for:**
- Flowcharts, process flows, decision trees
- Dependency diagrams, architecture diagrams
- Gantt charts, timelines
- Journey maps, quadrant charts, mind maps
- Org charts

**ALWAYS use emoji tables for:**
- Risk heat maps (not ASCII art)
- Priority matrices
- Status dashboards
- Any grid/matrix visualization

**NEVER use ASCII art for any visualization.** User explicitly rejected ASCII in favor of Mermaid and emoji tables.

**Mermaid styling:** Add `style` directives with colors for visual distinction. Use hex colors with `color:#fff` for text.

**Emoji heat map format:**
```markdown
| Impact \ Probability | Low | Medium | High |
|---------------------|-----|--------|------|
| **High** | 🟡 | 🟠 | 🔴 |
| **Medium** | 🟢 | 🟡 | 🟠 |
| **Low** | 🟢 | 🟢 | 🟡 |

> **Legend:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
```

### 5. Checklist Management

After creating a template, update the master checklist:
- Change `☐` to `✅` for the completed document
- Use `patch` tool for surgical updates

### 6. Batching

- Default: create 3 templates per batch for user review
- User reviews before moving to next batch
- Wait for user confirmation before proceeding

## Common Template Patterns

### Plans (Quality Plan, Risk Plan, etc.)
Sections: Objectives → Scope → Roles/Responsibilities → Processes → Tools → Metrics → Review Cadence

### Reports (Test Report, Audit Report, etc.)
Sections: Executive Summary → Scope → Methodology → Findings → Analysis → Recommendations → Appendices

### Specifications (SRS, API Spec, etc.)
Sections: Overview → Requirements (Functional/Non-Functional) → Constraints → Assumptions → Acceptance Criteria → Traceability

### Registers (Risk Register, Issue Register, etc.)
Sections: Purpose → Classification Scheme → Register Table → Summary/Dashboard → Review Process

### Strategies (Change Strategy, Security Strategy, etc.)
Sections: Context → Current State → Options Analysis → Recommendation → Implementation Plan → Governance

## Pitfalls

1. **Broken wikilinks** — Always use hyphens in wikilinks, never spaces. `[[Business-Case]]` not `[[Business Case]]`. Space-separated wikilinks break in Obsidian.
2. **Don't mix business and technical levels** — Business Requirements describe *what*, SRS describes *how*
3. **Don't skip the Executive Summary** — busy stakeholders read only this
4. **Don't forget traceability** — every document should link to related docs via `[[Hyphenated-Name]]` wikilinks
5. **Don't use vendor-specific language** — templates should be vendor-neutral
6. **Don't omit the "Related Documents" section** — cross-references are critical for the knowledge graph
7. **Mermaid edge labels with special characters** — Quote labels containing `()`, `/`, `:`, `,`. Example: `A -->|"1: submit()"| B`
8. **Duplicate checklist entries** — Check for duplicate item numbers after each batch update

## Reference Files

- `references/diagram-patterns.md` — Mermaid and emoji diagram patterns with color conventions
- `references/template-skeleton.md` — Copy-paste YAML frontmatter, document control block, section patterns by doc type
- `references/bok-document-mapping.md` — Which documents come from which BOKs, cross-BOK duplicates
