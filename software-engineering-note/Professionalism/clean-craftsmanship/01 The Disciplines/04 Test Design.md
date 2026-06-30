---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 04 Test Design

How to test the hard stuff: databases, GUIs, and fragile tests. Plus the Transformation Priority Premise — a way to make TDD's small steps systematic.

---

## Testing Databases

Testing code that talks to a database is hard because databases are slow and stateful.

### Strategies

| Strategy | How |
|----------|-----|
| **In-memory database** | Swap real DB for H2 during tests. Fast but not identical behavior. |
| **TestContainers** | Spin up real PostgreSQL in Docker. Real but slower. |
| **Repository pattern + mocking** | Mock the repository interface. Fastest but least integration coverage. |
| **Separate test schema** | Real DB, isolated test schema. Rollback after each test. |

> Test the business logic without the database. Then test the database integration separately. Don't test both in every test.

---

## Testing GUIs

GUIs are the hardest thing to test. They're visual, event-driven, and framework-dependent.

### Strategies

| Strategy | How |
|----------|-----|
| **Humble Object** | Extract all logic from the GUI into a plain object. Test that object. The GUI becomes so humble it barely needs testing. |
| **Presenters** | The View sends events to the Presenter. The Presenter updates the ViewModel. Test the Presenter. |
| **Self-Shunt** | The test itself implements the View interface. Captures what the Presenter sends. |
| **Test-Specific Subclass** | Subclass the GUI component to override painting methods — test the logic, not the pixels. |

---

## The Fragile Test Problem

> A fragile test breaks when you refactor — even though the behavior hasn't changed.

### The Cause: One-to-One Correspondence

When every class has exactly one test class, every method has exactly one test — tests become mirrors of structure, not behavior. Refactor the structure → tests break.

### The Fix: Break the Correspondence

| Instead of... | Do this... |
|--------------|-----------|
| One test class per production class | Test behavior, not classes |
| Test private methods | Test through public API |
| Mock everything | Use real collaborators where possible |

---

## The Video Store Example

Uncle Bob refactors a video rental system. The original tests mirror the class structure. After refactoring, the tests survive because they test behavior, not structure. This is the goal: **tests that enable refactoring, not prevent it.**

---

## Transformation Priority Premise

When doing TDD, transformations have a priority order. Prefer simpler transformations over complex ones:

| Priority | Transformation | Example |
|:--------:|---------------|---------|
| 1 | {} → Nil | Return null/empty |
| 2 | Nil → Constant | Return a fixed value |
| 3 | Constant → Variable | Replace constant with variable |
| 4 | Unconditional → Selection | Add if/else |
| 5 | Value → List | Single value → collection |
| 6 | Statement → Recursion | Iterative → recursive |
| 7 | Selection → Iteration | if → while/for |
| 8 | Value → Mutated Value | Mutation |

### Fibonacci Example

Generate Fibonacci numbers following transformation priority. Start with `fib(0) → 0`, `fib(1) → 1`. Apply transformations in order. The algorithm emerges naturally from the tests — no flash of insight required.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 4.
