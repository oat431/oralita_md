# Multi-Chapter Synthesis (Multiple Source Files → Single Note)

Use when the user wants to consolidate multiple book chapters into one cohesive study note, rather than one file per chapter.

## When to Use

- User says "combine chapters X-Y into a single note"
- Source files are pre-extracted `.txt` files (not raw PDFs)
- Output is a **synthesis** (integrated concepts) not a **summary** (per-chapter recap)
- Related chapters that form a natural unit (e.g., CLRS Ch33-35: Geometry + NP + Approximation)
- Target vault uses numbered file conventions (e.g., `06_Geometry_NP_and_Approximation.md`)

## Two Source File Patterns

### Pattern A: Separate Files (one .txt per chapter)
The standard case. Each chapter is its own `.txt` file. Use `read_file` on each in parallel.

### Pattern B: Single Combined File (all chapters in one .txt)
Some textbooks are distributed as a single combined `.txt` with stripped whitespace (no spaces between words — text appears as "ransmushed"). For these:

1. **Discover chapter boundaries** — use `search_files` with `output_mode: "content"` and pattern `^CHAPTER` to find line numbers for each chapter start
2. **Read in 600-line chunks** — the file may be 400K+ bytes and 6,000+ lines; start at the first chapter boundary and read forward
3. **Search for topic keywords** — within the combined file, search for domain terms (e.g., "Bell-LaPadula", "access control") to verify you're in the right section
4. **Check completeness** — the user may request chapters that don't exist in the source (e.g., Ch 11 when the file ends at Ch 10); report honestly

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

### Stripped-whitespace combined files need boundary scanning
Some combined `.txt` files have ALL spaces between words removed (text appears as "ransmushed"). Don't try to read the whole file at once — use `search_files` with pattern matching to find chapter start markers (e.g., `^CHAPTER`), then read in 600-line chunks from each boundary. Verify the source contains all requested chapters before synthesizing; the file may end earlier than expected (e.g., only Ch 5–10 when user asked for Ch 6–11).

### Non-CLRS format: Security engineering / software security vault
The `13_Software_Security/` vault uses a different format from both Algorithm_v2 and BOK-style vaults:
- **Frontmatter**: inline `tags: [security, access-control, mls]` (similar to Template D but no ISO references)
- **Top-level**: `# NN — Chapter Title` with number prefix matching vault convention
- **Structure**: conceptual synthesis across chapters using `## 1.`, `## 2.`, etc.; tables for comparisons; no pseudocode
- **Source attribution**: `source: "Anderson, Ross. Security Engineering, 3rd Edition. Chapters 6, 7, 9, 10."` in frontmatter
- **Sections**: each conceptual topic gets a numbered `##` section with `###` subsections; a `## Key Concepts Summary` with comparison tables at the end
- **Wikilinks**: use Obsidian `[[wikilinks]]` sparingly — only to existing vault topics

### Match existing file format, not the source format
The source `.txt` files are raw OCR output. The target `.md` must match the **vault's existing format** (found by reading an existing note in the same vault). The format reference file (`01_Amortized_Analysis.md`) defines the target, not the source files.

### Multi-chapter synthesis ≠ multi-chapter concatenation
Don't just put Ch33 content then Ch34 content then Ch35 content. Find the **connecting themes** (e.g., "exact geometry algorithms → NP-hardness barriers → approximation workarounds") and weave them into a coherent narrative. The "Big Picture" summary table at the end is critical for showing how the chapters relate.

### Wikilinks should reference files that exist (or will exist)
Check the vault's existing files before writing `[[wikilinks]]`. If the linked file doesn't exist yet, it's still OK (Obsidian shows it as unresolved) — but prefer linking to existing files when possible.

### Concatenated no-spaces source text needs different search patterns
Some `.txt` source files are raw text extractions with ALL spaces removed (e.g., "Chapter1 ■ WhatIsSecurityEngineering?"). Standard patterns like `^Chapter 1` or `grep "Chapter 1"` will find nothing. **Fix:** Use `search_files` with regex patterns that account for the missing spaces: `Chapter[1-9] ■` (with the actual Unicode ■ character) or `Chapter1[A-Z]`. Avoid `grep`/`terminal` for these files — `search_files` with `output_mode: "content"` handles Unicode more reliably.

### Chapters from one book may span multiple source files
The user's prompt may reference chapters that are distributed across different `.txt` files. Don't assume all chapters are in the file named after the topic. **Fix:** Before reading, run `search_files` with `pattern: "Chapter[1-9]|Chapter1[0-9]"` across the ENTIRE workspace directory (not just one file) to locate which chapters live in which files. Then batch-read from multiple files. In this session, Ch 8 (Economics) was in `sec-Access_Control_and_Architecture.txt`, not `sec-Security_Foundations.txt` with Ch 1–3.

## Non-CLRS Format

The synthesis pattern applies to ANY textbook, not just CLRS. Each textbook domain has its own format conventions — match the **vault's existing format**, not a generic template. See `references/software-quality-galin-run.md` for an SQA textbook example (tables, implementation tips, severity classifications, procedure structures — no pseudocode).

**Universal rules across all formats:**
- Read an existing note in the target directory FIRST to match YAML frontmatter style, heading conventions, wikilink format, and table conventions
- Use `search_files` with `pattern: "^chapter \d"` to discover actual chapter boundaries — the user's prompt may not match the source file structure
- When chapters are missing from the source, find cross-references and build summary-level sections; flag the limitation honestly
- Numbered file prefixes (`03_`, `06_`) must match the existing vault's numbering scheme

## Software Security Note Format

For the `13_Software_Security` vault, notes follow this pattern:

```markdown
---
tags:
  - security
  - threat-modeling
  - software-security
source: "Author, Book Title (Edition), Chapters X–Y"
created: YYYY-MM-DD
---

# NN Topic Name

> *"Key quote from the source."* — Author

---

## 1. First Major Section

| Col1 | Col2 | Col3 |
|------|------|------|
| ... | ... | ... |

> **Key insight:** Important takeaway in blockquote.

### 1.1 Subsection

\\```language
code example
\\```

---

## N. Key Principles for the Security Engineer

1. **Bold principle** — explanation
2. ...

---

## Sources

- Author, Book Title (Edition), Chapters X–Y
- Chapter X: Chapter Title (brief description)
```

### Format Conventions (Software Security vault)

- **YAML frontmatter:** Tags as inline list `tags: [tag1, tag2, tag3]` (NOT YAML list style). `source:` quoted string. `created:` date.
- **Heading hierarchy:** `##` for major topics, `###` for subtopics, `####` for deep subsections
- **Blockquotes:** Used heavily for key quotes (`> *"text"* — Author`) and insight callouts (`> **Key insight:** text`)
- **Tables:** Rich 3-5 column markdown tables. Bold column headers. Used for definitions, comparisons, and reference data.
- **Horizontal rules:** `---` between major sections (not between every subsection)
- **Sources section:** `## Sources` at the bottom (NOT `## See Also` or `## Related`). Lists each chapter with a brief description.
- **No emojis** in this vault (unlike BOK vaults which use 🔴🟡🟢). Use `**bold**` for emphasis, not emoji priority markers.
- **Code blocks:** Use with language tags when showing code, but most content is prose + tables.

## Proven On

- **CLRS Ch33-35 (Geometry + NP-Completeness + Approximation)** → `06_Geometry_NP_and_Approximation.md` (525 lines). Source: 3 pre-extracted `.txt` files (~2,600 + 825 + 825 lines). Format matched from `01_Amortized_Analysis.md`.
- **Security Engineering Ch 6–10 (Access Control + Distributed Systems + MLS + Boundaries)** → `03_Access_Control_and_Architecture.md` (627 lines, 23 KB). Source: single combined `.txt` file (6,787 lines, 439 KB, stripped whitespace). Five chapters synthesized into one note covering 4 conceptual sections. Format matched from `01_Cryptography.md` and `02_Authentication.md` in the same vault. Pattern B (single combined file) used for chapter discovery.
- **Anderson Security Engineering Ch 1–3, 8** → `01_Security_Fundamentals.md` (305 lines, 18.5 KB). Source: 2 pre-extracted `.txt` files (4,404 + 6,787 lines). Ch 8 was in a different file than Ch 1–3. Format matched from `01 Authentication Security.md`.
