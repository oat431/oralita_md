# SWE Theory & Practice Run

**Date:** 2026-07-18
**Book:** *Software Engineering: Theory and Practice* by Shari Lawrence Pfleeger & Joanne Atlee, 4th Edition
**PDF:** `F:\books\Engineering_Foundation\SWE_Theory_and_Practice.pdf` (4.3 MB, 783 pages)
**Target:** `F:\obsidian_note\swe-knowledge\engineering-foundation-note\`
**Combined with:** Engineering Fundamentals by Moaveni (physics/math, files 01-09)

## Outcome

- **Files:** 10 new files (10-19) + updated overview = 20 total files (01-19 + overview)
- **Size:** 248 KB total (engineering-foundation-note)
- **Batches:** 4 batches of 3 + 1 standalone
- **Issues:** 1 sub-agent wrote to wrong directory (SWEBOK instead of engineering-foundation-note); 4 files missing wikilinks

## Chapter Mapping

| Ch | File | Topics |
|---|---|---|
| 1-2 | `10_SE_Fundamentals_and_Process.md` | Why SE, software quality, systems approach, process models, life cycle |
| 3 | `11_Project_Planning_and_Management.md` | Tracking progress, personnel, effort estimation, risk management |
| 4 | `12_Requirements_Engineering.md` | Requirements process, elicitation, types, modeling notations, prototyping |
| 5 | `13_Software_Architecture.md` | Architecture design, styles, quality attributes, evaluation, product lines |
| 6 | `14_Design_Principles_and_Patterns.md` | OO design, UML, design patterns, OO measurement |
| 7 | `15_Coding_Standards_and_Practices.md` | Programming standards, guidelines, documentation |
| 8-9 | `16_Testing_Strategies.md` | Unit testing, integration testing, system testing, safety-critical |
| 10-11 | `17_Delivery_and_Maintenance.md` | Training, documentation, maintenance types, rejuvenation |
| 12-13 | `18_Evaluation_and_Improvement.md` | Evaluation techniques, metrics, process improvement |
| 14 | `19_Future_of_Software_Engineering.md` | Technology transfer, professionalization, ethics |

## Two-Book Vault Pattern

This run combined two complementary books into a single vault:
- **Moaveni** (files 01-09): Physics & math fundamentals
- **Pfleeger** (files 10-19): SE process & engineering foundations

The overview file uses a two-part structure:
- **Part 1: Engineering Fundamentals (Physics & Math)** — 9 files from Moaveni
- **Part 2: SWE Theory & Practice (Engineering Foundations)** — 10 files from Pfleeger
- Single Mermaid diagram showing relationships between both parts
- Reading paths for different goals

**Lesson:** When combining books, the overview should clearly separate the sources while showing how they relate. The Mermaid diagram should have subgraphs per source book.

## Lessons Learned

1. **Sub-agent directory routing** — The Ch14 sub-agent wrote to `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\19_Future_of_Software_Engineering.md` instead of the target directory. **Fix:** Check file locations after every batch, especially for files dispatched late or standalone. Move with `mcp_filesystem_move_file` if misplaced.

2. **4 files missing wikilinks** — Sub-agents for Ch4, Ch5, Ch10-11, Ch12-13 produced files with zero `[[wikilinks]]`. **Fix:** After batch completion, run `grep -c "\[\[" file` for each file. For files with 0 links, append a `## Related` section with appropriate wikilinks using the `append` approach (open file with `a` mode and write).

3. **Verification false negatives with exact substring** — `grep "Usability Testing"` found 0 matches because the file had "Usability Test Plan" and "Usability Test Report" (no -ing suffix). **Fix:** Use partial matches or regex in verification scripts. For category checks, use `any(keyword in c for keyword in ['Usability Test', 'Usability Testing'])` instead of exact substring.

4. **Chinese text in sub-agent output** — `14_Design_Principles_and_Patterns.md` was written entirely in Chinese (3255 Chinese characters). The sub-agent likely had Chinese training data or the source PDF had bilingual content. **Fix:** After sub-agents complete, run Python check: `chinese = [ch for ch in c if '\u4e00' <= ch <= '\u9fff']`. If count > 0, rewrite the entire file in English using `write_file`. Don't try to patch individual lines. Use Python's explicit Unicode range check (`'\u4e00' <= ch <= '\u9fff'`) — grep `[\\u4e00-\\u9fff]` matches both Chinese AND some ASCII ranges, producing false positives.
