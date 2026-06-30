---
tags:
- software-engineering
- swebok
---

# Software Architecture

> **Purpose:** This knowledge area covers the fundamental concepts, representation, process, and evaluation of software architectures. It treats architecture as a distinct discipline from design—focusing on the fundamental properties of a system in its environment, the structures needed to reason about it, and the decisions that shape it throughout the lifecycle.

## Knowledge Areas

- **Software Architecture Fundamentals (1.1–1.3)**: The three senses of "architecture"—as a discipline, as a process, and as an outcome (architecture descriptions). Covers stakeholders and concerns (e.g., performance, security, maintainability) and the uses of architecture for shared understanding, analysis, and reverse engineering.

- **Architecture Views and Viewpoints (2.1)**: Architecture views represent one or more aspects of an architecture addressing specific stakeholder concerns; viewpoints define the conventions, notations, and models for constructing views. Common viewpoints include logical, process, physical, development, scenarios/use cases, information, and deployment.

- **Architecture Patterns, Styles, and Reference Architectures (2.2)**: Catalogued reusable solutions at varying scales—from system-wide architectural styles (layered, client-server, microservices, MVC, pipes-and-filters) to finer-grained architectural patterns. Reference architectures capture domain-wide commonalities to guide individual system architectures.

- **Architecture Description Languages and Frameworks (2.3)**: Domain-specific languages (ADLs) for expressing architectures, ranging from style-specific (MetaH) to enterprise-wide (ArchiMate). UML is widely used as an ADL. Architecture frameworks (e.g., AUTOSAR, UAF, ISO RM-ODP) codify conventions, principles, and practices within a domain.

- **Architecture as Significant Decisions (2.4)**: Architecture is a network of decisions profoundly affecting downstream development. Includes rationale capture (why decisions were made, alternatives considered), architectural technical debt (costs deferred due to expedient decisions), and decision analysis as a basis for architecture evaluation.

- **Architectural Design Process (3.1–3.4)**: A general model of iterative architectural design comprising analysis (identifying architecturally significant requirements), synthesis (developing candidate solutions), and evaluation. Covers architecture in different contexts—traditional lifecycle, agile, product lines, and enterprise/system-of-systems—and the broader scope of software architecting beyond a single design stage.

- **Architecture Evaluation (4.1–4.4)**: Multi-faceted assessment of whether an architecture is "good"—robust, fit for purpose, cost-effective, and understandable. Covers structured evaluation methods (ATAM, SAAM, QAW, SARA), active design reviews, and quantitative architecture metrics (coupling, cohesion, cyclomatic complexity, and DevOps metrics like deployment frequency).

## Essential Concepts

- **Three senses of "architecture"**: Discipline (body of knowledge and practice), process (architecting activities), and outcome (architecture description of a system).
- **Architecture definition (ISO/IEC/IEEE 42010)**: The fundamental concepts or properties of a system in its environment, embodied in its elements, relationships, and design/evolution principles.
- **Architecturally Significant Requirements (ASRs)**: Requirements that influence the architecture—the design problems the architecture must solve, identified during architecture analysis.
- **Separation of concerns**: The foundational principle (Dijkstra) that different aspects of a system should be studied in isolation; architecture views enable this by focusing on distinct stakeholder concerns.
- **Stakeholders and concerns**: Each stakeholder (customer, user, developer, safety engineer) has distinct concerns; architecture must address the interplay of functional, non-functional, and constraint concerns that evolve over the system lifecycle.
- **Views and Viewpoints**: A view is a representation of the architecture addressing one or more concerns; a viewpoint defines the conventions (notations, models, practices) for constructing such views. Key distinction between synthetic (views integrated via correspondence rules) and projective (views derived from a single model) approaches.
- **4+1 View Model (Kruchten)**: A seminal architecture description approach using logical, development, process, and physical views, integrated through scenarios/use cases.
- **Architectural styles vs. patterns**: A style expresses a system's large-scale organization (e.g., layered, client-server, microservices, REST); a pattern is a common solution to a recurring problem at any scale. Both serve as idioms in viewpoint languages.
- **Reference Architecture**: A standardized architecture constraining or guiding architectures for individual systems, product lines, or families within a domain (e.g., automotive, healthcare, cloud).
- **Architectural technical debt**: The future cost incurred when expedient architectural decisions compromise maintainability, evolvability, or other qualities—debt that must be paid later, often by different people.
- **Architecture rationale**: The documented reasons behind each nontrivial architectural decision, including assumptions, alternatives considered, trade-offs, and rejected options—essential for future understanding and avoiding repeated mistakes.
- **Architectural design iteration (Analysis → Synthesis → Evaluation)**: The core cycle: analyze ASRs and context, synthesize candidate solutions with trade-offs, evaluate whether solutions satisfy ASRs—all performed concurrently at multiple granularities.
- **Conway's Law**: Organizations design systems that mirror their communication structures; architecture both shapes and is shaped by organizational structure.
- **Architecture review methods**: Structured evaluation includes ATAM (trade-off analysis via quality-attribute utility trees and scenarios), SAAM, active design reviews (reviewers perform specific activities rather than following checklists), and QAW (quality attribute workshops).
- **Viewtypes (Clements et al.)**: A three-way categorization—module, component-and-connector, and allocation—providing a high-level taxonomy for organizing viewpoints.

## Tools & Techniques Mentioned

- **ATAM** (Architecture Tradeoff Analysis Method) — methodical quality-attribute-based evaluation using utility trees and scenarios
- **SAAM** (Software Architecture Analysis Method) — scenario-based architecture evaluation
- **QAW** (Quality Attribute Workshops) — stakeholder workshops to elicit architecture-driving quality requirements
- **SARA Report** — general framework for architecture review and assessment
- **Active Design Reviews** (Parnas & Weiss) — reviewers perform specific activities rather than passive checklist review
- **4+1 View Model** (Kruchten) — five-view architecture description integrating logical, development, process, physical, and scenario views
- **UML** (Unified Modeling Language) — widely used as a general-purpose ADL
- **ArchiMate** — enterprise architecture modeling language
- **AUTOSAR** — automotive domain architecture framework
- **UAF** (Unified Architecture Framework) — OMG framework for enterprise/system-of-systems architecture
- **ISO/IEC/IEEE 42010:2011** — international standard for architecture description
- **ISO RM-ODP** — Reference Model for Open Distributed Processing
- **Architecture metrics** — component dependency, cyclomatic complexity, coupling/cohesion, nesting depth; DevOps metrics (lead time, deployment frequency, mean time to restore, change failure rate)

## Related SWEBOK Chapters

- [[01_Software_Requirements]]: Architecture shaped by requirements; ASRs bridge requirements and architectural decisions
- [[03_Software_Design]]: Design detail vs. architecture; design patterns and detailed decomposition follow architectural decisions
- [[04_Software_Construction]]: Construction follows architecture; architecture descriptions guide implementation
- [[11_Software_Engineering_Models_and_Methods]]: Architecture description methods, use cases for evaluation, modeling notations
- [[12_Software_Quality]]: Quality attributes ("ilities") are primary concerns driving architecture evaluation and trade-off analysis
