---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 07 Collaborative Programming

Programming is not a solo activity. Collaboration — through pairing, mobbing, and code review — distributes knowledge, reduces errors, and strengthens the team.

---

## Why Collaborate?

| Benefit | How |
|---------|-----|
| **Knowledge sharing** | No single person is the only one who understands a module |
| **Fewer errors** | A second pair of eyes catches mistakes in real time |
| **Better design** | Two minds on every design decision |
| **Mentoring** | Senior + junior = learning in both directions |
| **Bus factor** | If someone gets hit by a bus, the project survives |

---

## Pair Programming

Two developers, one workstation. Driver writes code. Navigator thinks strategically.

### The Rules

- **Voluntary.** Never mandated. Individual + team decision.
- **Intermittent.** Pair sometimes, solo sometimes.
- **Rotate frequently.** Pairs change. Knowledge spreads.
- **Short sessions.** 30 minutes to half a day.

### Ping-Pong Pairing

One writes the test, the other makes it pass. Then switch. TDD + Pairing combined.

---

## Mob Programming

The whole team on one problem. One driver, everyone else navigates. Extreme collaboration. Especially effective for:
- Complex architecture decisions
- Onboarding new team members
- Solving especially hard problems

---

## Collaboration as Code Review

Every line of code written in a pair or mob is reviewed as it's written. No separate review process needed. No pull requests sitting for days. No context-switching to review someone else's code.

> The most effective code review is the one that happens at the keyboard — not in a pull request 3 days later.

---

## The Cost Question

| Objection | Response |
|-----------|----------|
| "Two people on one task = half the output" | Two people produce more than half the output because they make fewer mistakes, design better, and don't get stuck. |
| "It's exhausting" | It IS intense. That's why sessions are short and pairing is intermittent. |
| "I work better alone" | Some tasks ARE better solo. Pairing is a tool, not a mandate. |

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 7.
