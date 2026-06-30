---
tags:
- software-engineering
- swebok
---

# Software Design

> **Purpose:** This knowledge area covers the discipline, processes, and work products of software design—the transformation of requirements into implementable specifications. It spans from foundational principles and design thinking through the three stages of design (architectural, high-level, and detailed), to strategies, methods, recording approaches, and quality evaluation.

## Knowledge Areas

### 1. Software Design Fundamentals
- **Design Thinking** — A five-step problem-solving process: crystallize purpose, formulate a concept, devise a mechanism, introduce a notation, and apply it. Design is fundamentally about creating the vocabulary to express both problem and solution.
- **Context of Software Design** — How design fits into the software development life cycle: its relationships with requirements (problem definition), architecture (constraints), construction (implementation guidance), and testing (validation foundation).
- **Key Issues in Software Design** — The fundamental concerns all designs must address: quality (performance, security, reliability, usability, maintainability), component refinement/organization, and crosscutting *aspects*—properties that affect systemic behavior rather than fitting into functional decomposition.
- **Software Design Principles** — Foundational truths guiding design decisions: abstraction, separation of concerns, modularization, encapsulation/information hiding, separation of interface and implementation, coupling (aim for loose), cohesion (aim for high), uniformity, completeness (sufficiency), verifiability, and ethically aligned design.

### 2. Software Design Processes
- **High-Level Design** — Outward-facing stage defining top-level structure, major components, external events/messages, data formats/protocols, timing relationships, end-to-end transaction tracing, and data persistence strategies. Operates within the envelope established by software architecture.
- **Detailed Design** — Inward-facing stage specifying each module's internal structure: algorithms, data structures, component modes/states, scope/visibility, data organization, user interfaces, and interactions among modules. Must be sufficient for programmers to code without reading source of peer components.

### 3. Software Design Qualities
- **Concurrency** — Refining software into concurrent units (processes, tasks, threads) with attention to efficiency, atomicity, synchronization, and scheduling.
- **Control and Event Handling** — Organizing control flow and handling reactive/temporal events through synchronization, implicit invocation, and callbacks.
- **Data Persistence** — Storage and management of data throughout the system.
- **Distribution of Components** — Distributing components across hardware/network while meeting performance, reliability, scalability, and availability.
- **Errors, Exception Handling, and Fault Tolerance** — Preventing, mitigating, and processing errors and exceptional conditions.
- **Integration and Interoperability** — Enabling heterogeneous systems or components (different frameworks/libraries/protocols) to interwork through data exchange or service access.
- **Assurance, Security, and Safety** — Ensuring correct behavior in critical situations, preventing unauthorized access/disclosure, and managing safety-critical behavior.
- **Variability** — Accommodating permissible variations for product lines, market segments, and context-aware software (captured via feature models).

### 4. Recording Software Designs
- **Model-Based Design (MBD)** — Evolution from document-based to model-based artifacts; tooling enables simulation, analysis, rapid prototyping, and continuous integration.
- **Structural Design Descriptions** — Notations for static structure: class/object diagrams, component diagrams, CRC cards, deployment diagrams, ERDs, IDLs, and structure charts.
- **Behavioral Design Descriptions** — Notations for dynamic behavior: activity diagrams, interaction diagrams (communication and sequence), DFDs, decision tables/diagrams, flowcharts, state diagrams/statecharts, formal specification languages, and pseudocode/PDLs.
- **Design Patterns and Styles** — Reusable solutions in context: creational (builder, factory, prototype, singleton), structural (adapter, bridge, composite, decorator, façade, flyweight, proxy), and behavioral (command, interpreter, iterator, mediator, memento, observer, publish-subscribe, state, strategy, template, visitor).
- **Specialized and Domain-Specific Languages (DSLs)** — Codifying domain concepts into computer languages with grammar-driven tooling; blurs lines among modeling, design, and programming languages.
- **Design Rationale** — Explicit documentation of *why* decisions were made: assumptions, alternatives considered, trade-offs, and rejected options. Critical for long-term maintainability and distributed/FOSS teams.

### 5. Software Design Strategies and Methods
- **General Strategies** — Divide-and-conquer, stepwise refinement, top-down vs. bottom-up, heuristics/patterns, iterative and incremental approaches.
- **Function-Oriented (Structured) Design** — Top-down functional decomposition following structured analysis, producing DFDs and process descriptions.
- **Data-Centered Design** — Starts from data structures; program units transform input structures to output structures.
- **Object-Oriented Design (OOD)** — Objects (nouns), methods (verbs), attributes (adjectives); inheritance and polymorphism; responsibility-driven design; SOLID principles (Single-responsibility, Open–closed, Liskov substitution, Interface segregation, Dependency inversion).
- **User-Centered Design** — Multidisciplinary approach emphasizing deep understanding of users, task context, prototyping, and evaluation against user requirements.
- **Component-Based Design (CBD)** — Decomposing into standalone components with well-defined interfaces conforming to a component model; emphasizes reuse and independent deployability.
- **Event-Driven Design** — Indirect invocation via events; publish/subscribe messaging with decoupled producers/consumers; simple, stream, and complex event processing.
- **Aspect-Oriented Design (AOD)** — Using aspects to implement crosscutting concerns and extensions; common in application frameworks and configurable libraries.
- **Constraint-Based Design** — Limiting the design space with constraints to exclude infeasible alternatives; used in UI design, gaming, and constraint satisfaction problems.
- **Domain-Driven Design** — Shared domain-specific language between analysts and stakeholders to express objects, roles, events, and activities in design descriptions.

### 6. Software Design Quality Analysis and Evaluation
- **Design Reviews and Audits** — Comprehensive examinations of status, coverage, open issues, and potential problems; can be conducted by design team, independent third party, or stakeholders.
- **Quality Attributes** — Runtime-observable qualities (performance, security, availability, usability) and non-runtime qualities (modifiability, portability, reusability, testability, conceptual integrity).
- **Quality Analysis and Evaluation Techniques** — Software design reviews (informal, rigorous, scenario-based, requirements tracing); static analysis (fault-tree analysis, automated cross-checking, formal mathematical models); simulation and prototyping.
- **Measures and Metrics** — Function-based measures (from structure charts) and object-oriented measures (from class diagrams: coupling, cohesion, complexity).
- **Verification, Validation, and Certification** — Verification confirms design satisfies stated requirements; validation establishes stakeholder expectations are met; certification provides third-party attestation of conformity.

## Essential Concepts

- **Design as problem-solving:** Software design transforms a problem statement into a solution statement through iterative vocabulary creation—a fundamentally linguistic process.
- **Three stages of design:** Architectural (system-wide fundamentals), high-level (outward-facing component identification and interfaces), and detailed (inward-facing module internals).
- **Separation of concerns (SoC):** Dijkstra's principle—the only available technique for effective ordering of one's thoughts; isolate concerns to focus on each in isolation.
- **Abstraction:** Focusing on essential information relevant to a purpose while ignoring the rest; the foundation of managing complexity.
- **Encapsulation / Information hiding:** Making nonessential details less accessible; Parnas's insight that modules should hide design decisions likely to change.
- **Coupling and cohesion:** Low coupling (loose interdependence between modules) and high cohesion (strong relatedness within a module) are universal design goals.
- **Separation of interface and implementation:** Define a component by its public contract, isolating clients from internal change. This enables independent construction and testing.
- **SOLID principles:** Single-responsibility, Open–closed, Liskov substitution, Interface segregation, Dependency inversion—the core principles of object-oriented class design.
- **Crosscutting concerns (aspects):** Properties affecting systemic behavior (performance, security, logging) that don't fit cleanly into functional decomposition; addressed via AOD or framework configuration.
- **Design patterns:** Proven reusable solutions to recurring problems; classified as creational, structural, or behavioral; serve as a shared solution vocabulary among designers.
- **Model-Based Design (MBD):** Shift from ambiguous document-based artifacts to tool-enabled models that support simulation, analysis, and continuous integration.
- **Design rationale:** Explicitly recording *why* decisions were made (assumptions, alternatives, trade-offs, rejected options) is essential for long-term maintainability, especially in distributed teams.
- **Variability:** The ability to create system variants for different markets or contexts; captured through feature models; fundamental to software product lines.
- **Verification vs. validation:** Verification confirms the design satisfies stated requirements; validation confirms the resulting system meets stakeholder expectations.
- **Unified Modeling Language (UML):** The widely used family of notations covering both structural and behavioral design concerns across all design stages.

## Tools & Techniques Mentioned

- **Notations:** UML (class/object diagrams, component diagrams, deployment diagrams, activity diagrams, interaction/sequence/communication diagrams, state diagrams/statecharts), ERDs, DFDs, structure charts, CRC cards, decision tables/diagrams, flowcharts, IDLs, formal specification languages, pseudocode/PDLs
- **Methods/Approaches:** Function-oriented (structured) design, data-centered design, object-oriented design, user-centered design, component-based design (CBD), event-driven design, aspect-oriented design (AOD), constraint-based design, domain-driven design (DDD), model-based design (MBD), model-driven development (MDD), service-oriented methods
- **Strategies:** Divide-and-conquer, stepwise refinement, top-down vs. bottom-up, iterative/incremental approaches, publish/subscribe messaging, simple/stream/complex event processing
- **Quality Techniques:** Design reviews (informal, rigorous, active, scenario-based), static analysis (fault-tree analysis, automated cross-checking, formal mathematical models), simulation and prototyping, requirements tracing
- **Metrics:** Function-based measures (structure chart analysis), object-oriented measures (class diagram coupling/cohesion/complexity), lines-of-code metrics
- **Patterns:** GoF design patterns (23 patterns across creational, structural, behavioral categories), architectural styles as patterns "in the large," SOLID principles, SOFA principles

## Related SWEBOK Chapters

- [[02_Software_Architecture]]: Architecture constrains design by capturing system fundamentals—major components, interconnections, APIs, styles, patterns, and architectural principles.
- [[04_Software_Construction]]: Construction executes design; design must provide sufficient detail (algorithms, data structures, interfaces) for programmers to code.
- [[05_Software_Testing]]: Testing validates design; design provides the foundation for overall testing strategy and test cases.
- [[11_Software_Engineering_Models_and_Methods]]: Design methods (OOD, structured, DDD, etc.) overlap significantly with SE models and methods; formal methods enable rigorous design analysis.
- [[16_Computing_Foundations]]: Abstraction, problem-solving techniques, and design theory fundamentals.
- [[09_Software_Engineering_Management]]: Design reviews, audits, and quality measurement.
- [[12_Software_Quality]]: Quality attributes, verification, validation, and certification.
