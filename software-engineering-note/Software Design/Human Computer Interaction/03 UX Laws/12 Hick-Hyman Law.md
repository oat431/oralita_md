# 12 Hick-Hyman Law

> **The more choices you give someone, the longer they take to decide.**

Every additional option increases decision time. This isn't linear — it's logarithmic. But the user experience impact IS linear: more options = more cognitive load = more abandonment.

---

## The Principle

![Hick's Law - more choices, longer decision time](https://lawsofux.com/images/hicks-law.svg)

*Source: lawsofux.com*

---

## The Math

$$RT = a + b \cdot \log_2(n)$$

| Variable | Meaning |
|----------|---------|
| RT | Reaction/decision time |
| n | Number of equally likely choices |

> Doubling the choices doesn't double the time — but it does increase it. More importantly, it increases **cognitive load** and **decision paralysis.**

---

## In Practice

### Navigation Menus

| ❌ | ✅ |
|----|-----|
| 15 items in the main nav | 5–7 items max in primary nav; rest in dropdowns or footer |
| "Products" with 20 sub-items | Group into categories: "Hardware", "Software", "Services" (3 choices → then sub-choices) |

### Forms & Onboarding

| ❌ | ✅ |
|----|-----|
| 20-field signup form on one page | Multi-step form: 3–4 fields per step with progress indicator |
| All settings on one massive page | Grouped settings with search |

### Homepages & Landing Pages

| ❌ | ✅ |
|----|-----|
| 10 equally-weighted CTAs | 1 primary CTA, maybe 1 secondary. Everything else is a link, not a button. |

---

## The Exception: Familiar Choices

Hick's Law applies to **unfamiliar** or **equally weighted** choices. When choices are familiar (like a list of countries you know), decision time drops.

| Scenario | Apply Hick's Law? |
|----------|:-----------------:|
| Choosing from 20 unfamiliar SaaS plans | ✅ Yes — simplify to 3 tiers |
| Picking your country from a list of 195 | ❌ No — users know their country; auto-detect or search works better than hiding options |

---

## Practical Rules

| Rule | Example |
|------|---------|
| **Categorize** | Instead of 30 settings, create 5 category tabs |
| **Progressive disclosure** | Show basic options first; "Advanced" expandable section |
| **Highlight recommended** | "Most Popular" badge on one pricing tier reduces decision from "which one?" to "this one?" |
| **Filter and search** | Large lists get a search bar — typing is faster than scanning |

---

## Sources

- *Laws of UX* — https://lawsofux.com/hicks-law/
- Hick, W.E. (1952). *On the rate of gain of information.*
