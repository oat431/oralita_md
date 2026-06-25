# 03 Law of Similarity

> **Elements that look similar are perceived as related or part of the same group.**

The brain groups things by shared visual characteristics — color, shape, size, orientation. Similarity works even when elements are far apart.

---

## The Principle

![Similarity - elements grouped by color/shape](https://lawsofux.com/images/similarity.svg)

*Source: lawsofux.com*

You see **rows of black dots** and **rows of white dots** — not columns of mixed dots. Color similarity overrides spatial arrangement.

---

## In UI Design

### ❌ Without Similarity

```
[Save] [Cancel] [Delete Account] [Export Data]
```

All buttons look the same. A tired user clicks Delete instead of Save.

### ✅ With Similarity

```
[Save]  [Cancel]              [Delete...]  [Export]
 ─── primary ───               ──── secondary ────
```

Primary actions share one style. Destructive/neutral actions share another. The styling communicates function before the user reads a word.

---

## Ways to Create Similarity

| Attribute | Example |
|-----------|---------|
| **Color** | All links are blue; all error messages are red |
| **Shape** | All buttons are rounded rectangles; all inputs are squared |
| **Size** | H1 > H2 > H3 — consistent hierarchy throughout |
| **Typography** | All body text same font/size; all code blocks monospace |
| **Icon style** | All icons filled, or all outlined — don't mix styles |

---

## The Danger: False Similarity

When things look the same but do DIFFERENT things:

| ❌ Bad | ✅ Good |
|--------|---------|
| Delete button styled same as Save | Delete gets distinct color/style (red, outline) |
| All cards identical — some are clickable, some aren't | Interactive cards get hover effects; static ones don't |
| "Cancel" and "Go Back" look the same but behave differently | Give them distinct styling or labels |

---

## Consistency = Applied Similarity

The Law of Similarity is why **design systems** exist. When every button uses the same classes, the user learns "this shape = I can click it" once, not 50 times.

---

## Sources

- *Laws of UX* — https://lawsofux.com/law-of-similarity/
- Wertheimer, M. (1923). *Laws of Organization in Perceptual Forms.*
