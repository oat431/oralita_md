---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 27 Consistency

> **Same thing, same way. Every time.**

Consistency is the single most powerful usability principle. When users learn something once, they expect it to work the same way everywhere. Every inconsistency is a small betrayal of that trust.

---

## Types of Consistency

| Type | Example |
|------|---------|
| **Visual** | All primary buttons look the same. All error messages use the same red. |
| **Functional** | Clicking a card always navigates. Swiping always goes back. The hamburger menu always opens navigation. |
| **Internal** | Within your product: settings works the same on every screen. |
| **External** | With other products: your app's search works like Google's. Your form works like every other form. (See [[13 Jakob's Law]]) |

---

## The Cost of Inconsistency

| One Inconsistency | User Impact |
|------------------|-------------|
| Delete is red on one page, blue on another | User hesitates — "Is this really delete?" |
| Cards are clickable on Page A, not on Page B | User taps dead cards, gets frustrated |
| "Save" sometimes auto-saves, sometimes doesn't | User loses work, loses trust |

---

## How to Maintain Consistency

| Technique | Tool/Pattern |
|-----------|-------------|
| **Design system** | A single source of truth for colors, typography, components |
| **Component library** | Build once, reuse everywhere — buttons, inputs, modals |
| **Design tokens** | Variables for colors, spacing, typography — change once, update everywhere |
| **Linters** | Automatic checks: "You used a non-standard button color here." |

---

## When to Break Consistency

Consistency is not a prison. Break it when:

| Reason | Example |
|--------|---------|
| **Critical difference** | Delete SHOULD look different from Save — the difference is intentional |
| **New pattern is clearly better** | Old pattern was confusing; new one tested better |
| **Different context demands it** | Mobile nav differs from desktop — and that's expected |

> **Rule:** Break consistency intentionally, not accidentally. And only after research shows the new way is better.

---

## Sources

- Nielsen, J. (1994). *10 Usability Heuristics for User Interface Design.*
- *Refactoring UI* by Adam Wathan & Steve Schoger
