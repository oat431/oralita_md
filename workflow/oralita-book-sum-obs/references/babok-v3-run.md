# BABOK v3 Run Notes

**Book:** BABOK® Guide v3 — IIBA, 2015
**PDF:** 514 pages, 3.2 MB
**Output:** 11 files, ~80 KB target

## Structure

BABOK v3 uses a unique Knowledge Area + Tasks structure:
- 6 Knowledge Areas, each with 4-6 tasks
- Each task has: purpose, description, inputs, elements, guidelines/tools, techniques, stakeholders, outputs
- Supporting chapters: Introduction (BACCM), Underlying Competencies, Techniques Catalog (50), Perspectives (5)

## Extraction

```
babok-01-Introduction_and_Key_Concepts  :  41,133 chars  (20 pp)
babok-02-BA_Planning_and_Monitoring     :  66,411 chars  (32 pp)
babok-03-Elicitation_and_Collaboration  :  45,906 chars  (22 pp)
babok-04-Requirements_Life_Cycle_Mgmt   :  47,816 chars  (24 pp)
babok-05-Strategy_Analysis              :  73,620 chars  (34 pp)
babok-06-Requirements_Analysis_and_Design: 62,286 chars  (30 pp)
babok-07-Solution_Evaluation            :  48,729 chars  (24 pp)
babok-08-Underlying_Competencies        :  66,677 chars  (30 pp)
babok-09a-Techniques_A_to_D             :  86,500 chars  (42 pp)
babok-09b-Techniques_E_to_P             : 128,643 chars  (60 pp)
babok-09c-Techniques_R_to_W             :  98,376 chars  (48 pp)
babok-10-Perspectives                   : 172,664 chars  (72 pp)
babok-11-Techniques_to_Task_Mapping     :  17,615 chars  (15 pp)
```

## Output Files

```
00_Introduction_to_BABOK.md           - Ch1: BACCM, key terms, stakeholders
01_BA_Planning_and_Monitoring.md      - Ch2: 5 tasks (approach, engagement, governance, info, performance)
02_Elicitation_and_Collaboration.md   - Ch3: 5 tasks (prepare, conduct, confirm, communicate, manage)
03_Requirements_Life_Cycle_Management.md - Ch4: 5 tasks (trace, maintain, prioritize, assess, approve)
04_Strategy_Analysis.md               - Ch5: 4 tasks (current state, future state, risks, change strategy)
05_Requirements_Analysis_and_Design.md - Ch6: 6 tasks (specify, verify, validate, architecture, options, value)
06_Solution_Evaluation.md             - Ch7: 5 tasks (measure, analyze, assess limitations, recommend)
07_Underlying_Competencies.md         - Ch8: 6 competency areas
08_Techniques_Catalog.md              - Ch9: 50 techniques (written directly, not via sub-agent)
09_Perspectives.md                    - Ch10: 5 perspectives (Agile, BI, IT, BizArch, BPM)
BABOK v3 - Overview.md                - Master index
```

## Key Decisions

1. **Techniques catalog written directly** — 314K chars across 3 files merged into one comprehensive catalog. Sub-agents would produce inconsistent formatting across 50 entries; direct writing ensures uniform style.

2. **Template D used** — Each Knowledge Area chapter follows the SWEBOK reference format with YAML frontmatter, source citation, Purpose, task-by-task breakdowns (inputs/elements/techniques/outputs per task), and Related Chapters.

3. **BACCM diagram** — The 6 core concepts (Change, Need, Solution, Stakeholder, Value, Context) are central to BABOK. Every KA file links back to this model.
