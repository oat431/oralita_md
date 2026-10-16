---
title: Panomete Component Template Inventory
version: 1.0-draft
date: 2026-10-16
status: Built · Library published v2
tags: [design-system, components, daisyui, figcraft, panomete]
source: daisyUI 5.7.x component docs · Panomete CI Manual (locked 2026-08-25)
library: F:\projects\design\panomete_design_system\panomete_design_system.figcraft
---

# Panomete — Component Template Inventory

The reusable component list for the Panomete design system, built as a FigCraft library.
Every component uses daisyUI 5 class names 1:1 (`btn`, `alert`, `badge`…) so the design ↔ code
translation is zero. All colors/radii are bound to the `panomete` variable collection — palette
changes propagate to every instance.

## Variant depth standard (agreed)

`Size × Style × State` — ~6–15 variants per component, except `btn` (30: it's the core CTA).
Colors are handled by the token system, not exploded into variants, except where daisyUI defines
color as a real modifier (alert, progress, status, tooltip).

## Tokens in use (from locked style guide)

- **Color (20):** primary `#1FB854` · secondary `#1EB88E` · accent `#1FB8AB` · neutral `#19362D` · base-100/200/300 · base-content `#CAC9C9` · + all `-content` pairs · info/success/warning/error
- **Number (11):** radius-selector 16 · radius-field 32 · radius-box 16 · border 1 · spacing 4/8/16/24/32/48/64
- **Text styles (6):** H1 · H2 · H3 · Body · Caption · Mono (Sarabun + JetBrains Mono)

---

## Page 01 Actions

| # | Component (set name) | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 1 | `btn` | Size=sm/md/lg · Style=primary/secondary/accent/ghost/error · State=default/disabled | 30 | `btn` `btn-sm..lg` `btn-primary..` `btn-ghost` `btn-error` `btn-disabled` | ✅ |
| 2 | `badge` | Size=xs/sm/md · Style=primary/secondary/accent/neutral/outline | 15 | `badge` `badge-xs..md` colors + `badge-outline` | ✅ |
| 3 | `kbd` | Size=xs/sm/md/lg | 4 | `kbd` `kbd-xs..lg` | ✅ |
| 4 | `divider` | Style=default/primary/neutral · Direction=horizontal/vertical | 6 | `divider` `divider-primary` `divider-neutral` `divider-vertical` | ✅ |

## Page 02 Forms

| # | Component | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 5 | `input` | Size=sm/md/lg · State=default/error/disabled | 9 | `input` `input-sm..lg` + `input-error` + native disabled | ✅ |
| 6 | `textarea` | State=default/error/disabled | 3 | `textarea` + `textarea-error` + native disabled | ✅ |
| 7 | `select` | Size=sm/md/lg · State=default/disabled | 6 | `select` `select-sm..lg` + native disabled | ✅ |
| 8 | `checkbox` | Size=sm/md · State=unchecked/checked/disabled | 6 | `checkbox` `checkbox-sm..md` + checked/disabled | ✅ |
| 9 | `radio` | Size=sm/md · State=unchecked/checked/disabled | 6 | `radio` + checked/disabled | ✅ |
| 10 | `toggle` | Size=sm/md · State=on/off/disabled | 6 | `toggle` + checked/disabled | ✅ |

## Page 03 Navigation

| # | Component | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 11 | `tab` | Style=box/border/lift · State=active/inactive | 6 | `tabs` `tabs-box..` `tab` `tab-active` | ✅ |
| 12 | `breadcrumbs` | *(single)* Home > Documents > current | 1 | `breadcrumbs` (last li plain) | ✅ |
| 13 | `pagination` | Size=sm/md | 2 | `join` + `join-item btn` + `btn-active/disabled` | ✅ |
| 14 | `navbar` | *(single)* start / center / end slots | 1 | `navbar` `navbar-start/center/end` | ✅ |
| 15 | `steps` | Direction=horizontal/vertical | 2 | `steps` `step` `steps-vertical` (completed=primary) | ✅ |

## Page 04 Data Display

| # | Component | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 16 | `table` | Size=sm/md · Style=plain/zebra | 4 | `table` `table-sm..md` `table-zebra` | ✅ |
| 17 | `avatar` | Size=sm/md/lg · State=online/offline/placeholder | 9 | `avatar` `avatar-online/offline/placeholder` (size = w-*) | ✅ |
| 18 | `status` | Size=sm/md · Color=primary/success/warning/error/info | 10 | `status` `status-*` colors | ✅ |
| 19 | `list` | *(single)* media list row | 1 | `ul.list` `li.list-row` | ✅ |

## Page 05 Feedback

| # | Component | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 20 | `alert` | Color=info/success/warning/error · Style=soft/outline/dash | 12 | `alert` `alert-info..` `alert-soft/outline/dash` (no size in daisyUI 5) | ✅ |
| 21 | `toast` | Color=info/success/error | 3 | `toast` corner stack of `alert` children | ✅ |
| 22 | `progress` | Color=primary/success/warning/error/info | 5 | `progress` `progress-*` | ✅ |
| 23 | `skeleton` | Shape=text/block/card | 3 | `skeleton` `skeleton-text` | ✅ |
| 24 | `tooltip` | Placement=top/bottom/left/right · Color=default/primary | 8 | `tooltip[data-tip]` `tooltip-primary` placements | ✅ |

## Page 06 Overlays

| # | Component | Variant props → options | # | daisyUI grounding | Build status |
|---|---|---|---|---|---|
| 25 | `modal` | Size=sm/md/lg | 3 | `modal` `modal-box` `modal-action` (dialog method) | ✅ |
| 26 | `dropdown` | Align=start/end · State=closed/open | 4 | `dropdown` `dropdown-content` `dropdown-end` `dropdown-open` | ✅ |

**Totals: 26 component sets · 165 variants** (v1 essentials; expand after real-project review)

---

## Design conventions applied

- **Radii:** buttons/fields → `radius/field` (32) · boxes/cards/modals → `radius/box` (16) · selectors (checkbox/radio/toggle/tab) → `radius/selector` (16) · border 1px `base-300`
- **Depth:** flat — no shadows (`--depth: 0`), borders for separation
- **Type:** all labels Body 14 Sarabun · data/code JetBrains Mono
- **States not in variants:** `loading` (child spinner element, not a variant), focus rings (interaction spec), hover (prototype layer) — documented in Interaction-Specifications later
- **Disabled rendering:** 60% opacity + `base-300` surface, matches daisyUI's disabled look

## Handoff

| Artifact | Consumer |
|---|---|
| `panomete_design_system.figcraft` (+ `.variables.json`) | Design work in FigCraft — place instances in any project file |
| `tools/build_harness.py` | Rebuild/extend the library headlessly (CI-friendly) |
| `panomete.tokens.css` (variable.export) | Dev — drop into any daisyUI project |
| This inventory | PO/Dev — what exists, variant axes, daisyUI class mapping |

## Build notes (QA outcomes 2026-10-16)

- **Verified**: every page render pixel-checked + vision-reviewed; all 165 variants audited for geometry collapse (0 failures); progress fill ratio measured at exactly 60/40 px.
- **Faithful subtleties (not bugs):** zebra rows use base-200 on base-100 (intentionally low-contrast per forest theme); disabled = 50% opacity reads subtle on dark — matches daisyUI's disabled treatment.
- **Deliberately out of variant scope:** hover/focus rings (belong in Interaction-Specifications), `loading` (child spinner element, not a variant), tooltips' `tooltip-open` (shown by presence of bubble).
- **Token coverage:** all fills/strokes/radii bound to `panomete` variables except: checkbox/radio inner geometry (4px/8px hardcode — no token exists), toggle track radius (999 pill), join-item corner radii (pagination geometry).

## Published library

| Field | Value |
|---|---|
| Library id | `83a34195523e9ac5` |
| Name | `panomete_design_system` |
| Version | 2 (2026-10-16) |
| Contents | 26 component sets · 6 text styles · 31 variables (1 collection) |
| CSS tokens | `panomete.tokens.css` (daisyUI v5 custom properties, ready to drop into `@plugin "daisyui/theme"` workflows) |

## Changelog

- v1.0 2026-10-16 — inventory + full build: 7 pages, 26 sets / 165 variants, foundations (tokens, type, spacing), all QA'd and fixed (toggle sizing, avatar children, table/list set bounds, progress contrast, section overlaps); library published v1→v2.
