# Clean Architecture

> *Source: Clean Architecture by Robert C. Martin (2018, Prentice Hall)*

---

## Core Principle

> **The goal of software architecture is to minimize the human resources required to build and maintain the required system. Architecture and design are the same thing — a continuum of decisions from high to low — and the rules of software architecture are timeless, independent of language, framework, or era.**

Good architecture makes systems easy to change. The measure of design quality is the effort required to meet customer needs. If that effort stays low over the system's lifetime, the design is good. If it grows with each release, the design is bad.

---

## Book Structure

| Part | Chapters | Topics |
|------|----------|--------|
| I: Introduction | 1–2 | What is design/architecture, the two values of software |
| II: Programming Paradigms | 3–6 | Structured, OOP, Functional Programming |
| III: Design Principles | 7–11 | SOLID principles (SRP, OCP, LSP, ISP, DIP) |
| IV: Component Principles | 12–14 | Components, cohesion, coupling |
| V: Architecture | 15–29 | Architecture definition through implementation |
| VI: Details | 30–34 | Database, web, frameworks, case study, code organization |
| VII: Appendix | A | Architecture archaeology — 45 years of lessons |

---

## Vault Structure

```
Clean Architecture/
├── Foundations/
│   ├── Clean Architecture Overview.md   ← you are here
│   ├── What Is Architecture.md
│   └── Screaming Architecture.md
├── Programming Paradigms/
│   ├── Programming Paradigms.md
│   └── Object-Oriented Programming.md
├── Design Principles/
│   ├── SOLID Design Principles.md
│   └── Policy and Business Rules.md
├── Component Principles/
│   ├── Component Cohesion.md
│   └── Component Coupling.md
├── Architecture - Core/
│   ├── The Clean Architecture.md
│   ├── Boundaries.md
│   ├── Architectural Independence.md
│   └── Layers and Boundaries.md
├── Architecture - Implementation/
│   ├── Presenters and Humble Objects.md
│   └── Main Component and Services.md
├── Architecture - Specialized/
│   ├── Testing and Embedded.md
│   └── Details - Database, Web, Frameworks.md
├── Applied Architecture/
│   ├── Case Study - Video Sales.md
│   └── The Missing Chapter.md
└── Historical Context/
    └── Architecture Archaeology.md
```

---

## Vault Index — All 20 Topic Files

### Foundations

- [[Clean Architecture Overview]] *(this file)* — Chapters 1–2: Design vs architecture, the two values of software, Eisenhower's matrix
- [[What Is Architecture]] — Chapter 15: Four perspectives (development, deployment, operation, maintenance), keeping options open
- [[Screaming Architecture]] — Chapter 21: Architectures should scream use cases, not frameworks

### Programming Paradigms

- [[Programming Paradigms]] — Chapters 3–4, 6: Structured programming, functional programming, paradigm overview
- [[Object-Oriented Programming]] — Chapter 5: Encapsulation, inheritance, polymorphism as the enabler of plugin architecture

### Design Principles

- [[SOLID Design Principles]] — Chapters 7–11: All five SOLID principles from the architectural perspective
- [[Policy and Business Rules]] — Chapters 19–20: Policy levels, entities (Critical Business Rules), use cases, request/response models

### Component Principles

- [[Component Cohesion]] — Chapters 12–13: REP, CCP, CRP, the tension diagram
- [[Component Coupling]] — Chapter 14: ADP, SDP, SAP, the A-I graph, Main Sequence

### Architecture — Core

- [[The Clean Architecture]] — Chapter 22: The concentric-circle diagram, Dependency Rule, crossing boundaries
- [[Boundaries]] — Chapters 17–18: Drawing lines (plugin architecture), boundary anatomy (monolith → services spectrum)
- [[Architectural Independence]] — Chapter 16: Decoupling layers, use cases, mode; independent develop-ability and deployability
- [[Layers and Boundaries]] — Chapter 25: Hunt the Wumpus case study, cost/benefit of boundaries

### Architecture — Implementation

- [[Presenters and Humble Objects]] — Chapters 23–24: Humble Object pattern, presenters/views, partial boundaries, facades
- [[Main Component and Services]] — Chapters 26–27: Main as the ultimate detail, services and the Kitty problem

### Architecture — Specialized

- [[Testing and Embedded]] — Chapters 28–29: Tests as system components, clean embedded architecture, OSAL, HAL
- [[Details - Database, Web, Frameworks]] — Chapters 30–32: All three are implementation details in the outermost circle

### Applied Architecture

- [[Case Study - Video Sales]] — Chapter 33: Full architecture walkthrough from product to dependency management
- [[The Missing Chapter]] — Chapter 34: Package by layer, feature, ports & adapters, component; organization vs encapsulation

### Historical Context

- [[Architecture Archaeology]] — Appendix A: Uncle Bob's 45-year journey through 13+ projects and their architectural lessons

---

## How to Use This Vault

1. **Start with this overview** and [[What Is Architecture]] for the high-level philosophy
2. **Read [[The Clean Architecture]]** — it's the central chapter; everything else orbits it
3. **Work through SOLID → Components → Boundaries** in that order — they build on each other
4. **Use [[Screaming Architecture]] and [[Details - Database, Web, Frameworks]]** as daily reminders of what matters
5. **Reference [[Boundaries]] and [[Architectural Independence]]** when designing new systems
6. **Check [[The Missing Chapter]]** when organizing code into packages and components

---

## Key Takeaways

- [ ] Architecture and design are the same — a continuum, not a hierarchy
- [ ] Behavior is urgent; architecture is important. Prioritize the important over the urgent.
- [ ] The only way to go fast is to go well. Clean code isn't slower — messy code is.
- [ ] Dependencies must point inward, toward higher-level policy (the Dependency Rule)
- [ ] Frameworks, databases, and web servers are details — plug them in later
- [ ] Boundaries exist on a spectrum: monolith → deployment components → local processes → services
- [ ] A good architect maximizes the number of decisions NOT made
- [ ] Tests are part of the system, not external — they follow the same Dependency Rule

---

## Related

- [[Clean Code Overview]] — The companion vault: function design, naming, comments, error handling, and more
