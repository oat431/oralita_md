---
date: 2026-08-20
tags: [fitness, template, tracking, index]
---

# Tracking Templates — Index

> Master designs for all tracking files. **Phase 3 live files are created from these** after the Phase 2 completion review (Sunday). Phase 2 files in `../phase_2/` stay untouched until then.

## What lives here

| Template | Fills in | Cadence | Live location (Phase 3) |
|----------|----------|---------|-------------------------|
| `daily-check-in.md` | Sleep, weight, protein, kcal, steps | Every day | Check-in tables inside `phase_3/logs/daily/training-log-phase3.md` |
| `training-log-week.md` | Session results, all working sets | After every session | `phase_3/logs/daily/training-log-phase3.md` |
| `run-walk-log.md` | Minutes, distance, pace, HR per cardio session | Wed + Sun | `phase_3/logs/daily/run-walk-log.md` |
| `blood-pressure-log.md` | Cuff readings | Baseline week daily → then Sun + Thu | `phase_3/logs/weekly/blood-pressure-log.md` |
| `blood-panel-baseline.md` | Clinic lab results | One-time draw, retest 6 months | **vault root** `blood-panel-baseline.md` |
| `body-metrics.md` | BIA + tape + photos | BIA weekly, tape/photo monthly | Split: BIA → `phase_3/logs/weekly/smart-scale-weekly.md`; tape/photos → **root** `body-measurements-monthly.md` |
| `food-log.md` | Thai freestyle kcal system — anchors + dish table + weekly audit | Structure daily, audit Thu | `phase_3/food-log.md` |

> **Live structure (from 2026-08-23):** cross-phase records live at the vault root (`baseline-assessment.md`, `blood-panel-baseline.md`, `body-measurements-monthly.md`); phase folders hold the active program only, with logs split into `logs/daily/` and `logs/weekly/`.

## Why these exist

From `[[training_audit_20260820]]` — the data gaps found in Phase 2:

1. Run/walk minutes logged 0 of 4 weeks → now minutes + distance + avg HR
2. No blood pressure → cuff log added
3. No blood panel baseline → clinic template added
4. Tape = single data point → monthly schedule added
5. No photos → monthly photo log added

Food tracking is now **designed** — see `food-log.md` (Thai anchors + dish table + weekly audit). The Kcal column in `daily-check-in.md` uses its scoring bands.

## Supporting notes

- HR zones + watch guidance: `[[smart-watch-settings]]`
- Warm-up rules: `[[warmup-protocol]]` (Phase 2 file — Phase 3 gets its own)
- Baseline metrics: `[[baseline-assessment]]`
