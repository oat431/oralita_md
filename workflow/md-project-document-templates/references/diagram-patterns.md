# Diagram Patterns — Established Conventions

## Emoji Heat Map (Risk, Priority, Impact)

```markdown
| Impact \ Probability | Low | Medium | High |
|---------------------|-----|--------|------|
| **High** | 🟡 | 🟠 | 🔴 |
| **Medium** | 🟢 | 🟡 | 🟠 |
| **Low** | 🟢 | 🟢 | 🟡 |

> **Legend:** 🔴 Critical — Immediate action required | 🟠 High — Mitigation plan required | 🟡 Medium — Monitor and manage | 🟢 Low — Accept and monitor
```

Place risk IDs directly in cells: `🔴 CR-01`, `🟠 BR-01`

## Mermaid: Process Flow

```mermaid
flowchart TD
    START([Start]) --> CHECK{Decision?}
    CHECK -->|Yes| ACTION[Action]
    CHECK -->|No| END([End])
    style START fill:#4CAF50,color:#fff
    style END fill:#4CAF50,color:#fff
    style CHECK fill:#FF9800,color:#fff
```

## Mermaid: Dependency Diagram

```mermaid
flowchart LR
    OBJ01[OBJ-01<br>Description] --> OBJ02[OBJ-02<br>Description]
    OBJ03[OBJ-03<br>Description] --> OBJ02
    style OBJ01 fill:#4CAF50,color:#fff
    style OBJ02 fill:#2196F3,color:#fff
```

## Mermaid: Gantt Timeline

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Task A :a1, 2026-08-01, 30d
    Task B :a2, after a1, 45d
    Gate Review :milestone, after a2, 0d
```

## Mermaid: Org Chart

```mermaid
flowchart TD
    CEO[CEO] --> VP1[VP Operations]
    CEO --> VP2[VP IT]
    VP1 --> MGR[Manager]
    style CEO fill:#1a237e,color:#fff
```

## Mermaid: Quadrant Chart (Effort vs Impact)

```mermaid
quadrantChart
    title Effort vs Impact
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Quick Wins
    quadrant-2 Strategic Projects
    Item-1: [0.3, 0.8]
    Item-2: [0.7, 0.9]
```

## Mermaid: Mind Map

```mermaid
mindmap
  root((Central Topic))
    Branch A
      Item 1
      Item 2
    Branch B
      Item 3
```

## Mermaid: Journey Map

```mermaid
journey
    title User Journey
    section Phase 1
      Step 1: 5: User
      Step 2: 4: User, System
```

## Mermaid: Pie Chart

```mermaid
pie title Distribution
    "Category A" : 40
    "Category B" : 35
    "Category C" : 25
```

## Color Conventions

| Element | Color | Hex |
|---------|-------|-----|
| Start/End nodes | Green | `#4CAF50` |
| Decision nodes | Orange | `#FF9800` |
| Error/Reject nodes | Red | `#f44336` |
| Process nodes | Blue | `#2196F3` |
| Data/Storage nodes | Orange | `#FF9800` |
| Integration nodes | Purple | `#9C27B0` |
| Observability nodes | Grey | `#607D8B` |
| Executive/Strategic | Dark Blue | `#1a237e` / `#283593` |
| Phases | Vary per phase | Green → Blue → Purple |
