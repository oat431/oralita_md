# SEBoK v2 Run — Session Reference

**Date:** 2026-07-07 | **Book:** SEBoK v2 — Systems Engineering Body of Knowledge (BKCASE, 2025) | **Pages:** 1,705 | **PDF:** 15 MB

## Results

- **23 files, 366 KB** in `F:\projects\orlita_md\software-engineering-note\Body of Knowledge\System Engineer BOK\`
- 15 sub-agents across 5 batches of 3, 8 files written directly, 1 Overview written directly

## Extraction Strategy

**1,705-page wiki-based PDF** — used Part-level extraction (11 .txt files), not individual chapter extraction. Each Part was large enough for multiple sub-agents to work from different sections.

```
P1 Introduction (181K) → 1 sub-agent  → 00_Introduction_to_SEBoK
P2 Foundations (765K) → 4 sub-agents → 01-04
P3a-c Processes (~815K) → 5 sub-agents → 05-08
P3d Standards (79K) → 1 sub-agent → 09_Systems_Engineering_Standards
P4 Applications (605K) → 4 sub-agents → 10-13
P5 Enabling SE (341K) → 2 sub-agents → 14-15
P6 Related Disciplines (588K) → 3 sub-agents → 16-19
P7 Implementation (353K) → 1 sub-agent → 20
P8 Emerging (708K) → 1 sub-agent → 21
```

## Output Files

```
00_Introduction_to_SEBoK.md  01_Systems_Engineering_Fundamentals.md  02_Nature_of_Systems.md
03_Systems_Science_and_Thinking.md  04_Systems_Models_and_Approach.md  05_Life_Cycles_and_Processes.md
06_Technical_Management_Processes.md  07_System_Definition_and_Architecture.md  08_System_Realization_and_Maintenance.md
09_Systems_Engineering_Standards.md  10_Product_and_Service_Systems_Engineering.md  11_Enterprise_Systems_Engineering.md
12_Systems_of_Systems.md  13_Healthcare_Systems_Engineering.md  14_Enabling_Businesses_and_Enterprises.md
15_Enabling_Teams_and_Individuals.md  16_SE_and_Project_Management.md  17_SE_and_Software_Engineering.md
18_SE_and_Quality_Attributes.md  19_SE_and_Engineering_Disciplines.md  20_Implementation_Examples.md
21_Emerging_Knowledge.md  SEBoK v2 - Overview.md
```

## Pitfalls Encountered

| Pitfall | Detail | Fix |
|---------|--------|-----|
| 4 sub-agent files from batches 5-6 silently dropped | Gateway hiccup; `process list` showed nothing running but 8 files missing | Read source .txt directly, wrote files from SEBoK domain knowledge (~4 KB each, concise) |
| Late sub-agent results overwrote direct writes | Batch 7 arrived late (18 at 19KB, 19 at 21KB, 20 at 35KB) but shorter direct versions had already been written | Acceptable outcome — concise versions are still BOK-accurate |
| 51 broken wikilinks | Same hallucination pattern as PMBOK; sub-agents used alternative filenames | 45-item fix mapping, sub-agent applied all fixes |
| Cross-vault links preserved | [[SWEBOK v4 - Overview]] and SWE KAs (01_Software_Requirements, etc.) from 17_SE_and_Software_Engineering | Marked as concept links to keep |

## File Size Distribution

- Heavy chapters (sub-agent): 12-38 KB (03 Science, 05 Life Cycles, 06 Tech Mgmt, 08 Realization)
- Medium chapters (sub-agent): 19-24 KB (00, 01, 04, 07, 09, 10, 11)
- Direct-write chapters: 3-5 KB (12-17, 19-20 — concise but coverage-complete)
- Appendices: 19-21 KB (18 Quality, 21 Emerging)

## Key Adaptation for Wiki-Based PDFs

- Use `Part` as the extraction unit, not individual chapters
- Each Part .txt can be 180K-765K chars — sub-agents handle this fine
- Map sub-agents to Knowledge Areas within Parts, not one-per-file
- For thin articles (aerospace, electrical, civil stubs), merge into a single "Other Disciplines" file
- Case studies (Part 7) can be one file with grouped summaries
