# Gantt Chart Patterns — Mermaid Reference

7 reusable Gantt chart patterns for project documents. All use Mermaid `gantt` syntax.

## 1. Full Project Gantt (All Activities)

```mermaid
gantt
    title Project Schedule
    dateFormat YYYY-MM-DD
    axisFormat %d %b %Y
    tickInterval 1week

    section Phase Name
    Activity Name           :a1, 2026-08-01, 10d
    Another Activity        :a2, after a1, 5d
    Milestone               :milestone, after a2, 0d
    Critical Milestone      :milestone, crit, after a2, 0d
```

Key patterns:
- `after task_id` for dependencies
- `milestone` for zero-duration events
- `crit` for critical path highlighting
- `tickInterval 1week` for weekly grid

## 2. Phase Summary (Executive View)

```mermaid
gantt
    title Project Phases - High Level
    dateFormat YYYY-MM-DD

    section Initiation
    Charter and Kickoff         :a1, 2026-08-01, 6d

    section Planning
    Requirements              :b1, after a1, 30d
    Design                    :b2, after b1, 19d

    section Execution
    Sprint 1                  :c1, after b2, 10d
    Sprint 2                  :c2, after c1, 10d
```

## 3. Sprint-Level Gantt

```mermaid
gantt
    title Sprint Schedule
    dateFormat YYYY-MM-DD

    section Sprint 1
    Planning                  :a1, 2026-10-05, 1d
    Development               :a2, after a1, 8d
    Review and Retro          :a3, after a2, 1d
```

Pattern: Plan (1d) - Dev (8d) - Review (1d) per sprint

## 4. Resource Allocation Gantt

```mermaid
gantt
    title Resource Allocation Timeline
    dateFormat YYYY-MM-DD

    section Management
    PM 50pct                  :a1, 2026-08-01, 170d

    section Development
    Senior Dev 1              :d1, 2026-10-01, 90d
    Senior Dev 2              :d2, 2026-10-01, 90d
```

Pattern: Group by role category, show allocation in label

## 5. Milestone Gantt

```mermaid
gantt
    title Key Milestones
    dateFormat YYYY-MM-DD

    section Gates
    Project Kickoff           :milestone, 2026-08-08, 0d
    Requirements Baselined    :milestone, 2026-09-05, 0d

    section Deployment
    Go-Live                   :milestone, crit, 2027-01-30, 0d
```

Pattern: Group milestones by phase, crit on key decision points

## 6. Critical Path Gantt

```mermaid
gantt
    title Critical Path
    dateFormat YYYY-MM-DD

    section Critical Path
    Activity 1                :crit, a1, 2026-08-11, 12d
    Activity 2                :crit, a2, after a1, 12d

    section Non-Critical Float
    Training                  :b1, after a2, 5d
```

Pattern: crit on all critical path activities, separate section for non-critical

## 7. Readiness Improvement Gantt

```mermaid
gantt
    title Readiness Improvement Actions
    dateFormat YYYY-MM-DD

    section People
    Communication Campaign  :a1, 2026-09-01, 30d
    Accelerated Training    :a2, 2026-09-15, 45d

    section Process
    Exception Documentation :c1, 2026-09-01, 14d
    Process Dry Runs        :c2, after c1, 14d
```

Pattern: Group by improvement category, show dependencies

## Export Commands

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.png
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.pdf
```
