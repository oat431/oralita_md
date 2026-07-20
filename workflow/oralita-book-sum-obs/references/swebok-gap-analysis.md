# SWEBOK Engineering Foundations Gap Analysis

**Date:** 2026-07-18
**Context:** User had two books (Moaveni *Engineering Fundamentals* + Pfleeger *SWE Theory & Practice*) and wanted to know how well they cover SWEBOK's Engineering Foundations KA.

## Approach

1. Read the SWEBOK Engineering Foundations note (`18_Engineering_Foundations.md`) to get the 10 topics
2. Compare each topic against the book contents (from TOC + chapter summaries)
3. Classify as ✅ Covered, 🟡 Partially Covered, or ❌ Not Covered
4. For partial coverage, specify what's covered vs what's missing
5. For gaps, recommend specific sources (web search or textbook)

## Coverage Matrix Template

| SWEBOK Topic | Coverage | File/Source |
|---|---|---|
| **Topic Name** | ✅/🟡/❌ | [[file]] or "Missing" |

## Decision Rule: Web Search vs Textbooks

When filling gaps against SWEBOK/BOK frameworks:
- **Web search is sufficient** for standardized, well-documented concepts:
  - Root Cause Analysis (5-whys, Ishikawa, FTA, FMEA)
  - Measurement Theory (GQM, nominal/ordinal/interval/ratio)
  - Empirical Methods (designed experiments, case studies, retrospective)
  - Industry 4.0 (IoT, AI/ML, Big Data, CSE)
  - Statistical Inference (hypothesis testing, confidence intervals)
  - Engineering Standards (ISO/IEC/IEEE organizations, 5-step framework)
- **Textbook needed** for deep academic treatment:
  - Formal proofs, worked examples, proprietary models
  - Domain-specific methodologies with detailed case studies

**User confirmed** this approach works — they explicitly asked "do we actually need the textbook for this?" and approved web-sourced filling for 4 SWEBOK Engineering Foundations gaps.

## Coverage Percentage Tracking

Track coverage percentage in the overview as gaps are filled:
- Initial assessment: ~50% (after book summarization)
- After web-sourced gaps: ~85% (4 files added)
- After remaining gaps: ~95% (2 more files added)
- Update the overview line: `This vault covers **~X%** of SWEBOK's Engineering Foundations KA.`

## Output Location

Gap analysis goes in the vault's Overview file, between the reading paths and the related links section. Structure:
- `### Covered` — table of topics with file links
- `### Partially Covered → Now Fully Covered` — table with file links (not "what's missing")
- `### Previously Not Covered → Now Filled` — table with file links
- `### Still Missing` — table with status (usually "All major topics now covered" when complete)
- `### Covered` — table of topics with file links
- `### Partially Covered` — table with what's covered vs missing
- `### Not Covered` — table with recommended sources
- `### Quick Fix Suggestions` — numbered list of files to add

## Cleanup After Gap Filling

After all gaps are filled, REMOVE the gap analysis section from the overview (or update it to "All major topics now covered"). The user explicitly asked to remove the gap analysis from the Engineering Foundation overview after all SWEBOK Engineering Foundations gaps were filled. Don't leave stale gap analysis tables — they confuse readers about the current state of the vault.

## Related

- [[oralita-book-sum-obs]] — Main summarization skill
- [[references/engineering-textbook-format.md]] — Format for engineering foundation notes
