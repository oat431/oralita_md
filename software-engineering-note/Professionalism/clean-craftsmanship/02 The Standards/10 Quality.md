---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 10 Quality

Quality is not a feature. It's not a phase. It's not something you "add later." It's the foundation everything else rests on.

---

## Continuous Improvement

> Software should get better over time, not worse.

Every change should leave the codebase slightly better than you found it. The Boy Scout Rule applied relentlessly: check in cleaner code than you checked out.

---

## Fearless Competence

> Developers should not fear their own code.

Fear of the codebase is the #1 indicator of quality problems. When developers are afraid to change code — afraid they'll break something, afraid they don't understand it — quality is already dead.

TDD gives you the courage to change code. A comprehensive test suite means you can refactor fearlessly. Without it, you're navigating a minefield blindfolded.

---

## Extreme Quality

Uncle Bob argues that quality should be taken to extremes:

| Extreme Quality Means... | Not... |
|-------------------------|--------|
| 100% test coverage of meaningful logic | 100% coverage by number (including getters/setters) |
| Mutation testing to verify test quality | Line coverage alone |
| Code that is so clean it's boring | Code that is "clever" and hard to understand |
| Refactoring until there's nothing left to improve | Refactoring "when there's time" |

---

## We Will Not Dump on QA

> QA is not your bug-finding service. QA is your specification-writing partner.

### The QA Disease

In dysfunctional organizations, QA is the last line of defense. Developers throw code "over the wall" and QA finds the bugs. This creates an adversarial relationship and a false sense of security.

### QA Will Find Nothing

The goal is zero bugs found by QA. Not because QA isn't testing — but because development prevented the bugs from existing in the first place. QA's role shifts from bug-finding to specification-writing and exploratory testing.

---

## Test Automation

> Manual testing is immoral. It's repetitive work that machines do better, faster, and more reliably. Forcing humans to do it is a waste of human potential.

| Automated | Manual (Acceptable) |
|-----------|-------------------|
| Unit tests | Exploratory testing |
| Integration tests | Usability testing |
| Acceptance tests | Ad-hoc investigation |
| Regression tests | |
| Performance tests | |

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 10.
