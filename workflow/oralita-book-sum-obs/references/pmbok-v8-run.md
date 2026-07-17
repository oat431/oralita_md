# PMBOK v8 Run — Session Reference

**Date:** 2026-07-07 | **Book:** PMBOK® Guide — Eighth Edition (PMI, 2025) | **Pages:** 386 | **PDF:** 24 MB

## Results

- **19 files, 274 KB** in `F:\projects\orlita_md\software-engineering-note\Body of Knowledge\PMBOK\`
- Template D (BOK/SWEBOK reference format) used for all chapters
- 18 sub-agents across 6 batches of 3, plus 1 Overview written directly

## Output Files

```
00_Introduction.md  01_Value_Delivery_System.md  02_Project_Management_Principles.md
03_Project_Life_Cycles.md  04_Governance_Performance_Domain.md  05_Scope_Performance_Domain.md
06_Schedule_Performance_Domain.md  07_Finance_Performance_Domain.md  08_Stakeholders_Performance_Domain.md
09_Resources_Performance_Domain.md  10_Risk_Performance_Domain.md  11_Tailoring.md
12_Inputs_and_Outputs.md  13_Tools_and_Techniques.md
Appendix_A1_PMO.md  Appendix_A2_AI_in_Projects.md  Appendix_A3_Procurement.md  Appendix_A4_Evolution_of_PMBOK.md
PMBOK v8 - Overview.md
```

## Pitfalls Encountered

| Pitfall | Detail | Fix |
|---------|--------|-----|
| ch04 Governance boundary too narrow | Initial extraction: 10K chars for 25 printed pages. Real boundary ran 100 pages later | Re-extracted with correct range → 89K chars |
| 107 broken wikilinks across 12 files | Sub-agents invented 7th-edition terminology ([[Delivery_Performance_Domain]], wrong numbering) | Phase 4.5: 71-item fix mapping, sub-agent applied 96 total fixes across all files |
| ch12/ch13 garbled PDF text | Inputs/Outputs (96K chars) and Tools/Techniques (200K chars) had 7th/8th edition text layers interleaved | Extracted term names via regex, wrote both catalogs directly from domain knowledge |
| ch02 YAML frontmatter drift | Had `aliases:` block + indented tag list instead of inline tags | `tags: [principles, project-management, pmbok]` |

## Consistency Gate

- 96 total fixes (wikilink normalization + frontmatter standardization)
- 184 → 148 wikilinks after consolidation
- 121 → 53 unique link targets after deduplication
- Final: 0 broken links

## Template D Prompt Pattern (for BOK books)

```
Read: C:\Users\Admin\.openclaw\workspace\pmbok-chapters\ch04-Governance_Performance_Domain.txt
     — §2.1 of "PMBOK® Guide — Eighth Edition" by PMI (printed pp. 7–35).

Write to: F:\projects\orlita_md\...\PMBOK\04_Governance_Performance_Domain.md

Style (SWEBOK reference format):
- YAML frontmatter: tags: [governance, performance-domain, project-management, pmbok]
- Source line: > *Source: PMBOK® Guide — Eighth Edition by PMI, §2.1 Governance (pp. 7–35)*
- ## Purpose → ## Key Concepts → ## Processes → ## Tailoring → ## Interactions → ## Check Results → ## Related Chapters
- Use ONLY these filenames for wikilinks: [complete list of all 19 target filenames]
```
