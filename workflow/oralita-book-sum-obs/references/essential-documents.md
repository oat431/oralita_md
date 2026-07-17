# Essential Documents Extraction

Post-summarization workflow for extracting "documents you need to produce" checklists from completed BOK vaults.

## When to Use

- User asks for a practical document checklist from a completed BOK vault
- User references the SWEBOK `Software Engineering Note Content.md` format
- User says "copy only the document part" or "create an essential documents file"
- A friend needs a quick reference without the full theory

## Format

Each Essential Document file follows this structure:

```markdown
---
tags: [overview, domain, standard, essential-documents]
---

# STANDARD — Essential Documents by Phase

> **Source:** [[Overview|Full Standard Name (Org, Year)]]
> Organized by life cycle phases
>
> ⚠️ **This is a document-only extract.** For the full body of knowledge, see:
> `path\to\full\vault\`

**Priority Legend:**

| Icon | Level | Meaning |
|---|---|---|
| 🔴 | **Must Have** | Essential for virtually all projects |
| 🟡 | **Nice to Have** | Recommended for medium+ complexity |
| 🟢 | **Optional** | Situational |

---

## 1. Phase Name

| Document | Description | Priority | ISO/IEEE Reference |
|---|---|---|---|
| **Document Name** | What it is and why | 🔴 Must Have | ISO XXXXX |

... (repeat for all phases)

---

### Key Standards Referenced

| Standard | Title |
|---|---|
| ISO XXXXX | Full title |

---

## Related

- Links back to original vault overview
- Links to other Essential Documents
```

## Key Columns

Each document table MUST have these columns:

1. **Document** — Bold name, with abbreviation if commonly used (e.g., **BRD** (Business Requirements Document))
2. **Description** — One-line description of what it is
3. **Priority** — 🔴 Must Have / 🟡 Nice to Have / 🟢 Optional
4. **ISO/IEEE Reference** — The applicable standard. Use `—` if no standard applies. Prefer specific clause references when available (e.g., `ISO/IEC/IEEE 15288 (§6.4.2)`)

## Owner Blockquotes

Every phase section MUST have an owner blockquote directly under the `## N. Phase Name` header:

```markdown
## 1. Research Phase
> **Owner:** UX Researcher / Product Manager

| Document | Description | Priority | ISO/IEEE Reference |
...
```

This tells the reader who is responsible for producing the documents in that phase. Use the most common role for that discipline (e.g., BA/PO for requirements, Architect for design, QA for testing, UX Researcher for user research). When multiple roles share responsibility, list them separated by `/`.

## Link-Back Strategy

Every Essential Document must clearly link back to the full BOK so readers don't wonder "where's the rest?":

1. **Source line** at top: `> **Source:** [[Overview|Full Name]]`
2. **⚠️ Banner**: Explains this is document-only, with path to full vault
3. **Related section**: Links to the full BOK overview + companion Essential Documents

## Standards Reference Table

At the bottom, include a `### Key Standards Referenced` table listing every standard cited in the document tables. This gives readers a one-glance view of all applicable standards.

## Overview File

When a folder has multiple Essential Documents, create an `Essential Documents - Overview.md` with:
- Purpose of the folder
- Links to all documents
- Quick comparison table across disciplines
- "Which checklist do I need?" guidance

## ISO Reference Retrofitting

When the user asks to add ISO/IEEE references to existing Essential Documents that were created without them:

1. Read each document table to identify all document types
2. Research applicable standards for each document (use domain knowledge + BOK source text)
3. Add `| ISO/IEEE Reference |` column to every table row
4. Use `—` when no specific standard applies
5. Add `### Key Standards Referenced` table at the bottom listing every standard cited
6. Use specific clause references when available (e.g., `ISO/IEC/IEEE 15288 (§6.4.2)`)

This is a post-creation enhancement — the Essential Documents were already valid, but adding ISO references makes them more useful for compliance and audit contexts.

## Proven On

- SWEBOK v4 → 7 SDLC phases, ~100 documents, 33 standards
- PMBOK v8 → 5 Focus Areas, ~60 documents, 12 standards (ISO references added post-creation)
- SEBoK v2 → 6 SE phases, ~60 documents, 22 standards (ISO references added post-creation)
- BABOK v3 → 6 Knowledge Areas, ~50 documents, 8 standards
- CyBOK v1.1 → 5 security domains, ~40 documents, 6 standards
- DMBOK v2 → 11 Knowledge Areas, ~55 documents, 5 standards
- **UX/UI Design** → 5 design phases (Research, UX, UI, Testing, Handoff), ~40 documents, HCI standards — created from domain knowledge (no dedicated BOK PDF), integrated into Essential Document folder as 7th discipline
