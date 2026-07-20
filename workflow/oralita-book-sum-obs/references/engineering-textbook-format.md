# Engineering Textbook → Obsidian Vault Format

Format conventions for converting Engineering Fundamentals textbook chapters into the `engineering-foundation-note` Obsidian vault.

## Vault Path

`F:\obsidian_note\swe-knowledge\engineering-foundation-note\`

## Source Files

Located at `C:\Users\Admin\.openclaw\workspace\engineering-chapters\` — pre-extracted `.txt` files from the Engineering Fundamentals textbook. Naming pattern: `eng-chTopic_and_Related_Parameters.txt`.

**Key quirk:** Each `.txt` file often contains content from the *previous* chapter at the top (OCR/page-boundary bleed). The target chapter doesn't start at line 1. Use `search_files` with the chapter heading pattern (e.g., `Chapter 11|11\.\d`) to find the actual start line, then read from there with `read_file(offset=N)`.

## File Naming

Sequential numbered prefix: `01_Fundamental_Dimensions.md`, `02_Length_and_Related_Parameters.md`, etc. The number indicates the reading/chapter order.

## YAML Frontmatter

```yaml
---
title: "Chapter Topic Name"
tags:
  - topic-tag1
  - topic-tag2
  - engineering
source: "Engineering Fundamentals Ch NN"
---
```

- Tags use YAML list format (not inline)
- Always include `engineering` as a tag
- `source` field uses the format: `"Engineering Fundamentals Ch NN"`

## Section Hierarchy

```
# Chapter Topic Name
## Major Section (e.g., "Temperature Scales")
### Subsection (e.g., "Kelvin (K) — SI Absolute Scale")
```

## Content Conventions

### Tables preferred over walls of text
- Use markdown tables for: conversion factors, material properties, comparison data, relationships
- Example: thermal conductivity table, heat transfer coefficient ranges

### Formulas
- Use `$$...$$` for display math (LaTeX notation)
- List variables with bullet points below each equation
- Keep equation numbers from the textbook in parentheses for reference

### Key Insight blockquotes
- Use `> **Key Insight:**` for the core conceptual takeaway of each major section

### Comparison tables
- Use tables for before/after, SI/US Customary, or concept comparisons
- Example: Celsius vs Fahrenheit vs Kelvin vs Rankine

### Quick Reference section at the end
- End each note with a `## Key Formulas Summary` table (formula name | equation | description)
- Add a `## Quick Reference Conversions` table for unit conversions

### Section separators
- Use `---` between major sections

## Example Structure

```markdown
---
title: "Temperature and Thermal Parameters"
tags:
  - temperature
  - heat-transfer
  - thermal
  - engineering
source: "Engineering Fundamentals Ch 11"
---

# Temperature and Thermal Parameters

## Temperature as a Fundamental Dimension

Brief intro paragraph.

> **Key Insight:** Core concept in blockquote.

### Why It Matters in Engineering

| Discipline | Application |
|---|---|
| ... | ... |

---

## Key Formulas Summary

| Formula | Equation | Description |
|---|---|---|
| ... | ... | ... |

---

## Quick Reference Conversions

| From → To | Formula |
|---|---|
| ... | ... |
```

## Pitfalls

### Source file has mixed chapter content
The `.txt` files may start with the previous chapter's content. Always search for the target chapter heading before reading. The file `eng-chTemperature_and_Related_Parameters.txt` started with Chapter 10 (Force) content — Chapter 11 didn't begin until line 848.

### Equation formatting from OCR
The source text uses `(cid:2)` and `(cid:3)` placeholders for special characters (≈, ≥, ×, etc.). Replace these with proper LaTeX or Unicode equivalents when writing the note.

### Table data may need manual extraction
OCR'd table data can be garbled or split across lines. Reconstruct tables from context, cleaning up spacing and alignment.

### Match existing vault format, not textbook format
The textbook uses numbered equations (11.1, 11.2, etc.) and inline variable definitions. The Obsidian notes use LaTeX display math with bullet-point variable lists. Convert between formats.

### Sub-agents skip wikilinks
Engineering textbook sub-agents consistently produce files with ZERO `[[wikilinks]]` because they focus on formulas and tables. After sub-agents complete, verify every file has at least one `[[` link. For files missing links, append a `## Related` section using `execute_code` with file append. This is faster than patching each file individually.

## Proven On

- **Ch 11 Temperature and Temperature-Related Parameters** → `04_Temperature_and_Thermal.md` (363 lines, 10.5 KB). Source: `eng-chTemperature_and_Related_Parameters.txt` (1794 lines, 103 KB). Chapter content started at line 848.
- **Full Engineering Fundamentals (720pp)** → 10 files, 91 KB. 13 chapters extracted, 9 summarized (skipped intro/tool chapters). Mixed-chapter content affected 6 of 13 source files. Sub-agents produced 7 files missing wikilinks — all fixed with manual Related section appends.
