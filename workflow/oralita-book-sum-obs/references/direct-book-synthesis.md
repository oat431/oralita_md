# Direct Book Synthesis (No Sub-Agent Pipeline)

Use when the full book PDF is available but spawning sub-agents is unnecessary — the agent reads the extracted text directly and synthesizes chapter-level notes inline.

## When to Use

- Book is structured as tips/chapters (not dense technical reference)
- Each chapter is manageable (~10-50 pages) and self-contained
- Agent can hold chapter content in context while writing
- Faster than the sub-agent pipeline (no delegate_task overhead)
- Good for medium books: The Pragmatic Programmer (352pp), Clean Craftsmanship (519pp)

## Structure

```
Professionalism/book-name/
├── Book Overview.md              ← Chapter map with [[wikilinks]], core philosophy
├── 01 Chapter Name.md            ← One file per chapter, covering all topics in that chapter
├── 02 Chapter Name.md
└── ...
```

### Chapter File Format

```markdown
# NN Chapter Name (Topics X–Y)

Brief intro.

---

## Topic X: Key Concept

> Blockquote with the core quote from the book.

| Left | Right |
|------|-------|
| ... | ... |

---

## Topic Y: ...

...

---

## Sources

- Author. *Book Title*, Publisher, Year.
```

## Key Conventions

- **Chapter-level files, not topic-level.** A tip-based book (50 tips across 8 chapters) gets 8 files, not 50.
- **Blockquotes for memorable lines.** The book's voice matters — capture it.
- **Comparison tables** — ❌/✅, Manual/Automated, Before/After.
- **Sources section** — every file ends with `## Sources`.
- **Numbered chapters** — `01`, `02`, etc. for reading order.

## Proven On

- Clean Craftsmanship (519pp, 14 chapters, 3 parts) → 15 files
- The Pragmatic Programmer (352pp, 50 tips, 8 chapters) → 9 files
- Clean Agile (235pp, 7 chapters + Afterword) → 19 files (topic-level, chapter-level hybrid)

## Pitfalls

### Don't over-split
A tip-based book should NOT get one file per tip. Group by chapter. 50 tips → 8 files, not 50.

### Small PDF = probably a summary
If the PDF is ~27 pages with short chapters, it's a student/book summary. Ask if the user has the full version. Check file size — summary is typically under 1MB. Full book: 2-8MB.

### Chapter-level vs topic-level hybrid
For dense books (Clean Agile), some chapters get multiple files (business practices → 3 files). For tip-based books, one file per chapter. Judge by chapter density, not page count.
