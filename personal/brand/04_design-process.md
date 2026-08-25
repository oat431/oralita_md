---
date: 2026-08-25
version: "1.0"
status: Locked
tags: [branding, process, checklist, panomete, personal-use]
---

# Brand Design Process — Panomete (Personal Use)

> Phase 4 workflow of [[00_brand-roadmap]], adapted for personal use. The original checklist assumes a client engagement (questionnaires, sign-offs, delivery folders). Panomete is a personal design system — no client, no sign-off gates, no testimonial collection. This version removes the agency workflow and keeps only what a solo engineer needs to maintain the system.

## What's Different (personal vs client)

| Original (client) | Panomete (personal) |
| --- | --- |
| Send questionnaire to client | Skip — you are the client |
| Competitor screenshots ×5 | Inspiration anchor (daisyUI forest) — done |
| 2–3 palette options, client picks | 1 locked palette — done |
| Written approval on direction | Self-approved — done |
| Revise rounds (2 included, bill extra) | Iterate freely, no billing |
| Delivery folder + walkthrough video | Live HTML preview + Obsidian docs |
| Ask for testimonial | Skip |
| 90-day brand audit | Self-audit when adding new surfaces |

## Personal Design Process — Checklist

### A. Foundation (✅ Done 2026-08-25)

- [x] Decide scope: personal design system, not a full brand
- [x] Choose inspiration anchor: daisyUI forest theme
- [x] Pull real color values from source (not guessed)
- [x] Convert OKLCH → HEX/RGB/CMYK + verify WCAG
- [x] Lock strategy: personality, emotion, positioning

### B. Visual Identity (✅ Done 2026-08-25)

- [x] Color palette locked (3 tiers + status, all WCAG-verified)
- [x] Typography locked (Sarabun + JetBrains Mono)
- [x] Logo system locked (wordmark + animal submarks spec)
- [x] Supporting elements locked (icons, grid, imagery rules)

### C. Documentation (✅ Done 2026-08-25)

- [x] [[01_brand-strategy]] written and locked
- [x] [[02_visual-identity]] written and locked
- [x] [[03_style-guide]] assembled and locked
- [x] This process doc adapted

### D. Application (🔄 Ongoing)

When starting ANY new Panomete surface:

- [ ] Open [[03_style-guide]] first
- [ ] Use the CSS variables from §3 (or `data-theme="forest"` if using daisyUI)
- [ ] Load fonts from §4
- [ ] Follow §9 for the surface type (web UI, presentation, API docs)
- [ ] If a new component state is needed, use status tokens — don't invent new colors
- [ ] If a new animal submark is needed, draw it in Penpot on 24×24 grid

### E. Asset Creation (📋 Planned, not urgent)

- [ ] Draw 6 animal submark SVGs in Penpot (🦉🐑🐜🐷🐿️🦌)
- [ ] Export wordmark as SVG (Sarabun 700 typeset)
- [ ] Create favicon set (16/32/180/512px)
- [ ] Build a daisyUI custom theme file (`panomete` theme = forest values)

### F. Maintenance

- [ ] When daisyUI updates forest theme, diff the new OKLCH values against locked HEX
- [ ] If values drift, decide: update locked values or pin to v5.7.22
- [ ] Log all changes in §Versioning of [[03_style-guide]]

---

## Deliverables Status

| # | Item | Status | Location |
| --- | --- | --- | --- |
| 1 | Positioning + strategy sheet | ✅ Done | [[01_brand-strategy]] |
| 2 | Moodboard | ✅ Done | = daisyUI forest theme |
| 3 | Logo system (wordmark + submark spec) | ✅ Spec done, SVGs pending | [[02_visual-identity]] §4 |
| 4 | Color palette spec (HEX/RGB/CMYK) | ✅ Done | [[02_visual-identity]] §2 |
| 5 | Typography spec | ✅ Done | [[02_visual-identity]] §3 |
| 6 | Style board | ✅ Done | Live HTML preview |
| 7 | CI manual / guidelines | ✅ Done | [[03_style-guide]] |
| 8 | Organized asset folder | 📋 Planned | — |

---

## Quick Reference — The "No Second-Guessing" Card

> **Paste this at the top of any new Panomete project.**

```
THEME:     daisyUI forest (data-theme="forest")
BACKGROUND: #1B1717  ·  TEXT: #CAC9C9  ·  BRAND: #1FB854
ACCENTS:   #1EB88E (secondary)  ·  #1FB8AB (accent)
STATUS:    success #00A96E · warning #FFBE00 · error #FF5861 · info #00B5FF
FONT:      Sarabun (body/headings)  ·  JetBrains Mono (code)
GRID:      8pt spacing  ·  12-col / 24px gutter  ·  max 1200px
RADIUS:    selector 1rem · field 2rem · box 1rem · border 1px · flat (no shadows)
IMAGERY:   none — type + color + data viz only
```

---

> **Adapted from:** [[00_brand-roadmap]] Phase 4 checklist · **Profile:** Solo engineer / personal design system · **Live preview:** `panomete-palette-preview.html`
