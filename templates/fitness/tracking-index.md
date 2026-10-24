---
date: 2026-10-24
tags: [fitness, template, tracking, index]
---

# Tracking Templates — Index

> Master designs for all tracking files. **Live files in `training/` are created from these.** The phase system was retired 2026-10-24 — `training/` is the single live program; phases 1–3 live read-only in `../archive/`.

## What lives here

| Template | Fills in | Cadence | Live location |
|----------|----------|---------|---------------|
| `daily-check-in.md` | Sleep, weight, protein, kcal, steps | Every day | Check-in tables inside `training/logs/daily/training-log.md` |
| `training-log-week.md` | Session results, all working sets | After every session | `training/logs/daily/training-log.md` |
| `walk-log.md` | Minutes, distance, HR per walk session | Tue/Thu/Sat (W1) | `training/logs/daily/walk-log.md` |
| `blood-pressure-log.md` | Cuff readings | Baseline week daily → then Sun + Thu | `training/logs/weekly/blood-pressure-log.md` |
| `blood-panel-baseline.md` | Clinic lab results | One-time draw, retest 6 months | **vault root** `blood-panel-baseline.md` |
| `body-metrics.md` | BIA + tape + photos | BIA weekly, tape/photo monthly | Split: BIA → `training/logs/weekly/smart-scale-weekly.md`; tape/photos → **root** `body-measurements-monthly.md` |
| `food-log.md` | Thai freestyle kcal system — anchors + dish table + weekly audit | Structure daily, audit Thu | `training/food-log.md` |

> **Live structure (from 2026-10-24):** cross-phase records live at the vault root (`baseline-assessment.md`, `blood-panel-baseline.md`, `body-measurements-monthly.md`); `training/` holds the live program (`program-overview.md`, `exercise/` session files by type, logs split into `logs/daily/` and `logs/weekly/`); `archive/` holds the retired phases.

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
- Warm-up rules: `[[warmup-protocol]]` (live copy in `training/`)
- Baseline metrics: `[[baseline-assessment]]`
