---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 03 Advanced TDD

Beyond the basics — what happens when TDD gets hard. Sorting algorithms, test doubles, and the London vs Chicago debate.

---

## Sort 1 & Sort 2 — When TDD Gets Stuck

Uncle Bob walks through implementing a sorting algorithm with TDD. At some point, you get **stuck** — the next test requires an algorithm shift too large for a single red-green-refactor cycle.

### The Solution: Comment Out the Failing Test

When you encounter a step too big, **comment out** the failing test, refactor the code to prepare for it, then uncomment and proceed. This is not cheating — it's acknowledging that some transformations are bigger than one cycle.

---

## Arrange, Act, Assert

Every test follows this pattern:

```java
// Arrange — set up the test data and state
Stack stack = new Stack();
stack.push(42);

// Act — do the thing being tested
int result = stack.pop();

// Assert — verify the outcome
assertEquals(42, result);
```

> If you can't write the test in Arrange-Act-Assert form, your design might be too coupled.

---

## Enter BDD (Behavior-Driven Development)

BDD shifts the language from "test" to "specification":

| TDD Language | BDD Language |
|-------------|-------------|
| Test | Specification / Example |
| Assert | Should |
| Method name | Sentence ("shouldPopLastPushedValue") |

The Given/When/Then format replaces Arrange/Act/Assert with business-readable language.

---

## Finite State Machines & BDD

Complex behavior (like a turnstile or vending machine) can be modeled as a state machine. BDD tests capture transitions: "Given the turnstile is locked, when a coin is inserted, then it should be unlocked."

---

## Test Doubles — The Full Taxonomy

| Type | Purpose | Example |
|------|---------|---------|
| **Dummy** | Fills parameter slots, never used | `new User(null, null)` |
| **Stub** | Returns canned answers | `when(repo.findById(1)).thenReturn(user)` |
| **Spy** | Records calls for later verification | `verify(emailService).send(orderConfirmation)` |
| **Mock** | Expects specific calls, fails if not met | `verify(mock, times(1)).save(any())` |
| **Fake** | Working implementation, not production-ready | In-memory database, test double of real service |

---

## The TDD Uncertainty Principle

> The more you mock, the less you test the real integration. The less you mock, the slower and more fragile your tests become.

---

## London vs Chicago

| | Chicago (Classic) | London (Mockist) |
|---|:---:|:---:|
| **Philosophy** | Test behavior, not implementation | Test units in isolation |
| **Mocks** | Avoid. Use real objects. | Heavy use. Mock all collaborators. |
| **Unit** | A behavior / use case | A class |
| **Fragility** | Lower (tests survive refactoring) | Higher (tests break on implementation change) |
| **Speed** | Slower (real objects) | Faster (mocks are cheap) |

### The Synthesis

Uncle Bob leans Chicago (classic). The goal is to test **behavior** — not implementation details. Tests that break when you refactor are worse than no tests. But there's a place for mocks: external systems, slow dependencies, non-deterministic behavior.

---

## Architecture Implications

> TDD influences architecture. Systems designed with TDD in mind tend toward plugin architectures — where high-level policy depends on abstractions, and low-level details implement those abstractions. The tests are the first consumers of your code. If the tests are hard to write, the design is wrong.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 3.
