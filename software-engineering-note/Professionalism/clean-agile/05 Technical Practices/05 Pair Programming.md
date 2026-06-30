---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 05 Pair Programming

Two programmers, one screen. One types (driver), one thinks (navigator). Pairing is optional, intermittent, and the team's decision — not the manager's.

---

## How Pairing Works

| Role | What They Do |
|------|-------------|
| **Driver** | Keyboard and mouse. Writes the code. |
| **Navigator** | Watches, thinks strategically, spots errors, gives direction. |

### Ping-Pong

One programmer writes a test. The other makes it pass. Roles switch frequently. This is TDD + Pairing combined.

---

## The Rules of Pairing

| Rule | Why |
|------|-----|
| **Optional** | Not mandated. Individual + team decision. |
| **Intermittent** | Pair sometimes, program alone sometimes. |
| **Spontaneous** | Not scheduled. Pairs form and dissolve naturally. |
| **Short-lived** | 30 minutes to a full working day. Then dissolve. |
| **Rotate frequently** | Knowledge spreads. No permanent pairs. |

---

## The Benefits (Beyond Obvious Efficiency Loss)

> At first glance: two programmers behind one screen can't write as much code as two separate workstations. But that's the wrong metric.

| Benefit | How |
|---------|-----|
| **Knowledge sharing** | Especially when seniors pair with juniors |
| **Fewer errors** | Navigator catches mistakes in real time |
| **Better design** | Two minds on every design decision |
| **Stronger collaboration** | Team cohesion improves |
| **Code review built-in** | Every line is reviewed as it's written |

---

## Pairing for Review, Not Just Writing

Pairing is useful for reviewing existing code — not just writing new code. Walk through the codebase together. Share understanding.

---

## Mob Programming

> Three or more people on one problem. Extreme pairing. Especially effective for complex problems, architecture decisions, or onboarding new team members.

---

## The Programmer's Domain

> Don't ask for permission to pair. This is the programmer's domain. The programmer is the expert.

Managers generally like seeing collaboration and knowledge sharing. They won't complain about pairing — but they also shouldn't mandate it.

---

## The Bottom Line

Without the technical practices — TDD, refactoring, simple design, pairing — Agile becomes a mess-making machine. You'll build a big mess in a hurry.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 5.
