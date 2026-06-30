---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 06 Simple Design

Simple design is not easy design. It takes discipline to write only what's needed — and the skill to make that minimal code expressive.

---

## YAGNI — You Ain't Gonna Need It

> Don't write code for features you might need someday. Write code for what you need NOW.

Every line of code you write for a hypothetical future is a line you must read, understand, test, debug, and maintain. It's dead weight. Cut it.

---

## Covered by Tests

> If it's not tested, it doesn't work. Simple design starts with passing tests.

Coverage is not a management metric. It's a team tool. Use it to find untested code — not to hit an arbitrary number. An asymptotic goal: 90%+, but never at the cost of meaningful assertions.

---

## Design?

Simple design IS a design activity. You're not "skipping design." You're designing in small increments, guided by tests, constrained by the need for simplicity.

---

## The Three Pillars of Simple Design

### 1. Maximize Expression

> Code should scream its intent. A reader should understand what it does in seconds.

| Expressive | Not Expressive |
|-----------|---------------|
| `calculateTotalPrice()` | `calc()` |
| `isEligibleForDiscount(customer)` | `check(c)` |
| `DAYS_UNTIL_EXPIRY = 30` | `30` (magic number) |

### 2. Minimize Duplication

> Don't say the same thing more than once.

Duplication isn't just copy-paste. It's also:
- **Accidental duplication** — two pieces of code that happen to look the same but serve different purposes. Don't merge them. They'll diverge.
- **Conceptual duplication** — two pieces of code that do the same thing in different ways. Merge them.

### 3. Minimize Size

> Delete code. Delete files. Delete classes. Less code = less to understand, less to maintain, less to break.

| Keep | Delete |
|------|--------|
| Code that serves a current use case | Dead code, commented-out code |
| Code that expresses intent clearly | Overly clever abstractions |
| Code covered by tests | Code with no test coverage |

---

## The Underlying Abstraction

> Good design reveals an underlying abstraction — a unifying concept that makes the code feel inevitable, like it couldn't have been written any other way.

The question to ask: "Is there a simpler way to express this idea?" If the answer is yes, refactor until the answer is no.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 6.
