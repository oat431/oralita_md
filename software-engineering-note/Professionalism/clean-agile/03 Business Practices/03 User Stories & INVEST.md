---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 03 User Stories & INVEST

User stories are not detailed feature specs. They are **reminders** of features — placeholders for conversations between business and development.

---

## User Story Format

> "As a **user**, I want to **do something** so that **some value is created.**"

Example: *"As a user, I want to be asked if I want to save my document when I close the application without saving."*

Details are left out at first and clarified when developers take the story up for development.

---

## Why Index Cards?

Despite modern tools, physical index cards have value:

| Benefit | Why |
|---------|-----|
| **Physical handling** | Cards can be moved, grouped, prioritized in meetings |
| **Discipline of vagueness** | Small card = can't write too much. Keeps planning from being bogged down by detail. |
| **Disposability** | Cards must not become too valuable to discard. Stories change. |

---

## INVEST — Six Qualities of Good Stories

| Letter | Quality | What It Means |
|:------:|---------|--------------|
| **I** | Independent | Stories don't depend on each other. Can be implemented in any order by business value. |
| **N** | Negotiable | Leave room for negotiation. Simple features, easy implementations save cost. |
| **V** | Valuable | Clear, quantifiable business value. Stories cut through all layers (frontend → backend → DB). Architecture and refactoring are NOT user stories. |
| **E** | Estimable | Concrete enough to estimate, vague enough to negotiate. Sweet spot: precise about business value, vague about implementation. |
| **S** | Small | One or two developers within a single iteration. Rule of thumb: roughly same number of stories as team members per iteration. |
| **T** | Testable | Accompanied by tests specified by business. Story is done when all tests pass. QA writes tests; developers automate and pass them. |

---

## Story Lifecycle

```
Write story (Iteration Zero) → Estimate (IPM) → Prioritize (Four-Quadrant) 
→ Implement (during sprint) → QA writes acceptance tests → Tests pass → Done
```

| Phase | Who |
|-------|-----|
| Writing | Business + Development |
| Estimating | Developers |
| Prioritizing | Stakeholders |
| Acceptance tests | QA (happy path: business; unhappy paths: QA) |
| Implementation | Developers |

---

## Edge Cases

| Story | Handling |
|-------|----------|
| **Trivial (0 points)** | Staple cards together. Multiple zeros add up. |
| **Too big (∞)** | Split into smaller stories that still comply with INVEST. |
| **Unclear (?)** | Create a **spike** — a meta-story that does research. Original story depends on spike. |

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 3.
