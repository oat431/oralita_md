# Architecture Document Patterns

Patterns discovered while creating 20 architecture templates (Section 9: Systems Architecture & Design).

## Diagram Types Used

| Document | Diagram Type | Mermaid Keyword |
|----------|-------------|----------------|
| Functional Architecture | Decomposition tree | `flowchart TD` |
| Logical Architecture | Layered component diagram | `flowchart TB` with subgraphs |
| Physical Architecture | Deployment diagram | `flowchart TB` with nested subgraphs |
| System Architecture | Multiple views | `sequenceDiagram`, `flowchart` |
| ICD | Interface register | Tables (not diagrams) |
| Trade Study | Weighted scoring matrix | Tables |
| SAD | Architecture overview + sequence | `flowchart TB` + `sequenceDiagram` |
| ADR | No diagrams needed | Structured text |
| Architecture Views (4+1) | 5 different views | Mixed — `flowchart`, `sequenceDiagram` |
| ASR Catalog | Traceability matrix | Tables |
| ATAM Evaluation | Utility tree | `flowchart TD` |
| C&C Views | Runtime component diagrams | `flowchart TB` with subgraphs |
| Module Views | Layered package diagram | `flowchart TB` with subgraphs |
| MBSE Models | 8 SysML diagram types | Mixed — `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram` |
| BOM | Dependency graph | `flowchart TD` |

## Mermaid Patterns for Architecture

### Layered Architecture (most common)

```mermaid
flowchart TB
    subgraph Presentation["Presentation Layer"]
        PORTAL[Portal]
        ADMIN[Admin]
    end
    subgraph Services["Service Layer"]
        SVC1[Service 1]
        SVC2[Service 2]
    end
    subgraph Data["Data Layer"]
        DB[(Database)]
    end
    Presentation --> Services
    Services --> Data
    style Presentation fill:#4CAF50,color:#fff
    style Services fill:#2196F3,color:#fff
    style Data fill:#9C27B0,color:#fff
```

### Deployment Architecture

```mermaid
flowchart TB
    subgraph Cloud["Cloud Platform"]
        subgraph Public["Public Subnet"]
            LB[Load Balancer]
        end
        subgraph App["Application Subnet"]
            CONTAINERS[Containers]
        end
        subgraph Data_Zone["Data Subnet"]
            DB[(Database)]
        end
    end
    LB --> CONTAINERS
    CONTAINERS --> DB
```

### C4-Style Context Diagram

```mermaid
flowchart TB
    subgraph Users["Users"]
        CUST([Customer])
        OPS([Operations])
    end
    subgraph System["System"]
        SERVICES[Services]
    end
    subgraph External["External Systems"]
        ERP[(ERP)]
    end
    CUST --> SERVICES
    OPS --> SERVICES
    SERVICES --> ERP
```

## Template Sections Common to Architecture Docs

Every architecture template should include:

1. **Purpose** — What this document defines
2. **Overview/Diagram** — Visual representation (Mermaid)
3. **Component/Element Catalog** — Table with ID, name, description, status
4. **Relationships/Interfaces** — How elements connect
5. **Design Decisions** — Why this structure was chosen
6. **Quality Attributes** — How the design addresses NFRs
7. **Related Documents** — Cross-references with `[[wikilinks]]`

## ADR Template Pattern

```markdown
# ADR-XXX: Title

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What forces are at play?]

## Decision
[What are we deciding?]

## Consequences
### Positive
- [What becomes easier?]
### Negative
- [What becomes harder?]

## Alternatives Considered
| Alternative | Why Not |
|-----------|---------|
```

## Trade Study Pattern

Always use weighted scoring matrix:

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|---------|---------|---------|
| C1 | X% | Score × W | Score × W | Score × W |
| **Total** | 100% | **Sum** | **Sum** | **Sum** |

## Key User Preferences for Architecture Docs

- Mermaid diagrams for ALL visual representations
- Emoji heat maps (not ASCII) for risk matrices
- Tables for structured data (registers, catalogs, matrices)
- `[[wikilinks]]` for cross-references
- YAML frontmatter with `standard_ref` pointing to source BOK
- Color semantics consistent across all diagrams
