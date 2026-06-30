---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 05 Refactoring

Refactoring is the discipline of continuous improvement. Without it, code rots. With it, code stays young forever.

---

## What Is Refactoring?

> Changing the structure of code without changing its behavior.

The behavior is defined by the tests. If the tests pass before AND after, you've refactored. If behavior changes, you've done something else.

---

## The Basic Toolkit

| Technique | What It Does |
|-----------|-------------|
| **Rename** | Change variable, function, class names to reveal intent |
| **Extract Method** | Pull a block of code into a named function |
| **Extract Variable** | Give a complex expression a name |
| **Extract Field** | Pull duplicated logic into a shared field |

These four techniques handle 90% of refactoring. Master them before reaching for heavier tools.

---

## Rubik's Cube — The Analogy

Solving a Rubik's Cube is done in layers. You solve one layer at a time, and as you solve later layers, earlier layers get temporarily disrupted but end up solved. Refactoring works the same way: small steps, temporary disorder, final order.

> Don't try to refactor everything at once. One small improvement at a time. Keep the tests passing the whole way.

---

## The Disciplines of Refactoring

| Discipline | What It Means |
|-----------|--------------|
| **Tests** | Never refactor without tests. The tests are your safety net. |
| **Quick Tests** | Tests must run in seconds. If they take minutes, you'll stop running them. |
| **Break Deep One-to-One Correspondences** | Tests should test behavior, not structure. Refactoring shouldn't break tests. |
| **Refactor Continuously** | Not scheduled. Not "when there's time." Every hour, every day. |
| **Refactor Mercilessly** | If you see something to improve, improve it NOW. Don't add it to the backlog. |
| **Keep the Tests Passing** | Never break the tests during refactoring. If a test breaks, you changed behavior — undo and try differently. |
| **Leave Yourself an Out** | Commit before refactoring. If it goes wrong, revert and try again. |

---

## Refactoring vs Rewriting

| Refactoring | Rewriting |
|------------|-----------|
| Small, continuous steps | Big, all-at-once |
| Tests pass throughout | Tests broken for weeks |
| Always deployable | Nothing works until "done" |
| Safe | Risky |

> Big redesigns usually fail. Refactor continuously instead. The system improves incrementally — and never stops working.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 5.
- Fowler, Martin. *Refactoring*, 2nd ed., 2018.
