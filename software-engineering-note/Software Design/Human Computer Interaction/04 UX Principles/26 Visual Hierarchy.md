---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 26 Visual Hierarchy

> **Guide the user's eye by making important elements look important.**

Users don't read — they scan. Visual hierarchy controls what they see first, second, and last. Without it, everything competes for attention and nothing wins.

---

## The Tools of Hierarchy

| Tool | How It Creates Hierarchy |
|------|------------------------|
| **Size** | Bigger = more important. H1 > H2 > body. Hero image > thumbnail. |
| **Color** | High contrast = important. Bright CTA button > muted secondary button. |
| **Position** | Top/left = seen first (F-pattern, Z-pattern reading). |
| **Whitespace** | More space around something = more attention. An isolated element screams "look at me." |
| **Weight** | Bold > Regular > Light. Use weight, not size, for subtle hierarchy. |
| **Contrast** | High contrast text = primary. Low contrast text = secondary/caption. |

---

## The Scanning Patterns

### F-Pattern (Text-Heavy Pages)
Users scan in an F shape: horizontal across the top → down the left edge → across again. Common on articles, search results, documentation.

### Z-Pattern (Landing Pages)
Users scan in a Z: top-left → top-right → diagonal down-left → bottom-right. Common on landing pages with a hero + CTA.

```
F-Pattern:              Z-Pattern:
████████████            ████ → → → ████
█                       ↓            ↓
█                       ↓            ↓
██████████              ████ ← ← ← ████
█
█
```

---

## Practical Rules

| ❌ Flat — Everything Equal | ✅ Hierarchical — Clear Priority |
|---------------------------|--------------------------------|
| All text same size, same weight | H1 (40px bold) > H2 (28px) > Body (16px regular) |
| 4 equally-styled buttons | 1 primary (solid color), 2 secondary (outline), 1 tertiary (text link) |
| No spacing variation | More space above a section than within it |

---

## The Squint Test

Squint at your design. Can you still tell what's most important? If everything blurs into gray, your hierarchy is broken.

---

## Sources

- *Refactoring UI* by Adam Wathan & Steve Schoger
- Nielsen Norman Group — https://www.nngroup.com/articles/visual-hierarchy/
