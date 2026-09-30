---
tags: [ui, design-systems, component-libraries, tailwind, shadcn, bootstrap, tradeoffs, design-notes]
---

# UI Libraries vs Building Your Own: A False Binary

> **Created:** 2026-09-30
> **Grew out of:** watching shadcn take over after Tailwind and Bootstrap, and noticing Linear/Stripe/Vercel look custom — which raised the hidden question: *is going custom the only "real" path?*
> **The question:** Do UI libraries matter? Should we strictly stick to one, or build our own?

## TL;DR

"Use a library vs build our own" is a false binary. The products that look custom are custom because of their **design token system** and years of design engineering — not because they avoid libraries. Linear (the poster child of custom) just finished migrating styled-components → **StyleX, Meta's atomic CSS library**, over 1,000+ PRs and ~5 months. They use **dnd-kit** for drag-and-drop. Their "custom look" lives in an LCH color token system, not in not-invented-here.

What actually makes a product look custom:

1. **Owned tokens** — color spaces (LCH/OKLCH), spacing scale, type scale, radii
2. **Motion & micro-interaction polish** — invested over years
3. **Typography choices** — Linear: Inter Display for headings, Inter for body
4. The *invisible* hard parts (accessibility, focus management) **borrowed from libraries**

Rule I take away: **own the tokens, borrow the primitives, pick the component kit per project.**

## 1. "UI library" is actually three different layers

Bootstrap, Tailwind, and shadcn are not alternatives in the same category — that conflation is why the question feels wrong:

| Layer | What it is | Examples | Build your own? |
|---|---|---|---|
| **Primitives** (headless) | Behavior + accessibility: focus traps, keyboard nav, aria attributes, portals | Radix UI, React Aria, Headless UI | **Never.** This is deep a11y expertise — focus restoration, screen reader announcements, escape handling — that took the industry a decade to accumulate |
| **Styling engine** | How CSS gets generated and applied | Tailwind, StyleX, vanilla CSS, Bootstrap's CSS layer | Rarely — it's a perf/workflow call (Tailwind vs StyleX), not an identity decision |
| **Component kit** | Pre-styled decisions: what a button/dialog looks like | Bootstrap, MUI, daisyUI, shadcn | **This is the only layer where "your design system" can live** |

Bootstrap = component kit with its own styling engine bundled. Tailwind = styling engine with **no components at all**. shadcn = components (copy-paste) built *on top of* Tailwind + Radix. Comparing them as one category is like comparing a menu, a kitchen, and a recipe.

## 2. What the "custom" products actually do (evidence)

**Linear, as of 2026:**
- Token system: **LCH color space**, 3 base variables (base, accent, contrast) auto-generating ~98 theme variables — including automatic high-contrast themes for accessibility
- Finished a **1,000+ PR migration** from styled-components to **StyleX** (Meta's library) for 20–35% less main-thread work — a perf decision, not a "purity" decision
- Uses **dnd-kit** for drag-and-drop, MobX, resize-observer-based responsive slots
- The custom feel comes from tokens + motion + Inter Display typography + years of iteration on layout structure

**shadcn/ui:**
- Its own README: *"This is NOT a component library… you copy and paste into your project. The code is yours."*
- It's a **distribution model**, not a dependency: Radix primitives (borrowed accessibility) + Tailwind (styling) + code ownership (you maintain what you paste)

The Linear path and the shadcn path converge on the same insight: **identity lives in the token layer; the hard invisible parts should be borrowed.**

## 3. Why "everything built with X looks the same"

The dated "Bootstrap look" was never the library's fault — it was **default tokens leaking**. Thousands of sites shipped the same default blue and the same border-radius. Today the same happens with default shadcn zinc/neutral themes.

The sin is *uncustomized defaults*, not *using a library*. Conversely, a heavily-themed Bootstrap (custom tokens, custom type) doesn't read as Bootstrap at all. Aesthetic-Usability Effect cuts both ways: the "premium" feel of Linear/Stripe comes from token coherence, not hand-made components.

## 4. What "build our own" actually costs

A button sounds like a weekend. Then: keyboard focus rings, `aria-expanded`, escape-to-close, portal rendering, click-outside, focus trap + restoration on close, screen reader announcements, high-contrast mode, RTL, controlled/uncontrolled variants, SSR hydration. Radix's Dialog component is thousands of lines of accessibility fixes for edge cases you have never hit. Rebuilding it = re-purchasing ten years of accumulated bug fixes.

**Tesler's Law applies:** complexity doesn't disappear, it moves. A component library is someone else having already paid that complexity. Your complexity budget is better spent at the token layer — color, spacing, motion, typography — which is the only layer users can actually see.

## 5. Decision table

| If you want… | Choose | Why |
|---|---|---|
| Speed to ship (MVP, client demo) | Component kit themed via its tokens (Bootstrap, daisyUI, MUI) | Pareto: ~20% of the effort covers ~80% of the UI |
| **To understand design** (my current goal) | shadcn-style: copy code into the repo, read it, modify it | The code lands in *your* codebase and you maintain it — forced reading. Radix source doubles as an accessibility textbook |
| Distinctive product identity | Own tokens + primitives + custom styling on top | The Linear path: identity at the token/motion/typography layer |
| Consistency across many teams | Mature kit + org-wide token overrides | Consistency at scale is exactly what a kit centralizes |

## 6. How this maps to what I already do

daisyUI + forest theme for Panomete is precisely the middle path: borrow the kit, **own the tokens** (34 library colors remapped to forest values, Sarabun/JetBrains Mono swapped in). The Penpot Design System is the token layer made explicit. Nothing to change — the practice finally has a name and a reasoning.

## Where this comes from

- [How we redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui) — LCH token system, 3 variables → 98, Inter Display
- [Linear's 1,000-PR styled-components → StyleX migration](https://www.infoq.com/news/2026/09/linear-stylex-meta/) — InfoQ, Sept 2026
- [shadcn/ui docs](https://ui.shadcn.com/docs) — "the code you end up with is exactly what you'd write yourself"
- [shadcn README](https://github.com/uiforks/shadcn-ui) — "This is NOT a component library"
