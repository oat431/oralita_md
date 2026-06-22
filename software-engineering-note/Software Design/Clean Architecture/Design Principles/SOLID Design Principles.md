# SOLID Design Principles

> *Source: Clean Architecture by Robert C. Martin, Chapters 7–11 (pp. 64–87)*

---

## Core Principle

> **Good architecture separates code by how, why, and when it changes, then organizes that separated code into a dependency hierarchy where high-level policy is protected from low-level detail. SOLID is not just a set of class-design heuristics—it is the brickwork that becomes the walls and rooms of an architecture.**

The five SOLID principles operate at the class and module level, but each one recurs at higher levels: SRP becomes the Axis of Change that creates Architectural Boundaries, OCP becomes the dependency hierarchy that protects business rules, LSP governs the substitutability of whole components and services, ISP shields components from unnecessary transitive baggage, and DIP becomes the Dependency Rule that all architectural boundaries obey. Taken together, they define how to partition a system into components that are independently developable, deployable, extensible, and resistant to cascading change.

---

## The Principles

### 1. SRP: Single Responsibility Principle

> **A module should be responsible to one, and only one, actor.**

The SRP is the most misunderstood SOLID principle. It does *not* mean "a module should do only one thing"—that is a function-level refactoring guideline. The architectural SRP defines a module as any cohesive set of functions and data structures, and ties its reason to change to a specific *actor* (a person or group of stakeholders who require that change).

A module that serves multiple actors couples those actors together. This coupling produces two architectural symptoms:

**Symptom 1: Accidental Duplication.** When two actors share an algorithm through a common private function, a change for one actor can silently corrupt the other actor's results—without either actor or developer noticing until the damage is done.

```
Employee (❌ — single class serving three actors)
├── calculatePay()   → CFO / Accounting
├── reportHours()    → COO / HR
└── save()           → CTO / DBA

     calculatePay() ──┐
                       ├── regularHours() ← shared algorithm
     reportHours()  ──┘
```

**Symptom 2: Merge Conflicts.** When the CTO's team and the COO's team both check out the same file for unrelated changes, merge collisions put both actors at risk.

**The Architectural Solution:** Separate code serving different actors into different components. Three approaches:

```
✅ Solution A — Data + Separate Classes
┌─────────────┐     ┌──────────────┐
│ EmployeeData│◄────│PayCalculator │  → CFO
│  (struct)   │     └──────────────┘
│             │     ┌──────────────┐
│  no methods │◄────│HourReporter  │  → COO
└─────────────┘     └──────────────┘
                    ┌──────────────┐
                    │EmployeeSaver │  → CTO
                    └──────────────┘

✅ Solution B — Facade Pattern
✅ Solution C — Keep core method on original class as facade
```

Each class is now a **scope**: its private methods are invisible to the other actors. No accidental sharing, no cross-actor merge risk.

At the component level, SRP becomes the **Common Closure Principle** (CCP). At the architectural level, it becomes the **Axis of Change** that defines where Architectural Boundaries are drawn.

---

### 2. OCP: Open-Closed Principle

> **A software artifact should be open for extension but closed for modification.**

The OCP is the fundamental motivation for software architecture. If a simple requirement extension forces massive code changes, the architecture has failed. The goal is to add new behavior by writing new code—not by editing existing code.

**The Thought Experiment: Financial Report Generator**

```
❌ BEFORE — One monolithic process
  Financial Data → Analysis → Web Display + Print Report
  (Adding printer support requires modifying analysis code)

✅ AFTER — Separated responsibilities, proper dependencies
  ┌──────────┐     ┌───────────┐     ┌────────────────┐
  │Controller│────►│Interactor │────►│FinancialData   │
  │          │     │(Business  │     │Gateway <I>     │
  └──────────┘     │ Rules)    │     └───┬────────────┘
                   └──────┬────┘         │implements
                          │              │
              ┌───────────┼──────────┐   │
              │           │          │   │
         ┌────▼─────┐ ┌───▼────┐ ┌──▼───▼──────┐
         │Web        │ │Printer │ │DataMapper   │
         │Presenter  │ │Presenter│ │(Concrete)   │
         └──────────┘ └────────┘ └─────────────┘
```

**The key insight:** All source code dependencies point *toward* the components we want to protect. The **Interactor** (business rules) is the most protected component—nothing it depends on can force it to change. Changes to the Database, Controller, Presenters, or Views have *zero* impact on the Interactor.

**Directional Control:** Interfaces like `FinancialDataGateway` and `FinancialReportPresenter` exist *solely* to invert dependencies. Without them, the Interactor would depend on the Database and the Controller would depend on the Interactor's internals. The complexity in an OCP-compliant design is not accidental—it is deliberate dependency management.

**Information Hiding:** The `FinancialReportRequester` interface protects the Controller from transitive dependencies on `FinancialEntities`. Transitive dependency is a violation of the principle that software entities should not depend on things they don't directly use—which is also the ISP.

> **Architectural OCP summary:** Partition the system into components. Arrange dependencies so that higher-level components (business rules, core policy) are protected from changes in lower-level components (details, frameworks, UI, database). The hierarchy of protection is the hierarchy of *level*.

---

### 3. LSP: Liskov Substitution Principle

> **Subtypes must be substitutable for their base types without altering the correctness of the program.**

Defined by Barbara Liskov in 1988: *If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T.*

**The Square/Rectangle Problem** (class-level LSP violation):

```java
// ❌ Square extends Rectangle — violates LSP
class Rectangle {
    int width, height;
    void setW(int w) { width = w; }
    void setH(int h) { height = h; }
}
class Square extends Rectangle {
    void setW(int w) { width = w; height = w; }  // changes both
    void setH(int h) { width = h; height = h; }
}

// Client code breaks:
Rectangle r = /* could be Square */;
r.setW(5);
r.setH(2);
assert(r.area() == 10);  // ❌ FAILS if r is a Square (area = 4)
```

The only fix is to pollute the client with `if (r instanceof Square)` checks—which proves the types are *not* substitutable.

**LSP at the Architectural Level**

The LSP extends far beyond inheritance. It governs any interface contract—Java interfaces, Ruby duck-types, or REST service endpoints. Architectural LSP violations are far more damaging than class-level ones.

**Taxi Dispatch Example (architectural LSP violation):**

```
System dispatches to: purplecab.com/driver/Bob
PUT /pickupAddress/24 Maple St./pickupTime/153/destination/ORD

✅ All dispatch services conform to the same REST interface:
   purplecab.com  → pickupAddress / pickupTime / destination
   yellowcab.com  → pickupAddress / pickupTime / destination

❌ Acme Taxi abbreviates the field:
   acme.com       → pickupAddress / pickupTime / dest
```

A single non-conforming service forces the architecture to add a special-case dispatch module with configuration-driven URI templates:

```
❌ The hack that no architect should allow:
    if (driver.getDispatchUri().startsWith("acme.com")) ...

✅ The architectural fix — configuration database keyed by dispatch URI:
    URI       | Dispatch Format
    acme.com  | /pickupAddress/%s/pickupTime/%s/dest/%s
    *.*       | /pickupAddress/%s/pickupTime/%s/destination/%s
```

A simple, seemingly minor interface deviation forces a significant and complex architectural mechanism. When LSP violations exist at service boundaries, the architecture becomes **polluted** with conditional logic, configuration databases, and extra indirection—all to compensate for a contract that should have been honored.

> **Architectural LSP:** Every interface, whether in-process or across a network, defines a contract. Violating substitutability at any level adds accidental complexity to the architecture. The principle applies to REST services, microservice contracts, plugin interfaces, and library APIs—not just class inheritance.

---

### 4. ISP: Interface Segregation Principle

> **Don't depend on things you don't need.**

```
❌ BEFORE — Fat interface                     ✅ AFTER — Segregated interfaces
┌────────┐                                   ┌────────┐
│ User1  │──► op1 ──┐                        │ User1  │──► U1Ops {op1}
└────────┘          │                        └────────┘
┌────────┐          │     ┌─────┐            ┌────────┐
│ User2  │──► op2 ──┼───► │ OPS │            │ User2  │──► U2Ops {op2}
└────────┘          │     └─────┘            └────────┘
┌────────┐          │                        ┌────────┐
│ User3  │──► op3 ──┘                        │ User3  │──► U3Ops {op3}
└────────┘                                   └────────┘   OPS implements all three
```

In statically typed languages, a class that imports a fat interface acquires *source code dependencies* on methods it never calls. A change to `op2` in `OPS` forces `User1` to be **recompiled and redeployed**—even though `User1` doesn't use `op2`.

**ISP and Language Type:** Dynamically typed languages (Ruby, Python) infer method signatures at runtime and have no `import`/`include` declarations. This eliminates the recompilation problem, making dynamically typed systems more flexible and less tightly coupled at the source-code level. But this doesn't mean the ISP is irrelevant—the deeper principle transcends language.

**ISP at the Architectural Level**

```
❌ Transitive dependency chain:
   S ──► F (framework) ──► D (database)
   
   If D contains features F doesn't use, and S
   doesn't care about, changes to those features in D
   still force redeployment of F... and therefore S.
   Failures in unused D features can cascade into S.

✅ What ISP demands:
   S should depend on only the slice of F it actually needs.
   F should expose only what S actually requires.
```

The architectural ISP is: **depending on a module that carries baggage you don't need causes unexpected trouble.** A framework bound to a database you don't use, a library that pulls in 40 transitive dependencies for one function, a microservice that responds with 200 fields when you need 3—all are architectural ISP violations that create unnecessary coupling, risk cascading failures, and force redeployment.

At the component level, ISP becomes the **Common Reuse Principle** (CRP): *don't force users of a component to depend on classes they don't need.* If you depend on a component, you should depend on *every class* in it—otherwise you're shipping and revalidating more than necessary.

---

### 5. DIP: Dependency Inversion Principle

> **Depend on abstractions, not concretions.**

The most flexible systems are those in which source code dependencies refer only to abstract interfaces, not concrete implementations. This is the culmination of SRP, OCP, LSP, and ISP: separating by actor, protecting high-level policy, honoring interface contracts, and avoiding unnecessary dependencies—then *inverting the dependency direction* so that concretion depends on abstraction, never the reverse.

**The rules:**

1. **Don't refer to volatile concrete classes.** Refer to abstract interfaces. This constrains object creation and enforces the use of Abstract Factories.
2. **Don't derive from volatile concrete classes.** Inheritance is the strongest, most rigid source code relationship. Use it sparingly and only toward stable abstractions.
3. **Don't override concrete functions.** Overriding inherits the original's source code dependencies. Make the function abstract and create multiple implementations instead.
4. **Never mention the name of anything concrete and volatile.** A restatement of the principle itself.

**The Abstract Factory Pattern (DIP in action):**

```
                    ┌─────────────────────────────┐
                    │        ABSTRACT SIDE         │
                    │                             │
   ┌──────────┐     │  ┌───────────────────┐      │
   │Application│───────►│  Service <I>      │      │
   │          │     │  └───────────────────┘      │
   │          │     │            ▲                │
   │          │     │            │ implements     │
   │          │     │  ┌───────────────────┐      │
   │          │──►  │  │ServiceFactory <I>  │      │
   └──────────┘     │  │  + makeSvc(): Svc  │      │
                    │  └───────────────────┘      │
                    │            ▲                │
                    ├────────────┼────────────────┤
                    │            │                │
                    │    CONCRETE SIDE            │
                    │            │                │
                    │  ┌───────────────────┐      │
                    │  │ServiceFactoryImpl  │      │
                    │  │  + makeSvc()       │──────┼──► ConcreteImpl
                    │  └───────────────────┘      │    (implements Service)
                    │            ▲                │
                    │            │                │
                    │       main() creates        │
                    │       and registers         │
                    └─────────────────────────────┘
                    
   ═══ curved line = ARCHITECTURAL BOUNDARY ═══
   → dependencies cross toward ABSTRACT side only
   → flow of control crosses in opposite direction (Dependency Inversion)
```

The curved line is an **architectural boundary**. All source code dependencies cross it in one direction: toward the abstract side. The flow of control crosses in the *opposite* direction—hence *Dependency Inversion*.

**Concrete Components:** The concrete side will always contain at least one DIP violation (the factory that instantiates concrete objects). DIP violations cannot be eliminated, but they can be **gathered** into a small number of concrete components—often called `main`—and kept isolated from the rest of the system. The abstract side contains all high-level business rules; the concrete side contains implementation details.

> **Architectural DIP:** This is the most visible organizing principle in Clean Architecture. The curved line becomes the architectural boundaries in every diagram that follows. The rule that dependencies cross boundaries pointing *toward more abstract entities* becomes the **Dependency Rule**—the central organizing principle of the entire architecture.

---

## Summary Checklist

- [ ] **SRP:** Is each module responsible to exactly one actor? Are changes for the CFO isolated from changes for the COO?
- [ ] **OCP:** Can new behavior be added by writing new code rather than modifying existing code? Do dependencies point toward the components you want to protect (business rules first)?
- [ ] **LSP:** Are all subtypes and service implementations fully substitutable for their base types or contracts? Would a REST service with a malformed field force architectural workarounds?
- [ ] **ISP:** Do modules depend only on what they actually use? Are you pulling in framework baggage that forces redeployment when unrelated features change?
- [ ] **DIP:** Do high-level policy modules depend on abstract interfaces, not volatile concretions? Are concrete dependencies gathered into `main` and isolated from the rest of the system?
- [ ] **At the component level:** Do SRP → CCP, OCP → dependency hierarchy, ISP → CRP, and DIP → Dependency Rule translate into actual component boundaries?
- [ ] **At the architectural level:** Are dependencies crossing architectural boundaries pointing toward abstractions (the Dependency Rule)? Does the flow of control invert against those dependencies?

---

## Related

- [[Clean Architecture Overview]]
- [[Object-Oriented Programming]]
- [[Programming Paradigms]]
- [[Component Cohesion]]
- [[Component Coupling]]
- [[The Clean Architecture]]
- [[Boundaries]]
- [[Policy and Business Rules]]
- [[Layers and Boundaries]]
