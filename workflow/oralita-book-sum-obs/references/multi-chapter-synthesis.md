# Multi-Chapter Synthesis (Multiple Source Files → Single Note)

Use when the user wants to consolidate multiple book chapters into one cohesive study note, rather than one file per chapter.

## When to Use

- User says "combine chapters X-Y into a single note"
- Source files are pre-extracted `.txt` files (not raw PDFs)
- Output is a **synthesis** (integrated concepts) not a **summary** (per-chapter recap)
- Related chapters that form a natural unit (e.g., CLRS Ch33-35: Geometry + NP + Approximation)
- Target vault uses numbered file conventions (e.g., `06_Geometry_NP_and_Approximation.md`)

## Don't Use When

- Each chapter is self-contained → use `direct-book-synthesis.md` (one file per chapter)
- Book needs sub-agent parallel processing → use main pipeline (Phase 4)
- User wants separate files per topic → use Template A/B/C/D

## Structure

```
vault-path/
├── 01_Topic.md          ← previously created, single-chapter note
├── ...
└── NN_Multi_Topic.md    ← this pattern: N chapters → 1 file
```

## Synthesis Workflow

1. **Read a reference file first** — find an existing `.md` in the target vault to match format (YAML frontmatter style, heading conventions, table formats, wikilink patterns)
2. **Read ALL source files** — batch `read_file` calls for all `.txt` sources in parallel
3. **Map chapter boundaries** — identify where each chapter's content starts/ends in the source files; source files may contain content from adjacent chapters (OCR bleed)
4. **Synthesize, don't concatenate** — integrate related concepts across chapters; use cross-references within the note (e.g., "as shown in §33.1" or "the reduction chain in §34.4")
5. **Match the vault's existing format exactly** — YAML frontmatter fields, tag style, heading hierarchy, table column conventions, wikilink format

## CLRS Algorithm Study Note Format

For the `Algorithm_v2` vault, notes follow this pattern:

```markdown
---
title: "Topic Name"
tags:
  - tag1
  - tag2
  - clrs
  - algorithms
source: CLRS Chapters XX–YY
---

# Topic Name

> One-paragraph overview connecting the chapters.

---

## Chapter XX — Section Title

### XX.1 Subsection

Explanation with **bold** for key terms.

#### Algorithm Name — Time Complexity

**Idea:** One-line description.

\```
PSEUDOCODE(INPUT):
    step 1
    step 2
\```

#### Key Theorem (Theorem XX.N)

Statement with $math$ notation.

**Proof sketch:** Brief argument.

### XX.2 Next Subsection

...

---

## Summary Table

| Category | Problem | Algorithm | Time | Quality |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

---

## Key Takeaways

1. **Bold insight** — explanation
2. ...

---

## See Also

- [[Related_Note]] — why it's related
```

### Format Conventions (Algorithm_v2 vault)

- **YAML frontmatter:** `tags` as YAML list (not inline), `source:` field references CLRS chapters
- **Section hierarchy:** `##` for chapters, `###` for chapter sections, `####` for algorithms/theorems
- **Pseudocode:** Indented code blocks with algorithm name as header, using CLRS-style variable names
- **Math:** LaTeX inline `$...$` and display `$$...$$`
- **Tables:** Summary/comparison tables at end of major sections
- **Cross-references:** `[[filename]]` wikilinks (hyphens in names for Obsidian compat)
- **No emojis** in the Algorithm_v2 vault (unlike BOK vaults)

## Pitfalls

### OCR'd source files need cleaning
CLRS `.txt` files are OCR'd PDFs with garbled characters: `‚` for `,`, `¤` for `≠`, `f g` for `{ }`, `D` for `=`, `j j` for `| |`. Focus on extracting the **semantic content** rather than trying to faithfully reproduce the garbled text. Reconstruct formulas from context.

### Source files may contain adjacent chapter content
The `clrs-chApproximation_Algorithms.txt` file contained NP-Completeness content (Ch34), not Ch35. Always check file boundaries — the OCR extraction may have captured pages from neighboring chapters. Use `grep` to find the actual chapter boundaries.

### Match existing file format, not the source format
The source `.txt` files are raw OCR output. The target `.md` must match the **vault's existing format** (found by reading an existing note in the same vault). The format reference file (`01_Amortized_Analysis.md`) defines the target, not the source files.

### Multi-chapter synthesis ≠ multi-chapter concatenation
Don't just put Ch33 content then Ch34 content then Ch35 content. Find the **connecting themes** (e.g., "exact geometry algorithms → NP-hardness barriers → approximation workarounds") and weave them into a coherent narrative. The "Big Picture" summary table at the end is critical for showing how the chapters relate.

### Wikilinks should reference files that exist (or will exist)
Check the vault's existing files before writing `[[wikilinks]]`. If the linked file doesn't exist yet, it's still OK (Obsidian shows it as unresolved) — but prefer linking to existing files when possible.

## Proven On

- **CLRS Ch33-35 (Geometry + NP-Completeness + Approximation)** → `06_Geometry_NP_and_Approximation.md` (525 lines). Source: 3 pre-extracted `.txt` files (~2,600 + 825 + 825 lines). Format matched from `01_Amortized_Analysis.md`.
