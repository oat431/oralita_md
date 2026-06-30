---
tags:
- design-patterns
- introduction
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Introduction to Design Patterns" (pp. 26–31)*

## Core Principle

> Design patterns are typical solutions to commonly occurring problems in software design — pre-made blueprints you customize, not copy-paste code.

---

## What's a Design Pattern?

- **Definition:** A general, reusable solution to a recurring problem in software design. It's a concept, not finished code you drop into your program.
- **Pattern vs. Algorithm:**
  - An **algorithm** is like a cooking recipe — it defines a clear, ordered set of steps to achieve a goal.
  - A **pattern** is like a blueprint — you can see the result and its features, but the exact order of implementation is up to you.
- **Blueprint Analogy:** You follow the pattern's details and adapt the solution to fit the realities of your own program. The same pattern applied to two different programs may produce different code.

---

## Anatomy of a Pattern

Most patterns are described formally so they can be reproduced across many contexts. A standard pattern description includes:

- **Intent** — Briefly describes both the problem and the solution.
- **Motivation** — Further explains the problem and how the pattern solves it.
- **Structure of Classes** — Shows each part of the pattern and how the parts relate to one another.
- **Code Example** — A concrete implementation in a popular language that makes the idea easier to grasp.

Some pattern catalogs also include:

- Applicability (when to use / when not to use)
- Implementation steps
- Relations with other patterns

---

## Classification

Patterns differ by complexity, level of detail, and scale of applicability:

- **Idioms** — The most basic, low-level patterns. Usually tied to a single programming language.
- **Patterns** — The mid-level patterns this book focuses on; language-agnostic solutions to common design problems.
- **Architectural Patterns** — The most universal, high-level patterns. Can be implemented in virtually any language and used to design the architecture of an entire application.

### By Intent (Three Main Groups)

| Group | Purpose |
|---|---|
| **Creational** | Provide object creation mechanisms that increase flexibility and reuse of existing code. |
| **Structural** | Explain how to assemble objects and classes into larger structures while keeping them flexible and efficient. |
| **Behavioral** | Take care of effective communication and the assignment of responsibilities between objects. |

---

## History

- The pattern concept originated with **Christopher Alexander**, an architect who wrote *A Pattern Language: Towns, Buildings, Construction*. The book describes a "language" for designing urban environments whose units are patterns (window height, building levels, green areas, etc.).
- The idea was adopted by four software engineers — **Erich Gamma, John Vlissides, Ralph Johnson, and Richard Helm** — known as the **Gang of Four (GoF)**.
- In **1994**, they published *Design Patterns: Elements of Reusable Object-Oriented Software*, applying the pattern concept to programming. The book catalogued **23 patterns** for object-oriented design and became a best-seller.
- Since then, dozens more object-oriented patterns have been discovered, and the pattern approach has spread to many other programming fields beyond OOP.

---

## Why Learn Patterns?

- **Toolkit of tried and tested solutions** — Patterns give you ready-made approaches to common design problems. Even if you never encounter the exact problem, studying patterns teaches you how to solve all sorts of problems using OOP principles.
- **Common language for teams** — Patterns define a shared vocabulary. You can say *"Use a Singleton for that"* and everyone on the team immediately understands the idea — no lengthy explanation needed.

---

## Summary Checklist

- [ ] Understand that a pattern is a general solution concept, not copy-paste code
- [ ] Distinguish between a pattern (blueprint) and an algorithm (recipe)
- [ ] Name the four standard sections of a pattern description: Intent, Motivation, Structure, Code Example
- [ ] Know the three levels of classification: Idioms → Patterns → Architectural Patterns
- [ ] Know the three groups by intent: Creational, Structural, Behavioral
- [ ] Recognize GoF as the Gang of Four who published the 23-pattern catalog in 1994
- [ ] Recall Christopher Alexander as the originator of the pattern concept (urban architecture)
- [ ] Articulate the two main reasons to learn patterns: reusable solutions + shared team vocabulary

---

## Related

- [[introduction-to-oop]]
- [[design-principles]]
- [[solid-principles]]
- [[factory-method]]
- [[abstract-factory]]
- [[Builder]]
- [[Prototype]]
- [[Singleton]]
- [[Adapter]]
- [[Bridge]]
- [[Composite]]
- [[Decorator]]
- [[Facade]]
- [[Flyweight]]
- [[Proxy]]
- [[chain-of-responsibility]]
- [[Command]]
- [[Iterator]]
- [[Mediator]]
- [[Memento]]
- [[Observer]]
- [[State]]
- [[Strategy]]
- [[template-method]]
- [[Visitor]]
