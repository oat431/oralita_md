---
name: obsidian-vault-maintenance
description: Detect and fix broken wikilinks, add YAML frontmatter tags, and run batch maintenance on Obsidian vaults.
category: note-taking
---

# Obsidian Vault Maintenance

Maintenance operations that keep a multi-vault Obsidian setup healthy: wikilink fixing and batch tagging.

## When to Load

- User says "fix broken backlinks", "wikilinks are wrong", or "check my links"
- User wants to add tags to all notes
- After major vault restructuring (renames, moves, consolidations)

## Broken Wikilink Detection & Fixing

When the user notices broken backlinks, follow the workflow in `references/wikilink-fixer.md`:
1. Scan all `.md` files for `[[wikilinks]]` that don't resolve
2. Build a correction mapping (`broken_text → correct_target`)
3. Batch-apply fixes to all affected files
4. **Re-scan after each pass** — first pass rarely catches everything
5. Repeat until zero broken links remain (typically 2-3 passes)

Key rules:
- Obsidian resolves by filename, not path — `[[01 Law of Proximity]]` works across any folder
- Handle aliases: `[[broken||alias]]` → `[[correct|alias]]`
- Leave user's personal notes (daily notes, memory) alone — only fix knowledge vaults
- **Concept-only links** (no file exists, e.g. `[[viruses]]`, `[[CRM]]`) → convert to **bold text**, don't delete
- **Path-qualified links** (`[[BABOK/Note]]`, `[[../dir/Note]]`) → flatten to `[[Note]]` (Obsidian resolves by filename)
- **Folder-style links** (`[[02-Creational/]]`) → remove entirely
- **Placeholder text** (`[[wikilinks]]`, `[[Related Topic]]`) → remove entirely
- **Backslash in links** (`[[Note\|alias]]`) → fix to `[[Note|alias]]` (single `\` is common, not just `\\`)

### Multi-Pass Strategy

Most vaults need 2-3 passes. Each pass should re-scan before deciding what to fix next:
- **Pass 1**: Numbered cross-refs (off-by-one chapter numbers), relative paths, profile name mismatches, backslash cleanup
- **Pass 2**: Remaining wrong chapter numbers, path-qualified links, folder-style links
- **Pass 3**: Catch-all — convert all remaining broken links to bold via regex replacement

See `references/wikilink-fixer.md` for the full Python script and correction patterns.

## Batch Tagging

When the user wants to add Obsidian tags (`tags: [...]` in YAML frontmatter) to all notes, follow `references/batch-tagger.md`:
1. Define tag rules as `(path_fragment, tags)` pairs — vault-level, category, and special tags
2. Process all `.md` files: parse existing frontmatter, merge tags, write back
3. Run cleanup pass for false matches (e.g., `foundation` tag leaking into software-engineering folders)

See `references/batch-tagger.md` for the full Python script and tagging conventions.

## Pitfalls

- **Obsidian is a bundled skill** — do not try to edit it. This skill is a companion.
- **False tag matches**: substring matching on path fragments means `GraphQL.md` matches `("Graph", ["graphs"])`. Always run cleanup.
- **User's personal notes**: skip files in `Personal Project/`, `Quick Note/`, `memory/`, and any with `2026-06-` date patterns (daily notes).
- **Single-pass is never enough**: real vaults need 2-3 fix passes. Always re-scan between passes.
- **Backslash encoding**: Python `repr()` shows `\\` for a single backslash (0x5C). Don't confuse this with actual double-backslash. Check raw bytes if unsure. Use `\\+` in regex to match either.
- **Catch-all ordering**: The final "convert remaining broken links to bold" pass MUST run last — after all targeted number/path/name fixes. Running it early converts fixable links into bold text.
- **Concept links are content**: `[[viruses]]` in a cybersecurity note is meaningful — convert to `**viruses**`, don't delete. Only remove true placeholders like `[[wikilinks]]` or `[[Related Topic]]`.
- **Path-qualified links**: Obsidian resolves by filename, not path. `[[BABOK/Note]]` and `[[../dir/Note]]` should flatten to `[[Note]]` — but only if the filename is unique across the vault. Check with the diagnostic scan first.
- **Chapter numbering mismatches**: BOK vaults often use spec chapter numbers (1-22) while vault files use zero-indexed (00-20). Always check actual filenames before building the mapping.
