# PDF-to-Vault Summarization Workflow

> *How to turn any PDF book into a topic-separated Obsidian knowledge base using LLM sub-agents.*

---

## Prerequisites

- PDF file accessible to OpenClaw's sandbox (allowed directories)
- LLM credits (DeepSeek or similar) — ~200K–400K input tokens for a 500-page book
- Python with `pdfplumber` installed (`pip install pdfplumber`)
- Obsidian vault with a target directory for output files

---

## The 5-Phase Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 1: STRUCTURE EXTRACTION               │
│         Extract TOC → Identify chapter page ranges           │
├─────────────────────────────────────────────────────────────┤
│                  PHASE 2: TOPIC MAPPING                      │
│    Human reviews TOC → Maps topics to chapters/files         │
├─────────────────────────────────────────────────────────────┤
│                  PHASE 3: TEXT EXTRACTION                    │
│    Python script splits PDF into per-chapter .txt files      │
├─────────────────────────────────────────────────────────────┤
│                  PHASE 4: PARALLEL SUB-AGENTS                │
│     Spawn 15 sub-agents → Each summarizes one chapter        │
├─────────────────────────────────────────────────────────────┤
│                  PHASE 5: OVERVIEW & LINKING                 │
│     Update overview.md → Verify [[wikilinks]] → Polish       │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Structure Extraction

**Goal:** Get the table of contents and identify exact PDF page ranges for each chapter.

**Script:**
```python
import pdfplumber

pdf = pdfplumber.open(r'F:\books\your-book.pdf')

# Scan first ~30 pages for TOC
for i in range(min(30, len(pdf.pages))):
    page = pdf.pages[i]
    text = page.extract_text()
    if text:
        print(f'--- PAGE {i+1} ---')
        print(text[:2000])
        print()

pdf.close()
```

**Prompt to agent:**
> Extract the table of contents from the first pages of this PDF. I'll read the first ~30 pages to find the chapter structure.

---

## Phase 2: Topic Mapping

**Goal:** Decide what `.md` files to produce and which chapters map to which topics.

**Do this manually** (you, the human, make the decisions):

1. Review the TOC from Phase 1
2. Create a mapping table:

```
Chapter 2: Meaningful Names    → naming-conventions.md
Chapter 3: Functions           → function-design.md
Chapter 4: Comments            → comment-patterns.md
...
```

3. **Pro-tip:** Some chapters are self-contained (one file). Some topics span multiple chapters — in that case, extract the relevant chapters into one file.

4. **Pro-tip:** Case study chapters (like Clean Code 14-16) get standalone files with "Case Study - " prefix. Reference chapters (like Ch 17, smells catalog) get catalog-style formatting.

---

## Phase 3: Text Extraction

**Goal:** Split the PDF into per-chapter text files for sub-agents to read.

**First, find exact page boundaries:**
```python
import pdfplumber, re

pdf = pdfplumber.open(r'F:\books\your-book.pdf')

for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text:
        lines = text.strip().split('\n')
        first_line = lines[0].strip()
        if re.match(r'^\d{1,2}$', first_line):
            print(f'PDF p{i+1}: {first_line} {lines[1].strip() if len(lines) > 1 else ""}')

pdf.close()
```

**Then extract each chapter range to a text file:**
```python
import pdfplumber, os

pdf = pdfplumber.open(r'F:\books\your-book.pdf')
out_dir = r'C:\Users\Admin\.openclaw\workspace\book-chapters'
os.makedirs(out_dir, exist_ok=True)

chapters = [
    # (start_idx, end_idx, chapter_num, 'Chapter-Name')
    (31, 47, 1, 'Clean-Code'),
    (47, 61, 2, 'Meaningful-Names'),
    # ... add all chapters
]

for start_idx, end_idx, num, name in chapters:
    filename = os.path.join(out_dir, f'ch{num:02d}-{name}.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(start_idx, end_idx):
            text = pdf.pages[i].extract_text()
            if text:
                f.write(text + '\n')
    print(f'ch{num:02d} {name}: {os.path.getsize(filename)} chars')

pdf.close()
```

**You'll get something like:**
```
ch01 Clean-Code : 15000 chars (~3750 tokens)
ch02 Meaningful-Names : 12000 chars (~3000 tokens)
...
```

---

## Phase 4: Parallel Sub-Agents (The Magic 🔮)

**Goal:** Spawn one sub-agent per chapter to produce the `.md` file. They all run simultaneously.

**Template prompt for each sub-agent:**

```
Read: C:\Users\Admin\.openclaw\workspace\book-chapters\ch03-Functions.txt
     — Chapter 3 of "Book Title" by Author Name.

Write to: F:\projects\orlita_md\your-vault\Topic\Function Design.md

Style:
- Start with: `> *Source: Book Title by Author, Chapter X (pp. Y–Z)*`
- Core principle quote at top
- Rules organized under ### headings with bold names
- Before/after code examples using ```java blocks with ❌ / ✅ labels
- Summary checklist with checkboxes at the bottom
- `## Related` section with `[[wikilinks]]` to related topics
- Professional, direct tone. No fluff. Actionable.

Topics covered in this chapter: [list key sections from TOC]
```

**Limitations:**
- Max 5 sub-agents concurrently per session
- Spawn in batches of 5, use `sessions_yield` between batches
- Big chapters (20K+ tokens) may take longer — spawn them last

**Batch workflow:**
1. Spawn 5 → yield
2. When completions arrive, spawn next 5
3. Repeat until all done
4. The big/heavy chapters go in the last batch so they don't block the pipeline

---

## Phase 5: Overview & Polish

**Goal:** Update the vault overview and verify everything links.

1. **Write/edit overview.md** — a master file with chapter map, `[[wikilinks]]` to every topic, and a "How to Use" guide
2. **Verify files exist** — check the directory listing
3. **Spot-check 2-3 files** — open them, check formatting, examples, wikilinks
4. **Fix any broken links** — sub-agents sometimes use slightly wrong filenames

---

## Style Guide for Output `.md` Files

Every chapter summary should follow this consistent format:

```markdown
# Topic Name

> *Source: Book Title by Author, Chapter X (pp. A–B)*

---

## Core Principle

> **The central idea of this chapter as a blockquote.**

Brief 2-3 sentence explanation.

---

## The Rules

### 1. Rule Name (Bold)

Explanation with code examples:

```java
// ❌ Bad
badCodeHere();

// ✅ Good
goodCodeHere();
```

### 2. Next Rule

...

---

## Summary Checklist

- [ ] Rule 1 check
- [ ] Rule 2 check
...

---

## Related

- [[Related Topic One]]
- [[Related Topic Two]]
```

---

## Token Budget Estimation

| Book Size | Pages | Raw Tokens | Approx. Cost (DeepSeek) |
|-----------|-------|-----------|------------------------|
| Small (200pp) | ~200 | ~150K | Low |
| Medium (350pp) | ~350 | ~250K | Medium |
| **Clean Code** | **462** | **~300K** | **Medium** |
| Large (600pp) | ~600 | ~450K | High |
| Huge (1000pp) | ~1000 | ~750K | Very High |

**Formula:** `chars ÷ 4 ≈ tokens`. Each chapter produces output at roughly 30-50% of input size.

---

## Real Example: Clean Code Run

| Phase | Time | Tokens |
|-------|------|--------|
| 1. Structure extraction | 30s | ~5K |
| 2. Topic mapping (human) | 2 min | — |
| 3. Text extraction | 30s | — |
| 4. 15 sub-agents (parallel) | ~3 min | ~300K in / ~100K out |
| 5. Overview polish | 1 min | ~2K |
| **Total** | **~7 min** | **~400K tokens** |

18 files produced, 261 KB total, full `[[wikilinks]]`.

---

## Quick Checklist for Future Runs

- [ ] PDF copied to accessible directory (`F:\programming_practice\` or workspace)
- [ ] `pdfplumber` installed (`pip install pdfplumber`)
- [ ] Python path correct (use full path on Windows: `C:\Users\Admin\...\Python312\python.exe`)
- [ ] Target vault directory created (`F:\projects\orlita_md\...`)
- [ ] TOC extracted and reviewed
- [ ] Topic-to-chapter mapping done
- [ ] Chapter text files extracted
- [ ] Sub-agent prompts written (use template above)
- [ ] LLM credits topped up
- [ ] Batches of 5 sub-agents spawned
- [ ] Overview.md updated with final file list
- [ ] 2-3 files spot-checked for quality
