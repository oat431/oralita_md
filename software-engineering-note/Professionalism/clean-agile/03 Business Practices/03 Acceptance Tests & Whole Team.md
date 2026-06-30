---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 03 Acceptance Tests & Whole Team

Acceptance tests turn vague requirements into unambiguous completion criteria. Whole Team removes the walls between roles.

---

## Acceptance Tests — The Definition of Done

> A story is not specified until its acceptance tests are written. A story is not completed until its acceptance tests pass.

### The Specification Conflict

| Role | Wants Specification To Be... |
|------|---------------------------|
| **Business** | Vague, natural language, flexible |
| **Programmers** | Precise, machine-executable |

**The solution:** Business specifies tests in natural language with a formal structure. Developers implement them in code. Those tests become the **Definition of Done.**

---

### Given / When / Then (BDD)

```
Given a customer with items in their cart
And a valid credit card on file
When the customer completes checkout
Then the order is created with status "CONFIRMED"
And payment is charged
And the cart is emptied
```

| Section | Purpose |
|---------|---------|
| **Given** | Preconditions / setup |
| **When** | The action being tested |
| **Then** | Expected outcomes |

---

### Happy Path vs Unhappy Paths

| Who | What They Define |
|-----|-----------------|
| **Business** | Happy path — shows the system produces intended value |
| **QA** | Unhappy paths — corner cases, ways users might break the system |

---

### QA's New Role

| Old QA | New Agile QA |
|--------|-------------|
| Bottleneck at end of iteration | Deeply involved from beginning |
| Finding lots of bugs = proof of doing job | Bugs found = process failure |
| Manual testing heroes | Test specification authors |
| Last to touch the system | First to write the tests |

> QA supplies test specifications to development. Development makes sure those tests pass. The process of running tests should be automated.

---

## Whole Team

Formerly called "On-Site Customer." Based on reducing physical distance to improve communication.

### Co-Location Benefits

| Benefit | How |
|---------|-----|
| **Efficient communication** | No email chains. Walk over and talk. |
| **Serendipity** | Unplanned interactions at coffee machine create synergy. |
| **Shared understanding** | Everyone hears the same conversations. |

### Remote Teams

Technology has improved. Remote works well if there's only a gap in **space** but none in culture, language, or time zone. However, serendipitous conversation and nonverbal communication are significantly reduced.

> "Customer" is meant in a broad sense: stakeholder, Scrum Product Owner, actual end user.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 3.
