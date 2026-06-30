---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 08 Acceptance Tests

Acceptance tests are the business's definition of "done." They are specification, documentation, and regression safety net — all in one.

---

## The Discipline

> A story is not complete until its acceptance tests pass. Period.

Acceptance tests are written BEFORE or DURING development — never after. They are the executable specification of what the system should do.

---

## Who Writes Acceptance Tests?

| Role | Responsibility |
|------|---------------|
| **Business / Product Owner** | Defines the happy path. "When a customer places an order, the order should be confirmed." |
| **QA** | Extends with unhappy paths. "What if the credit card is declined? What if inventory is zero?" |
| **Developers** | Automate the tests and make them pass. |

> QA is not the bottleneck at the end of the iteration. They're deeply involved from the beginning — writing specifications, not finding bugs.

---

## The Continuous Build

Acceptance tests must run in the **continuous build** — automatically, on every commit. If they don't, they'll be skipped. If they're skipped, they don't define "done."

### Requirements for Continuous Acceptance Testing

| Requirement | Why |
|------------|-----|
| **Fast** | Must complete in minutes, not hours |
| **Reliable** | No flaky tests. A failing test must mean a real problem. |
| **Isolated** | Tests don't interfere with each other |
| **Automated** | No human intervention needed |

---

## BDD — Behavior-Driven Development

Acceptance tests are written in Given/When/Then format:

```
Given a customer with items in their cart
When the customer completes checkout
Then the order is confirmed
And an email confirmation is sent
```

These specifications are readable by business AND executable by machines. They bridge the gap between "what the business wants" and "what the code does."

---

## The Test Pyramid Revisited

```
        ┌──────────┐
        │   E2E     │  ← Few. Slow. Brittle.
       ┌┴──────────┴┐
       │ Acceptance │  ← Business-readable. Automated.
      ┌┴────────────┴┐
      │  Integration │  ← Service + real dependencies.
     ┌┴─────────────┴┐
     │     Unit      │  ← Most. Fastest. Most reliable.
     └──────────────┘
```

Acceptance tests sit between integration and E2E. They're more business-facing than unit tests, but more reliable than full E2E browser tests.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 8.
