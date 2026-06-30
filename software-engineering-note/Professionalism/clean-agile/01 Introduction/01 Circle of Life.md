---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 01 Circle of Life

From Kent Beck's *Extreme Programming Explained* — the Circle of Life organizes XP practices into three concentric rings. Practices in the inner rings depend on those in the outer rings. Start from the outside and work inward.

---

## The Three Rings

```
        ┌──────────────────────────┐
        │    Business-Facing       │
        │  ┌────────────────────┐  │
        │  │   Team-Facing      │  │
        │  │  ┌──────────────┐  │  │
        │  │  │  Technical   │  │  │
        │  │  │   Practices  │  │  │
        │  │  └──────────────┘  │  │
        │  └────────────────────┘  │
        └──────────────────────────┘
```

### Outer Ring — Business-Facing (like Scrum)

| Practice | What It Is |
|----------|-----------|
| **Planning Game** | Break project into features, stories, tasks |
| **Small Releases** | Regular, small increments |
| **Acceptance Tests** | Unambiguous completion criteria ("Definition of Done") |
| **Whole Team** | Programmers, testers, management working together |

### Middle Ring — Team-Facing

| Practice | What It Is |
|----------|-----------|
| **Sustainable Pace** | Progress without burnout |
| **Collective Ownership** | No code silos. Everyone can work on anything. |
| **Continuous Integration** | Frequent merging, fast feedback |
| **Metaphor** | Common vocabulary and language |

### Inner Ring — Technical

| Practice | What It Is |
|----------|-----------|
| **Pair Programming** | Two programmers, one screen |
| **Simple Design** | No waste. Code only what's needed. |
| **Refactoring** | Continuous improvement of all work products |
| **Test-Driven Development** | Quality at speed |

---

## Practices Mapped to Manifesto Values

| Manifesto Value | Supporting Practices |
|----------------|---------------------|
| **Individuals and interactions** over processes | Whole Team, Metaphor, Collective Ownership, Pairing |
| **Working software** over documentation | Acceptance Tests, TDD, Simple Design, Refactoring, CI |
| **Customer collaboration** over contract | Planning Game, Small Releases, Acceptance Tests, Metaphor |
| **Responding to change** over plan | Planning Game, Small Releases, Acceptance Tests, Sustainable Pace, Refactoring, TDD |

---

## The Critical Warning

> Without the technical practices (inner ring), the code degrades. Then the Agile practices in the outer rings will make a mess of everything **very quickly.**

The inner ring is what keeps Agile from becoming an efficient mess-making machine. Ignore TDD, refactoring, simple design, and pairing — and Agile becomes Waterfall with shorter deadlines.

---

## Sources

- Beck, Kent. *Extreme Programming Explained*, 2nd ed., Addison-Wesley, 2004.
- Martin, Robert C. *Clean Agile*, Chapter 1.
