# 24 Robustness Principle (Postel's Law)

> **Be conservative in what you do, be liberal in what you accept from others.**

In UX: be strict and consistent in your output (clear, predictable interface). Be flexible and forgiving in what you accept as input (any reasonable format, any user behavior).

---

## The Principle

Originally from TCP specification (Jon Postel, 1981), but applies perfectly to UX:

| Conservative in Output | Liberal in Input |
|-----------------------|-----------------|
| Your UI is predictable, consistent, clear | You accept varied user input gracefully |
| Buttons always work the same way | Forms accept multiple formats |
| Navigation is always in the same place | Search handles typos, synonyms, natural language |

---

## In Practice

### Form Input Flexibility

| ❌ Rigid (User must adapt) | ✅ Flexible (System adapts) |
|--------------------------|---------------------------|
| "Enter phone: (XXX) XXX-XXXX" | Accept any format: 1234567890, 123-456-7890, (123) 456-7890 |
| "Date: DD/MM/YYYY" | Accept slashes, dashes, dots. Parse intelligently. |
| "Credit card: XXXX-XXXX-XXXX-XXXX" | Accept with or without spaces/dashes |

### Search

| ❌ | ✅ |
|----|-----|
| Exact spelling required | "Did you mean...?" fuzzy matching |
| Must use correct keywords | Natural language understanding |
| No results = dead end | "No results for X. Try Y." with suggestions |

### Error Handling

| ❌ | ✅ |
|----|-----|
| "Error 403: Invalid input" | "The email address looks incomplete — did you mean user@gmail.com?" |

---

## The Balance

| Too Liberal | Too Conservative |
|------------|-----------------|
| Accepting anything → unpredictable behavior | Rejecting everything → frustrated users |
| Inconsistent output → users confused | Inflexible input → users quit |

> **The best UX is conservative in output (consistent, predictable) and liberal in input (forgiving, flexible).**

---

## Sources

- *Laws of UX* — https://lawsofux.com/postels-law/
- Postel, J. (1981). *RFC 793 — Transmission Control Protocol.*
