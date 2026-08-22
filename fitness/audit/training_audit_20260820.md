---
date: 2026-08-20
tags: [fitness, audit, data, phase-2, tracking]
auditor: coach (gym profile)
scope: Phase 2 W8 — data & tracking audit
---

# Training Audit — Data Gaps — 2026-08-20

> **Audit scope:** data capture only. Exercise selection was reviewed separately — verdict: current exercise set is adequate, no additions needed. This file lists what is NOT being captured and what it would cost to fix.

## Summary

The program file, day notes, and review cadence are in good shape. The gap is between the data we *ask for* and the data that *actually lands* in the log. Ranked below by value.

## Data Gaps — Ranked

| # | Gap | Why it matters | Fix | Effort | Destination |
|---|-----|----------------|-----|--------|-------------|
| 1 | **Run/walk: minutes + distance + avg HR never logged** (W5–W8, 4 weeks missing minutes) | Marathon goal (12:00/km pace). Without duration/pace/HR there is no run progression decision possible. HR 117–137 bpm = Zone 2 target already defined | Log 3 numbers after each Wed session: minutes, distance (km), avg HR | 10 sec | `[[training-log-phase2]]` Wed row |
| 2 | **Calories never audited** — only "protein 160 ✓" is logged | The 2,050 kcal cut (W8) was applied blind. We don't know if it's actually being eaten | Add **kcal** column to daily check-in table; 2-week light food log (kcal + protein per meal, no full macro tracking) to calibrate | 1 number/day | Daily check-in tables |
| 3 | **Tape measurements: single data point** (08-16 only) | Waist 130 cm is the real health headline (WtH 0.73 vs <0.5 target). Needs a trend line, not a snapshot | Monthly: waist, hip, chest — Sunday morning, same protocol as 08-16 baseline | 2 min/month | `[[smart-scale-tracking]]` tape table |
| 4 | **No progress photos** | BIA noise is ±0.5 kg; photos are the only reliable recomp evidence over months | Monthly front + side, same light/distance | 30 sec/month | `audit/` or photo folder |
| 5 | **No blood pressure** | At 121 kg this is the missing health metric; RHR alone doesn't cover cardiovascular load | Weekly, same time of day — only if a cuff exists | Skip if no cuff | `[[smart-scale-tracking]]` or check-in |
| 6 | **No blood panel baseline** | 12-month visceral-fat goal (<10) needs a starting lab value | One clinic visit: fasting glucose, HbA1c, lipids. One-time, at Phase 3 start | 1 visit, optional | `[[baseline-assessment]]` |

## Explicit Non-Priorities (do not track)

- **Water intake** — target (3–4 L/day) exists; logging adds noise.
- **Watch active calories** — self-admitted unreliable; `[[smart-watch-settings]]` already says not to chase it.
- **Daily body fat %** — daily BIA is random noise; Sunday standardized reading only.

## Open Data Signals — W8 (act on these in the Sunday completion review)

| Signal | Current value | Threshold | Action if triggered |
|--------|---------------|-----------|---------------------|
| Weight drop speed | 121.2 → 120.0 kg in 5 days | 7d MA >0.6 kg/week for 2 consecutive weeks | Revert 2,050 → 2,200 kcal/day |
| Muscle mass | 75.3 kg (-0.7 since baseline) | Acceleration of loss | Protect protein 160 g; check deficit depth |
| Resting HR | 78 bpm in W7 (vs 57–59 baseline) | Still elevated in W8 | Phase 3 starts with a light week (80% volume) |
| Bench W8 log | 47.5→45→42.5 (invalid 3×5) | — | Phase 3 bench starts at 45 kg, rebuilds. 47.5 is unearned |
| Wed minutes | W8 row empty (4th time) | — | Zero run-progression decisions possible until fixed |

## Proposed File Changes (Phase 3 fold-in)

1. Daily check-in table gains a **kcal** column (target 2,050).
2. Wed day note gains **distance + avg HR** log fields next to minutes.
3. `[[smart-scale-tracking]]` tape table gains a monthly schedule row.
4. Tape + photo reminder added to the Sunday review checklist in `[[phase_2/weekly-review-summary]]`.

*Handoff: implementation to be folded into the Phase 3 completion review (Sunday). This audit is the data-side input.*
