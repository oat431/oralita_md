---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 13 Integrity

Integrity is doing the right thing when no one is watching. For a programmer, it means maintaining quality, consistency, and discipline — even when cutting corners would be easier.

---

## Small Cycles

> Work in small, verifiable steps. Never let a day pass without proving your code works.

The history of source code control tells the story: from tapes to SCCS to Subversion to Git. Each step made it easier to work in small cycles. Git's cheap branching enabled `test && commit || revert` — the ultimate small cycle.

---

## Short Cycles → Continuous Integration

| Cycle Length | What It Enables |
|-------------|----------------|
| Minutes | Continuous Build — tests run on every commit |
| Hours | Feature branches merged to mainline |
| Days | Sprints, iterations |
| Never | Branches that live for weeks = merge hell |

### Branches vs Toggles

| Strategy | When |
|----------|------|
| **Feature branches** | Short-lived. Merge to mainline within hours/days. |
| **Feature toggles** | Code deployed but hidden. Toggle on when ready. Better than long-lived branches. |
| **Continuous Deployment** | Every green build goes to production. The holy grail. |

---

## Continuous Build

> The continuous build must never break. If it does, fixing it is the highest priority.

Once discipline slips and the build stays broken, it never gets fixed. Broken builds lead to broken deployments. Broken deployments lead to broken trust.

---

## Relentless Improvement

| Area | What It Means |
|------|--------------|
| **Test Coverage** | More tests. Better tests. Mutation testing to verify test quality. |
| **Cleaning** | Refactor continuously. Boy Scout Rule. Leave code better than you found it. |
| **Creations** | Write new code that sets a higher standard. Don't match the mess — raise the bar. |

---

## Semantic Stability

> The meaning of names, functions, and modules should be stable. A function called `calculateTotal` should calculate a total. Not also send an email. Not also update a database.

Semantic stability is about being honest in your code. A function does what its name says — nothing more, nothing less.

---

## Maintain High Productivity

### Viscosity

Design viscosity is how much the design resists the right change. High viscosity = doing the right thing is hard. Low viscosity = doing the right thing is easy.

### Managing Distractions

| Distraction | Defense |
|------------|---------|
| Slack/Teams notifications | Mute. Check on your schedule, not theirs. |
| Email | Process in batches. Never first thing in the morning. |
| "Quick questions" | Schedule office hours. Protect your focus time. |
| Meetings | Decline if no agenda. Leave if no value. |

### Time Management

> Pomodoro Technique: 25 minutes of uninterrupted work, 5-minute break. Four pomodoros, longer break. This is how you ship.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 13.
