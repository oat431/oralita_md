---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 05 Refactoring & Simple Design

Refactoring improves structure without changing behavior. Simple Design writes only what's needed. Together, they keep the codebase alive.

---

## Refactoring

> The practice of improving the structure of the code without changing its behavior — defined by passing tests.

### Red / Green / Refactor

```
🔴 RED:    Write a failing test
🟢 GREEN:  Write minimal production code to pass
🔵 REFACTOR: Clean up without breaking any tests
```

> Writing code that works is hard enough. Writing code that's clean is also hard. Those two goals are best achieved in **two separate steps.**

### What Refactoring Includes

| Level | Example |
|-------|---------|
| **Cosmetic** | Rename variables, functions, classes |
| **Structural** | Split big functions/classes into smaller ones |
| **Architectural** | Rewrite switch statements with polymorphic dispatch |
| **Organizational** | Move code into other functions, classes, components |

### Continuous, Not Scheduled

Refactoring is ongoing — not something put on a schedule once the mess becomes unbearable. With continuous refactoring, no big mess is ever made.

Even large-scale refactorings stretching over long periods should follow the continuous approach: all tests passing throughout the entire process.

---

## Simple Design — Kent Beck's Four Rules

> Write only the code required, with structure as simple, small, and expressive as possible.

| Rule | What It Means |
|------|--------------|
| **1. Pass all the tests** | Code must work as intended. |
| **2. Reveal the intent** | Code must be expressive — easy to read, self-descriptive. Small units, clean names. |
| **3. Remove duplication** | Don't say the same thing more than once. Extract functions. For deeper duplication: Strategy, Decorator patterns. |
| **4. Decrease elements** | Remove superfluous classes, functions, variables. If it's not needed, delete it. |

---

## Design Weight

Complex design puts the programmer under high **cognitive load** — the Design Weight. High Design Weight = more effort to understand and manipulate.

A trade-off exists:

```
Simple requirements + Simple design = Low cognitive load
Complex requirements + Simple design = May not handle complexity well
Complex requirements + Elaborate design = Higher cognitive load, but handles complexity
```

> Find the balance. Design Weight should match requirement complexity — no more, no less.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 5.
- Fowler, Martin. *Refactoring*, 2nd ed., Addison-Wesley, 2018.
- Beck, Kent. *Extreme Programming Explained*, 2nd ed., 2004.
