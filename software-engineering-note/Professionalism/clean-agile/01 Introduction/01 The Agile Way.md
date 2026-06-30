---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 01 The Agile Way

Agile replaces hope with data. Waterfall guesses. Agile measures.

---

## The Iron Cross of Project Management

Every project is constrained by four forces. You can pick three:

```
       Good
       /  \
      /    \
  Fast ────── Cheap
      \    /
       \  /
       Done
```

| Lever | Agile Response |
|-------|---------------|
| **Schedule** | End date usually fixed. Not negotiable. |
| **Staff** | Brooke's Law: "Adding manpower to a late project makes it later." |
| **Quality** | Lowering quality gives illusion of speed. Reality: "The only way to go fast is to go well." |
| **Scope** | **The only sensible choice.** Reduce to what's absolutely needed. |

---

## Iterations vs Waterfall

| | Waterfall | Agile |
|---|-----------|-------|
| Analysis | One big phase at start | Every iteration, never ends |
| Design | One big phase in middle | Every iteration |
| Implementation | One big phase at end | Every iteration |
| When problems found | End of implementation (too late) | End of every iteration |

### Iteration Zero

Used to write initial stories, estimate them, set up dev environment, draft tentative design, rough plan. Not a full phase — just enough to start.

---

## Velocity & Burn-Down Charts

| Metric | What It Tells You |
|--------|------------------|
| **Velocity** | Story points completed per iteration. Noisy at first, averages out after ~4 iterations. |
| **Burn-down chart** | Points remaining until milestone. Slope predicts likely completion date. |

> Velocity is a **measurement, not an objective.** Don't put pressure on what you measure. That creates story point inflation.

After a few iterations, you have a realistic average velocity and can calculate the real release date. This might be disappointing — but it's **honest.** Hope is replaced by data.

---

## The First Iteration is Not a Failure

After Iteration 1, fewer stories are done than estimated. This is **not failure** — it's the first real measurement. Use it to adjust the plan. Like today's weather predicting tomorrow's, the first half of an iteration predicts its second half.

---

## Scope Adjustment

At the start of every sprint, implement only what stakeholders really need. "Nice to have" features waste precious time. When the Iron Cross tightens, scope is what you cut — not quality, not people, not the deadline.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 1.
