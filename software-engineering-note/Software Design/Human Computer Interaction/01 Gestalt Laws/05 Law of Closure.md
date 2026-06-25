# 05 Law of Closure

> **The brain fills in missing information to perceive a complete shape.**

When parts of an object are missing, the brain automatically "closes" the gaps. This is why you can recognize a dashed circle as a circle — and why minimal logos and icons work.

---

## The Principle

![Closure - brain completes incomplete shapes](https://lawsofux.com/images/closure.svg)

*Source: lawsofux.com*

You see a triangle and a panda — even though the lines don't fully connect. The brain fills in the gaps.

---

## In UI Design

### Icon Design

| Example | How Closure Works |
|---------|------------------|
| Loading spinners | A partial circle — brain completes it, perceives rotation |
| Progress bars | A partially filled bar — brain sees the full track as "100%" |
| Hamburger menu icon | Three lines — brain reads them as a menu, not random dashes |
| Truncated text | "Read more..." — closure tells you there's more content |

### The Power of Suggestion

You don't need to draw everything. The brain does the work:

```
❌ Over-designed icon:
┌──────┐
│ FILE │  ← too literal, unnecessary
└──────┘

✅ Closure-driven icon:
  ┌──┐
  │  │  ← folded corner suggests "document" without drawing the whole thing
  └──┘
```

---

## Practical Applications

| Use Case | How to Apply Closure |
|----------|---------------------|
| **Carousels** | Show partial next/previous items at edges — user knows there's more to scroll |
| **Scrollable areas** | Cut off content at the bottom of a card — implies scrolling |
| **Logo design** | FedEx arrow (negative space), NBC peacock (partial shapes) |
| **Pagination** | "1 2 3 ... 10" — the ellipsis triggers closure for the missing numbers |

---

## When NOT to Use Closure

| ❌ Problem | ✅ Fix |
|-----------|-------|
| Incomplete icon that's unclear | If users need text labels to understand your icons, the closure isn't working |
| Truncated critical information | Don't use "..." for things users MUST see — like error messages or prices |
| Missing borders on input fields | Floating label inputs without borders can look like plain text — provide enough visual cues |

---

## Sources

- *Laws of UX* — https://lawsofux.com/law-of-closure/
- Wertheimer, M. (1923). *Laws of Organization in Perceptual Forms.*
