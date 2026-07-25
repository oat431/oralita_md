# Software Architecture in Practice (SAiP) — Run Notes

**Date:** 2026-07-21
**Book:** Software Architecture in Practice, 4th Edition by Bass, Clements & Kazman
**PDF:** 620 pages, 5.9 MB
**Target:** `F:\obsidian_note\swe-knowledge\software-engineering-note\02_Software_Architecture`

## Topic Mapping

28 chapters mapped to 11 summary files + overview:

| File | Chapters | Topics |
|------|----------|--------|
| 01_Architecture_Fundamentals | Ch 1-3 | What architecture is, structures & views, contexts & stakeholders |
| 02_Quality_Attributes_Overview | Ch 4, 12 | QA scenarios, specifying QAs, tactics framework |
| 03_Availability_and_Interoperability | Ch 5-6 | Fault detection/recovery, service discovery, mediation |
| 04_Modifiability_and_Performance | Ch 7-8 | Coupling/cohesion, resource management, concurrency |
| 05_Security_and_Testability | Ch 9-11 | Security tactics, test interfaces, usability |
| 06_Tactics_and_Patterns | Ch 13 | Full tactics catalog + 10 architecture patterns |
| 07_Design_and_Documentation | Ch 16-18 | ASRs, ADD method, views & beyond |
| 08_Architecture_in_Agile | Ch 15 | Agile architecting, just-in-time design |
| 09_Evaluation_and_Governance | Ch 19-22 | ATAM, reconstruction, conformance, management |
| 10_Economics_and_Product_Lines | Ch 23-25 | CBAM, architecture competence, software product lines |
| 11_Cloud_and_Edge_Architecture | Ch 26-27 | Cloud-native patterns, edge systems |

## Batches

- **4 batches total:** 3 batches of 3 sub-agents, 1 batch of 2 sub-agents
- **Batch 3 ran synchronously** — delegation pool at capacity (max_concurrent_children). Files written sequentially.
- **Batch 4 dispatched async** — 10 and 11 done in parallel.

## Vault Integration

The existing `02_Software_Architecture` folder already had:
- `Software Architecture Overview.md` — SWEBOK KA overview with "What's Missing" section
- `Microservice/` — 7 subdirectories with 28 files on microservice patterns

Post-summarization actions:
1. Added SAiP section to Overview's "My Notes" — 11 entries
2. Removed "What's Missing" section — SAiP filled all listed gaps
3. SAiP files complement (don't replace) the Microservice section

## Issues Hit

1. **Sub-agents skipped wikilinks (Pitfall 18b):** 8 of 12 files (01, 03, 05, 06, 08, 09, 10, 11) had zero `[[wikilinks]]`. Fixed with execute_code appending Related sections.
2. **Batch 3 went missing (Pitfall 15):** 09_Agile_and_Project_Types.md was silently dropped. Re-dispatched as a single-task delegation.
3. **Synchronous batch:** Pool at capacity forced sync execution for batch 3.
