---
name: vault-completion
description: "Fill missing Obsidian vault notes from overview/MOC files with wikilinks, Mermaid diagrams, ASCII removal, cross-vault linking, and content migration from old stubs to new vaults."
---

# Vault Completion

Complete workflow for filling Panomete's Obsidian vaults from overview files. Covers gap analysis, note format preferences, Mermaid diagram insertion, cross-vault linking, and content migration.

## When to Use

- User has an Overview/MOC file with `[[wikilinks]]` pointing to non-existent notes
- "Fill in the missing notes", "Complete the vault", "Summarize X based on the overview"
- User has an old stub note that needs expanding into a full topic vault
- User wants Mermaid diagrams added to existing pattern/architecture notes

## Core Workflow

1. **Read source material** — reference document (SWEBOK chapter, book TOC, website)
2. **Read the Overview/MOC** — identify dead `[[wikilinks]]` vs existing files
3. **Present gap analysis** — table: Topic | In Overview? | Has Note? | Status
4. **Fill missing notes** — synthesize from source + your knowledge. Priority: user-specified URL → provided reference → own knowledge
5. **Update Overview** — add `[[wikilinks]]` to plain-text headings
6. **Verify** — run verification script: file count, size >1KB, Sources present, Mermaid valid

## Note Format

- `# Topic N: Title` + brief intro
- Tables over prose for rules, comparisons, patterns
- `## When to Use` with categorized examples
- `## Comparison` for similar/confusable concepts (use ❌/✅ pairs)
- `## Practical Applications` — "Why This Matters in SE" or equivalent
- `⚠️ Target-Audience Traps` — dedicated error-pattern section if teaching specific audience (Thai speakers, etc.)
- `## Quick Test` — 5 questions with answers
- `## Sources` — cite reference material

### Style Rules
- Tables > prose, bold keywords, scannable, practical not academic
- ❌/✅ pairs for immediate contrast
- Images: `![](url)` from authoritative sources only — never fabricate URLs

## Directory Structure

- **Category folders** with numbered prefixes: `01 Foundation/`, `02 Tenses & Time/`
- **Flat files inside** — NOT folder-per-topic. `Topic Name.md` goes directly in its category folder
- Files numbered for teaching order: `01 Parts of Speech.md`, `02 Articles.md`
- For sub-topics needing individual files: subfolder with Overview index: `05 12 English Tense/` containing `05 12 English Tense Overview.md` + `05.1 Present Simple.md` through `05.12 Future Perfect Continuous.md`
- **Sub-topic folder pattern:** when a topic naturally splits into many sub-topics (e.g., 12 tenses, 22 design patterns, 15 UX laws), create a numbered subfolder containing an overview index and individual numbered files. The folder replaces the single `.md` file: `05 12 English Tense/` instead of `05 12 English Tense.md`. Individual sub-topic files use decimal numbering: `05.1`, `05.2`, `05.12`.
- Overview file lives at vault root OR inside the topic folder (when there are many files)

## Mermaid Diagrams

Obsidian renders Mermaid natively. Prefer over ASCII art for design patterns, architecture, flows.

### When to Add Mermaid
- **classDiagram** — design patterns, OOP, architecture components
- **sequenceDiagram** — API flows, auth, Saga orchestration, event chains
- **graph TD/LR** — deployment pipelines, decision trees, protocol flows
- **stateDiagram-v2** — circuit breaker, order lifecycle, auth states

### GoF Design Pattern Conventions
- Interfaces: `<<interface>>`, Abstract classes: `<<abstract>>`
- Relationships: `..>` (Dependency), `-->` (Association), `o--` (Aggregation), `*--` (Composition), `..|>` (Implementation), `<|--` (Inheritance)
- Keep diagrams focused — pattern participants, not every method

### ASCII Removal Workflow
1. Add Mermaid alongside existing ASCII — don't delete ASCII yet
2. Once all files have Mermaid, ASK before stripping ASCII
3. Batch-remove with Python script using `patch()` or direct file writes
4. Verify: no `┌└├┐┘┤─│┬┴┼` chars remain
5. Re-verify: all files still have ````mermaid` blocks, no broken mermaid (plain text inside mermaid fence)

### Mermaid Verification
Check all files:
- ````mermaid` present
- First line after fence is a valid diagram type
- No plain text accidentally pulled into mermaid block during edits

## Cross-Vault Linking

When a topic spans vaults (programming-note stubs ↔ software-engineering-note deep content):
1. Identify overlap — compare both vaults
2. Fill the stub vault with practical notes + Mermaid
3. Cross-link from overview: "For philosophy see [[Boundaries]] in Clean Architecture"
4. Update Content.md to route to new full notes
5. Remove old stub after verification

## Content Migration (Stub -> Full Vault)

1. Create `Topic/` folder with overview + category subfolders + numbered topic files
2. Move content from old stub into new overview (preserve: personal experiments, GitHub links, home server configs)
3. Update root Content.md to reference `[[Topic Overview]]`
4. Delete old stub file
5. Verify: old file gone, folder has correct count, Content.md updated

## Content Hub Pattern (programming-note)

When a vault root has a `Content.md` that links to both stubs and full vaults:
- Rewrite it as a routing table: Topic | Primary Content | Local Note
- When a stub becomes a full vault, update the routing table — both columns point to `[[New Overview]]`
- The Content.md becomes a compass: quick stubs for scanning, deep vaults for learning
- Keep unique local content (personal GitHub repos, home server configs) in the new overview

## Stub Removal Workflow

1. Create full vault folder with overview + category subfolders + numbered topic files
2. Verify all content from old stub is covered in new vault
3. Run verification script (file count, Sources sections, Mermaid validity)
4. Update root Content.md routing table
5. `rm` the old stub file
6. Re-verify old stub is gone + Content.md has correct link

## Batch Construction

For large vaults (>10 files):
1. Create ALL directories first — single `mkdir -p` with all paths
2. Write files in parallel batches (write_file is independent per file)
3. After all writes, run verification script
4. Update overview and Content.md last

## Verification Script Pattern

Use `execute_code` with tempfile scripts that check:
- File count matches expected
- All files > 1KB (not stubs)
- `## Sources` section present in every file
- ````mermaid` blocks have valid diagram types (no plain text in mermaid fence)
- Overview has sufficient wikilinks (≥ half the file count)
- Content.md references correct overview name

```python
# Skeleton verification script
import os, re, tempfile
verify = r"""...checks..."""
tmp = os.path.join(tempfile.gettempdir(), "hermes-verify-<vault>.py")
with open(tmp, "w") as f: f.write(verify)
rc = os.system(f'python "{tmp}"')
os.remove(tmp)
```

## Anti-patterns

- Don't build academic syllabi for practical teaching — ask about the target student
- Don't over-engineer taxonomy — >8 categories is too many. User rejected 8-section English structure.
- Don't create `Topic/Topic.md` folder-per-file wrappers — flat files in category folders
- Don't write walls of prose — tables, bullets, headers
- Don't skip gap analysis — show what's being filled before writing
- Don't fabricate image URLs — use authoritative sources or skip
- Don't delete ASCII before Mermaid is confirmed working
- Don't leave broken Mermaid blocks — verify after edits
- Don't rename files on disk while also changing wikilinks — use `patch()` on content, `mv` for files, update references after
- Don't remove the old stub until the new vault is verified complete
- **Summary vs complete book:** a PDF under 1MB with ~27 pages is a student summary. The user may later provide the 2-8MB, 200+ page complete book. Don't rewrite — add missing chapters and enrich existing files with the full book's depth (personal stories, examples, additional sections). Use `ls -la` to check file size before extraction.

## Bulk Tagging

Add Obsidian YAML frontmatter `tags: [...]` to all `.md` files based on vault path and folder structure.

### Tag Hierarchy
- **Vault-level tag** based on root folder: `programming`, `software-engineering`, `fitness`, `english`, `math`
- **Sub-tags** from folder names: `database`, `api`, `networking`, `book-summary`, `design-patterns`
- **Book summaries:** add `book-summary` + author tag (`uncle-bob`, `pragmatic-programmer`)
- **Overview/MOC files:** add `overview` tag
- **Respect existing frontmatter:** merge new tags into existing YAML frontmatter. Don't overwrite user's existing tags.

### Tag Cleanup
After initial tagging, scan for false matches:
- `grammar`/`foundation` leaking into software-engineering files (folder name overlap)
- `discrete-math`/`graphs` hitting GraphQL or database graph files
- `clean-code` hitting `clean-coder` files
Remove false matches with a second pass.

### Script Reference
See `scripts/tag-vault.py` for the bulk tagging + cleanup script.

## Wikilink Repair

Find and fix broken `[[wikilinks]]` across all vaults. Obsidian resolves wikilinks by filename (not path), so map broken names to correct filenames.

### Common Breakage Patterns
- **Wrong chapter numbers:** SWEBOK files reference old numbering (`06_` → `08_`)
- **Case mismatches:** `[[SOLID Principles]]` → `[[solid-principles]]`
- **Renamed files:** `[[03 Migration & Versioning]]` → `[[03 Migration Backup & Scaling]]`
- **Folder links:** `[[01 Gestalt Laws/]]` → `[[01 Law of Proximity]]` (filename-only)
- **Cross-vault links:** use Obsidian's `../vault-name/Note Name` format

### Approach
1. Build a set of all existing filenames (case-insensitive)
2. Scan all `.md` files for `[[wikilinks]]`
3. For each broken link, find the closest matching existing file
4. Batch-replace with correct targets
5. Re-scan to verify count goes to zero (except user's personal notes)

### Script Reference
See `scripts/fix-wikilinks.py` for the bulk repair script.

### Script Reference
See `scripts/fix-wikilinks.py` for the bulk repair script.

## Checklist Simplification (Ponytail Mode)

When user invokes ponytail skill on checklists: turn overengineered reference manuals into actual tick-box checklists.

### Pattern
- **Reference manual** (100-300 lines): code examples, version trivia, tutorials, migration notes → stays as reference
- **Launch checklist** (30-50 lines): `- [ ]` tick boxes, one-liners, `→ [[vault]]` links for deep knowledge
- Each checklist file lives in its domain folder next to the reference files

### Two-Layer Checklist Architecture

The generic + framework companion pattern. One framework-agnostic launch checklist, then framework-specific companions that inherit from it:

```
backend-checklist/
├── API Launch.md              ← Generic: tick first, 45 items
├── spring-boot-api.md          ← Reference manual (263 lines)
├── fiber-v3-api.md             ← Go/Fiber companion, ~80 items
├── nestjs-api.md               ← NestJS companion, ~75 items
└── rust-axum-api.md            ← Rust/Axum companion, ~80 items

frontend-checklist/
├── Frontend Launch.md          ← Generic: tick first, 48 items
├── react-js.md                 ← Reference manual (134 lines)
├── react-js-v2.md              ← React/Next.js launch companion, ~55 items
├── vue-js.md                   ← Vue 3 + Nuxt companion, ~70 items
└── angular.md                  ← Angular 17+ companion, ~80 items
```

Each framework companion: references the generic (`Tick [[API Launch]] first`), adds framework-specific items (middleware chain, DI, build tools), and follows the same section structure as the generic for consistency.

### Rules
- No code examples in launch checklists (generic or companion)
- No version-specific trivia
- No tutorials
- Every item: `- [ ] Short action → [[vault note]]` for how
- Keep original deep-reference files — don't delete, just add the slim version
- Framework companions should have the same top-level sections as the generic for easy cross-referencing
- After building a companion, **cross-check** all companions in the same domain: if NestJS has a Swagger section but Fiber doesn't, add it to Fiber too
- When a user asks "what framework for X?", give a one-line recommendation with brief rationale before building the checklist

### Pitfalls
- **Missing form validation:** checklists under "State & Data" or "Forms" should include both client-side validation (Zod, class-validator) AND server-side re-validation (client UX, server security). User caught this gap in Frontend Launch.
- **Inconsistent companions:** after creating a new framework companion, scan the others for sections the new one introduced that the old ones lack (e.g., Swagger/OpenAPI, Form validation, Observability)
