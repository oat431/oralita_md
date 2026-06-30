---
tags:
- clean-architecture
- software-design
- software-engineering
---

# The Clean Architecture

> *Source: Clean Architecture by Robert C. Martin, Chapter 22 (pp. 161–166)*

---

## Core Principle

> **Divide software into concentric layers with strict inward-pointing dependencies. The further inward, the higher-level the policy. The outer circles are mechanisms; the inner circles are policies.**

The Clean Architecture unifies Hexagonal Architecture (Ports and Adapters), DCI, and BCE into a single actionable diagram. Its overriding rule — the Dependency Rule — states that source code dependencies must point only inward, toward higher-level policies. Nothing in an inner circle may know anything about an outer circle. This produces systems that are independent of frameworks, testable without external elements, and easy to change when UI, database, or infrastructure details become obsolete.

---

## The Architecture: Concentric Circles

The system is organized into four concentric layers. Each layer depends only on the layer directly inward — never outward.

```
┌──────────────────────────────────────────────────────┐
│  Frameworks & Drivers                                │
│  ┌────────────────────────────────────────────────┐  │
│  │  Interface Adapters                             │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Use Cases (Application Business Rules)   │  │  │
│  │  │  ┌────────────────────────────────────┐  │  │  │
│  │  │  │  Entities (Enterprise Business Rules)│  │  │  │
│  │  │  └────────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
    ← Dependencies point inward only
```

### 1. Entities (Innermost Circle)

**Encapsulate enterprise-wide Critical Business Rules.** An entity can be an object with methods or a set of data structures and functions. If there is no enterprise — just a single application — entities are the application's business objects. They encapsulate the most general, highest-level rules and are the **least likely to change** when something external changes (page navigation, security, operational changes).

### 2. Use Cases (Application Business Rules)

**Encapsulate and implement all use cases of the system.** This layer contains application-specific business rules that orchestrate the flow of data to and from entities and direct entities to use their Critical Business Rules to achieve use case goals.

Changes to application operation *will* affect this layer. But changes to externalities (database, UI, frameworks) should not. The use cases layer is isolated from such concerns.

### 3. Interface Adapters

**Convert data between the format most convenient for use cases/entities and the format most convenient for external agencies.** This layer wholly contains:

- **GUI MVC architecture** — Presenters, Views, Controllers
- **Database adapters** — All SQL is restricted to this layer
- **External service adapters** — Any adapter converting between external and internal data formats

Models passing between controllers and use cases are plain data structures — not entity objects or database rows.

### 4. Frameworks & Drivers (Outermost Circle)

**Where all the details go.** The web is a detail. The database is a detail. Generally you write little code here beyond glue code that communicates inward. Keeping details on the outside minimizes the harm they can do.

> **There is no rule that says you must have exactly four circles.** The diagram is schematic. You may need more layers. But the Dependency Rule always applies: dependencies point inward, and the level of abstraction increases as you move inward.

---

## The Dependency Rule

> **Source code dependencies must point only inward, toward higher-level policies.**

**Absolute prohibition:** Nothing in an inner circle can know anything about something in an outer circle. This includes:

- **Names** — No function, class, variable, or any named software entity declared in an outer circle may be mentioned by code in an inner circle
- **Data formats** — No data format declared in an outer circle (especially framework-generated formats) may be used by an inner circle
- **Framework imports** — No `import` or `using` statement in a use case or entity may reference a framework or driver module

The further inward you go, the higher-level and more abstract the software becomes. The innermost circle is the most general and highest level. The outermost circle is low-level concrete details.

---

## Crossing Boundaries

The flow of control and source code dependencies often point in opposite directions. The Dependency Inversion Principle resolves this.

### The Problem

Control flow typically starts in the controller (outer), moves through the use case (inner), then executes in the presenter (outer). The use case may need to call the presenter — but a direct call from inner to outer would violate the Dependency Rule.

### The Solution: Interface Inversion

1. **Define an interface in the inner circle** (the "Use Case Output Port")
2. **The use case calls the interface** — satisfying the Dependency Rule (both interface and use case are inner)
3. **The presenter in the outer circle implements the interface** — the outer circle depends on the inner circle, not the other way

```
Controller ──→ UseCaseInteractor ──→ OutputBoundary (interface, inner)
                                           ↑
                                     implements
                                           │
                                      Presenter (outer)
```

The same technique — dynamic polymorphism to oppose source code dependencies to the flow of control — is used to cross all boundaries at all layers.

### What Crosses Boundaries

**Simple, isolated data structures only.** You can use:

- Plain structs or simple Data Transfer Objects (DTOs)
- Function call arguments
- Hashmaps
- Constructed objects (without inner-circle-violating dependencies)

**What must NOT cross:**
- Entity objects
- Database rows or row structures from frameworks
- Any data structure with dependencies that violate the Dependency Rule

Data crossing a boundary is always in the form most convenient for the **inner** circle.

---

## A Typical Scenario (Web-Based Java System)

The diagram in Figure 22.2 illustrates the full request lifecycle:

| Step | Layer | Action |
|------|-------|--------|
| 1 | Web Server | Gathers input from user, hands to Controller |
| 2 | Controller | Packages input into a **plain Java object**, passes it through `InputBoundary` to `UseCaseInteractor` |
| 3 | UseCaseInteractor | Interprets input data, orchestrates Entities |
| 4 | UseCaseInteractor | Uses `DataAccessInterface` to bring entity data from Database into memory |
| 5 | UseCaseInteractor | Gathers results from Entities, constructs **OutputData** (plain Java object) |
| 6 | UseCaseInteractor | Passes OutputData through `OutputBoundary` interface to Presenter |
| 7 | Presenter | Repackages OutputData into **ViewModel** — strings, flags, formatted dates/currency, button/menu states |
| 8 | View | Moves data from ViewModel into the HTML page (almost nothing left to do) |

**All arrows cross boundaries pointing inward, following the Dependency Rule.**

---

## Summary Checklist

- [ ] Are source code dependencies pointing **only inward** — never toward an outer circle?
- [ ] Can business rules be tested **without** the UI, database, web server, or any external element?
- [ ] Can the UI be swapped (web → console) **without changing business rules**?
- [ ] Can the database be swapped (Oracle → MongoDB) **without touching entities or use cases**?
- [ ] Do entities encapsulate the **most general, highest-level** business rules?
- [ ] Are use cases isolated from database, UI, and framework concerns?
- [ ] Are all SQL statements restricted to the **Interface Adapters** layer?
- [ ] Is all data crossing boundaries in the form most convenient for the **inner circle**?
- [ ] Are boundary crossings resolved via **interfaces** (Output Ports) using the Dependency Inversion Principle?
- [ ] Are only **simple data structures** (DTOs, plain objects, arguments) crossing boundaries — never entity objects or database rows?
- [ ] Are frameworks and drivers treated as **details** on the outermost circle?

---

## Related

- [[Clean Architecture Overview]] — The full picture and motivations behind Clean Architecture
- [[SOLID Design Principles]] — The Dependency Inversion Principle (DIP) is how boundaries enforce the Dependency Rule
- [[Boundaries]] — Crossing boundaries with interfaces and the formal boundary-decoupling patterns
- [[Policy and Business Rules]] — Entities and Use Cases: the distinction between enterprise-wide Critical Business Rules and application-specific logic
- [[Presenters and Humble Objects]] — How Interface Adapters keep the View humble and testable
- [[Screaming Architecture]] — An architecture should scream its intent; the Clean Architecture achieves this by making business rules the center
- [[Details - Database, Web, Frameworks]] — Why the database, web, and frameworks belong in the outermost circle
- [[Component Cohesion]] — How higher-level architecture decisions translate to component grouping
- [[Component Coupling]] — Dependency management at the component level mirrors the Dependency Rule
