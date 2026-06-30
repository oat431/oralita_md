---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Features of Good Design" (pp. 32–36)*

# Features of Good Design

## Core Principle

> Good design balances two competing forces: **maximizing code reuse** to reduce cost and time-to-market, and **building for extensibility** so the system can adapt to the inevitable changes that follow. Design patterns sit at the sweet spot between the low-level reuse of individual classes and the high-risk investment of full frameworks.

---

## Code Reuse

- **Cost and time are the two most valuable metrics** in software development. Less time in development means entering the market earlier; lower costs leave more budget for marketing and broader customer reach.
- Code reuse is the most straightforward way to cut development costs — *in theory*. In practice, making existing code work in a new context often takes significant extra effort.
- **What kills reusability:**
  - Tight coupling between components
  - Dependencies on concrete classes instead of interfaces
  - Hardcoded operations
- Design patterns increase component flexibility and reusability, though sometimes at the cost of increased complexity.

### Three Levels of Reuse (Erich Gamma)

Erich Gamma, one of the Gang of Four, describes reuse in three layers of increasing scale and risk:

| Level | Scope | Characteristics | Risk | Example |
|-------|-------|-----------------|------|---------|
| **Classes** (lowest) | Class libraries, containers, class "teams" like container/iterator | Granular, concrete code reuse | Low | Standard library collections |
| **Patterns** (middle) | Description of how classes relate and interact | Reuse design ideas independently of concrete code | Moderate | Observer, Strategy, Factory |
| **Frameworks** (highest) | Distills design decisions; identifies key abstractions and defines relationships | You hook in via subclassing | High (significant investment) | JUnit, Spring |

> *"The framework lets you define your custom behavior, and it will call you when it's your turn to do something. Same with JUnit, right? It calls you when it wants to execute a test for you, but the rest happens in the framework."* — Erich Gamma

This is the **Hollywood Principle**: *"Don't call us, we'll call you."*

- **Why patterns win the middle layer:** Patterns offer reuse that is less risky than frameworks. Building a framework is a high-risk, high-investment endeavor. Patterns let you reuse design ideas and concepts independently of concrete code — you get the design wisdom without locking into a framework's constraints.

---

## Extensibility

> *Change is the only constant thing in a programmer's life.*

Three forces drive change in every software project:

### 1. Understanding Grows Over Time
- By the time you finish the first version, you understand the problem much better than when you started.
- You've grown professionally — and your own earlier code now looks like crap.
- Many developers finish v1 ready to rewrite from scratch.

### 2. The World Changes Around You
- External factors beyond your control force change.
- Examples: browsers dropping Flash support, new operating systems, shifting platform requirements.
- Entire dev teams pivot from original ideas when the environment shifts.

### 3. The Goalposts Move
- Clients see the excellent first version and realize *even more is possible*.
- They request features they never mentioned in original planning sessions.
- These aren't frivolous — the first version proved the value, and now they want to expand it.

> Bright side: *if someone asks you to change something in your app, that means someone still cares about it.*

- **Takeaway:** Seasoned developers design architecture with future changes in mind from the start — not to predict every change, but to make changes *cheap* when they arrive.

---

## Summary Checklist

- [ ] Understand that code reuse is a cost/time lever, not an automatic win
- [ ] Avoid tight coupling, concrete class dependencies, and hardcoded operations
- [ ] Know the three levels of reuse: classes → patterns → frameworks
- [ ] Recognize that patterns offer design reuse with less risk than frameworks
- [ ] Internalize the Hollywood Principle: "Don't call us, we'll call you"
- [ ] Accept that change is constant — understanding grows, the world shifts, and goalposts move
- [ ] Design architecture to make future changes cheap, not to predict every change

---

## Related

- [[Introduction to OOP]]
- [[Design Principles]]
- [[SOLID Principles]]
