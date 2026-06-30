---
tags:
- software-engineering
- swebok
---

# Software Requirements

> **Purpose:** This knowledge area covers what software requirements *are* (an expression of needs and constraints on a product or project) and the activities needed to develop and maintain them over the software's service life. Getting requirements wrong triggers exponentially cascading rework—each requirement error fans out into many design, code, and test errors. The two primary real-world problems are **incompleteness** (stakeholder needs that never reach engineers) and **ambiguity** (requirements open to multiple interpretations).

## Knowledge Areas

- **Requirements Fundamentals**: Defines what a software requirement is, categorizes them (functional vs. nonfunctional; product vs. project), and explains why categorization matters—different categories need different elicitation, analysis, specification, and validation approaches. Introduces the Perfect Technology Filter to separate functional from nonfunctional requirements.

- **Requirements Elicitation**: The goal is surfacing candidate requirements from stakeholders (clients, customers, users, SMEs, regulators, developers) and non-person sources (prior systems, documentation, competitive benchmarking, observation). Covers techniques like interviews, JAD/JRP workshops, focus groups, prototyping, user story mapping, design thinking, and apprenticing. Emphasizes that elicitation is active work—stakeholders leave things unsaid.

- **Requirements Analysis**: Refines elicited statements into true requirements. Each requirement should be unambiguous, testable, binding, atomic, and acceptable to all stakeholders. Introduces the 5-Whys technique to uncover the real problem behind solution-shaped requirements. Covers the economics of quality-of-service constraints (perfection point, fail point, most cost-effective performance level), formal analysis for high-integrity systems, and conflict resolution via negotiation or product family development (separating invariant from variant requirements).

- **Requirements Specification**: Recording requirements so they can be remembered and communicated. The most contentious topic—questions of whether to write requirements down, what form they should take, and whether to maintain them over time. Specification techniques span a spectrum: unstructured natural language, structured natural language (actor-action format, use cases, user stories), acceptance criteria-based (ATDD/BDD—directly addressing ambiguity by using precise test-case language), and model-based (UML/SysML structural and behavioral models at varying formality levels from Agile sketches to formal Z/VDM). Also covers additional attributes like rationale, source, priority, stability.

- **Requirements Validation**: Gaining confidence that requirements represent true stakeholder needs. Three methods: requirements reviews (multi-perspective—clients, spec experts, downstream engineers), simulation and execution (hand-interpreting formal specs against demo scenarios), and prototyping (exposing assumptions, getting concrete feedback).

- **Requirements Management**: Maintaining the agreement on requirements over time. Includes requirements scrubbing (finding the smallest set that meets needs), change control (explicit process in plan-based life cycles; implicit via backlog prioritization in Agile), and scope matching (ensuring requirements scope does not exceed cost/schedule/staffing constraints—quantitative where possible, using functional size units).

- **Practical Considerations**: The requirements process is inherently iterative—breadth and depth expand in alternating cycles. Prioritization uses factors like value, dissatisfaction (Kano model), cost, and risk, optionally combined into an objective function like `Priority = Value × (1 − Risk) / Cost`. Requirements tracing supports consistency checking and impact analysis. Stability assessment helps design for change-tolerant architectures. Functional size measurement (FSM) and story points quantify requirements volume for estimation.

- **Software Requirements Tools**: Three categories—requirements management tools (storing attributes, tracing, change control), requirements modeling tools (visual creation, static analysis, simulation; formal tools include theorem provers and model checkers), and functional test case generation tools (mechanically deriving test cases from formal or BDD specifications).

## Essential Concepts

- **Two core problems = Incompleteness + Ambiguity.** Every requirements technique addresses one or both. Poor elicitation → incompleteness. Natural language → ambiguity. ATDD/BDD directly solves ambiguity; combining them with test coverage criteria reduces incompleteness.

- **Functional vs. Nonfunctional separation.** Use the Perfect Technology Filter: if a requirement would still exist on an infinitely fast, zero-cost, never-failing computer, it's functional. Everything else is a technology constraint (named tech mandates) or quality-of-service constraint (performance levels). Stakeholders own functional; engineers own nonfunctional. Don't mix them in review.

- **Requirements are not a phase—they're a process.** They begin at project start and continue refining throughout the service life. The life cycle (waterfall, iterative, Agile) determines *when* work happens, not *what* or *how*. Downstream maintainers should not be able to infer the life cycle from the requirements artifacts alone.

- **5-Whys drives to the real problem.** When a stakeholder gives a solution-shaped requirement ("the system shall export to Excel"), ask why until the answer is "if this isn't done, the problem is unsolved." Usually 2–3 cycles suffice.

- **Quality-of-service has an economic curve.** Every QoS constraint (response time, throughput, reliability) has a perfection point (beyond which value stops increasing) and a fail point (below which value is zero). The stated requirement point is often arbitrary. Find the most cost-effective level—where value minus cost is maximized.

- **ATDD/BDD is requirements, not just testing.** A test case says "we expect the software to produce Y." Change "expect" to "shall" and it becomes a precise, unambiguous requirement. Acceptance criteria-based specification is the strongest defense against ambiguity.

- **Model formality is a spectrum, not binary.** Agile sketches → semiformal UML/SysML → formal Z/VDM. More formality = less ambiguity, more static analysis, easier test case generation. Wing's compromise: formal underpinnings with readable surface syntax.

- **Specification choice depends on context, not dogma.** Whether to write requirements, and in what form, depends on: domain familiarity, precedent, risk severity, staff turnover, team distribution, outsourcing, contractual requirements, and testing expectations. No single right answer.

- **Requirements scrubbing before validation.** Eliminate out-of-scope, low-ROI, and low-importance requirements *before* stakeholders review them. In Agile, this happens implicitly in sprint planning. In waterfall, do it just before the validation review.

- **Prioritize by dissatisfaction, not just satisfaction (Kano model).** Users may be *happier* with a spam filter, but far more *unhappy* if attachments don't work. Prioritize what causes the most pain when absent—not just what brings the most joy when present.

- **Scope matching must be quantitative.** When requirements exceed constraints, cut lowest-priority items, increase capacity, or both. Express tradeoffs in functional size units, not gut feel.

- **Requirements tracing enables impact analysis.** Trace forward to design and code; trace backward to source documents. When a requirement changes, the footprint of affected work is immediately visible. Manual tracing is impractical without tool support.

- **Derived requirements are real.** An architect's decision from the project-wide perspective becomes a requirement from a sub-team's perspective. The aerospace industry formalized this concept—requirements depend on viewpoint.

- **Stakeholder analysis prevents bias.** Identify stakeholder classes (groups with similar perspectives), not just individuals. This prevents requirements from skewing toward the loudest or best-represented stakeholders.

- **Change control = maintaining the agreement.** In plan-based life cycles: explicit request → impact analysis → decision → notification → tracking. In Agile: items go on the backlog; they only become "accepted" when prioritized into a sprint.

## Tools & Techniques Mentioned

| Category | Items |
|---|---|
| **Elicitation** | Interviews, JAD/JRP workshops, brainstorming, protocol analysis, focus groups, questionnaires/market surveys, exploratory prototyping (low/high-fidelity), user story mapping, observation, apprenticing, task analysis, design thinking, QFD House of Quality, competitive benchmarking, decomposition (epics → features → stories) |
| **Analysis** | 5-Whys, Perfect Technology Filter, economic value/cost curves, Kano model, product family development (invariant/variant separation), formal analysis (theorem proving, model checking) |
| **Specification** | Unstructured natural language, actor-action format, use case templates, user stories ("As a… I want… so that…"), decision tables, ATDD (acceptance test-driven development), BDD (Given/When/Then scenarios), UML structural models (class/ER diagrams), UML behavioral models (use case diagrams, interaction diagrams, state models, activity diagrams), SysML, data-flow modeling, Z, VDM, SDL, Planguage (Gilb) |
| **Validation** | Multi-perspective requirements reviews (checklists/definition of done), specification simulation/execution, prototyping |
| **Management** | Requirements scrubbing, change control process, scope matching (functional size units), requirements tracing, prioritization schemes (MoSCoW, numeric scales, priority-sorted lists, value-risk-cost formulas) |
| **Measurement** | Functional Size Measurement (FSM), story points, quality indicators derived from desirable requirements properties |
| **Tools** | Requirements management tools (attributes, tracing, document generation, change control), requirements modeling tools (visual modeling, static analysis, simulation, theorem provers, model checkers), functional test case generation tools |
| **Standards** | ISO/IEC/IEEE 29148 (Requirements Engineering), ISO/IEC 25010 (SQuaRE quality models), ISO/IEC/IEEE 24765 (Vocabulary) |

## Related SWEBOK Chapters

- [[02_Software_Architecture]]: Architecture is shaped by requirements; nonfunctional requirements especially drive architectural decisions
- [[03_Software_Design]]: Design realizes requirements; each requirement fans out into many design decisions
- [[04_Software_Construction]]: Construction translates requirements-based designs into code
- [[05_Software_Testing]]: Testing validates against requirements; ATDD/BDD blur the boundary between specification and testing
- [[08_Software_Configuration_Management]]: Requirements documentation is subject to CM; change control is a shared concern
- [[09_Software_Engineering_Management]]: Requirements drive project scope, estimation, and trade-off decisions
- [[11_Software_Engineering_Models_and_Methods]]: Model-based requirements specification (UML, SysML, formal methods)
- [[12_Software_Quality]]: Requirements quality (well-formedness) and reviews/audits
- [[15_Software_Engineering_Economics]]: Economic analysis of quality-of-service constraints and cost-value trade-offs
- [[13_Software_Security]]: Security requirements as a critical, often-overlooked nonfunctional category
