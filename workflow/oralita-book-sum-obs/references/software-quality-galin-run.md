# Software Quality (Galin) — Multi-Chapter Synthesis

## Run Summary

- **Source:** `sqa-Reviews_and_Infrastructure.txt` (7,156 lines, 384 KB) — pre-extracted OCR text from Galin's SQA textbook
- **Chapters:** 8 (Reviews) + 14 (Procedures) + 15–19 (Infrastructure — from cross-references only)
- **Output:** `03_Reviews_and_Infrastructure.md` (588 lines, 27 KB) in `12_Software_Quality/`
- **Target vault:** `F:\obsidian_note\swe-knowledge\software-engineering-note\12_Software_Quality\`

## Workflow

### 1. Discover file structure

The source file contained chapters 8–14 (not just 8 + 14–19 as the user's prompt suggested). Chapters 15–19 are NOT present in the file.

**Technique:** Use `search_files` with `pattern: "^chapter \d"` to find every chapter boundary. This revealed chapters 8, 9, 10, 11, 12, 13, 14 all in one file.

### 2. Find cross-references for missing chapters

Chapters 15–19 were missing, but the file contained rich cross-references:
- Section 11.4.3: "SQA infrastructure components" lists all six components matching Ch 14–19
- Chapter 8 references checklists (→ Ch 15), corrective actions (→ Ch 17)
- Chapter 14 itself covers procedures and work instructions

**Technique:** Use `search_files` with topical keywords (`template`, `checklist`, `training`, `certification`, `corrective action`, `CAPA`, `configuration management`, `documentation control`) to find all references across the file.

### 3. Read relevant chapters in parallel

Use `read_file` with offsets to read Chapter 8 (lines 106–1255, ~1,150 lines) and Chapter 14 (lines 6876–7156, ~280 lines) plus Section 11.4.3 (lines 5062–5211, ~150 lines for infrastructure overview).

### 4. Match existing vault format

Read an existing note in the target directory to match conventions:
- **YAML frontmatter:** Inline tags (`tags: [a, b, c]`), `quality:`, `source:`, `created:` fields
- **Heading convention:** Numbered prefix (`03_`)
- **Wikilink format:** `[[filename|display]]` in a `## Related` section
- **Table conventions:** 4-column comparison tables, priority tables

## Output Structure

```markdown
---
quality: review
reviews: inspection
...
tags: [software-quality, reviews, inspections, ...]
---

# 03 — Reviews & SQA Infrastructure

> Source blockquote

## 1. Review Objectives (Ch 8.1)
## 2. Formal Design Reviews (Ch 8.2)
## 3. Peer Reviews (Ch 8.3)
## 4. Comparison of Team Review Methods (Ch 8.4)
## 5. Expert Opinions (Ch 8.5)
## 6. Procedures and Work Instructions (Ch 14)
## 7. Supporting Quality Devices (Ch 15) — from cross-refs
## 8. Staff Training and Certification (Ch 16) — from cross-refs
## 9. Corrective and Preventive Actions (Ch 17) — from cross-refs
## 10. Configuration Management (Ch 18) — from cross-refs
## 11. Documentation and Quality Records Control (Ch 19) — from cross-refs
## 12. Summary: The SQA Infrastructure Framework (Mermaid diagram)
## Related (wikilinks to other vault notes)
```

## Key Techniques Used

### Handling missing source chapters

When chapters aren't in the source file but are referenced:
1. Find the "infrastructure components overview" section (11.4.3) that lists all six components
2. Search for topical cross-references scattered through available chapters
3. Build summary-level sections from cross-references, clearly noting the limitation
4. Do NOT fabricate content — transparently flag what's derived from cross-references vs. direct source

### Table-heavy content formatting

SQA textbooks are dense with comparison tables, checklists, and severity classifications. Format them as markdown tables with:
- Bold key terms in the first column
- Concise descriptions (one sentence where possible)
- Severity scales as separate tables with numeric + descriptive columns

### Implementation tips and anti-patterns

Galin's text includes "Implementation tip" boxes and anti-pattern warnings. Format these as:
- `> ⚠️ **Anti-pattern:**` blockquotes for warnings
- `> **Tip:**` blockquotes for advice
- Regular tables for structured comparisons

## Comparison with CLRS Format

| Aspect | CLRS Algorithm Notes | Galin SQA Notes |
|--------|---------------------|-----------------|
| Content type | Pseudocode, theorems, proofs | Tables, procedures, checklists, severity scales |
| YAML tags | YAML list | Inline `[a, b, c]` |
| Source field | `source: CLRS Chapters XX–YY` | `source: "Galin SQA Ch X, Y–Z"` |
| Section references | `§XX.Y` notation | `(→ Ch XX)` notation |
| Key takeaways | Bold insights list | Summary framework diagram (Mermaid) |
| Code blocks | Pseudocode with CLRS variables | No code blocks (procedure structure instead) |

## Pitfalls

1. **Source file structure doesn't match user's prompt** — user said "Ch 8, 14–19" but file contained Ch 8–14. Always verify actual chapter boundaries before assuming the prompt is exact.
2. **Missing chapters need honest handling** — don't fabricate content for chapters that aren't in the source. Use cross-references and clearly flag what's summary-level vs. direct.
3. **OCR text has concatenated words** — `"productfeatures"`, `"developmentprocess"`, `"Proceduresand"` — read for meaning, not literal fidelity.
4. **Numbered prefixes in filenames matter** — match the existing vault's numbering scheme (`03_` in this case) rather than inventing a new one.
