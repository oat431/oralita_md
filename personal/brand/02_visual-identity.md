---
date: 2026-08-25
version: "1.0"
status: Locked
tags: [branding, visual-identity, color, typography, logo, panomete, locked]
---

# Visual Identity — Panomete

> Phase 2 of [[00_brand-roadmap]]. **Status: LOCKED 2026-08-25.** Requires [[01_brand-strategy]] (locked). All values verified — colors converted from OKLCH source, WCAG contrast tested, fonts confirmed on Google Fonts.

## 1. Moodboard

No separate moodboard collection. The moodboard IS the daisyUI forest theme — a dark, green-forward, flat-surface dev-tool aesthetic. The palette was derived from the theme's OKLCH source values, not invented in isolation.

**Mood anchors:** Linear (dark, minimal, high-contrast) · GitHub (dark dev-tool, functional) · Grafana (data-dense, status-colored). But the actual colors come from daisyUI forest, not from these references.

## 2. Color Palette (3 tiers + status)

Source: `daisyui@5/themes.css` v5.7.22 — `[data-theme=forest]`. OKLCH values converted to HEX/RGB/CMYK. All contrast ratios verified.

### Brand Colors

| Tier | Role | Token | HEX | RGB | CMYK | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | brand recognition carrier | `primary` | `#1FB854` | 31, 184, 84 | 83, 0, 54, 28 | signature Panomete green |
| Secondary | accents, highlights | `secondary` | `#1EB88E` | 30, 184, 142 | 84, 0, 23, 28 | teal-green |
| Accent | secondary accent | `accent` | `#1FB8AB` | 31, 184, 171 | 83, 0, 7, 28 | cyan-teal |

### Neutral / Surface Colors

| Tier | Role | Token | HEX | RGB | CMYK | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Neutral | unsaturated UI panels | `neutral` | `#19362D` | 25, 54, 45 | 54, 0, 17, 79 | dark green-gray |
| Neutral-content | text on neutral | `neutral-content` | `#CDD3D1` | 205, 211, 209 | 3, 0, 1, 17 | light gray-green |
| Base-100 | page background | `base-100` | `#1B1717` | 27, 23, 23 | 0, 15, 15, 89 | near-black warm |
| Base-200 | elevated surface | `base-200` | `#161212` | 22, 18, 18 | 0, 18, 18, 91 | darker |
| Base-300 | borders / depth | `base-300` | `#110D0D` | 17, 13, 13 | 0, 24, 24, 93 | darkest |
| Base-content | body text on base | `base-content` | `#CAC9C9` | 202, 201, 201 | 0, 0, 0, 21 | light warm gray |

### Status / Semantic Colors

| Role | Token | HEX | RGB | Content token | Contrast | WCAG |
| --- | --- | --- | --- | --- | --- | --- |
| Info | `info` | `#00B5FF` | 0, 181, 255 | `info-content` (#000) | 9.05:1 | AAA ✓ |
| Success | `success` | `#00A96E` | 0, 169, 110 | `success-content` (#000) | 6.90:1 | AA ✓ |
| Warning | `warning` | `#FFBE00` | 255, 190, 0 | `warning-content` (#000) | 12.62:1 | AAA ✓ |
| Error | `error` | `#FF5861` | 255, 88, 97 | `error-content` (#000) | 6.82:1 | AA ✓ |

### Usage Ratio

```
60% neutral (base-100/200/300 backgrounds)
30% primary (brand green — CTAs, active states, key labels)
10% secondary/accent (highlights, secondary actions)
```

### Quality Gates

- [x] Text on background passes WCAG AA: base-content/base-100 = 10.76:1 (AAA)
- [x] Works in single-color print (grayscale test: all values have sufficient luminance separation)
- [x] Distinct from common dev-tool palettes (green-forward, not blue)
- [x] `base-content` on `primary` fails (1.58:1) — **use `primary-content` (black) on primary, never white text on green**

### OKLCH Source Values (for reference)

```
primary:          oklch(68.628% 0.185 148.958)
secondary:        oklch(69.776% 0.135 168.327)
accent:           oklch(70.628% 0.119 185.713)
neutral:          oklch(30.698% 0.039 171.364)
neutral-content:  oklch(86.139% 0.007 171.364)
base-100:         oklch(20.84% 0.008 17.911)
base-200:         oklch(18.522% 0.007 17.911)
base-300:         oklch(16.203% 0.007 17.911)
base-content:     oklch(83.768% 0.001 17.911)
```

## 3. Typography System

Two families: Sarabun (display + body) and JetBrains Mono (code/data). No third family.

| Use | Font | Weight | Size / Line-height | Tracking | Color |
| --- | --- | --- | --- | --- | --- |
| H1 | Sarabun | 700 | 28px / 1.2 | -0.02em | primary |
| H2 | Sarabun | 600 | 21px / 1.3 | 0 | base-content |
| H3 | Sarabun | 600 | 17px / 1.4 | 0 | base-content |
| Body | Sarabun | 400 | 14px / 1.6 | 0 | base-content |
| Caption | Sarabun | 400 | 12px / 1.5 | 0 | base-content @ 70% opacity |
| Mono / code | JetBrains Mono | 500 | 14px / 1.5 | 0 | secondary |

**Web fallback stacks:**
```css
font-family: 'Sarabun', system-ui, -apple-system, sans-serif;       /* body/headings */
font-family: 'JetBrains Mono', 'SF Mono', monospace;                 /* code/data */
```

**Font loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

- [x] Web fallback stack declared
- [x] License: both OFL (Sila Open Font License) — covers web/desktop/app/print
- [x] Sarabun: weights 400/500/600/700/800 available, v17 on Google Fonts, full Latin + Thai coverage
- [x] JetBrains Mono: weights 400/500/700 available, designed for code legibility

**Honest note:** Sarabun's Latin glyphs are wider than Inter/Geist at 12–14px in dense dashboards. This is mitigated by using JetBrains Mono for all code/dense-data contexts. Sarabun handles prose, headings, and Thai.

## 4. Logo System

### Primary — Wordmark

```
Lockup:    "Panomete" in Sarabun 700, letter-spacing -0.02em
Color:     "Pano" in base-content (#CAC9C9), "mete" in primary (#1FB854)
Clearspace: = height of "P" on all sides
Minimum:   120px wide (digital) / 30mm (print)
```

**Variants:**
- Full color (on dark base-100): "Pano" #CAC9C9 + "mete" #1FB854
- Reversed (on light): "Pano" #1B1717 + "mete" #1FB854
- Single black: all #000 (for single-color print)
- Favicon: "P" in primary green on base-100 background

**Don'ts:**
- No stretching or scaling non-proportionally
- No rotation
- No drop shadow
- No recolor outside the palette
- No outline/stroke around the wordmark
- No rebuilding the two-tone split differently (always "Pano"|"mete", never "Panom"|"ete")

### Secondary — Animal Submarks

Each Panomete service carries an animal code name. The submark gives each project a recognizable avatar while sharing one visual language.

| Service | Code Name | Animal | Domain |
| --- | --- | --- | --- |
| Blog | Cute Gufo | 🦉 Owl | `blog.panomete.com` |
| URL Shortener | Fluffy Mouton | 🐑 Sheep | `short.panomete.com` |
| Todo List | Tiny Mchwa | 🐜 Ant | `todo.panomete.com` |
| Ledger | Big Schwein | 🐷 Pig | `ledger.panomete.com` |
| Cookbook | Shy Ardilla | 🐿️ Squirrel | `recipe.panomete.com` |
| Hora | White Jelen | 🦌 Deer | `hora.panomete.com` |

**Submark spec:**
- Single-color on neutral (#19362D) tile
- 8rem (128px) rounded box, 1px border (#110D0D), 0.5rem radius
- Vector SVG icons on 24×24 grid, consistent stroke weight
- Production: draw in Penpot (self-hosted at `design.panomete.com`)

> Note: Emoji shown as placeholders. Production submarks should be hand-drawn vector icons, not emoji.

## 5. Supporting Elements

| Element | Rule |
| --- | --- |
| **Iconography** | Outline style · 1.5px stroke · 24×24 grid · corner radius 2px · no filled icons · source: Lucide or Phosphor (open-source) |
| **Photography** | **None.** No stock photography, no decorative imagery. Visual content = data viz + architecture diagrams + code only. |
| **Illustration** | Not used. |
| **Pattern / texture** | Subtle dot grid on base-100, 4% opacity, 8px spacing. For section separation only, never decoration. |
| **Layout grid** | 8pt spacing system (4/8/16/24/32/48/64) · 12-column desktop (24px gutter) · 4-column mobile (16px gutter) · max width 1200px |
| **Radii** | selector 1rem · field 2rem · box 1rem · border 1px · depth 0 (flat, no shadows) — from daisyUI forest theme |

---

**Gate:** ✅ All sections locked 2026-08-25. Assemble into [[03_style-guide]].
