User preferences: colons > em-dashes. Mermaid diagrams > ASCII. Single-backslash LaTeX (\frac not \\frac). English for communication but Thai-language content in Thai subject notes. Uses numbered prefixes (00, 01...) for ordering BOK files. IPST textbooks = primary reference (free PDFs at ipst.ac.th). BOK purpose: parent-child communication tool for Thai education (not exam prep).
§
SWE: 250+ templates at F:\projects\project_spec\template\. SearXNG MCP re-setup 2026-07-30, now working but rate-limits (429) after ~3 rapid calls — space out searches or rely on model knowledge for Thai curriculum content.
§
Social Studies (58), English (45), Arts (22 files, 19 concept areas, 3 domain folders at Art/, complete 2026-08-04). Thai notes fully in Thai.
§
File naming: 01_Name.md per folder. LaTeX: $$...$$ in table cells, single backslash only. Mermaid over ASCII.
§
Mermaid rules for Obsidian: (1) `flowchart` not `graph`, (2) NO `()` in labels → use `&#40;`/`&#41;`, (3) NO `"1."` dot-numbers → `"1 "`, (4) NO `&` → use `and`. All tested and render correctly.
§
oralita-book-sum-obs workflow (F:\obsidian_note\oralita_md\workflow\oralita-book-sum-obs\SKILL.md) needs Template E for clinical/psychology/practitioner's guide books. Proven: adapted Template A with (Purpose, Key Concepts, Clinical Techniques, Case Vignettes, Summary Checklist, Related). Schema Therapy run: 10 ch, 449pp, 328KB, 4 batches. Psychology book vault at F:\obsidian_note\psychology_book\schema_therapy\.
§
Thai content via execute_code batch writing can produce encoding artifacts (mixed Latin/Thai chars like ควam, กlอน, วrอง). Always run sed cleanup pass after batch generation. Pattern: grep for known artifact strings, then sed replace across all .md files in the strand folder.
§
Senior SWE career path paused 2026-01-05 after completing 7/9 capability areas (Technical Ownership through Mentoring & Team Leadership). Partial work on 08_Engineering_Economics and 09_Promotion_Evidence committed. Future work: finish last 2 areas OR update F:\obsidian_note\swe-knowledge\checklist for library updates (user's next priority).