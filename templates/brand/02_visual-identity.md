---
date: 2026-08-25
tags: [branding, template, visual-identity, logo, color, typography]
---

# Visual Identity — Build Sheet

> Phase 2 of [[00_brand-roadmap]]. Requires [[01_brand-strategy]] completed. Copy as `YYYYMMDD-<brand>-identity.md`. A logo alone is not an identity — build the **system**: mark, color, type, supporting elements reinforcing each other.

## 1. Moodboard First

Collect 15–30 images (product, texture, type, photography) that *feel* like the personality adjectives from strategy. Arrange, delete until only cohesive pieces remain. Derive palette candidates FROM the board — never invent colors in isolation.

## 2. Color Palette (3 tiers)

Tiered so designers never ask "which blue?". Max ~6 swatches total (Hick's law applies to palettes too).

| Tier | Role | Swatch | HEX | RGB | CMYK | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | brand recognition carrier | | # | , , | , , | signature color |
| Secondary | accents, highlights, CTA | | | | | 1–2 max |
| Neutral | backgrounds, body text | | | | | incl. near-black, off-white |

**Quality gates**

- [ ] Text on background passes WCAG AA: ≥ 4.5:1 normal text, ≥ 3:1 large text/UI
- [ ] Works in single-color print (test grayscale)
- [ ] Distinct from top competitor's cluster (from strategy audit)

## 3. Typography System

One family with weights usually beats three families. If two: display face for headings + workhorse for body.

| Use | Font | Weight | Size / Line-height | Tracking |
| --- | --- | --- | --- | --- |
| H1 | | Bold 700 | | |
| H2/H3 | | SemiBold 600 | | |
| Body | | Regular 400 | | |
| Caption/small | | Regular 400 | | |

- [ ] Web fallback stack declared (`font-family: "X", system-ui, sans-serif`)
- [ ] License covers intended use (web/desktop/app)
- [ ] Legible at 12px and at poster distance

## 4. Logo System (not one mark)

| Asset | Purpose | Format needed |
| --- | --- | --- |
| Primary logo | main lockup | SVG, EPS, PNG transparent |
| Secondary / submark | square avatars, stamps | SVG + PNG |
| Wordmark | when icon is absent | SVG |
| Favicon / app icon | 16–512px | ICO, PNG |

Define in the guide:

```markdown
Clearspace: = height of the [x-element] on all sides
Minimum size: digital ___px wide · print ___mm wide
Backgrounds approved: [light / dark / photo w/ overlay]
Variants: full color · reversed white · single black
```

**Don'ts list (write yours):** no stretch, no rotate, no drop shadow, no recolor outside palette, no busy backgrounds, no rebuilding the lockup.

## 5. Supporting Elements

| Element | Rule to define |
| --- | --- |
| Iconography | outline or filled? stroke width? corner radius? grid? |
| Photography | subject, lighting, color grade, people-or-not |
| Illustration | style, when used instead of photo |
| Pattern / texture | construction rule, allowed opacity/placement |
| Layout grid | columns/margins for key formats |

---

**Gate:** all sections locked → assemble everything into the manual via [[03_style-guide]].
