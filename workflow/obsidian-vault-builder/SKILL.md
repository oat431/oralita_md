---
name: obsidian-vault-builder
description: Build out incomplete Obsidian vaults from skeleton overview files. When the user has a vault with an overview/MOC file but missing topic notes, follow this pipeline to fill every gap.
category: note-taking
---

# Obsidian Vault Builder

When the user has an Obsidian vault with an overview (MOC) file full of `[[wikilinks]]` or bullet-point topics, but the actual topic notes are missing or stubs — fill every gap.

## Pipeline

### -2. Complete Vault Audit (when user says "review everything")

When the user wants ALL sections reviewed (not just one), iterate section by section:

1. Read the root index (`Programming Note Content.md` or equivalent) to get the full section list
2. For each section: read all files → give the three-tier assessment → move to next
3. After all sections: provide a summary table (section × status)
4. The user will typically say "next topic" between sections — don't dump everything at once
5. Only propose new content AFTER completing the full audit — user may want to prioritize differently

**Key insight:** Look for TWO types of gaps:
- **"What to know"** — missing knowledge domains (Algorithms, Database, etc.)
- **"How to work"** — missing engineering craft (Git, Clean Code, Design Patterns, CI/CD)

The vault may have excellent coverage of CS topics but zero coverage of daily engineering workflows.

### -1. Review & Fill Gaps (when user asks "review section X")

When the user says "review X" or "check if anything is missing in Y" — they want a **gap analysis**, not a full rebuild. This is a different workflow from building from overviews.

**Steps:**
1. Read ALL files in the section (not just the overview) — use `mcp_filesystem_read_multiple_files` for efficiency
2. Give a structured assessment with three tiers:
   - ✅ **What's solid** — list each file with a one-line quality verdict
   - ⚠️ **What's missing** — gaps with impact level (🔴 High / 🟡 Medium / 🟢 Low)
   - ❌ **What's not needed** — topics that sound relevant but are covered elsewhere or aren't worth adding
3. Make specific recommendations: "create new file" vs "patch existing file" vs "no action needed"
4. Wait for user confirmation before creating anything

**When to CREATE a new file vs PATCH an existing one:**

| Signal | Action |
|--------|--------|
| Topic is a broad domain with 5+ distinct sub-areas | Create new file (e.g., String Algorithms, Math Algorithms) |
| Topic is a single concept/paradigm that fits in 8-12KB | Create new file (e.g., Functional Programming, Deque) |
| 3 small additions to one topic (error format, CORS, idempotency) | Patch existing file — don't create a 3KB standalone |
| Topic already has deep coverage in another vault | Don't duplicate — at most create a fundamentals-level note with cross-vault link |
| Topic is niche/advanced and the section is already comprehensive | Skip — tell the user it's not needed |

### 0. Cross-Vault Deduplication (BEFORE building)

When the vault is part of a multi-vault workspace (e.g. `programming-note/` alongside `software-engineering-note/`), check related vaults for existing coverage BEFORE creating new content. The user may already have deep book-level notes on the topic elsewhere.

- List sibling vault directories. Read their overviews/indices.
- If a topic already has substantial coverage in another vault, **don't duplicate it** at the same depth. Instead:
  - Create a fundamentals-level reference in the target vault (teaching-quality, not book-level)
  - Add a note pointing to the deeper content: `> For deep architectural coverage: see [[Topic]] in software-engineering-note`
  - Ask the user: "X already has book-level coverage in vault Y. Do you want a teaching-level note here, or should I skip it?"
- If a topic has ZERO coverage across all vaults, it's a genuine gap — build it.

### 1. Analyze the Gap

- Read the overview file. Extract all topics that need notes.
- `search_files` with `target="files"` to find existing `.md` files.
- Cross-reference: which topics in the overview have NO corresponding file?
- **Decide structure**: Is this a broad domain (Algorithm, Database) → multi-file section? Or a single concept/paradigm (OOP, FP, Error Handling) → one file? Don't over-split.

### 2. Propose Structure

Present the gap analysis as a table. Propose the folder structure before building:

```
├── 01 Category/
│   ├── 01 Topic.md
│   └── 02 Topic.md
├── 02 Category/
```

Ask if the user wants to proceed. Once confirmed, create directories in one batch.

### 3.5 Match Existing Style

Read 2-3 existing content files from DIFFERENT sections of the vault before writing. Extract the exact conventions:
- YAML frontmatter format (inline `tags:` vs array)
- Table style (alignment, column names)
- Code example conventions (primary language, secondary languages)
- Emoji usage (❌/✅, 🔴🟡🟢, ⚠️)
- Section divider style (`---`)
- Sources section format
- How `[[wikilinks]]` are used (inline vs `> [[link]]` bullet format)

New files must be indistinguishable from existing ones. If the vault uses Java-primary code with Python secondary, don't suddenly write TypeScript-primary notes.

### 4. Write Content — Batch Strategy

- Write ALL files. Don't stop after 2-3 — the user wants the vault filled.
- Use `write_file` for new notes; `patch` for existing ones needing updates.
- Batch independent writes together for speed.
- Update the overview to add proper `[[wikilinks]]` where missing.

### 4. Content Standards for Every Note

Each note must include:
- **Tables** for comparisons, rules, concepts
- **Code examples** where relevant (Java/Spring Boot preferred for backend; YAML for config; pseudocode for language-agnostic patterns)
- **Mermaid diagrams** (`classDiagram`, `sequenceDiagram`, `graph`, `stateDiagram-v2`) — prefer Mermaid over ASCII art
- **Sources** section with books, URLs, RFCs
- For learning/teaching vaults: add "⚠️ Thai Speaker Traps" sections with ❌/✅ examples
- For SE vaults: add "Why This Matters" or practical application tables

### 4.5 Update Parent Index

If the vault has a root-level content index file (e.g. `Programming Note Content.md`), update it to include the new section with a table row linking to the section overview. Don't leave the parent index stale.

### 5. Verify

After all writes, verify with a temp Python script that:
- All expected files exist
- Minimum file size (>500 bytes)
- Mermaid blocks don't contain broken content
- Sources sections present
- Overview has updated wikilinks

### ASCII → Mermaid Conversion Rules

When converting ASCII diagrams to Mermaid, use this decision framework:

**Convert to Mermaid** (flow/sequence/state):
- Arrow chains showing process flow → `graph LR` or `graph TD`
- Request/response sequences → `sequenceDiagram`
- State transitions → `stateDiagram-v2`
- Pipeline stages → `graph LR`
- Architecture connections → `graph LR`

**Keep as ASCII** (spatial/structural where position IS meaning):
- Memory layouts (stack grows ↓, heap grows ↑ — spatial direction matters)
- Process memory maps (Code/Data/Heap/Stack relative positions)
- Binary representations (IPv4 bit positions, page table entries)
- Inverted indexes (word → doc ID alignment)

**The rule:** If the diagram shows **flow or sequence** → Mermaid. If it shows **spatial structure where position carries meaning** → keep ASCII.

When doing bulk conversion, process in batches of 7-8 files per subagent. Read each file first, then write the full updated content. Keep all non-diagram content exactly as-is.

### 6. Clean Up Previous Format

If the vault previously had:
- ASCII art diagrams → replace with Mermaid, then strip ASCII
- Flat topic folders wrapping single files → flatten or consolidate
- Stub overviews → rewrite as proper MOCs with reading routes

## Folder Structure Rules

| Vault Size | Structure |
|-----------|-----------|
| Small (< 10 topics) | Flat files in root |
| Medium (10-25) | Category folders + numbered files |
| Large (25+) | Category folders + numbered files + overview indexes |
| Topics with sub-topics | Sub-folder (e.g., `05 12 English Tense/` containing `05.1`, `05.2`, ...) |

## Key Patterns from Past Vaults

- **Math for SE**: 12 topics, one folder per topic (each topic self-contained)
- **English Skill**: 27 topics, 8 category folders, numbered globally (01-27)
- **HCI/UI/UX**: 29 topics, 4 category folders, embedded images from lawsofux.com
- **Design Patterns**: 22 patterns + OOP intro, Mermaid classDiagram added to existing content
- **Microservices**: 19 topics, 7 categories, overview moved into folder
- **API Design**: 10 topics, 4 categories, protocol comparison guides
- **Programming Fundamentals**: 12 topics (01-09 + overview), 1 flat folder, Java-primary + multi-language secondary, cross-vault links to `software-engineering-note`. Paradigms (OOP, FP) as single files; broad domains (Algorithm, Database) as multi-file sections in sibling folders.
- **programming-note vault review**: Section-by-section gap analysis across entire vault (12 sections, ~131 files). Read all files per section (not just overview). Three-tier assessment (✅ solid / ⚠️ missing / ❌ not needed). Content decisions: paradigms → single file, domains → multi-file, small additions → patch existing, quick-references for book summaries → lightweight lookup. Cross-vault check against `software-engineering-note` before creating. Full style conventions in `references/programming-note-vault-style.md`. Key insight: the vault covers "what to know" (knowledge domains) — when reviewing, also look for "how to work" (engineering craft) gaps like Git, Clean Code, Design Patterns.
- **programming-note vault sections**: Fundamental (15), Algorithm (17), API (12), Computer Networks (10), Cybersecurity (13), Database (10), Microservice (19), Operating Systems (10), QA (13), Design Patterns (4), Version Control (4), Clean Code (4). Each section follows the same style conventions documented in `references/programming-note-vault-style.md`.
- **programming-note ASCII→Mermaid pass**: Converted ~15 files from ASCII diagrams to Mermaid where appropriate. Key decision: convert flows/sequences/state diagrams, keep spatial/structural layouts (memory maps, binary representations) as ASCII. Delegated in 2 parallel batches of 7-8 files each. Pattern: read file → identify ASCII blocks → replace with ```mermaid``` → write full file.
- **programming-note final sections**: Added Design Patterns (4 files), Version Control (4 files), Clean Code (4 files), plus standalone Fundamental files (Data Formats, Logging, Regex, CI/CD, Docker). Total: 131 files across 12 sections.

## Cross-Vault Linking (separate Obsidian vaults)

When two vaults are separate Obsidian vaults (not just subfolders), wikilinks like `[[Topic]]` won't resolve across vaults. Use this pattern instead:

1. Add a `## Book Deep Dive` or `## Deep Dives in <vault-name>` section before Sources
2. Use file paths (not wikilinks) to reference the sibling vault: `software-engineering-note/Software Design/Design Pattern/02-Creational/builder.md`
3. Add a table mapping quick-reference topics to their book-level counterparts
4. Clarify the relationship: "The notes here are **quick references**. The book summaries are **deep dives**."

Example from Design Patterns overview:
```
## Deep Dives in software-engineering-note

For book-level depth on each pattern, see the **Design Pattern** section in `software-engineering-note/Software Design/Design Pattern/`:

| Pattern | Book Summary |
|---------|-------------|
| Singleton, Factory Method, Builder | `02-Creational/` — each with intent, structure, Java examples |
| Adapter, Decorator, Facade, Proxy | `03-Structural/` — each with UML, real-world usage |
```

Also update the parent index (`Programming Note Content.md`) with a table row for each new section.

## Batch Delegation Pitfalls

When dispatching parallel subagent batches for file creation/conversion:
- **Verify before re-dispatching.** If you dispatch a re-run because you think the first batch failed, check the actual file state first (search for mermaid blocks, read file headers). A batch that appears to "fail" in its report may have actually succeeded — patches fail because the old text is already gone.
- **Don't dispatch 3 batches when 2 suffice.** If batch 1 is slow, wait for it before dispatching a replacement. Running in parallel means the replacement will also fail (file already modified).
- **Patch vs full rewrite.** Patches are faster but fragile with special characters (ASCII art, Unicode arrows). If patches fail on the first attempt, fall back to read-full-file → write-full-file immediately — don't retry patches.
