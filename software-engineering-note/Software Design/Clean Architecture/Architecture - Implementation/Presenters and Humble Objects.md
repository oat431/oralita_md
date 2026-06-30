---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Presenters and Humble Objects

> *Source: Clean Architecture by Robert C. Martin, Chapters 23–24 (pp. 167–173)*

---

## Core Principle

> **Split every architectural boundary into a testable module and a "humble" module stripped down to its barest essence. The humble object contains only the hard-to-test behaviors; the testable module contains everything else. This separation defines and protects architectural boundaries while making the entire system testable without frameworks, databases, or GUIs.**

The Humble Object pattern originated in unit testing as a way to isolate untestable code. But its true power is architectural: Presenters, Views, Database Gateways, ORMs, and Service Listeners are all Humble Object boundaries. When a full boundary is too expensive, implement a *partial boundary*—skip the last step, use the Strategy pattern, or rely on a Facade—to hold the place for future separation without paying the full cost upfront.

---

## The Rules / Key Concepts

### 1. The Humble Object Pattern

Originally identified to help unit testers, the Humble Object pattern separates behaviors that are *hard to test* from behaviors that are *easy to test*. Split the code into two modules or classes:

- **The Humble module:** Contains all hard-to-test behaviors, stripped to their barest essence. It does no processing—it only moves data.
- **The Testable module:** Contains all the logic that was extracted from the humble object. It is fully testable with stubs and doubles.

GUIs are the classic example. Unit-testing a screen is nearly impossible—you cannot programmatically see pixels and verify widget placement. But most GUI *behavior* (deciding what should appear, formatting values, setting enabled/disabled state) is pure logic that tests beautifully.

### 2. Presenters and Views

The Presenter/View split is the canonical Humble Object pair for UI:

- **The View is humble.** It is hard to test, so it is kept dead simple. It moves data from a View Model into the screen but performs no processing, no formatting, no decisions. It reads strings, booleans, and enums and slaps them onto GUI widgets.
- **The Presenter is testable.** It accepts raw application data, formats it for display, and populates a plain View Model data structure.

The **View Model** is a simple data structure with no behavior—just strings, booleans, and enums. Everything the screen can display is represented there:

| What appears on screen | What goes in the View Model |
|---|---|
| A date field | String (pre-formatted by Presenter) |
| A currency amount | String (with decimal places and markers) |
| A negative-currency-coloring rule | Boolean flag (red = true) |
| Button names and enabled/disabled state | String + Boolean |
| Menu items, radio buttons, checkboxes | Strings + Booleans |
| Table cells | Pre-formatted strings |

The View loads the View Model and renders it. That is all. No `if` statements, no formatting, no logic. The Presenter does every decision upstream.

### 3. Database Gateways (Humble Objects Between Interactors and ORM)

Between use case interactors and the database sit **Database Gateways**—polymorphic interfaces that expose every CRUD operation the application needs. For example:

```
interface UserGateway {
    List<String> getLastNamesOfUsersWhoLoggedInAfter(Date date);
}
```

- SQL is **not allowed** in the use cases layer. The interactors call the gateway interface, never the database directly.
- The gateway **implementation** (in the database layer) is the humble object. It simply translates each method into SQL or whatever the database interface requires.
- The **interactors** are not humble—they contain business rules—but they are testable because the gateway can be swapped with stubs and test-doubles.

This boundary lets you unit-test business logic without a running database.

### 4. Data Mappers (ORMs Belong in the Database Layer)

Object-relational mappers (ORMs) like Hibernate are not true "object mappers" because objects are *not* data structures:

- From the user's point of view, an object is a set of operations—its data is private and invisible.
- A data structure is a set of public variables with no implied behavior.

ORMs would be better named **Data Mappers**: they load relational data into plain data structures. They belong squarely in the **database layer**, behind the gateway interface. ORMs form another Humble Object boundary—the gateway interface isolates the use cases from the ORM, and the ORM is humble (it just maps data, nothing more).

### 5. Service Listeners

When an application communicates with external services, the Humble Object pattern creates a **service boundary**:

- **Outbound:** The application loads data into simple data structures and passes them across the boundary to modules that format and send them to external services.
- **Inbound:** Service listeners receive raw data from the service interface, parse it, and place it into a simple data structure that crosses the service boundary back to the application.

The listener/formatting module is humble (hard-to-test wire protocols and serialization). The application-side logic remains testable, isolated behind the service boundary.

### 6. Partial Boundaries — When a Full Boundary Is Too Expensive

Full architectural boundaries are expensive. They require reciprocal polymorphic interfaces, Input/Output data structures, and the dependency management to keep both sides independently compilable and deployable—plus ongoing maintenance overhead.

A good architect sometimes judges the full boundary cost too high—but still wants a placeholder in case the boundary is needed later. Three strategies:

#### 6a. Skip the Last Step

Do *all* the design work: reciprocal interfaces, Input/Output structures, dependency inversion. But compile and deploy everything as a **single component** instead of splitting them.

- **Pro:** Same code and design as a full boundary; no version-tracking or multi-component release burden.
- **Con:** Without the physical barrier of separate components, boundaries degrade over time. Dependencies start crossing in the wrong direction. Re-separation becomes a chore.

*FitNesse used this pattern.* The web-server component was designed to be separable from the wiki/testing component, but they shipped one jar. Over time, the separation weakened because it was never exercised.

#### 6b. One-Dimensional Boundaries (Strategy Pattern)

Use the **Strategy pattern** with a single interface, no reciprocal interface:

```
Client  ──►  ServiceBoundary (interface)
                  ▲
                  │
            ServiceImpl (implements)
```

- The Client depends on the `ServiceBoundary` interface; `ServiceImpl` implements it. Dependency inversion is in place *in one direction only*.
- **Pro:** Lower cost than a full boundary. Sets the stage for future separation.
- **Con:** Without a reciprocal interface, nothing prevents the Client from grabbing a concrete reference to `ServiceImpl` (the dreaded "backchannel" dotted arrow). Discipline alone enforces the boundary.

#### 6c. Facades

Even simpler: a **Facade class** lists all services as methods and delegates calls to service classes the client is not supposed to touch directly.

```
Client  ──►  Facade  ──►  Service classes (hidden)
```

- **Pro:** Lowest cost. Easy to implement.
- **Con:** The Client has a *transitive dependency* on every service class. In static languages, a source change in any service forces the Client to recompile. Backchannels are trivially easy to create—the boundary is purely a naming convention.

---

## Summary Checklist

- [ ] Every architectural boundary splits into a humble module (hard to test, no logic) and a testable module (contains all behavior)
- [ ] Views are humble—they load a View Model and render it; Presenters own all formatting logic
- [ ] Database Gateways isolate interactors from SQL/ORM; the gateway implementation is humble
- [ ] ORMs (Data Mappers) live in the database layer behind the gateway interface, never in the use-case layer
- [ ] Service Listeners encapsulate wire-protocol details behind a humble boundary so application logic stays testable
- [ ] Full boundaries are evaluated for cost; partial boundaries (skip the last step, Strategy, Facade) serve as placeholders when full isolation isn't justified yet
- [ ] Every partial boundary carries a degradation risk—discipline and regular review are the only defense

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Boundaries]]
- [[Screaming Architecture]]
- [[Layers and Boundaries]]
- [[Policy and Business Rules]]
- [[Testing and Embedded]]
