# Methodology Synthesis (Multi-Source)

Use when the user wants methodology notes (Agile, Lean, Waterfall, etc.) but doesn't have a single canonical book. You synthesize from multiple sources: existing PDFs in the vault, domain knowledge, and cross-references from BOK chapters.

## When to Use

- User asks for "software methodology" notes
- No single authoritative PDF exists for the topic
- Multiple books in the vault touch on the methodology (e.g., clean-agile.pdf for Agile, BABOK for BA perspective, PMBOK for predictive approach)
- User wants a comparison/overview, not deep single-methodology coverage

## Structure

```
Software Methodology/
├── Software Methodology - Overview.md    ← Index, comparison table, Mermaid diagram, decision guide
├── 00_Agile_Methodology.md              ← From clean-agile.pdf (Scrum, XP, TDD, CI)
├── 01_Lean_Methodology.md               ← Synthesized from domain knowledge (7 principles, waste, Kaizen)
├── 02_Methodologies_Overview.md         ← Comparison matrix, decision guide, anti-patterns
├── 03_Kanban_and_Flow.md                ← From Kanban book concepts (WIP limits, Little's Law, CFD)
└── ...
```

## Source Strategy

| Source Type | How to Use |
|---|---|
| **PDF in vault** (e.g., clean-agile.pdf) | Extract key chapters with pdfplumber, summarize via sub-agents or direct synthesis |
| **BOK chapters** (e.g., BABOK Agile Perspective, PMBOK adaptive approach) | Cross-reference for methodology-specific content |
| **Domain knowledge** | Synthesize from well-known sources (Poppendieck for Lean, Anderson for Kanban, Royce for Waterfall) |
| **User's existing notes** | If the user has methodology notes elsewhere, link to them |

## File Format

Each methodology file follows the SWEBOK-style reference format:

```markdown
---
tags: [methodology-name, methodology, software-methodology]
---

# Methodology Name

> *Source: Book Title by Author (Year)*

## Purpose

## Core Principles/Values

## Practices (numbered list with descriptions)

## Comparison Table (vs other methodologies)

## Anti-Patterns

## Related

- [[00_Agile_Methodology]] — Related methodology
- [[02_Methodologies_Overview]] — Comparison
```

## Overview File Requirements

The `Software Methodology - Overview.md` must include:

1. **Summary table** — All methodologies with Focus, Cadence, Best For
2. **Mermaid diagram** — Showing methodology relationships (Lean → Agile, Lean → Kanban, etc.)
3. **Quick Decision Guide** — "If your situation is... consider... because..."
4. **Cross-links** — To Essential Documents and BOK vaults

## ISO Reference Retrofitting

When the user asks to add ISO/IEEE references to existing Essential Documents:

1. Read each document table
2. Research applicable standards for each document type
3. Add `| ISO/IEEE Reference |` column to every table
4. Add `### Key Standards Referenced` table at bottom
5. Use specific clause references when available (e.g., `ISO/IEC/IEEE 15288 (§6.4.2)`)

Standards mapping patterns:
- **Project Management:** ISO 21500/21502/21505, ISO 31000, ISO 10006/10007
- **Systems Engineering:** ISO/IEC/IEEE 15288, 42010, 29148, 12207
- **Software Engineering:** ISO/IEC/IEEE 29119, 14764, 32675, 20000-1
- **Safety:** IEC 61508, ISO 26262, IEC 62304
- **Security:** ISO/IEC 27001, IEC 60812/61025
- **Quality:** ISO 9001, ISO/IEC 25010

## Proven On

- **Software Methodology** — Synthesized from clean-agile.pdf + domain knowledge → 6 files (Agile, Lean, Kanban, Waterfall/V-Model, Overview, Comparison)
- **ISO retrofitting** — PMBOK and SEBOK Essential Documents had ISO/IEEE references added after initial creation

## Waterfall/V-Model File

Always include a dedicated `04_Waterfall_and_V-Model.md` file in the methodology vault. The user will notice if it's missing — Waterfall and V-Model are referenced in comparison tables but need their own file for completeness. Content: origin, phases, strengths/weaknesses, V-Model verification levels, documentation tables, hybrid approaches, anti-patterns, when to use. Link to it from [[02_Methodologies_Overview]] and the overview file.
