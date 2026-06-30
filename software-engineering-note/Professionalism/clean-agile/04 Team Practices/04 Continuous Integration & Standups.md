---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 04 Continuous Integration & Standups

CI keeps the team in sync. Standups keep the team aligned. Both are about feedback — fast, frequent, honest.

---

## Continuous Integration

> Programmers should run all tests locally before checking in code, so that the continuous build **never breaks.**

### The Evolution of CI

| Era | Practice |
|-----|----------|
| Early XP | Check in and merge with mainline every couple of hours |
| Modern | Continuous Build runs all tests automatically as code is checked in — cycle shortened to minutes |

### Feature Toggles

Changes that are deployed but not yet active are hidden behind feature toggles. This allows merging to mainline without exposing unfinished work.

### When the Build Breaks

> It's the **highest priority** for the entire team to get the build running and tests passing again.

Once discipline slips and the build is left broken, the team very unlikely will make the effort to "catch up later." Broken systems will be deployed sooner or later.

**The rule:** Never leave the build broken overnight. Fix it now, or revert the change that broke it.

---

## Standup Meetings (Daily Scrum)

Standups are **optional.** They can be held less often than daily, at whatever schedule fits the team best. ~10 minutes, regardless of team size.

### The Three Questions

> Team members stand in a circle and answer:

1. **What did I do since the last meeting?**
2. **What will I do until the next meeting?**
3. **What is in my way?**

### The Rules

| Rule | Why |
|------|-----|
| No discussions held | This is reporting, not problem-solving |
| No explanations given | Keep it brief |
| No complaints made | Obstacles are stated, not ranted about |
| ~30 seconds per person | Forces conciseness |
| Non-developers: listen or follow same rules | No special status |

---

## The Chicken and the Pig

A fable about commitment vs involvement:

| Animal | Sacrifice | Role | Weight in Decisions |
|--------|-----------|------|:-------------------:|
| **Pig** | Life (to provide ham) | Developer | Full |
| **Chicken** | Eggs (small sacrifice) | Manager, stakeholder | Limited |

> Those who are merely *involved* (chickens) should not have the same weight in decisions as those who are *committed* (pigs). In standups, chickens should listen — not direct.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 4.
