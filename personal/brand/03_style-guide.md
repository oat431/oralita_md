---
date: 2026-08-25
version: "1.0"
status: Locked
tags: [branding, style-guide, ci-manual, panomete, locked]
---

# Panomete Style Guide (CI Manual)

> Phase 3 of [[00_brand-roadmap]]. **Status: LOCKED 2026-08-25.** Turns strategy ([[01_brand-strategy]]) + identity ([[02_visual-identity]]) into ONE reference anyone can follow without asking a designer. This is the document you open before starting any Panomete surface.

---

## 0. Cover & Intro

| Field | Value |
| --- | --- |
| **Brand** | Panomete |
| **Version** | 1.0 |
| **Date** | 2026-08-25 |
| **Owner** | Sahachan (`flowero`) |
| **Mission** | Build a personal design system so every project ships with zero visual deliberation. |
| **Scope** | All surfaces under `*.panomete.com`, all knowledge-base decks, all project documentation. |
| **Who must follow** | Myself, and any tool/agent building Panomete surfaces. |

---

## 1. Brand Foundation

**Positioning:** For a software engineer who builds personal projects and knowledge decks, Panomete is the personal design system that eliminates visual second-guessing. Unlike ad-hoc per-project styling, every surface uses one locked token system.

**Personality:** Technical / Confident / Understated

**Emotion:** Confidence — "this person knows what they're doing"

**Voice:** Short, direct, no hype. Technical terms where precise. "Deploy", "configure", "verify" — never "unleash", "empower", "transform".

---

## 2. Logo Usage

### Primary Wordmark

```
"Panomete" in Sarabun 700, letter-spacing -0.02em
"Pano" = base-content (#CAC9C9)  |  "mete" = primary (#1FB854)
```

**Rules:**
- Clearspace = height of "P" on all sides
- Minimum size: 120px digital / 30mm print
- Approved backgrounds: base-100 (dark) or white/light
- Variants: full color · reversed · single black

**Don'ts:** ✗ no stretch · ✗ no rotate · ✗ no drop shadow · ✗ no recolor outside palette · ✗ no outline/stroke · ✗ no rebuilding the two-tone split

### Animal Submarks (per-project)

| Service | Code Name | Animal |
| --- | --- | --- |
| Blog | Cute Gufo | 🦉 |
| URL Shortener | Fluffy Mouton | 🐑 |
| Todo List | Tiny Mchwa | 🐜 |
| Ledger | Big Schwein | 🐷 |
| Cookbook | Shy Ardilla | 🐿️ |
| Hora | White Jelen | 🦌 |

Format: vector SVG on 24×24 grid, single-color, on neutral (#19362D) tile. Draw in Penpot.

---

## 3. Color

### Brand Colors (3 tiers)

| Tier | Token | HEX | RGB | CMYK | Usage |
| --- | --- | --- | --- | --- | --- |
| Primary | `primary` | `#1FB854` | 31, 184, 84 | 83, 0, 54, 28 | Brand carrier, CTAs, active states |
| Secondary | `secondary` | `#1EB88E` | 30, 184, 142 | 84, 0, 23, 28 | Accents, highlights |
| Accent | `accent` | `#1FB8AB` | 31, 184, 171 | 83, 0, 7, 28 | Secondary accent |

### Neutral / Surface

| Token | HEX | RGB | CMYK | Usage |
| --- | --- | --- | --- | --- |
| `base-100` | `#1B1717` | 27, 23, 23 | 0, 15, 15, 89 | Page background |
| `base-200` | `#161212` | 22, 18, 18 | 0, 18, 18, 91 | Elevated surface |
| `base-300` | `#110D0D` | 17, 13, 13 | 0, 24, 24, 93 | Borders / depth |
| `base-content` | `#CAC9C9` | 202, 201, 201 | 0, 0, 0, 21 | Body text on base |
| `neutral` | `#19362D` | 25, 54, 45 | 54, 0, 17, 79 | Unsaturated UI panels |
| `neutral-content` | `#CDD3D1` | 205, 211, 209 | 3, 0, 1, 17 | Text on neutral |

### Status Colors

| Token | HEX | Content | Contrast | WCAG |
| --- | --- | --- | --- | --- |
| `info` | `#00B5FF` | black | 9.05:1 | AAA ✓ |
| `success` | `#00A96E` | black | 6.90:1 | AA ✓ |
| `warning` | `#FFBE00` | black | 12.62:1 | AAA ✓ |
| `error` | `#FF5861` | black | 6.82:1 | AA ✓ |

### Usage Ratio

```
60% neutral (backgrounds)  ·  30% primary (brand green)  ·  10% secondary/accent
```

### CSS Variables (daisyUI v5)

```css
[data-theme="panomete"] {
  --color-primary: #1FB854;
  --color-primary-content: #000000;
  --color-secondary: #1EB88E;
  --color-secondary-content: #000C07;
  --color-accent: #1FB8AB;
  --color-accent-content: #010C0B;
  --color-neutral: #19362D;
  --color-neutral-content: #CDD3D1;
  --color-base-100: #1B1717;
  --color-base-200: #161212;
  --color-base-300: #110D0D;
  --color-base-content: #CAC9C9;
  --color-info: #00B5FF;
  --color-info-content: #000000;
  --color-success: #00A96E;
  --color-success-content: #000000;
  --color-warning: #FFBE00;
  --color-warning-content: #000000;
  --color-error: #FF5861;
  --color-error-content: #000000;
  --radius-selector: 1rem;
  --radius-field: 2rem;
  --radius-box: 1rem;
  --border: 1px;
  --depth: 0;
}
```

---

## 4. Typography

| Use | Font | Weight | Size / LH | Tracking | Color |
| --- | --- | --- | --- | --- | --- |
| H1 | Sarabun | 700 | 28px / 1.2 | -0.02em | primary |
| H2 | Sarabun | 600 | 21px / 1.3 | 0 | base-content |
| H3 | Sarabun | 600 | 17px / 1.4 | 0 | base-content |
| Body | Sarabun | 400 | 14px / 1.6 | 0 | base-content |
| Caption | Sarabun | 400 | 12px / 1.5 | 0 | base-content @ 70% |
| Mono | JetBrains Mono | 500 | 14px / 1.5 | 0 | secondary |

**Fallback stacks:**
```css
font-family: 'Sarabun', system-ui, -apple-system, sans-serif;
font-family: 'JetBrains Mono', 'SF Mono', monospace;
```

**Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

**Licenses:** Both OFL (Sila Open Font License) — web/desktop/app/print.

**Do:** ✓ use real weights (400/600/700) · ✓ use mono for code, ports, endpoints, status IDs
**Don't:** ✗ fake bold (browser-synthesized) · ✗ use decorative fonts · ✗ mix more than 2 families

---

## 5. Voice & Tone

| Do say | Don't say |
| --- | --- |
| short, direct sentences | corporate filler |
| active verbs | hype without proof |
| technical terms where precise | decorative adjectives |
| "deploy", "configure", "verify" | "unleash", "empower", "transform" |

**Tone by context:** Status page = terse, data-first · Presentation = slightly more narrative, still technical · Error message = clear cause + action, no blame.

---

## 6. Imagery & Photography

**Rule: None.** No stock photography. No decorative imagery. Visual content is:
- Data visualization (charts use forest palette tier colors)
- Architecture diagrams (mermaid or hand-drawn)
- Code blocks (JetBrains Mono)

---

## 7. Iconography & Graphic Elements

| Element | Spec |
| --- | --- |
| Icon style | Outline, 1.5px stroke, 24×24 grid, 2px corner radius |
| Source | Lucide or Phosphor (open-source, consistent) |
| Pattern | Dot grid on base-100, 4% opacity, 8px spacing — section separation only |
| Radii | selector 1rem · field 2rem · box 1rem · border 1px |
| Depth | 0 (flat, no shadows) |

---

## 8. Layout & Grid

- **Spacing:** 8pt system (4 / 8 / 16 / 24 / 32 / 48 / 64 px)
- **Desktop:** 12-column grid, 24px gutter, max-width 1200px
- **Mobile:** 4-column grid, 16px gutter
- **Breakpoints:** sm 640px · md 768px · lg 1024px · xl 1200px (Tailwind standard)

---

## 9. Digital Applications

| Touchpoint | Spec |
| --- | --- |
| **Web/product UI** | daisyUI components with forest theme tokens. Buttons = primary/secondary/accent. States use status colors. |
| **Social** | Animal submark as avatar. Forest palette. |
| **Email** | Dark background (#1B1717) not recommended for email — use reversed wordmark on white. |
| **Presentations** | Dark slides (#1B1717), Sarabun headings, JetBrains Mono for code/diagrams. Chart colors = primary/secondary/accent/status. |
| **API docs** | daisyUI forest theme. Code blocks in JetBrains Mono. Status indicators use info/success/warning/error tokens. |

### Presentation (PowerPoint) Spec

| Element | Value |
| --- | --- |
| Slide background | `#1B1717` (base-100) |
| Title | Sarabun 700, 28px, primary green `#1FB854` |
| Body | Sarabun 400, 14px, `#CAC9C9` |
| Code block | JetBrains Mono 500, 14px, `#1EB88E` on `#161212` background |
| Chart series 1 | primary `#1FB854` |
| Chart series 2 | secondary `#1EB88E` |
| Chart series 3 | accent `#1FB8AB` |
| Status indicators | success `#00A96E` · warning `#FFBE00` · error `#FF5861` · info `#00B5FF` |

---

## 10. Assets & Downloads

| Asset | Location | Format |
| --- | --- | --- |
| Color tokens (CSS) | This document §3 | CSS variables |
| daisyUI theme CSS | `https://cdn.jsdelivr.net/npm/daisyui@5/themes.css` | CDN |
| Font (Sarabun) | `https://fonts.google.com/specimen/Sarabun` | TTF/WOFF2 |
| Font (JetBrains Mono) | `https://fonts.google.com/specimen/JetBrains+Mono` | TTF/WOFF2 |
| Animal submarks | TBD — draw in Penpot (`design.panomete.com`) | SVG |
| Wordmark | This document §2 (Sarabun 700 typeset) | typeset |

**Naming convention:** `panomete-<asset>-<variant>.<ext>` (e.g. `panomete-wordmark-fullcolor.svg`)

**Exception approval:** Sahachan (`flowero`)

---

## Versioning

```markdown
Version: 1.0   Date: 2026-08-25
Changed by: UX (designer agent) + Sahachan
Sections touched: ALL (initial lock)
Changelog: Initial locked version. Strategy compressed, visual identity built from daisyUI forest theme v5.7.22 source values, all WCAG-verified.
```

---

## Quality Gates

- [x] Version/status/date set
- [x] All 🔴 items complete (strategy + visual identity)
- [x] Style Guide includes all design tokens (color, type, spacing)
- [x] Accessibility baseline met (WCAG AA: all content-on-color pairs verified)
- [x] Heuristic check: consistency (#4), recognition over recall (#6), aesthetic minimalism (#8) — all satisfied
- [x] Handoff specs complete (CSS variables, font loading, PowerPoint spec)

> **Template standard:** Based on [[00_brand-roadmap]] · **Color source:** daisyUI v5.7.22 `[data-theme=forest]` · **Fonts:** Google Fonts (OFL)
