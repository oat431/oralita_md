# PDF-to-Vault Summarization Workflow

> *How to turn any PDF book into a topic-separated Obsidian knowledge base using Hermes sub-agents. Driven by the `oralita-book-sum-obs` skill.*

---

## Prerequisites

- PDF file accessible from the shell (any drive)
- Hermes with `delegate_task` tool enabled
- LLM credits (DeepSeek or similar) — ~300K–500K input tokens for a 500-page book
- Python *outside* Hermes venv with `pdfplumber` installed:
  ```bash
  # Use system Python 3.12, NOT the Hermes-bundled Python 3.11
  "C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" -m pip install pdfplumber
  ```
- Obsidian vault with a target directory for output files

---

## The 5-Phase Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  PHASE 1: STRUCTURE EXTRACTION                   │
│         Extract TOC → Identify chapter page ranges               │
├─────────────────────────────────────────────────────────────────┤
│                  PHASE 2: TOPIC MAPPING                          │
│    Human reviews TOC → Maps topics to chapters/files             │
├─────────────────────────────────────────────────────────────────┤
│                  PHASE 3: TEXT EXTRACTION                        │
│    3a: Find exact PDF boundaries → 3b: Map printed page #s      │
│    3c: Extract per-chapter .txt files with printed page ranges   │
├─────────────────────────────────────────────────────────────────┤
│                  PHASE 4: PARALLEL SUB-AGENTS                    │
│     Spawn batches of 3 → Each summarizes one chapter             │
│     Uses 3 templates: A (rules), B (case study), C (catalog)     │
├─────────────────────────────────────────────────────────────────┤
│                PHASE 4.5: CONSISTENCY GATE                       │
│     Normalize source headers → Fix page ranges → Broken links    │
├─────────────────────────────────────────────────────────────────┤
│                  PHASE 5: OVERVIEW & POLISH                      │
│     Write Overview.md → Broken link scan → Spot-check 3 files    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Structure Extraction

**Goal:** Get the table of contents and identify approximate chapter boundaries.

**Script — scan first ~30 pages for TOC:**
```python
import pdfplumber

pdf = pdfplumber.open(r'F:\books\your-book.pdf')

for i in range(min(30, len(pdf.pages))):
    page = pdf.pages[i]
    text = page.extract_text()
    if text:
        print(f'--- PDF PAGE {i+1} ---')
        print(text[:2000])
        print()

pdf.close()
```

**Completion criterion:** You have a list of chapter titles and their approximate PDF page boundaries (e.g., "Ch3 Functions starts around PDF p47").

---

## Phase 2: Topic Mapping (Human Decision)

**Goal:** Decide what `.md` files to produce and which chapters map to which topics.

**Decision rules:**

| Chapter type | Map to… | Example |
|---|---|---|
| Self-contained rules chapter | One `.md` file | Ch3 Functions → `Function Design.md` |
| Multiple chapters form one topic | Merge into one file | — |
| Case study / walkthrough | `Case Study/` subfolder, "Case Study - " prefix | Ch14 → `Case Study/Case Study - Args Parser.md` |
| Reference catalog | Catalog format, no ❌/✅ examples needed | Ch17 → `Code Smells Catalog.md` |

**Output — a mapping table:**
```
Ch 1: Clean Code              → Clean Code Principles.md
Ch 2: Meaningful Names        → Naming Conventions.md
Ch 3: Functions               → Function Design.md
...
Ch14: Args Parser             → Case Study/Case Study - Args Parser.md
Ch17: Smells & Heuristics     → Code Smells Catalog.md
```

---

## Phase 3: Text Extraction

### Step 3a — Find exact PDF page boundaries

```python
import pdfplumber, re

pdf = pdfplumber.open(r'F:\books\your-book.pdf')

for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text:
        lines = text.strip().split('\n')
        first_line = lines[0].strip()
        if re.match(r'^\d{1,2}$', first_line):
            print(f'PDF p{i+1}: Chapter {first_line}  {lines[1].strip() if len(lines) > 1 else ""}')

pdf.close()
```

### Step 3b — Map PDF page indices to printed page numbers

Identify the offset: find where printed page 1 begins (usually after TOC/preface). Create a mapping:
```
PDF p31 → printed p1  (Chapter 1 starts)
PDF p47 → printed p17 (Chapter 2 starts)
...
```

Feed this to sub-agents so page ranges in source headers are accurate.

### Step 3c — Extract each chapter range to a .txt file

```python
import pdfplumber, os

pdf = pdfplumber.open(r'F:\books\your-book.pdf')
out_dir = r'C:\Users\Admin\.openclaw\workspace\book-chapters'
os.makedirs(out_dir, exist_ok=True)

chapters = [
    # (pdf_start_idx, pdf_end_idx, chapter_num, 'Chapter-Name', printed_start, printed_end)
    (31, 47, 1, 'Clean-Code', 1, 15),
    (47, 61, 2, 'Meaningful-Names', 17, 30),
    # ... add all chapters
]

for start_idx, end_idx, num, name, p_start, p_end in chapters:
    filename = os.path.join(out_dir, f'ch{num:02d}-{name}.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(start_idx, end_idx):
            text = pdf.pages[i].extract_text()
            if text:
                f.write(text + '\n')
    print(f'ch{num:02d} {name}: {os.path.getsize(filename)} chars  (printed pp. {p_start}–{p_end})')

pdf.close()
```

**You'll get something like:**
```
ch01 Clean-Code : 15000 chars (~3750 tokens)  (printed pp. 1–15)
ch02 Meaningful-Names : 12000 chars (~3000 tokens)  (printed pp. 17–30)
...
```

---

## Phase 4: Parallel Sub-Agent Summarization

**Goal:** Spawn one sub-agent per topic/chapter. They all run simultaneously in batches.

### Sub-agent prompt templates — pick the right one per chapter

**Template A — Rules/practices chapter** (standard style guide):
```
Read: C:\Users\Admin\.openclaw\workspace\book-chapters\ch03-Functions.txt
     — Chapter 3 of "Book Title" by Author Name (printed pp. 31–52).

Write to: F:\projects\orlita_md\vault-path\Topic\Function Design.md

Style:
- Start with: > *Source: Book Title by Author, Chapter X (pp. Y–Z)*
- Core principle quote at top in blockquote
- Rules organized under ### headings with bold names
- Before/after code examples using ``` blocks with ❌ // Bad and ✅ // Good labels
- Summary checklist with checkboxes at the bottom
- ## Related section with  to related topics in the vault
- Professional, direct tone. No fluff. Actionable.

Topics covered in this chapter: [list key sections from TOC]
```

**Template B — Case study chapter** (step-by-step refactoring walkthrough):
```
Read: C:\Users\Admin\.openclaw\workspace\book-chapters\ch14-Args-Parser.txt
     — Chapter 14 of "Book Title" by Author Name.

Write to: F:\projects\orlita_md\vault-path\Case Study\Case Study - Args Parser.md

Style:
- Start with: > *Source: Book Title by Author, Chapter X (pp. Y–Z)*
- Lead with the final clean code first (what we're building toward)
- Then walk through: rough draft → how it got messy → step-by-step refactoring phases
- Each refactoring phase gets a ### heading, shows code before/after, ends with a **Heuristic:** takeaway
- ## Summary section with key heuristics bullet list
- ## Related section with 
- Preserve the narrative — this is a story of successive refinement, not a rulebook
```

**Template C — Reference catalog chapter** (categorized listing):
```
Read: C:\Users\Admin\.openclaw\workspace\book-chapters\ch17-Smells-Heuristics.txt
     — Chapter 17 of "Book Title" by Author Name.

Write to: F:\projects\orlita_md\vault-path\Code Smells Catalog.md

Style:
- Start with: > *Source: Book Title by Author, Chapter X (pp. Y–Z)*
- Categorize all items under ## category headings
- Each item: #### **Code** — **Name** followed by explanation paragraph
- Include cross-references to related vault files with 
- End with a ## Quick-Reference table (code | name | one-word fix)
- ## See Also section with  to all related vault topics
- No ❌/✅ code examples needed — this is a reference, not a tutorial
```

### Batch workflow (Hermes-native)

1. Spawn up to **3 sub-agents concurrently** using `delegate_task` with `tasks=[]`
2. When completions arrive, spawn the next batch
3. Heavy/long chapters go in the **last batch** so they don't block
4. Each sub-agent gets `toolsets: ['terminal', 'file']` — they only need to read a .txt and write a .md

---

## Phase 4.5: Consistency Gate

After all sub-agents finish, run the consistency gate to catch format drift.

**Checklist:**
- [ ] **Normalize source headers** — all must be `> *Source: Book Title by Author, Chapter X (pp. Y–Z)*`
- [ ] **Add missing page ranges** — use the Phase 3b mapping
- [ ] **Verify every file has a `## Related` section** with at least 2 ``
- [ ] **Broken link scan** — extract all `` and cross-reference against actual `.md` filenames
- [ ] **Fix formatting only** — don't change content, just normalize inconsistencies

Use `search_files` with regex `\[\[(.*?)\]\]` across all `.md` files and cross-check against the directory listing from `mcp_filesystem_directory_tree`. Fix broken links with `mcp_filesystem_edit_file`.

This costs ~2K tokens and saves 10+ minutes of manual cleanup.

---

## Phase 5: Overview & Polish

1. **Write `Overview.md`** — a master index file with:
   - Book metadata (title, author, ISBN)
   - Chapter map table with `` to every topic
   - "How to Use This Vault" guide (3–5 use cases)
   - Core philosophy summary

2. **Verify all files exist:**
   ```bash
   ls -la "F:\projects\orlita_md\vault-path\"
   find "F:\projects\orlita_md\vault-path\" -name "*.md" | wc -l
   ```

3. **Broken link scan (Hermes-native):**
   Use `search_files` with pattern `\[\[(.*?)\]\]` across all `.md` files. Extract unique link targets, then check each against the file listing. Fix any broken links.

4. **Spot-check 3 files** — one early chapter, one middle, one late. Verify source header format, core principle blockquote, and wikilinks.

---

## Style Guide for Output `.md` Files

### Rules Chapter (Template A)
```markdown
# Topic Name

> *Source: Book Title by Author, Chapter X (pp. A–B)*

---

## Core Principle

> **The central idea of this chapter as a blockquote.**

Brief 2–3 sentence explanation.

---

## The Rules

### 1. Rule Name

Explanation with code examples:

```java
// ❌ Bad
badCodeHere();

// ✅ Good
goodCodeHere();
```

---

## Summary Checklist

- [ ] Rule 1 check
- [ ] Rule 2 check

---

## Related

- **Related Topic One**
- **Related Topic Two**
```

### Case Study Chapter (Template B)
```markdown
# Case Study - Feature Name

> *Source: Book Title by Author, Chapter X (pp. A–B)*

---

## Final Result

(Show the clean end-state code first)

---

## The Journey

### Phase 1: The Rough Draft

What it looked like initially, why it was messy.

### Phase 2: First Refactoring

Code before/after. **Heuristic:** one-line takeaway.

### Phase 3: Second Refactoring

...

---

## Summary

- Heuristic 1
- Heuristic 2
- ...

---

## Related

- **Related Topic**
```

### Catalog Chapter (Template C)
```markdown
# Code Smells Catalog

> *Source: Book Title by Author, Chapter X (pp. A–B)*

---

## Category One: Names

#### **N1** — **Descriptive Name**
Explanation paragraph. See [[Naming Conventions]].

---

## Quick-Reference

| Code | Name | Fix |
|------|------|-----|
| N1 | Descriptive Name | Rename |
| ... | ... | ... |

---

## See Also

- **Topic One**
- **Topic Two**
```

---

## Token Budget Estimation

| Book Size | Pages | Raw Tokens | Approx. Cost (DeepSeek) |
|-----------|-------|------------|--------------------------|
| Small (200pp) | ~200 | ~150K | ~$0.05 |
| Medium (350pp) | ~350 | ~250K | ~$0.10 |
| **Clean Code** | **462** | **~300K** | **~$0.15** |
| Large (600pp) | ~600 | ~450K | ~$0.25 |
| Huge (1000pp) | ~1000 | ~750K | ~$0.40 |

**Formula:** `chars ÷ 4 ≈ tokens`. Each chapter produces output at roughly 30–50% of input size.

---

## Proven Runs

| Book | Pages | Files | Tokens | Time | Cost |
|------|-------|-------|--------|------|------|
| Clean Code | 462 | 18 `.md` | ~400K | ~7 min | ~$0.15 |
| The Clean Coder | 244 | 16 `.md` | ~86K in | ~5 batches | ~$0.05 |

---

## Quick Checklist for Future Runs

- [ ] PDF copied to accessible directory
- [ ] `pdfplumber` installed on **system Python 3.12** (not Hermes venv Python 3.11)
- [ ] Target vault directory created (`F:\projects\orlita_md\...`)
- [ ] Phase 1: TOC extracted and reviewed
- [ ] Phase 2: Topic-to-chapter mapping done (use decision rules above)
- [ ] Phase 3a: Exact PDF boundaries found
- [ ] Phase 3b: Printed page number mapping completed
- [ ] Phase 3c: Chapter `.txt` files extracted with printed page ranges
- [ ] Phase 4: Sub-agent prompts written using correct template (A, B, or C)
- [ ] Phase 4: Sub-agents spawned in batches of 3 (Hermes max concurrent)
- [ ] Phase 4.5: Consistency gate run (source headers, page ranges, broken links)
- [ ] Phase 5: `Overview.md` written with chapter map and usage guide
- [ ] Phase 5: Broken link scan returns zero results
- [ ] Phase 5: 3 files spot-checked against PDF for accuracy

---

## Common Pitfalls

1. **Source header drift** — sub-agents invent their own format. Always run Phase 4.5.
2. **Missing page ranges** — sub-agents guess or omit printed page numbers. Feed the Phase 3b mapping.
3. **Wrong wikilink filenames** — Phase 4.5 + Phase 5 broken link scan catches these.
4. **Hallucinated cross-references** — sub-agents link to files that don't exist. Phase 4.5 catches this.
5. **Using wrong template** — a case study with Template A loses the narrative. Check Phase 2 decision rules.
6. **PDF page ≠ printed page** — without Phase 3b mapping, all page range citations are wrong.
7. **Big chapters blocking pipeline** — put the heaviest chapters in the last batch.
8. **Skipping Phase 4.5** — costs ~2K tokens and saves 10+ minutes of human editing.
9. **Wrong Python on Windows** — Hermes venv Python 3.11 may not have `pdfplumber`. Use system Python 3.12: `"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"`. Verify: `"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" -c "import pdfplumber; print('ok')"`.
10. **Summary vs complete PDF** — if the PDF has ~27 pages with short chapters, it's a summary. When the full book arrives: (a) check file size (summary <1MB, full 2–8MB); (b) re-extract; (c) compare TOCs; (d) add missing chapters, don't rewrite everything; (e) update Overview.
11. **Mermaid diagrams** — Obsidian renders `mermaid` natively. Add diagrams for class hierarchies, sequences, state machines. Remove old ASCII-art diagrams (┌ └ ├ ─ │).

---

## Related Skills

- **`oralita-book-sum-obs`** — the Hermes skill that drives this pipeline
- **Direct Book Synthesis** — for tip-based or chapter-level books, synthesize notes directly without sub-agents
- **Overview-Driven Fill** — start from an existing Overview/MOC, identify missing topics, fill from web sources
