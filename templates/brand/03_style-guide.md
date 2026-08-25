---
date: 2026-08-25
tags: [branding, template, style-guide, guidelines, ci-manual]
---

# Style Guide (CI Manual) — Document Skeleton

> Phase 3 of [[00_brand-roadmap]]. Turns strategy ([[01_brand-strategy]]) + identity ([[02_visual-identity]]) into ONE reference doc anyone can follow without asking a designer. Copy as `YYYYMMDD-<brand>-guidelines.md` (or export to PDF/slides for sharing).

## The 10 Sections

### 0. Cover & Intro
Brand name, version, date, owner, one-line mission. State what the doc covers and who must follow it.

### 1. Brand Foundation
Mission · vision · values · positioning statement · personality adjectives. Copied verbatim from strategy — this justifies every visual rule that follows.

### 2. Logo Usage
All variants displayed at actual sizes · clearspace diagram · minimum size · approved/rejected background examples · **don'ts row** (stretched, rotated, recolored, shadowed — show each violation crossed out).

### 3. Color
Swatch table with **all three models**: HEX (web) · RGB (screen/social) · CMYK (print) · usage ratio guidance (e.g. 60% neutral / 30% primary / 10% secondary).

### 4. Typography
Font names + licenses · full hierarchy table (H1→caption with weight/size/line-height) · web fallback stack · do/don't examples (no fake bold, no tight tracking on body).

### 5. Voice & Tone
Do-say / don't-say word lists · sample rewrite (boring sentence → brand sentence) · tone-per-channel mini-table (support ≠ launch post ≠ error message).

### 6. Imagery & Photography
Style rules, color grade, composition do/don't pairs, stock-photo selection criteria.

### 7. Iconography & Graphic Elements
Icon style spec (grid, stroke, radius), pattern usage rules, illustration boundaries.

### 8. Layout & Grid
Grid specs + templates for recurring formats: social posts, slides, documents, signage.

### 9. Digital Applications ← *your UX/UI + PowerPoint layer*
| Touchpoint | Spec to pin down |
| --- | --- |
| Web/product UI | buttons, forms, states using brand tokens |
| Social | avatar crops, post templates, story frames |
| Email | header/footer blocks, CTA style |
| **Presentations** | master slides, chart colors = palette tier, title/body styles |

### 10. Assets & Downloads
Where files live (link), naming convention, who approves exceptions, changelog.

## Production Rules

- **Show, don't tell:** every rule paired with a ✓ correct and ✗ incorrect visual example
- **Practical over exhaustive:** a guide teams actually open beats a 200-page book nobody reads
- **Living document:** version + date on cover; log changes in §10

## Versioning Block (fill per release)

```markdown
Version: 1.__   Date: YYYY-MM-DD
Changed by: 
Sections touched: 
Changelog: 
```

## Format Decision

| Format | Use when |
| --- | --- |
| PDF | small team, vendor handoff, print |
| Online hub (Frontify-style) | multiple teams/products, frequent updates — see IBM, Starbucks, Firefox, Klarna portals |
| Notion/Obsidian page | internal-first, fast iteration |
