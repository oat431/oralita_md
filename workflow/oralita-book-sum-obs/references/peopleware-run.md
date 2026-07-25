# Peopleware Run — Session Notes

**Session:** 2026-07-21
**Book:** Peopleware: Productive Projects and Teams, 3rd Edition
**Authors:** Tom DeMarco & Timothy Lister
**Format:** 272 pages, 4.3 MB, 39 chapters across 6 parts

## Run Summary

| Metric | Value |
|---|---|
| Files created | 5 chapter files + overview |
| Total size | 88 KB |
| Batches | 2 (3+2 due to max_concurrent_children=3) |
| Post-batch fixes | Frontmatter fix on 03 (date→created, quoted source) |

## Issue
File 03 frontmatter inconsistency: sub-agent used `date:` instead of `created:`, and unquoted source with em-dash (`Peopleware — Productive Projects`) breaking YAML parsing. Fixed to match 01 format: `created: 2026-07-21` and quoted source `"DeMarco & Lister, Peopleware: Productive Projects and Teams (3rd ed.)..."`.