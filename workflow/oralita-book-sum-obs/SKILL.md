---
name: oralita-book-sum-obs
description: "Use when the user asks to summarize a PDF book into their Obsidian vault as a topic-separated knowledge base. 5-phase pipeline: extract TOC, map topics, split chapters, parallel sub-agent summarization, overview + polish. Produces consistently-formatted .md files with wikilinks, code examples, and checklists."
version: 1.7.0
author: Panomete + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pdf, summarization, obsidian, vault, book, pipeline, orlita]
    related_skills: []
---

# Orlita Book → Obsidian Vault Summarization

## Overview

Turns any source material (PDF books, body-of-knowledge documents, online resources) into a cross-linked Obsidian knowledge base. Two workflows:

2. **PDF Book → Vault** (main pipeline): Extract chapters, spawn parallel sub-agents, produce `.md` files with `[[wikilinks]]`, ❌/✅ code examples, and checklists.
2. **Direct Book Synthesis** (see `references/direct-book-synthesis.md`): For tip-based or chapter-level books, read extracted text and synthesize notes directly without sub-agents. Faster for medium books with self-contained chapters.
4. **Multi-Chapter Synthesis** (see `references/multi-chapter-synthesis.md`): When multiple source chapters are consolidated into a single cohesive study note (e.g., CLRS Ch33-35 → one file). Uses pre-extracted `.txt` files, matches existing vault format.
2. **Overview-Driven Fill** (see `references/overview-driven-fill.md`): Start from an existing Overview/MOC, identify missing topics via gap analysis, and fill them from web sources or body-of-knowledge documents. Direct agent summarization for small vaults (~10-15 topics).

**Proven on:**
- Clean Code (462pp) → 18 files, 261 KB, ~7 min, ~400K tokens (~$0.20 on DeepSeek)
- The Clean Coder (244pp) → 16 files, ~86K input tokens, ~5 batches of 3 sub-agents
- **PMBOK v8 (386pp)** → 19 files, 274 KB, 6 batches, ~800K tokens — BOK with Template D. See `references/pmbok-v8-run.md`
- **SEBoK v2 (1,705pp)** → 23 files, 366 KB, 8 batches, ~1.2M tokens — wiki-based BOK with Template D. See `references/sebok-v2-run.md`
- **BABOK v3 (514pp)** → 11 files, 257 KB, 4 batches — Knowledge Area + Tasks structure with Template D. See `references/babok-v3-run.md`
- **CyBOK v1.1 (1,067pp)** → 22 files, 262 KB, 7 batches — Cyber security KAs with Template D. See `references/cybok-v1-run.md`
- **DMBOK v2 (628pp)** → 13 files, 329 KB, 4 batches — 11 Knowledge Areas with Template D. See `references/dmbok-v2-run.md`
- **CLRS (1313pp)** → 7 files (gap analysis), 90 KB — Only advanced topics not in existing Algorithm v1 notes. See `references/clrs-gap-analysis-run.md`
- **Software Methodology** → 5 files synthesized from clean-agile.pdf + domain knowledge. See `references/methodology-synthesis.md`
- **UX/UI Design** → 6 files integrated into existing HCI folder (29 theory files + 5 process files + 1 overview). See `references/direct-vault-creation.md`

## When to Use

- User says "summarize this PDF book into my vault"
- User mentions `pdf-to-vault`, "book summarization pipeline", or references this skill by name
- The PDF is a technical/programming book with clear chapter structure
- **For overview-driven filling (non-PDF):** see `references/overview-driven-fill.md` — use when the user has an existing Overview/MOC and wants to fill missing notes from web sources
- **For small/summary PDFs (under ~50 pages):** skip the sub-agent pipeline entirely. Extract all text with `pdfplumber`, read it into context, and synthesize topic files directly. Proven on Clean Agile (27-page book summary).
- **For methodology/philosophy books without a single canonical PDF:** see `references/methodology-synthesis.md` — synthesize from multiple sources (existing PDFs + domain knowledge). Proven on Software Methodology (Agile from clean-agile.pdf + Lean/Kanban from domain knowledge).
- **For adding ISO/IEEE references to existing Essential Documents:** see `references/essential-documents.md` — retrofit ISO reference columns to document tables. Proven on PMBOK and SEBOK.
- **For creating new vaults from domain knowledge (no PDF):** see `references/direct-vault-creation.md` — when the user wants a knowledge base for a topic not covered by existing BOKs. Proven on Software Methodology (5 files) and UX/UI Design (6 files).
- **For integrating new content into existing vault structure:** see `references/existing-vault-integration.md` — when the user asks for content in an area that may already have partial coverage. Check existing folders first, integrate rather than duplicate. Proven on UX/UI Design → HCI folder merge.
- **For partial summarization (gap analysis):** see `references/clrs-gap-analysis-run.md` — when the user has existing notes and wants to summarize a book that partially overlaps. Compare book TOC against existing notes, identify gaps, summarize ONLY the missing topics. Produces focused files instead of redundant ones. Proven on CLRS (1313pp → 7 files covering only advanced topics not in Algorithm v1).

**Don't use for:** novels, reference manuals without chapters, PDFs under 20 pages, or when the user wants a single-file summary instead of a topic-separated vault.

## Prerequisites

- PDF file accessible from the shell (any drive)
- `pdfplumber` installed: `pip install pdfplumber`
- Obsidian vault with a target directory (e.g., `F:\projects\orlita_md\...`)
- LLM credits — budget ~300-500K input tokens for a typical 400-page book

---

## Phase 1: Structure Extraction

**Goal:** Extract the table of contents and identify exact PDF page ranges for each chapter.

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
| **Body of Knowledge chapter** | **Numbered file with SWEBOK-style format** | **Governance → `04_Governance_Performance_Domain.md`** |

**For BOK books (PMBOK, SWEBOK, standards):** Use Template D. Files get numbered prefixes (`00_`, `01_`, ...). Appendices get `Appendix_A1_` prefix. Overview file named `BookTitle vX - Overview.md`. YAML frontmatter tags use inline format: `tags: [topic, category, standard]`.

**Output:** A mapping table:
```
Ch 1: Clean Code              → Clean Code Principles.md
Ch 2: Meaningful Names        → Naming Conventions.md
Ch 3: Functions               → Function Design.md
Ch 4: Comments                → Comment Patterns.md
...
Ch14: Args Parser             → Case Study/Case Study - Args Parser.md
Ch17: Smells & Heuristics     → Code Smells Catalog.md
```

**Completion criterion:** Every chapter in the TOC has a target `.md` filename assigned.

---

## Phase 3: Text Extraction

**Goal:** Split the PDF into per-chapter text files for sub-agents to read.

### Step 3a — Find exact page boundaries

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

**Completion criterion:** All `.txt` files exist in `out_dir` with non-zero size.

---

## Phase 4: Parallel Sub-Agent Summarization

**Goal:** Spawn one sub-agent per topic/chapter. They all run simultaneously in batches.

### Sub-agent prompt templates

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
- ## Related section with [[wikilinks]] to related topics in the vault
- Professional, direct tone. No fluff. Actionable.

Topics covered in this chapter: [list key sections from TOC]
```

**Template B — Case study chapter** (step-by-step refactoring walkthrough):
```
Read: C:\Users\Admin\.openclaw\workspace\book-chapters\ch14-Args-Parser.txt
     — Chapter 14 of "Book Title" by Author Name.

Write to: F:\projects\orlita_md\vault-path\Case Study\Case Study - Args Parser.md

Style:
- Start with: **Source:** *Book Title* by Author — Chapter X (pp. Y–Z)
- Lead with the final clean code first (what we're building toward)
- Then walk through the rough draft → how it got messy → step-by-step refactoring phases
- Each refactoring phase gets a ### heading, shows code before/after, and ends with a **Heuristic:** takeaway
- ## Summary section with key heuristics bullet list
- ## Related section with [[wikilinks]]
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
- Include cross-references to related vault files with [[wikilinks]]
- End with a ## Quick-Reference table (code | name | one-word fix)
- ## See Also section with [[wikilinks]] to all related vault topics
- No ❌/✅ code examples needed — this is a reference, not a tutorial
```

**Template D — Body of Knowledge / reference book** (PMBOK, SWEBOK, standards, academic textbooks):

```
Read: C:\Users\Admin\.openclaw\workspace\pmbok-chapters\ch04-Governance_Performance_Domain.txt
     — §2.1 of "Book Title" by Author/Organization (printed pp. X–Y).

Write to: F:\projects\orlita_md\vault-path\04_Governance_Performance_Domain.md

Style (SWEBOK reference format):
- Start with YAML frontmatter: tags: [topic, category, pmbok]
- Source line: > *Source: Book Title — Edition by Author/Org, §X.X Topic Name (pp. X–Y)*
- # Title — use the chapter number as prefix (e.g., "04 — Governance Performance Domain")
- ## Purpose — what this chapter covers and why it matters
- ## Key Concepts — hierarchical breakdown of topics with bold names, organized under ### subheadings
- ## Processes — (if applicable) numbered list of formal processes with brief descriptions
- ## Tailoring Considerations — how to adapt this domain to different contexts
- ## Interactions With Other Domains — cross-domain dependencies
- ## Check Results — outcome verification criteria (table format)
- ## Related Chapters section at the bottom with [[wikilinks]] to connected files

IMPORTANT — Use ONLY these exact filenames for wikilinks:
[INSERT COMPLETE LIST OF ALL TARGET FILENAMES HERE, e.g.:]
00_Introduction  01_Value_Delivery_System  02_Project_Management_Principles  ...

Format requirements:
- All YAML frontmatter tags MUST use inline format: tags: [tag1, tag2, tag3]
- Do NOT add aliases: to frontmatter
- Do NOT use indented list style for tags
- Professional reference tone — concise, actionable, no code examples needed
- Each major section (## heading) MUST have an owner blockquote: > **Owner:** Role Name
- Tables MUST include an ISO/IEEE Reference column as the last column (use — if no standard applies)
```

### Batch workflow

1. Spawn up to 3 sub-agents concurrently using `delegate_task` with `tasks=[]` (Hermes default max concurrent)
2. When completions arrive, spawn the next batch
3. Heavy/long chapters go in the last batch so they don't block
4. Each sub-agent gets `toolsets: ['terminal', 'file']` — they only need to read a .txt and write a .md

**Completion criterion:** All target `.md` files exist and have substantial content (>1KB).

---

## Phase 4.5: Consistency Gate (NEW — catches format drift)

After all sub-agents finish, run the consistency gate. Two approaches:

**Approach A — Inline (preferred on Hermes):** Use `search_files` with regex `\[\[(.*?)\]\]` across all .md files to extract every wikilink. Cross-reference against the directory listing (`mcp_filesystem_directory_tree`). Fix broken links with `mcp_filesystem_edit_file`. Use `read_file` to spot-check source headers. This is faster and cheaper than spawning a sub-agent.

**Approach B — Sub-agent (if many issues expected):**

```
Goal: Read every .md file in F:\projects\orlita_md\vault-path\ (recursively) and fix:

1. Source headers — normalize ALL to: > *Source: Book Title by Author, Chapter X (pp. Y–Z)*
   (Replace **Source:**, *Source:*, and YAML frontmatter source: variants with the standard format.)

2. Page ranges — add printed page ranges to any file missing them. Use the chapter→page mapping from Phase 3b.

3. Broken wikilinks — find all [[wikilinks]], verify they resolve to existing .md files. Remove or fix any that don't.

4. Ensure every file has a ## Related section with at least 2 [[wikilinks]].

Do NOT change content — only fix formatting inconsistencies. Report what you changed.
```

**Completion criterion:** Sub-agent reports zero remaining inconsistencies (or lists the ones it couldn't auto-fix).

---

## Phase 5: Overview & Polish

1. **Write `Overview.md`** — a master index file with:
   - Book metadata (title, author, ISBN)
   - Chapter map table with `[[wikilinks]]` to every topic
   - "How to Use This Vault" guide (3-5 use cases)
   - Core philosophy summary

2. **Verify all files exist:**
   ```bash
   ls -la "F:\projects\orlita_md\vault-path\"
   find "F:\projects\orlita_md\vault-path\" -name "*.md" | wc -l
   ```

3. **Broken link scan (Hermes-native):**
   Use `search_files` with pattern `\[\[(.*?)\]\]` across all .md files in the vault. Extract unique link targets, then check each against the file listing from `mcp_filesystem_directory_tree`. Any link target that doesn't match an existing filename (minus `.md`) is broken. Fix with `mcp_filesystem_edit_file`.
4. **Spot-check 3 files** — open one early chapter, one middle chapter, and one late chapter. Verify source header format, core principle blockquote, and wikilinks.

**Completion criterion:** Overview.md written, file count matches expected, zero broken wikilinks, 3 spot-checks pass.

---

## Token Budget Estimation

| Book Size | Pages | Raw Tokens | Approx. Cost (DeepSeek) |
|-----------|-------|-----------|------------------------|
| Small (200pp) | ~200 | ~150K | ~$0.05 |
| Medium (350pp) | ~350 | ~250K | ~$0.10 |
| **Clean Code** | **462** | **~300K** | **~$0.15** |
| Large (600pp) | ~600 | ~450K | ~$0.25 |
| Huge (1000pp) | ~1000 | ~750K | ~$0.40 |

**Formula:** `chars ÷ 4 ≈ tokens`. Each chapter produces output at roughly 30-50% of input size.

---

## Quick Checklist for Future Runs

- [ ] PDF copied to accessible directory
- [ ] `pdfplumber` installed (`pip install pdfplumber`)
- [ ] Target vault directory created
- [ ] Phase 1: TOC extracted and reviewed
- [ ] Phase 2: Topic-to-chapter mapping done (use decision rules above — Template D for BOK books)
- [ ] Phase 3: Chapter text files extracted with printed page ranges; verify sizes — if a 25-printed-page chapter is <15K chars, the boundary is wrong
- [ ] Phase 4: Sub-agent prompts written using the correct template (A/B/C/D); EVERY prompt includes the COMPLETE list of all target filenames for correct [[wikilinks]]
- [ ] Phase 4: Sub-agents spawned in batches of 3 (Hermes max concurrent)
- [ ] Phase 4.5: Consistency gate agent run (source headers, page ranges, broken links)
- [ ] Phase 5: Overview.md written with chapter map and usage guide
- [ ] Phase 5: Broken link scan returns zero results
- [ ] Phase 5: 3 files spot-checked against PDF for accuracy

---

## Common Pitfalls

1. **Source header drift** — sub-agents invent their own format (`**Source:**`, YAML frontmatter, italic-only). Always run Phase 4.5 to normalize.

2. **Missing page ranges** — sub-agents guess or omit printed page numbers. Feed the Phase 3b mapping in the prompt context.

3. **Wrong wikilink filenames** — sub-agents link to `[[Function Design]]` but the file is `Function Design.md`. Obsidian resolves this, but the Phase 5 grep check catches exact mismatches.

4. **Hallucinated cross-references** — sub-agents may link to files that don't exist (e.g., `[[Clean Architecture Overview]]` for a Clean Code vault). Phase 4.5 + Phase 5 broken link scan catches these.

5. **Using the wrong template** — a case study chapter summarized with Template A loses the narrative. Check the Phase 2 decision rules before writing prompts.

6. **PDF page ≠ printed page** — the extraction script uses PDF indices. Without Phase 3b mapping, all page range citations will be wrong.

7. **Big chapters blocking the pipeline** — a 50-page chapter spawned in batch 1 holds up everything. Put the heaviest chapters in the last batch.

8. **Skipping Phase 4.5** — without the consistency gate, you'll need manual cleanup to fix format drift and broken links. It costs ~2K tokens and saves 10+ minutes of human editing.

9. **Wrong Python on Windows** — the Hermes venv Python (3.11) is first in PATH and may not have `pdfplumber`. Use the full path to the system Python: `C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe`. Verify with: `"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" -c "import pdfplumber; print('ok')"`.
10. **Summary vs complete PDF** — if the PDF has ~27 pages with short chapters, it's a book summary, not the full book. The user may later provide the complete PDF (e.g., 235 pages for Clean Agile, 519 pages for Clean Craftsmanship). When this happens: (a) check file size — `ls -la /f/books/*.pdf` — a summary is typically under 1MB, a full book is 2-8MB; (b) re-extract the full book; (c) compare TOCs — identify new chapters, expanded sections, missing appendices/afterwords; (d) add missing chapters/content rather than rewriting everything; (e) update the Overview's chapter map and Structure table. The existing files were correct for the summary — don't discard them. Also check the books folder for new PDFs the user may have added since the last session — run `ls -la /f/books/` to see what's available.

11. **Ad-hoc verification on Windows** — after creating many files, write a temp Python verification script under `C:\\Users\\Admin\\AppData\\Local\\Temp` with a `hermes-verify-` filename prefix. Check: file count vs expected, minimum file size (>1000 bytes), Sources section presence, Mermaid diagram count, overview wikilink count. Run it and clean up. Use the full Python path (`C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\python.exe`) to avoid venv conflicts. Don't claim \"fully verified\" — call it \"ad-hoc verification\" and report pass/fail.

12. **Mermaid diagrams in Obsidian notes** — Obsidian renders `mermaid` code blocks natively. For any vault with UML/architecture/sequence content, add Mermaid diagrams. Key syntaxes: `classDiagram` (OOP, design patterns), `sequenceDiagram` (auth flows, event chains), `graph TD/LR` (architecture, pipelines), `stateDiagram-v2` (circuit breakers, state machines). Use `..>` for dependency (dashed), `-->` for association, `o--` for aggregation (empty diamond), `*--` for composition (filled diamond), `..|>` for implementation, `<|--` for inheritance. When adding diagrams, remove old ASCII-art diagrams (box-drawing characters like ┌ └ ├ ─ │). Verify with `mcp_filesystem_directory_tree` to ensure zero ASCII art remains.

13. **Sub-agents hallucinate wikilink filenames at scale** — sub-agents don't know the final filenames unless you tell them. They will invent their own numbering schemes, use human-readable names, or reference terminology from previous editions. **Fix:** In every sub-agent prompt, include the COMPLETE list of all target filenames so they can create correct `[[wikilinks]]`. Example: "Use ONLY these exact filenames for wikilinks: 00_Introduction, 01_Value_Delivery_System, 02_Project_Management_Principles, ..." Without this, expect 100+ broken links requiring Phase 4.5 cleanup. Proven on PMBOK v8 run: 107 broken links across 12 files because 18 sub-agents independently invented different naming schemes.

14. **PDF section headers may be garbled** — pdfplumber text extraction can produce garbled headers like "SSeeccttiioonn 13" instead of "Section 3" or "IInnttrroodduuccttiioonn" instead of "Introduction". The Phase 3a script matching `^\d{1,2}$` won't catch these. **Fix:** In Phase 1, scan the first ~40 pages with broader pattern matching (`if 'ection' in first.lower()` or `if target_keyword in line.lower()`). Also manually verify extracted chapter sizes — if a chapter that should be 25 printed pages is only 10K chars, the boundary is wrong (proven on PMBOK Governance domain: initially 10K chars, corrected to 89K).

15. **Sub-agent results dropped silently by gateway** — gateway hiccups can cause sub-agent completions to never appear, with no error indication. Symptoms: no background processes running (`process action='list'` returns empty), yet expected files are missing from the output directory. **Fix:** After all batches dispatched, wait a reasonable time (~3-5 minutes for most chapters, longer for 200K+ char files), then verify file count with `mcp_filesystem_list_directory_with_sizes`. If files are missing and no processes are running, the sub-agents were dropped — read the source `.txt` files directly and write the missing chapters yourself. Don't re-dispatch; direct writing is faster and more reliable for the affected files. Proven on SEBoK v2 run: 8 of 21 sub-agents silently dropped, written directly from source in ~3 minutes total.

16. **Garbled PDF text in reference catalog chapters** — Some PDFs have layered text (e.g., old edition + new edition overlays). pdfplumber extracts both layers interleaved, producing unreadable text like \"SSeeccttiioonn 13\" or \"IInnttrroodduuccttiioonn\" mixed with valid content. Reference catalogs (Inputs/Outputs, Tools/Techniques, glossaries) are worst affected because each entry is short and the garbling corrupts critical name/description pairs. **Symptoms:** .txt file is large (50K-200K chars) but sub-agents can't produce coherent output because they can't separate valid text from garbled text. **Fix:** Extract term names programmatically using regex patterns on the garbled text (e.g., `re.findall(r'^([A-Z][a-z]+(?: [a-z]+){1,4})\\.', text, re.MULTILINE)`), then write the catalog chapter directly using your own knowledge of the domain. Don't waste sub-agent tokens on unreadable text. Proven on PMBOK v8: ch12 (Inputs/Outputs, 96K chars, 88 terms) and ch13 (Tools/Techniques, 200K chars) both produced via direct writing after sub-agents failed on garbled text.

17. **Essential Documents extraction** — a post-summarization workflow for extracting just the "documents you need to produce" checklist from a BOK vault. See `references/essential-documents.md`. Use when the user asks for a practical document checklist organized by life cycle phase, with priority levels (🔴🟡🟢) and links back to the full BOK chapters. Also see the `bok-essential-documents` skill for the full workflow including project profiles and UX/UI integration.

18. **Consistency gate sub-agent is unreliable** — Approach B (dispatching a sub-agent to fix broken links) can fail silently due to gateway hiccups, same as any other sub-agent dispatch. When you dispatch a consistency gate and the links are still broken minutes later with no background processes running, the sub-agent was dropped. **Fix:** Use `execute_code` with a Python script that reads each `.md` file, applies all replacements via a `fixes` dictionary, and writes back only changed files. This is ~10 lines of Python, runs in <1 second, and cannot be dropped. Pattern:
```python
fixes = {'Wrong_Name': 'Correct_Name', ...}
for fname in os.listdir(base):
    content = open(path).read()
    for old, new in fixes.items():
        content = content.replace(f'[[{old}]]', f'[[{new}]]')
    if changed: write back
```
Proven on SEBOK v2 (45 fixes) and BABOK v3 (43 fixes) — both had their delegated consistency gates dropped silently, then fixed in seconds via execute_code.

18b. **Sub-agents skip wikilinks entirely** — Different from hallucinated filenames: sub-agents may produce files with ZERO `[[wikilinks]]` because they focus on content and forget the linking requirement. This is especially common when the prompt doesn't explicitly emphasize wikilinks. **Fix:** After sub-agents complete, verify every file has at least one `[[` link. For files missing links, add a `## Related` section with appropriate wikilinks using `patch()`. Proven on CLRS Algorithm v2: 4 of 6 sub-agent files had zero wikilinks, had to add Related sections manually.

19. **BOK parent overview maintenance** — When you add a new BOK vault, you MUST also update the parent `Body of Knowledge - Overview.md` with: (a) the new entry in the summary table, (b) a new section with chapter/KA breakdown, (c) a new bullet in the relationship list, (d) a new reading path, and (e) the Mermaid diagram updated to include the new BOK. **Trust the user when they remind you** — if they say "should we also update the overview?", the answer is always YES. Don't skip this step.

20. **Mermaid over ASCII for relationship diagrams** — For BOK relationship diagrams showing how multiple BOKs nest/complement each other, use `mermaid flowchart TD` with `subgraph` for nesting and `-.->` dashed arrows for cross-cutting concerns (e.g., CyBOK securing all layers, BABOK feeding needs). Remove old ASCII box-drawing diagrams (┌ └ ├ ─ │) when converting. Obsidian renders Mermaid natively. The user has explicitly requested Mermaid format over ASCII.

21. **Cross-vault linking pattern** — When creating a new vault, establish bidirectional links: (a) New vault → Essential Documents (link to document checklists), (b) New vault → BOK vaults (link to relevant BOK chapters), (c) Essential Documents → New vault (add to "Which Checklist Do I Need?"), (d) BOK overview → New vault (if relevant, add to relationship diagram). This creates a web of interconnected knowledge rather than isolated silos. Proven across 6 BOKs + 2 methodology vaults + UX/UI Design vault.

22. **Check existing vault structure before creating new folders** — When the user asks for a new topic area (e.g., "I need UX/UI design content"), FIRST scan the existing vault for related material under different names. The user may have content in unexpected locations (e.g., "Human Computer Interaction" containing UX/UI theory). Creating a duplicate folder wastes effort and confuses the user — you'll end up merging it back later. **Fix:** Before creating new folders, run `mcp_filesystem_directory_tree` on the parent vault and check for existing subfolders that cover similar territory. If found, integrate the new content INTO the existing structure rather than creating a parallel one. Proven on UX/UI Design: created a separate folder, then discovered the user had `Software Design/Human Computer Interaction/` with 29 files of Gestalt laws, UX laws, and UI principles. Had to move all files back and update cross-links.

23. **Gap analysis for partial summarization** — When the user has existing notes and wants to summarize a book that partially overlaps, DON'T summarize the whole book. Instead: (a) read the existing notes to understand what's already covered, (b) scan the new book's TOC to identify chapters/topics, (c) compare and identify gaps (topics in the book NOT in the existing notes), (d) extract and summarize ONLY the gap chapters. This produces 5-8 focused files instead of 20+ redundant ones. The user explicitly chose this approach for CLRS — 1313 pages, but only 7 files covering advanced topics (amortized analysis, B-trees, Fibonacci heaps, MST, max flow, NP-completeness, number theory) that the v1 Algorithm notes didn't have. **Key:** present the gap analysis to the user with a clear "what's covered / what's missing / what I recommend" table before proceeding.

25. **Sub-agent language drift** — sub-agents can output in unexpected languages (Chinese, Japanese, etc.) when the source material or their training context is in that language. This is especially likely when the source PDF has bilingual content or the sub-agent's model has strong non-English training data. **Symptoms:** File passes structural verification (YAML, wikilinks, tags) but content is in the wrong language. **Fix:** After sub-agents complete, check a sample of output files for language correctness. If non-English text found, rewrite the entire file in English using `write_file`. Don't try to patch individual lines — the whole file needs rewriting. Proven on CLRS Algorithm v2: `04_Linear_Programming.md` was 453 lines of Chinese with English math notation. Rewrote entirely in English (14.3 KB). The earlier grep `[\u4e00-\u9fff]` matched both Chinese AND some ASCII ranges — use Python's explicit Unicode range check `'\u4e00' <= ch <= '\u9fff'` for reliable detection.

26. **Rename + backlink fix workflow** — when renaming a vault folder (e.g., `Algorithm_v2` → `Algorithm_advance`), you must update ALL references: (a) rename the folder itself, (b) rename any files with the old name (e.g., overview file), (c) fix internal references in all files within the folder, (d) fix external references in files that link TO the renamed folder (e.g., parent overviews, cross-vault links). Use `search_files` with pattern `Old_Name|OldFolder` to find all references, then fix with `patch()`. Verify with a Python script that checks no references to the old name remain. Proven on Algorithm_v2 → Algorithm_advance rename: 3 references fixed (2 internal in overview, 1 external in v1 overview), plus 7 broken wikilinks corrected.

24. **Adding a new discipline to existing project profiles** — When the user creates a new Essential Document (e.g., UX/UI), the existing project profiles (Small/Medium/Large) need updating too. For each profile: (a) add a new section with appropriate document density (startup = 2-3 docs, medium = 6-8 docs, large = 15+ docs), (b) add owner blockquote, (c) add checklist items to the Quick-Start Checklist at the end, (d) add the new Essential Document to the Sources section. The section should be named `Xb. Discipline Name` (e.g., `2b. UX/UI Design`, `4b. UX/UI Design`, `6b. UX/UI Design`) to fit between existing sections without renumbering. Proven on UX/UI Design: added to all 3 profiles (Small: 3 docs, Medium: 12 docs, Large: 20 docs with ISO references).

- **For renaming vault folders and fixing backlinks:** see `references/rename-and-fix-backlinks.md` — systematic workflow for renaming folders, fixing internal/external references, and verifying no broken links remain. Proven on Algorithm_v2 → Algorithm_advance rename.
- **For post-creation verification**, see `references/ad-hoc-verification.md` — temp Python scripts that check file counts, Sources sections, Mermaid validity, and orphaned stubs.
