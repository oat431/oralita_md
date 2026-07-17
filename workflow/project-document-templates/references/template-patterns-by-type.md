# Template Patterns by Document Type

Concrete section patterns learned from creating 29 templates across BABOK, PMBOK, SWEBOK, SEBOK, CyBOK, DMBOK, UX/UI.

## Strategy/Analysis Documents (BABOK)

Used for: Business Case, Current State, Future State, Change Strategy, Gap Analysis, Potential Value, Design Options, Solution Recommendation

### Standard Sections
1. Executive Summary (1-page decision view)
2. Context / Background
3. Analysis (detailed findings with tables)
4. Options / Alternatives (if applicable)
5. Comparison / Evaluation (weighted scoring matrix)
6. Recommendation
7. Risk & Mitigation
8. Appendices

### Key Patterns
- **Weighted Scoring Matrix:** Criterion | Weight | Option A Score | Option B Score | Weighted Total
- **Gap Analysis:** Gap ID | Current State | Future State | Gap | Severity | Resolution Approach
- **Before/After Table:** Dimension | Current | Future | Improvement %
- **Effort/Impact Matrix:** Use Mermaid `quadrantChart` — never ASCII grid

## Approach/Plan Documents (BABOK, PMBOK)

Used for: BA Approach, Governance Approach, Info Management Approach, Benefits Management Plan, Stakeholder Engagement

### Standard Sections
1. Executive Summary
2. Methodology / Approach
3. Scope & Boundaries
4. Roles & Responsibilities (RACI matrix)
5. Tools & Techniques
6. Timeline / Schedule (Mermaid gantt)
7. Quality Assurance
8. Risks & Assumptions

### Key Patterns
- **RACI Matrix:** Activity | Role 1 | Role 2 | Role 3 (use **A** for bold Accountable)
- **Governance Model:** Use Mermaid `flowchart TD` with subgraphs for Strategic/Tactical/Operational
- **Communication Matrix:** Stakeholder | What | When | Channel | Format | Owner
- **ADKAR Assessment:** Awareness → Desire → Knowledge → Ability → Reinforcement (Mermaid flowchart)

## Assessment Documents (BABOK, SEBOK)

Used for: Enterprise Readiness Assessment, Risk Analysis Results, BA Performance Assessment

### Standard Sections
1. Executive Summary (dashboard with scores)
2. Assessment Framework (dimensions, scoring scale)
3. Detailed Assessment (per dimension)
4. Score Summary (weighted matrix)
5. Visualization (radar chart, heat map)
6. Improvement Actions
7. Go/No-Go Criteria (if applicable)

### Key Patterns
- **Readiness Radar:** Use Mermaid `radar-beta` for multi-dimensional scores
- **Heat Map:** Emoji table (never ASCII)
- **Weighted Score:** Factor | Weight | Score | Weighted Score — sum at bottom
- **Status Thresholds:** 🟢 Ready (4.0+) / 🟡 Conditional (3.0-3.9) / 🟠 At Risk (2.0-2.9) / 🔴 Not Ready (<2.0)

## Requirements Documents (BABOK, SWEBOK, SEBOK)

Used for: Business Requirements, SRS, SyRS, Stakeholder Needs

### Standard Sections
1. Executive Summary
2. System/Business Context (Mermaid context diagram)
3. Functional Requirements (register table)
4. Non-Functional Requirements (categorized by type)
5. Business Rules
6. Interface Requirements
7. Constraints & Assumptions
8. Traceability Matrix

### Key Patterns
- **Requirements Register:** Req ID | Description | Category | Priority | Source | Status
- **NFR Categories:** Performance, Availability, Security, Usability, Scalability
- **Business Rules:** Rule ID | Rule | Category | Exception | Source
- **Traceability:** Requirement | Source Need | Objective | Test Case | Status
- **Context Diagram:** Use Mermaid `flowchart TB` with subgraphs for External Entities, System Boundary, External Systems

## Elicitation Documents (BABOK)

Used for: Elicitation Activity Plan, Elicitation Results (Unconfirmed/Confirmed), Stakeholder Engagement Approach

### Standard Sections
1. Activity Summary (metadata)
2. Stakeholder Identification
3. Technique Selection (matrix)
4. Schedule (Mermaid gantt)
5. Activity Detail Cards (repeatable template)
6. Findings / Results
7. Open Questions
8. Confirmation Plan (for unconfirmed results)

### Key Patterns
- **Activity Card:** Activity ID | Type | Objective | Date | Participants | Agenda | Expected Output
- **Technique Matrix:** Technique | Best For | Participants | Output | Time per Session
- **Stakeholder Register:** ID | Name | Role | Influence | Interest | Attitude | Engagement Level
- **Power/Interest Grid:** Use Mermaid `quadrantChart` with 4 quadrants labeled

## Concept/Definition Documents (SEBOK)

Used for: Mission Analysis, ConOps, Feasibility Study, Market Analysis

### Standard Sections
1. Executive Summary
2. Mission/Need Statement
3. Operational Context (Mermaid architecture)
4. Operational Scenarios (Mermaid sequence diagrams)
5. Capability Gaps
6. Measures of Effectiveness
7. Constraints & Assumptions

### Key Patterns
- **Operational Scenario:** Use Mermaid `sequenceDiagram` with actors, alt/else blocks
- **Capability Gap:** Gap ID | Current | Required | Severity | Approach
- **MOE Table:** MOE ID | Measure | Unit | Threshold | Objective | Source
- **Feasibility Verdicts:** Per-dimension verdict table with overall recommendation

## Cross-Cutting Document Types

### Stakeholder Register (appears in multiple sections)
Standard columns: ID | Name | Title | Department | Role | Contact | Influence | Interest | Attitude | Engagement Level
Always include: Power/Interest Grid (Mermaid quadrantChart), Change Log

### Risk Analysis (appears in multiple contexts)
Standard columns: ID | Risk | Probability | Impact | Level | Response | Owner
Always include: Heat Map (emoji table), Response Strategy detail cards

### Decision Records
Standard fields: Decision | Options Considered | Selected Option | Rationale | Conditions | Approvals
