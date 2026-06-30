---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 03 Planning & Estimation

Planning in Agile is continuous, not a one-time phase. Estimation is honest, not exact. The goal: replace hope with data.

---

## The Estimation Trade-Off

```
More precision = More time spent estimating
Less precision = Less time, but more uncertainty
```

> An estimate should be as **accurate** as possible, but only as **precise** as necessary.

### Trivariate Estimation

Give best-case, nominal-case, and worst-case:

| Estimate | Probability of Finishing Within |
|----------|:-------------------------------:|
| Best-case (8 days) | 5% |
| Nominal-case (12 days) | 50% |
| Worst-case (16 days) | 95% |

Out of 100 similar tasks: 5 finish in best-case, 50 in nominal, 95 in worst-case.

---

## Story Points

Story points are **relative, not absolute.** They do not map to units of time.

### How It Works

1. Pick a **Golden Story** of average size. Assign, say, 3 points.
2. Compare every other story against the Golden Story.
3. Different developers would take different amounts of time — but thanks to the **Law of Large Numbers**, those differences even out over many sprints.

### Iteration Planning Meeting (IPM)

- Max: 1/20th of iteration (half a day for 2-week sprint)
- Whole team attends: stakeholders, programmers, testers, analysts, managers
- **Programmers estimate velocity** (how many points they think they can complete)
- **Stakeholders choose stories** to fit within that velocity

> ⚠️ Velocity estimate is **not a commitment.** It's a rough guess — way too high for the first iteration. That's expected.

---

## The Four-Quadrant Game

Stakeholders prioritize by **return on investment (ROI):**

```
                    High Value
                        │
         ┌──────────────┼──────────────┐
         │   DO NOW     │   DO LATER   │
   Low   │              │              │   High
  Cost   ├──────────────┼──────────────┤  Cost
         │ CONSIDER     │   DISCARD    │
         │  (much later)│              │
                    Low Value
```

1. **Valuable + Cheap** → Do immediately
2. **Valuable + Expensive** → Do later
3. **Not Valuable + Expensive** → Discard
4. **Not Valuable + Cheap** → Consider (much) later

---

## Estimation Techniques

### Flying Fingers
Read story → discuss → developers hold up fingers behind backs → show on count of 3. Consensus = write number. Big deviation = discuss, re-estimate.

### Planning Poker
Fibonacci cards: 1, 2, 3, 5, 8, ∞ (too big), ? (unclear), 0 (trivial).

| Card | Meaning |
|:----:|---------|
| 0 | Trivial — staple multiple 0s together |
| ∞ | Too big — split into smaller INVEST-compliant stories |
| ? | Unclear — create a **spike** (thin slice through system) for research |

---

## Iteration & Release

| Rule | Why |
|------|-----|
| **Finish entire stories, not tasks** | 80% of stories done > 80% of tasks per story done |
| **Stories picked, not assigned** | Autonomy. Experienced devs guide rookies away from overloading. |
| **Velocity is a measurement, not an objective** | Pressure → point inflation. Keep the Golden Story as reference. |
| **Falling velocity = bad code quality** | Code rot slows everything. Fewer tests → fear of refactoring. |
| **Rising velocity = possible inflation** | Check against Golden Story. |

### Release Often

The goal is **Continuous Delivery** — release to production after every change. Modern tools (Git, CI) make this possible. Old organizations must change culturally to overcome inertia.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 3.
