# Vault-Filling Examples (2025-06-24)

## Math for Software Engineering
- **Source:** `F:\projects\orlita_md\software-engineering-note\Body of Knowledge\17_Mathematical_Foundations.md`
- **Target:** `F:\projects\orlita_md\math-for-software-engineering-note\`
- **Overview:** `Math For SE Note Overview.md`
- **Result:** 11 new notes (Basic Logic was already done), all 12 SWEBOK topics covered
- **Format:** Topic number, LaTeX math, tables, code examples, "Why This Matters in SE" section

## English Skill
- **Source:** Domain knowledge + English Grammar in Use (Murphy) + Practical English Usage (Swan)
- **Target:** `F:\projects\orlita_md\English Skill\`
- **Overview:** `English Skill Content.md` (was 1 line, became full curriculum map)
- **Result:** 28 files across 8 category folders, including 12 individual tense deep-dives
- **Notable:** 12 English Tense split from one file into 13 (overview index + 12 individual files)
- **Format:** Tables, ❌/✅ comparisons, code snippets, ⚠️ Thai speaker traps, quick tests

## HCI / UI / UX
- **Source:** Laws of UX (lawsofux.com) + Refactoring UI + Don't Make Me Think
- **Target:** `F:\projects\orlita_md\software-engineering-note\Software Design\Human Computer Interaction\`
- **Result:** 32 files across 4 category folders: Gestalt Laws (5), UI Design (4), UX Laws (15), UX Principles (5)
- **Notable:** Each note has `![](url)` images from lawsofux.com; user later said they'll create their own images

## Design Pattern Mermaid Diagrams
- **Target:** 22 pattern files + 1 OOP intro
- **Action:** Added ` ```mermaid classDiagram ``` ` blocks after each `## Structure` section
- **Then:** Removed all ASCII art diagrams (box-drawing chars) since Mermaid is superior
- **Pitfall hit:** abstract-factory and memento lost their Mermaid during ASCII cleanup — had to re-add
- **Pitfall hit:** strategy.md got a broken mermaid block with plain text — had to clean up
- **Verification:** `execute_code` with Python scanning for ` ```mermaid ` presence across all files

## Programming Note Cross-Reference
- **Pattern:** When two vaults overlap, keep both but rewrite the content/index file
- **Result:** `Programming Note Content.md` now links to `software-engineering-note/` for deep content, keeps local stubs + unique topics (Cybersecurity)
