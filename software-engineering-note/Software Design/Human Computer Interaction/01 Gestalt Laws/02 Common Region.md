---
tags:
- hci
- software-design
- software-engineering
- ui
- ux
---

# 02 Common Region

> **Elements within the same bounded area are perceived as a group.**

If you put a border, background color, or card around things — the brain treats them as one unit. Common Region overrides Proximity when they conflict.

---

## The Principle

![Common Region - elements inside a boundary are grouped](https://lawsofux.com/images/common-region.svg)

*Source: lawsofux.com*

The dots inside the oval are seen as one group, even though some dots are closer to dots outside the oval than inside it. The **boundary wins** over proximity.

---

## In UI Design

### ❌ Without Common Region

```
[Username: _______________]
[Password: _______________]
[Remember me] [Forgot password?]
[          Login          ]
```

Everything floats in white space. What's part of the form? What's separate?

### ✅ With Common Region

```
┌──────────────────────────────┐
│  Username: _______________   │
│  Password: _______________   │
│  [Remember me] [Forgot?]     │
│  [        Login        ]     │
└──────────────────────────────┘
```

The card makes it obvious: everything inside is one form.

---

## Common Region Techniques

| Technique | Example |
|-----------|---------|
| **Cards** | Product cards, dashboard widgets, profile sections |
| **Background shading** | Table row striping, selected items, active states |
| **Borders** | Input groups, message threads, comment sections |
| **Dividers** | Menu separators, section breaks |

---

## Proximity vs Common Region

| Principle | When It Wins |
|-----------|-------------|
| **Proximity** | Items are close but don't share a background/border |
| **Common Region** | Items share a visible container — overrides proximity |

> If you want to group things that MUST be far apart, use Common Region. The card/border does the grouping for you.

---

## Real-World Examples

| Example | How Common Region Works |
|---------|----------------------|
| Facebook posts | Each post is a card — comments inside the card vs separate from other posts |
| iOS Control Center | Each section (connectivity, brightness, music) has its own rounded container |
| Twitter/X DM | Each message bubble is a distinct region separating sender from receiver |

---

## Sources

- *Laws of UX* — https://lawsofux.com/law-of-common-region/
- Palmer, S.E. (1992). *Common region: A new principle of perceptual grouping.*
