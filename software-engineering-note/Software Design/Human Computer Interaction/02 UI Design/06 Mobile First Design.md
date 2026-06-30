---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 06 Mobile First Design

> **Design for the smallest screen first, then scale up.**

It's easier to add features for larger screens than to cram a desktop design onto a phone. Mobile-first forces you to prioritize — you can only fit what matters.

---

## The Principle

![Mobile first vs desktop first approach](https://cdn.shopify.com/s/files/1/0070/7032/files/mobile-first-design.png)

*When you start mobile-first, you naturally expand. Starting desktop-first forces awkward cramming.*

---

## Why Mobile First

| Reason | Explanation |
|--------|------------|
| **Forces prioritization** | You have 375px. What's actually essential? |
| **Performance** | Mobile designs are naturally lighter — benefits desktop too |
| **Majority traffic** | Over 55% of web traffic is mobile (and growing) |
| **Google ranking** | Mobile-first indexing since 2019 |
| **Progressive enhancement** | Add complexity as screen size increases, not remove it |

---

## The Workflow

```
1. Design at 375px (mobile)
       ↓
2. What breaks at 768px? (tablet)
       ↓
3. What needs more at 1024px? (small desktop)
       ↓
4. Full layout at 1440px (large desktop)
```

---

## Practical Rules

### Layout

| Screen | Pattern |
|--------|---------|
| Mobile (< 768px) | Single column, stacked |
| Tablet (768–1024px) | 2 columns where it makes sense |
| Desktop (> 1024px) | Multi-column, sidebars, full navigation |

### Navigation

| Screen | Pattern |
|--------|---------|
| Mobile | Hamburger menu or bottom tab bar |
| Tablet | Condensed horizontal nav or hamburger |
| Desktop | Full horizontal navigation |

### Touch Targets

Mobile users tap with fingers, not precision cursors:

| Rule | Measurement |
|------|------------|
| Minimum touch target | 44×44px (Apple HIG), 48×48px (Material Design) |
| Spacing between targets | At least 8px |
| Thumb zone | Critical actions in the bottom half of the screen |

---

## ❌ Common Mistake

**Hiding desktop features on mobile instead of redesigning for mobile.**

| ❌ Bad | ✅ Good |
|--------|---------|
| "We'll just hide the sidebar on mobile." | Redesign the navigation as a bottom tab bar |
| "The table will scroll horizontally." | Redesign as cards or a list for mobile |
| "They can pinch to zoom." | Use readable font sizes (16px minimum body text) |

---

## Sources

- *Refactoring UI* by Adam Wathan & Steve Schoger
- Google Material Design — https://m3.material.io/
- Apple Human Interface Guidelines — https://developer.apple.com/design/human-interface-guidelines/
