---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 04 Metaphor & Collective Ownership

Team Practices are about the relationships of team members to one another and to the product. Metaphor creates shared language. Collective Ownership eliminates knowledge silos.

---

## Metaphor — Ubiquitous Language

Effective communication requires a **common vocabulary** of terms and concepts.

| Good Metaphor | Bad Metaphor |
|--------------|-------------|
| Multi-step process = assembly line | Embarrassing or insulting toward stakeholders |
| Helps team and customer communicate | Confuses more than clarifies |

### Ubiquitous Language (Eric Evans, DDD)

> A model of the problem domain, described by a commonly accepted vocabulary — used by programmers, QA, managers, customers, users, **everyone** involved with the project.

When the business says "order fulfillment" and the code says `OrderFulfillmentService`, they're speaking the same language. That's Ubiquitous Language.

---

## Collective Ownership

> Code is not owned by individuals. It is owned by the team as a whole.

| With Collective Ownership | Without |
|--------------------------|---------|
| Knowledge distributed across team | Knowledge concentrated in individuals |
| Anyone can work on anything | "That's Bob's code — don't touch it" |
| Team makes better decisions together | Miscommunication, finger-pointing |
| Code is shared and reused | Same solution written multiple times |

### Specialization vs Generalization

Specialization is allowed and becomes necessary as the system grows. But the ability to work **outside** one's specialty must be maintained. Generalization only comes from seeing the big picture — which requires reading and understanding code across the system.

---

## The Dysfunction of Individual Ownership

Teams that practice individual code ownership with strong barriers to modifying (or even reading) others' code become dysfunctional:

- Finger-pointing when something breaks
- Miscommunication about who owns what
- Duplicate code solving the same problem
- Bus factor = 1 for every module

> Collective Ownership doesn't mean no expertise. It means no one is the **only** person who understands a piece of the system.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 4.
- Evans, Eric. *Domain-Driven Design*, Addison-Wesley, 2003.
