---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Layers and Boundaries

> *Source: Clean Architecture by Robert C. Martin, Chapter 25 (pp. 174–180)*

---

## Core Principle

> **Architectural boundaries exist everywhere. They are expensive to implement but even more expensive to add later when they are missing. The architect's job is not to build every boundary upfront—it is to watch for the inflection point where the cost of implementing a boundary drops below the cost of ignoring it, and act at exactly that moment.**

Simple systems can be expressed as three components (UI, business rules, database), but most real systems hide many more boundaries than first meet the eye. Using the Hunt the Wumpus game as a case study, this chapter walks through the gradual discovery of architectural boundaries—showing how a program that could be written in 200 lines of Kornshell reveals layer after layer of legitimate separation when you examine the axes of change. The conclusion is deliberately unsatisfying: there is no formula. The architect must watch, guess intelligently, and adapt continuously.

---

## The Rules / Key Concepts

### 1. Hunt the Wumpus — A Simple Case Study

The chapter uses the classic 1972 text-based adventure game *Hunt the Wumpus* as a proxy for a much larger system. The player types commands like `GO EAST` and `SHOOT WEST`; the computer responds with what the player sees, smells, hears, and experiences in a system of caverns filled with traps, pits, and a Wumpus to hunt.

Even this tiny game exposes multiple architectural boundaries when you look closely:

- **Initial decomposition:** UI component (messages from player), Game Rules (state of play), Data Storage (persisting game state).
- **First boundary—Language:** The UI may need to support English, Spanish, or other languages. A Language API decouples the Game Rules from any specific human language. The Game Rules define the API; Language components (English, Spanish) implement it.
- **Second boundary—Text Delivery:** Language is one axis of change; the *mechanism* for communicating text is another. A shell window, SMS, or chat application are all valid delivery mechanisms. A TextDelivery API isolates Language from the communication channel.

At each step, the **Dependency Rule** holds: source code dependencies point *inward* (or upward in the diagrams), toward higher-level policy. The API is always owned and defined by the *user* of the interface, not the implementer.

### 2. The Stream Architecture

Once the boundaries are in place, data flow organizes itself into **streams**:

- **Left stream:** User input rises from TextDelivery → Language → GameRules. GameRules output descends back through Language → TextDelivery to the user.
- **Right stream:** GameRules ships state down to DataStorage; DataStorage returns persisted state back up.

Both streams meet at the top at **GameRules**, which is the highest-level policy component (historically called the *Central Transform*). The arrows in the diagrams point in the direction of **source code dependencies**, not data flow—this is a critical distinction. Data flows in whatever direction it needs; dependencies always point toward abstractions.

### 3. Crossing the Streams — When to Add New Streams

Not all systems have exactly two streams. As systems grow more complex, the component structure splits into additional streams, all controlled by the highest-level policy component.

**Example:** A multiplayer version of Hunt the Wumpus introduces a **Network component**. The data flow now divides into three streams (text delivery, data persistence, and network communication), each originating from and returning to GameRules.

The principle: **streams multiply in proportion to the system's integration surface.** Each new I/O channel or external dependency creates a legitimate candidate for its own stream.

### 4. Splitting the Streams — Higher-Level Policies Within a Single Component

Even within what appears to be a single component, internal boundaries can emerge. Inside GameRules:

- **MoveManagement (lower-level):** Knows the mechanics of the cavern map—how caverns connect, where objects are, how the player moves between them, what events trigger on entering a cavern.
- **PlayerManagement (higher-level):** Knows the player's health, the cost or benefit of events (FoundFood, FellInPit), and ultimately decides whether the player wins or loses.

MoveManagement declares *events* to PlayerManagement; PlayerManagement manages state and policies at a higher level of abstraction. This is a legitimate architectural boundary within what originally looked like a single component.

**When this boundary becomes physical:** In a massive multiplayer version, MoveManagement runs locally on each player's computer while PlayerManagement runs on a server, exposed as a **micro-service API**. What was an internal conceptual split becomes a full-fledged architectural boundary with network separation.

### 5. The Cost of Boundaries

Fully implemented architectural boundaries are **expensive**. They require:

- Reciprocal polymorphic interfaces (in both directions)
- Input and output data structures that pass through the boundary
- Build and deployment isolation for independently compilable components
- Ongoing maintenance to prevent dependency leakage over time

At the same time, when a boundary is ignored and later proves necessary, the cost of retrofitting it is **very high**—even with comprehensive test suites and refactoring discipline. The codebase has grown without the separation, and untangling it requires surgical changes across dozens or hundreds of files.

### 6. YAGNI vs. Anticipatory Design — The Architect's Dilemma

The chapter frames the central tension honestly:

- **YAGNI wisdom:** *"You aren't going to need it."* Over-engineering (building boundaries you never use) is often worse than under-engineering. Every unnecessary boundary adds complexity, build overhead, and maintenance burden.
- **Retrofit pain:** When you discover you truly need a boundary that does not exist, the cost and risk of adding it late can dwarf the cost of having built it early.

Both sides are right. The resolution is not to choose one philosophy permanently but to **continuously re-evaluate**.

### 7. The Watchful Eye — Implement at the Inflection Point

Martin's operating advice for architects:

1. **You must see the future.** Guess intelligently about where architectural boundaries lie. Decide which should be fully implemented, partially implemented, or ignored—but not as a one-time decision at project start.

2. **Watch the system evolve.** Note where boundaries *may* be required. Pay attention to the first hints of **friction**—places where the absence of a boundary causes pain, repeated workarounds, or fragile code.

3. **Weigh costs frequently.** Compare the ongoing cost of ignoring a boundary against the cost of implementing it. Revisit the decision as the system changes.

4. **Implement at the inflection point.** The goal is to build the boundary exactly when the cost of implementing it becomes less than the cost of ignoring it—not before, not long after. This requires a **watchful eye** and the discipline to act when the signals appear rather than deferring indefinitely.

---

## Summary Checklist

- [ ] Look beyond the obvious three-component decomposition (UI / business rules / database)—most systems hide multiple legitimate architectural boundaries
- [ ] The Dependency Rule still applies: APIs are defined and owned by the *user* of the interface, not the implementer
- [ ] Data flow organizes into streams; source code dependencies point toward higher-level policy, not in the direction of data flow
- [ ] When systems grow, streams multiply—each new I/O channel or external integration is a candidate for its own stream
- [ ] Higher-level policies can hide inside what appears to be a single component; watch for the moment when they need to split
- [ ] Architectural boundaries are expensive in both directions: building them too early wastes effort, adding them too late risks the codebase
- [ ] Do not decide once at project start—watch continuously, weigh costs frequently, and implement at the inflection point
- [ ] The first hint of friction (workarounds, fragility, repeated pain) is the signal to re-evaluate whether a boundary is overdue

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Boundaries]]
- [[Screaming Architecture]]
- [[Presenters and Humble Objects]]
- [[Architectural Independence]]
- [[Main Component and Services]]
- [[Component Cohesion]]
