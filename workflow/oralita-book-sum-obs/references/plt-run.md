# PLT Run — Programming Language Theory

**Date:** 2026-07-18
**Book:** *Principles and Practice of Programming Language*
**Pages:** 429
**PDF Size:** 1.2 MB (small book)
**Target:** `F:\obsidian_note\swe-knowledge\computing-foundation-note\Programming Language Theory`

## Run Stats

- **Files produced:** 8 (7 chapters + overview)
- **Total size:** 61 KB
- **Batches:** 3 (3+3+1+1 overview)
- **Total time:** ~5 minutes

## Topic Mapping

| File | Source | Topics |
|---|---|---|
| 01_Expressions_and_Evaluation | Ch 3 | Values, types, expressions, static type checking |
| 02_Binding_and_Scope | Ch 4 | Value/type bindings, scoping, closures, pattern matching |
| 03_Data_Types_and_Polymorphism | Ch 6 | Collections, options, tuples, polymorphism |
| 04_Syntax_and_Parsing | Ch 11-13 | Concrete syntax, CFGs, abstract syntax, ASTs |
| 05_Type_Systems_and_Judgments | Ch 14-17 | Static scoping, judgments, inference rules, type systems |
| 06_Operational_Semantics | Ch 18-20 | Big-step semantics, closures, recursion |
| 07_Evaluation_and_Functions | Ch 21-22 | Small-step semantics, evaluation order, substitution |
| Programming Language Theory Overview | — | Index + Mermaid diagram |

## Issues & Fixes

1. **Sub-agents skipped wikilinks** — 3 of 7 files had zero `[[wikilinks]]` (01, 02, 04). Fixed by appending Related sections.
2. **Source file naming** — plt-Expressions_and_Evaluation.txt only contained the preface; actual Ch 3 content was in plt-Binding_and_Scope.txt (lines 1-267). Sub-agent adapted.
3. **Source file incomplete** — plt-Data_Types_and_Polymorphism.txt cut off at page 55; Maps, sets, classes, ADTs, parametric polymorphism not covered. Sub-agent noted this.

## Verification

- 8/8 files passed (YAML frontmatter, wikilinks, >1KB)
- Computing Foundation Overview updated (PLT added, removed from "What's Missing")
- Only AI/ML remains missing from SWEBOK Computing Foundations

## SWEBOK Computing Foundations Status (after this run)

| KA | Status |
|---|---|
| Computer Architecture | ✅ Computer Organization vault (8 files) |
| Data Structures & Algorithms | ✅ Algorithm + Algorithm_advance |
| Programming Fundamentals | ✅ Fundamental vault |
| Operating Systems | ✅ Operating Systems vault |
| Database Management | ✅ Database vault |
| Computer Networks | ✅ Computer Networks vault |
| HCI | ✅ HCI Simplify vault |
| AI/ML | ❌ Still missing |
| Programming Language Theory | ✅ **This run** |
