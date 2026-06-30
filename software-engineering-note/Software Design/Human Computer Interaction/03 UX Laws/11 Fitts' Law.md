---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 11 Fitts' Law

> **The time to reach a target depends on its size and distance.**

Bigger + closer = faster to click. Smaller + farther = slower. This is the single most important law for button and interactive element design.

---

## The Principle

![Fitts' Law - target size and distance](https://lawsofux.com/images/fitts-law.svg)

*Source: lawsofux.com*

The time to acquire a target is a function of: **distance to target ÷ size of target**. Make targets bigger, put them closer, or both.

---

## The Math

$$T = a + b \cdot \log_2\left(\frac{2D}{W}\right)$$

| Variable | Meaning |
|----------|---------|
| T | Time to reach the target |
| D | Distance from starting point to target center |
| W | Width of the target |

> Don't memorize the formula. Remember the rule: **bigger + closer = faster.**

---

## Practical Rules

### Button Sizing

| Element | Minimum Size | Recommended |
|---------|:----------:|:-----------:|
| Touch target (mobile) | 44×44px (iOS) / 48×48px (Android) | 48×48px+ |
| Click target (desktop) | 24×24px | 32×32px+ |
| Small icon buttons | Never below 24px | Add padding for a larger hit area |

### Edge & Corner Targets

Screen edges and corners are **infinitely large targets** — you can't overshoot them. This is why:

| Example | Why It Works |
|---------|-------------|
| macOS menu bar (top edge) | Infinite height — you just slam the cursor to the top |
| Windows Start button (corner) | Infinite width AND height — easiest target on screen |
| Mobile bottom nav | Edge of screen = easy thumb reach |
| Right-click context menu | Appears at cursor position — zero distance |

### The "Meatball" Problem

When you click a small icon and it opens a dropdown, the dropdown items should be:
- Close to the cursor (short distance)
- Tall enough to click (minimum 32px height)

---

## What to Avoid

| ❌ | ✅ |
|----|-----|
| Tiny click targets (12px icons with no padding) | At least 44px touch targets, 24px click targets |
| Important buttons far from where the user's cursor is | Place primary actions near the natural cursor path |
| Closely spaced small links (fat-finger problem on mobile) | Add padding between tappable items |
| "Click the X to close" — tiny 12px X in corner | Make the close button at least 32px, or use swipe-to-dismiss on mobile |

---

## Sources

- *Laws of UX* — https://lawsofux.com/fittss-law/
- Fitts, P.M. (1954). *The information capacity of the human motor system.*
