---
name: document-template-authoring
description: Create structured markdown document templates for software engineering projects — with YAML frontmatter, Mermaid diagrams, backlinks, and checklist management. Use when generating project document templates, BOK-based documentation, or template libraries.
trigger: User asks to create project document templates, engineering document templates, BOK-based templates, or template checklists.
---

# Document Template Authoring

## Template Structure

Every template follows this pattern:

```markdown
---
document_type: [Document Name]
version: "1.0"
status: Draft
author: "[Author Name]"
created: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
project_name: "[Project Name]"
project_id: "[Project-ID]"
classification: "Internal / Confidential"
tags: [tag1, tag2, standard-ref]
standard_ref:
  - Standard Name v1 — Section
---

# [Document Title]

> **Project:** [Project Name]
> **Version:** [X.Y] | **Status:** [Draft | Under Review | Approved]
> **Last Updated:** [YYYY-MM-DD]

---

## 1. Purpose
## 2-N. Content Sections (with tables, Mermaid diagrams)
## Related Documents (backlinks)
## Template Standard footer
```

## Backlink Pattern (CRITICAL)

Use **hyphens** in wikilinks, NEVER spaces:
- ✅ `[[Business-Case]]`
- ✅ `[[Risk-Assessment-Report-Security]]`
- ❌ `[[Business Case]]` ← BROKEN in Obsidian
- ❌ `[[Risk Assessment Report]]` ← BROKEN

Cross-folder backlinks use relative references or wikilinks (Obsidian resolves them).

## Mermaid Diagram Conventions

- **Edge labels with special characters MUST be quoted**: `|"label with ()/"|` not `|label with ()/|`
- Use `flowchart` (not `graph`) for flowcharts
- Use `erDiagram` for ER diagrams
- Use `stateDiagram-v2` for state diagrams
- Use `sequenceDiagram` for sequence diagrams
- Style nodes with color: `style NodeId fill:#color,color:#fff`
- Subgraphs for grouping: `subgraph Name["Label"]`

## Emoji Heat Map (not ASCII)

Use emoji tables for risk/impact matrices:
| Likelihood \ Impact | Low | Medium | High |
|-------------------|-----|--------|------|
| **High** | 🟡 | 🟠 | 🔴 |
| **Medium** | 🟢 | 🟡 | 🟠 |
| **Low** | 🟢 | 🟢 | 🟡 |

Legend: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

## Checklist Management

When creating templates in bulk:
1. Create section directory: `XX_Section_Name/`
2. Create templates with consistent naming: `Document-Name.md`
3. Update master checklist: change `☐` to `✅` for completed items
4. Use `patch` tool for checklist updates, not full rewrites

## Profile Checklists

For project-size-based checklists (Small/Medium/Large):
- Create under `XX_Project_Size/` directory
- Each entry has backlink + folder reference + status
- Documents without templates use `—` in Template column
- Include summary table with counts by priority

## Placeholder Convention

Use `[brackets]` for fill-in values:
- `[Project Name]`, `[YYYY-MM-DD]`, `[Author Name]`
- `[X.Y]` for versions
- `[X]` for counts/values

## Batch Creation Pattern

For creating N templates at once:
1. Create directory if needed
2. Write templates in batches of 3 (parallel writes)
3. Update checklist in one `patch` call after all templates done
4. Summarize with document count and section progress

## Common Pitfalls

- **Don't merge checklist sections** — keep section headers separate, don't add documents from one section into another
- **Verify checklist after edits** — use `grep` to confirm entries ended up in the right section
- **Count documents carefully** — match checklist range to actual documents created
- **Don't use `read_multiple_files`** — it doesn't exist in hermes_tools; use individual `read_file` calls
