---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 05 Test-Driven Development

TDD is the programmer's equivalent of double-entry bookkeeping. Every required behavior is entered twice: once as test code, once as production code. The difference must be zero — zero failing tests.

---

## The Accounting Analogy

Accountants developed double-entry bookkeeping because a single mistake can have huge consequences:

| Accounting | Programming (TDD) |
|-----------|-------------------|
| Every transaction entered twice (credit + debit) | Every behavior entered twice (test + production code) |
| Check difference after every entry | Run tests after every change |
| Difference must be zero | Failing tests must be zero |

> TDD catches mistakes as they enter the codebase — and prevents them in time. Unlike double-entry bookkeeping, TDD is not (yet) required by law.

---

## The Three Laws of TDD

| Law | What It Means |
|-----|--------------|
| **1.** | Don't write production code until you have test code failing due to the lack of that production code. |
| **2.** | Don't write more test code than needed to fail — compiler errors count as failing. |
| **3.** | Don't write more production code than needed to make the test pass. |

Programmers oscillate between test and production code at a rate of just a few seconds. The code that introduced an error is always among the few lines just written.

---

## Courage, Not Coverage

| Metric | Right Use | Wrong Use |
|--------|-----------|-----------|
| **Code coverage** | Internal team metric. Requires strong understanding to interpret. | Management metric. Enforcing thresholds creates bogus tests without assertions. |

> The ultimate goal of TDD is **courage**, not coverage. Developers with trust in their test suite fearlessly modify and improve code. Developers without trust shy away from messy code — and the code rots.

---

## Why Write Tests First

| Test-First (TDD) | Test-After |
|-----------------|-----------|
| Code is designed for testability | Code not designed for testing = hard to test |
| Fun: oscillating between red/green | Boring busy work: testing already-manually-tested code |
| Tests get written | Tests get skipped, leaving holes in the suite |
| Passing suite = deployable | Passing suite = can't be trusted |

---

## Debugging Skills

> You only need to debug a lot if you have a lot of bugs. With TDD, fewer bugs are introduced. It's OK for TDD-disciplined developers to be bad at operating debuggers.

Debugging is still required now and then — but much less often. A comprehensive test suite is also the best kind of documentation: working, self-contained, small code examples.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 5.
- Beck, Kent. *Test-Driven Development: By Example*, Addison-Wesley, 2002.
