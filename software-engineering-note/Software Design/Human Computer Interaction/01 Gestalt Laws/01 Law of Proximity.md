---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 01 Law of Proximity

> **Objects that are close together are perceived as a group.**

The brain assumes things near each other belong together — even if they look completely different. This is the most powerful Gestalt principle for UI design.

---

## The Principle

![Proximity example - dots grouped by distance|339](https://lawsofux.com/images/proximity.svg)

*Source: lawsofux.com*

The 12 dots on the left aren't seen as "12 dots." They're seen as **three groups of four** — purely because of spacing. The dots on the right are seen as two groups.

---

## In UI Design

### ❌ Bad — Related things are far apart

```
[Username: _______________]

[Password: _______________]

                        [Login]
```

The login button is far from the form fields. The brain doesn't connect them.

### ✅ Good — Related things are together

```
[Username: _______________]
[Password: _______________]
[          Login          ]
```

The button belongs to the form because it's close to the fields.

---

## Practical Rules

| Rule | Example |
|------|---------|
| Labels go **directly above or beside** their input fields | "Email" label touching the email input |
| Section headers are **closer to their content** than to previous section | More space above a heading than below it |
| Related buttons are **grouped together** | Save + Cancel together, separated from Delete |
| Card content has **less internal spacing** than space between cards | Padding inside cards < gaps between cards |

---

## The Golden Rule of Spacing

> **Space between groups > space within groups.**

```
┌─────────────────────────────────┐
│  Section A          ← tight ──→ │  ← more space between sections
│  [Field 1]  [Field 2]           │
├─────────────────────────────────┤
│  Section B                      │
│  [Field 3]  [Field 4]           │
└─────────────────────────────────┘
```

---

## Real-World Examples

| Example | How Proximity Works |
|---------|-------------------|
| Google search results | Title + URL + snippet are grouped by tight spacing; wide gaps separate results |
| iPhone Settings | Each section has items grouped together; sections separated by wider gaps |
| Navigation menus | Menu items are close together; logo sits apart on the left |

---

## Sources

- *Laws of UX* — https://lawsofux.com/law-of-proximity/
- Wertheimer, M. (1923). *Laws of Organization in Perceptual Forms.*
