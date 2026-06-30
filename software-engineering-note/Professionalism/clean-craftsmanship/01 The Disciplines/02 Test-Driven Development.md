---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 02 Test-Driven Development

TDD is the foundational discipline. Without it, the rest crumbles. This chapter covers the basics — what every craftsman must know cold.

---

## Software — The Core Insight

> Software is a compound word. "Soft" means easy to change. "Ware" means product. Software is a product that is easy to change.

The whole point of software is that it can be changed. If it can't be changed easily, it's not software — it's just hardware in disguise.

---

## The Three Laws of TDD

| Law | What It Means |
|-----|--------------|
| **1.** Don't write production code until you have a failing test. |
| **2.** Don't write more of a test than is sufficient to fail (compiler errors count). |
| **3.** Don't write more production code than is sufficient to pass the test. |

---

## The Fourth Law (Uncle Bob's Addition)

> **4. Don't write more production code than is sufficient to pass all currently failing tests.**

This prevents the temptation to "just add this one more feature real quick" while you're in the code. Stay in the red-green-refactor cycle. Don't wander.

---

## The Basics — Step by Step

```
1. Write a test. Watch it fail.          ← RED
2. Write JUST enough code to pass.       ← GREEN
3. Clean up the code. Keep tests green.  ← REFACTOR
4. Repeat.
```

The cycle time should be **seconds to minutes.** If you're spending more than a few minutes between red and green, your test is too big.

---

## Three Classic Examples

### Stack

Implement a stack with TDD. Start with: empty stack, push, pop, LIFO behavior. Each test drives exactly one behavior. By the end, you have a working, tested stack — and every line of code was demanded by a test.

### Prime Factors

Generate prime factors of a number. Start simple: `primeFactors(1) → []`. Add test cases one at a time. The algorithm emerges from the tests. You don't design it up front — it crystallizes as the tests accumulate.

### The Bowling Game

The famous kata. Score a bowling game from rolls. Start with a gutter game (all zeros). Add spares. Add strikes. Add the 10th frame. The algorithm evolves test by test. By the end, you understand why TDD is a **design** technique, not a testing technique.

---

## TDD is a Design Discipline

> TDD is not about testing. It's about design. The tests force you to think about how the code will be used before you write it. They force you to decouple. They force you to keep things simple.

Code written with TDD is naturally:
- **Testable** — because it was written to be tested
- **Decoupled** — because tight coupling makes testing hard
- **Minimal** — because you only write what the tests demand

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 2.
