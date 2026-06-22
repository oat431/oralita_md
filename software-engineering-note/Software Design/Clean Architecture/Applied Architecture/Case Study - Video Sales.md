# Case Study - Video Sales

> *Source: Clean Architecture by Robert C. Martin, Chapter 33 (pp. 220–224)*

---

## Core Principle

> **Separate components by actor (who triggers change) and by policy level (how fast they change), then defer deployment grouping decisions until you see how the system actually evolves.**

Architecture is not about getting the final deployment topology right on day one. It's about building a code structure that keeps options open—so you can independently develop, test, and deploy components that change for different reasons and at different rates. The Dependency Rule and the Single Responsibility Principle are the two axes that make this possible.

---

## The Case Study

### The Product

A website that sells video tutorials. Videos can be streamed or downloaded. There are three license models:

- **Individuals** pay one price to stream, a higher price to download and own permanently. The individual is both purchaser and viewer.
- **Businesses** purchase streaming licenses in batches with quantity discounts. The purchaser and the viewer are often different people.
- **Video authors** supply video files, descriptions, and ancillary materials (exams, problems, solutions, source code).
- **Administrators** manage video series, add or remove videos, and set prices for each license type.

### Step 1: Identify Actors and Use Cases

Four primary actors drive all change in the system. Under the **Single Responsibility Principle**, each actor is a distinct axis of change—a feature requested by one actor should not ripple into code that serves another.

| Actor | Role |
|---|---|
| Viewer | Watches streamed videos |
| Purchaser | Buys licenses (individual or business) |
| Author | Supplies video content and materials |
| Admin | Manages catalog, series, and pricing |

The use-case diagram also introduces **abstract use cases**—general policies that concrete use cases flesh out. For example, `View Catalog as Viewer` and `View Catalog as Purchaser` both inherit from an abstract `View Catalog` use case. This abstraction isn't strictly necessary for functionality, but recognizing the shared behavior early avoids duplication and creates a natural extension point.

### Step 2: Preliminary Component Architecture

With actors and use cases known, Martin draws a component architecture split along two dimensions:

1. **By architectural layer**: Views → Presenters → Interactors → Controllers → Utilities
2. **By actor**: Each layer is subdivided into components for Viewer, Purchaser, Author, and Admin

Each box in the diagram represents a potential `.jar` or `.dll`. The abstract `View Catalog` use case becomes abstract classes in dedicated **Catalog View** and **Catalog Presenter** components, which the concrete viewer/purchaser components inherit from.

This is not a deployment diagram—it's a **compile-time partitioning**. The physical grouping into deployable files is deliberately deferred:

- Could ship as **many small .jars** (one per component).
- Could **merge by layer**: views.jar, presenters.jar, interactors.jar, controllers.jar, utilities.jar (5 files).
- Could **merge by volatility**: views+presenters together, everything else together (2 files).

The point: the code structure makes any of these groupings trivial, so the team can adapt deployment based on how the system actually changes in production—not based on a guess made upfront.

### Step 3: Dependency Management and the Dependency Rule

Control flows **right to left** in the diagram: Controllers receive input → Interactors process it → Presenters format results → Views display them.

But dependency arrows point **left to right**—against the flow of control, toward higher-level policy. This is the Dependency Rule in action:

- **Using relationships** (open arrows) follow the flow of control.
- **Inheritance relationships** (closed arrows) point against the flow of control, implementing the **Open–Closed Principle**: high-level policy defines interfaces; low-level details implement them. Changes to views or controllers never force recompilation of interactors or business rules.

### Step 4: Two Dimensions of Separation

The architecture has two orthogonal axes of decoupling:

| Dimension | Principle | Separates by… |
|---|---|---|
| Actor axis | Single Responsibility Principle | *Reason* for change (who requested it) |
| Policy axis | Dependency Rule | *Rate* of change (high-level policy vs. low-level detail) |

Together, they ensure that a pricing change requested by Admin doesn't break the viewer's streaming experience, and a UI framework migration doesn't force a rewrite of the purchase interactor.

---

## Summary Checklist

- [ ] Identify all actors before drawing a single component—each actor is a primary source of change
- [ ] Partition the system so a change serving one actor never forces a rebuild of another actor's code
- [ ] Use abstract use cases to unify shared behavior early (e.g., `View Catalog` for viewer and purchaser)
- [ ] Separate by architectural layer: Views, Presenters, Interactors, Controllers, Utilities
- [ ] Cross-cut layers by actor: Viewer, Purchaser, Author, Admin
- [ ] Every component is a potential .jar/.dll at compile time—not necessarily at deploy time
- [ ] Defer deployment grouping; the architecture must make regrouping trivial when conditions change
- [ ] Dependencies always point toward higher-level policy (against the flow of control)
- [ ] Inheritance arrows point against control flow to satisfy the Open–Closed Principle
- [ ] Two dimensions of separation: actor (SRP) determines *why* things change; policy level (Dependency Rule) determines *how fast* they change

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Policy and Business Rules]]
- [[Boundaries]]
- [[Component Cohesion]]
- [[Component Coupling]]
- [[Presenters and Humble Objects]]
