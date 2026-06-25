# 08 Color & Opacity

Color is the first thing users notice and the easiest thing to get wrong. Good color use creates hierarchy, communicates state, and guides attention. Bad color use creates chaos.

---

## The 60-30-10 Rule

A classic interior design rule that works perfectly for UI:

| % | Role | What It Colors |
|:--:|------|---------------|
| **60%** | Dominant (background) | Page background, card backgrounds |
| **30%** | Secondary (base UI) | Sidebars, headers, navigation |
| **10%** | Accent (calls to action) | Primary buttons, links, highlights |

```
┌──────────────────────────────────┐  60% white/light gray (background)
│  ┌────────────────────────┐      │
│  │ 30% blue-gray (nav)    │      │
│  └────────────────────────┘      │
│                                  │
│  [10% accent button]  [muted]    │  10% = only the primary action
│                                  │
└──────────────────────────────────┘
```

---

## Color Hierarchy

| Level | Color Style | Used For |
|-------|------------|----------|
| **Primary** | Saturated, bold | Main CTAs, active nav items |
| **Secondary** | Muted, desaturated | Less important buttons, cards |
| **Tertiary** | Very subtle, near-background | Borders, dividers, disabled states |
| **Semantic** | Red (error), Green (success), Yellow (warning), Blue (info) | Alerts, form validation, badges |

### Gray Is Not Just Gray

Good grays have a hint of color — usually blue or purple. Pure `#808080` looks flat and dead.

| ❌ Dead Gray | ✅ Alive Gray |
|-------------|--------------|
| `#808080` | `#6B7280` (Tailwind gray-500 — blue-tinted) |
| `#CCCCCC` | `#D1D5DB` (Tailwind gray-300) |

---

## Opacity

Opacity creates depth without adding more colors.

| Value | Use |
|:-----:|-----|
| **100%** | Primary text, active elements |
| **80%** | Secondary text, icons |
| **60%** | Placeholder text, disabled elements |
| **40%** | Borders, dividers |
| **20%** | Subtle backgrounds, hover states |
| **10%** | Very subtle hover, focus rings |

### Practical Opacity Tricks

| Trick | How |
|-------|-----|
| **Text on images** | Add a semi-transparent overlay (black at 40–60% opacity) between image and text |
| **Disabled buttons** | Reduce opacity to 40–50% instead of changing color |
| **Shadows** | Use black at 10–20% opacity instead of pure black |
| **Borders** | Use your text color at 15–20% opacity — automatically matches the theme |

---

## Accessibility With Color

| Rule | Why |
|------|-----|
| **Never use color alone** to convey information | Colorblind users (4.5% of population) can't distinguish red/green |
| **Contrast ratio ≥ 4.5:1** for body text | WCAG AA standard |
| **Contrast ratio ≥ 3:1** for large text (18px+) | |
| ✅ "Error: Password is required" | ❌ Just a red border with no text |

---

## Sources

- *Refactoring UI* by Adam Wathan & Steve Schoger
- WebAIM Contrast Checker — https://webaim.org/resources/contrastchecker/
