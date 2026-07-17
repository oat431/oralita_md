---
name: obsidian-vault-filling
description: Fill incomplete Obsidian vaults from overview files + web sources. Identify gaps, write structured notes, add Mermaid diagrams, verify completeness.
---

# Obsidian Vault Filling

Take an incomplete Obsidian vault (overview/stubs only) and fill all missing topic notes with structured content, visuals, and cross-links.

## Overlap with `oralita-book-sum-obs`

For PDF-based book summarization, use `oralita-book-sum-obs` — it has the full extraction + sub-agent pipeline. For overview-driven vault filling from web sources or body-of-knowledge documents, use this skill. For the direct book synthesis pattern (reading extracted PDF text and writing chapter files inline), see `oralita-book-sum-obs` → `references/direct-book-synthesis.md`.

## Overlap with `obsidian-vault-builder`

These two skills cover similar territory. `obsidian-vault-builder` is the newer, more concise version created as a quick-reference. `obsidian-vault-filling` is the detailed reference with the full pitfall catalog. Prefer `obsidian-vault-builder` for quick runs; consult this skill when you hit edge cases (read_file quirks, ASCII removal, Mermaid syntax issues).

User points at a vault with an overview/MOC file and empty or stub topic notes. Common signs:
- Overview has `[[wikilinks]]` that don't resolve (dead links)
- Topic files exist but are bullet-point outlines only
- User says "fill the gap," "summarize this," "complete this vault"

## Workflow

### Phase 1: Survey

1. Read the overview/MOC file first — it's the map of what should exist.
2. Use `mcp_filesystem_directory_tree` to see the actual file structure.
3. Cross-reference: which `[[wikilinks]]` in the overview have no corresponding file?
4. Read a few existing content files to understand the style, depth, and format the user expects.
5. Present a gap analysis table **before** writing anything.

### Phase 2: Source Content

1. If the user provides a source URL (GeeksForGeeks, lawsofux.com, etc.), fetch it.
2. If the page is an SPA (React/Next.js), the raw HTML may have JSON-embedded content — parse it.
3. If the page is a portal (index of sub-topics), fetch specific sub-pages per topic.
4. For well-known topics (design patterns, grammar rules, UX laws), domain knowledge is sufficient — cite sources at the bottom.

### Phase 3: Write Notes

1. Create category folders with numbered prefixes: `01 Foundation/`, `02 Tenses & Time/`.
2. **Place files FLAT inside category folders** — do NOT create `Topic Name/Topic Name.md` wrapper folders. The filename is self-explanatory. A single topic = a single `.md` file inside its category.
3. Number individual files sequentially across the entire vault: `01 Parts of Speech.md`, `05 12 English Tense.md`, etc. The number tells the teaching/reading order.
4. Every note follows the same format:
   - Title with topic number
   - Core concept (one-sentence summary)
   - Structured sections with **tables** (preferred over walls of text)
   - `❌` / `✅` comparison patterns
   - Code examples where relevant (use ` ``` ` with language tag)
   - A "⚠️ Pitfalls" or "Common Mistakes" section
   - Quick test/quiz at the end (for learning-oriented vaults)
   - Sources section
5. Use `write_file` or `mcp_filesystem_write_file` — creates parent directories automatically.
6. If the user is Thai or teaching Thai speakers, include Thai-specific traps with Thai text examples.
7. For reference tables with priority/importance columns, sort by priority (🔴 → 🟡 → 🟢). See `references/reference-table-formatting.md`.

### Phase 4: Add Visuals

1. For web images: use `![](url)` with attribution in alt text. Source from lawsofux.com, Wikipedia, etc.
2. For UML/diagrams: use Mermaid code blocks. Obsidian renders ` ```mermaid ` natively.
3. For design patterns: classDiagram with standard GoF notation (`<|--` inheritance, `<|..` implementation, `*--` composition, `o--` aggregation, `-->` association, `..>` dependency).
4. After adding Mermaid, **remove ASCII art diagrams** — they're redundant. ASCII art lives in ` ``` ` blocks with box-drawing characters (┌└├┐┘┤─│).

### Phase 5: Verify

1. Use `mcp_filesystem_directory_tree` to confirm all files exist.
2. Use `execute_code` with `os.listdir` to programmatically verify every file has required elements.
3. Update the overview to add proper `[[wikilinks]]` for all topics.
4. Rewrite the overview if it's a stub — make it a proper teaching roadmap with routes.

## Pitfalls

### read_file quirks
- `read_file(path)` (no limit) returns `{"content_returned": "..."}` with line number prefixes like `42|` on each line.
- `read_file(path, limit=N)` returns `{"content": "..."}` without prefixes.
- Always check which key you're getting before processing the output.

### patch precision
- `patch()` with `old_string` must be **exact** including whitespace, newlines, and trailing characters.
- When removing blocks between headings, include enough context lines to make the match unique.
- An imprecise patch can eat adjacent content — always verify the result.
- After any batch of patches, spot-check surrounding content in the target files.

### ASCII art removal
- Box-drawing characters to scan for: `┌└├┐┘┤─│┬┴┼`
- Some ASCII diagrams aren't in ` ``` ` blocks — check with `execute_code` using `os.listdir` + `any(c in content for c in ascii_chars)`.
- After bulk removal, **always re-verify** all files still have their Mermaid diagrams. Removing ASCII blocks can accidentally eat adjacent Mermaid blocks if the regex/patch isn't precise.
- Check: `if "```mermaid" not in content` per file. Fix any missing ones by re-adding the Mermaid diagram.
- A regex for fenced ASCII blocks: `re.search(r'\n?```\n.*?```', content, re.DOTALL)`.

### Mermaid syntax
- Never put plain text inside a ` ```mermaid ` block — only valid Mermaid syntax.
- `<<interface>>` for interface classes, `<<abstract>>` for abstract classes.
- Use `~` for generics: `List~Component~`.
- `*` after method name for abstract methods: `+makeSound()*`

### Checklist simplification (ponytail mode)

When a vault contains verbose reference checklists (200+ lines with tutorials, code examples, version trivia), create simplified launch checklists:
- Strip tutorials, code examples, and version-specific details
- Keep only tick boxes (`- [ ]`) with one-line descriptions
- Link to vault notes (`→ [[vault-note]]`) instead of embedding explanations
- Target ~40-50 items per file
- Keep the original as deep reference; create a sibling `-v2.md` or `-launch.md`

Pattern: `spring-boot-api.md` (263 lines) → `API Launch.md` (45 items). The launch checklist references the original for deep dives.

For framework-specific checklists, the full pattern is:
1. **Generic Launch** — framework-agnostic, tick-first (`API Launch.md`, `Frontend Launch.md`, `Microservice Launch.md`)
2. **Framework Reference** — detailed v1 with version-specific config, code examples, tech comparisons (`spring-boot-api.md`, `react-js.md`, `api-gateway.md`)
3. **Framework Launch (v2)** — stripped checklist, ~50 items, references both the generic Launch and the framework reference (`react-js-v2.md`, `api-gateway-v2.md`)

Each framework gets its own file in the same folder: `backend-checklist/` holds `API Launch.md` + `spring-boot-api.md` + `fiber-v3-api.md` + `nestjs-api.md` + `rust-axum-api.md`. Similarly for frontend and microservice folders.

### Post-fill maintenance

After filling a vault, additional operations may be needed:
- **Batch tagging**: Add `tags: [...]` YAML frontmatter to all files for Obsidian's graph/filter. See `references/batch-tagging.md` for the Python script, rule design, and false-match cleanup.
- **Wikilink fixing**: Scan all `[[wikilinks]]` across the vault, cross-reference against actual files, and batch-fix broken links. See `references/wikilink-fixing.md` for the full scan→map→fix pipeline.
