---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 18 Doherty Threshold

> **Productivity increases when the computer and user interact at a pace (< 400ms) that ensures neither has to wait for the other.**

When a system responds in under 400ms, the user stays in flow. Above 400ms, attention breaks — the user switches to something else, loses context, gets frustrated.

---

## The Principle

![Doherty Threshold - keep response under 400ms](https://lawsofux.com/images/doherty-threshold.svg)

*Source: lawsofux.com*

---

## The Response Time Hierarchy

| Response Time | User Perception | What Happens |
|:------------:|-----------------|--------------|
| **< 100ms** | Instant | Feels like a physical reaction — ideal |
| **100–400ms** | Fast enough | User stays in flow, barely notices |
| **400–1000ms** | Noticeable delay | Attention starts to wander — flow breaks |
| **1–3 seconds** | Waiting | User checks phone, loses context |
| **3–10 seconds** | Frustrating | User considers leaving |
| **> 10 seconds** | Abandonment | User leaves unless they HAVE to be there |

---

## Practical Techniques

### Perceived Performance (Psychological)

| Technique | How |
|-----------|-----|
| **Skeleton screens** | Show layout placeholders immediately — feels faster than a spinner |
| **Optimistic UI** | Assume the action succeeded; roll back if it failed (likes, upvotes, checkboxes) |
| **Progressive loading** | Load visible content first; lazy-load everything else |

### Actual Performance (Technical)

| Technique | How |
|-----------|-----|
| **Preload next page** | Start loading before the user clicks (link hover, scroll position) |
| **Cache aggressively** | Don't re-fetch data the user just saw |
| **Debounce inputs** | Don't search on every keystroke — wait for a pause |

---

## The Spinner Problem

A spinner says "wait." After 400ms of spinner, the user's mind has left the building.

| ❌ | ✅ |
|----|-----|
| Full-page spinner for 3 seconds | Skeleton screen that fills in progressively |
| Button → spinner → result | Button → instant visual feedback (disable + color change) → result |
| "Loading..." text | Show partial content as it arrives |

---

## Sources

- *Laws of UX* — https://lawsofux.com/doherty-threshold/
- Doherty, W.J. & Thadani, A.J. (1982). *The economic value of rapid response time.*
