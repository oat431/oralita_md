# AI: A Modern Approach — Run Reference

**Book:** *Artificial Intelligence: A Modern Approach* by Stuart Russell & Peter Norvig (Pearson)
**Pages:** 1151
**Size:** 20.9 MB
**Date:** 2026-07-18

## Chapter Extraction

8 chapter groups extracted, ~2.8M chars total:

| Group | Pages | Chars | Chapters |
|---|---|---|---|
| AI_Foundations | 62 | 167K | Ch 1-2 |
| Search_and_CSP | 169 | 449K | Ch 3-6 |
| Logic_and_Reasoning | 245 | 662K | Ch 7-12 |
| Uncertainty_and_Decisions | 212 | 582K | Ch 13-17 |
| Machine_Learning | 136 | 370K | Ch 18-20 |
| Reinforcement_Learning | 29 | 79K | Ch 21 |
| NLP_and_Perception | 159 | 420K | Ch 22-25 |
| AI_Ethics_and_Future | 32 | 96K | Ch 26-27 |

## Focused Approach

Used **focused approach** (not full BOK summarization) — selected chapters relevant to SWEBOK Computing Foundations KA. Skipped detailed math/algorithms already covered in Algorithm vault (Ch 3-4 search details, Ch 13 probability math).

## Output

9 files, 93 KB in `Artificial_Intelligence/`:

| File | Size | Source |
|---|---|---|
| 01_AI_Foundations.md | 10.4 KB | Ch 1-2 |
| 02_Search_and_CSP.md | 17.1 KB | Ch 3-6 |
| 03_Logic_and_Reasoning.md | 17.3 KB | Ch 7-12 |
| 04_Uncertainty_and_Decisions.md | 13.3 KB | Ch 13-17 |
| 05_Machine_Learning.md | 6.2 KB | Ch 18-20 |
| 06_Reinforcement_Learning.md | 4.9 KB | Ch 21 |
| 07_NLP_and_Perception.md | 9.0 KB | Ch 22-25 |
| 08_AI_Ethics_and_Future.md | 13.4 KB | Ch 26-27 |
| AI Overview.md | 2.5 KB | — |

## Issues

1. **6 of 8 files missing wikilinks** — sub-agents skipped `[[wikilinks]]` again. Fixed by appending `## Related` sections in batch via `execute_code`.
2. **No language drift** — all files were in English (no Chinese characters detected).

## Verification

Ad-hoc verification: 9/9 PASS after wikilink fixes. Computing Foundation Overview updated with AI added and "What's Missing" changed to "All major SWEBOK Computing Foundations topics are now covered."
