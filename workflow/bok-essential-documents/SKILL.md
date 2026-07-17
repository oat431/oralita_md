---
name: bok-essential-documents
description: Use when extracting standard documents/artifacts from any Body of Knowledge (SWEBOK, BABOK, PMBOK, SEBOK, CyBOK, DMBOK) or non-BOK discipline (UX/UI Design) into an Obsidian vault's Essential Document folder. Also use for creating cross-BOK project-type profiles (Small/Startup, Medium/Enterprise, Large/Safety-Critical).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bok, essential-documents, obsidian, sdlc, swebok, babok, pmbok, sebok, cybok, dmbok, ux-ui, profile]
    related_skills: [obsidian, obsidian-vault-builder, oralita-book-sum-obs]
---

# BOK Essential Documents Extraction

## Overview

Extract standard documents/artifacts from any Body of Knowledge (SWEBOK, BABOK, PMBOK, SEBOK, CyBOK, DMBOK) into the Obsidian vault's `Essential Document/` folder. Produces markdown tables sorted by priority (🔴→🟡→🟢) with document name, description, priority, and ISO/IEEE reference column. Includes section-level owner blockquotes.

## When to Use

- User asks to "extract standard documents" from a new BOK
- User says "list all standard documents like the other BOK"
- User adds a new BOK to `Body of Knowledge/` and wants its document catalog
- User asks for "essential documents" from any framework
- User asks for "project profiles" or "project-type templates" that tailor document selection by project size
- User wants to know "how much documentation do I need for X type of project"

**Supported BOKs:** SWEBOK v4, BABOK v3, PMBOK v8, SEBOK v2, CyBOK v1.1, DMBoK v2
**Supported non-BOK disciplines:** UX/UI Design (from HCI folder — industry standards, not a single BOK)

Don't use for: general Obsidian vault filling, book summaries, or any non-BOK document extraction.

## Workflow

### 1. Scan the BOK folder

Explore `F:\projects\orlita_md\software-engineering-note\Body of Knowledge\<BOK-NAME>\` to understand the chapter structure. Every BOK has an overview file and numbered KA/chapter files.

### 2. Read all KA files

Read the overview first to understand the BOK structure, then read every KA/chapter. Use batch parallel reads for efficiency — independent files can be read simultaneously.

### 3. Extract document artifacts

For each KA/chapter, extract every document/artifact that gets produced. Look for:
- Explicit "Outputs" sections (BABOK task outputs)
- Documents mentioned in Tools & Techniques tables
- Documents listed in Knowledge Area breakdowns
- Standards referenced alongside documents

### 4. Build the 4-column table

Every table row must have:

| Column | Content |
|---|---|
| **Document** | Bold name + abbreviation. Format: `**SRS** (Software Requirements Specification)` |
| **Description** | One concise sentence describing what the document captures |
| **Priority** | `🔴 Must Have`, `🟡 Nice to Have`, or `🟢 Optional` |
| **Reference** | Always `ISO/IEEE Reference` — the column header is universal across all BOKs. Map every document to the closest relevant ISO/IEEE standard. For BABOK, this means mapping BA outputs to ISO/IEC/IEEE 29148 (Requirements), ISO 31000 (Risk), ISO/IEC 25010 (SQuaRE), etc. — do NOT use BABOK task numbers in this column. Use `—` only when no standard applies. For UX/UI, use ISO 9241 series: ISO 9241-210 (human-centred design), ISO 9241-110 (dialogue principles), ISO 9241-112 (presentation), ISO 9241-11 (usability), ISO/IEC 40500 (WCAG 2.0). |

**Priority assignment rules:**
- 🔴 **Must Have** — the BOK treats it as foundational; skipping creates significant risk; explicitly listed as a core deliverable
- 🟡 **Nice to Have** — recommended for medium+ complexity; mentioned as good practice but not mandatory
- 🟢 **Optional** — situational (domain-specific, safety-critical only, methodology-dependent)

When uncertain, default to 🟡. Err toward 🔴 for anything explicitly called a "key output" by the BOK.

### 5. Add Owner blockquotes

Each section (KA or phase) gets a blockquote under the heading declaring who owns those documents:

```markdown
## 1. BA Planning & Monitoring
> **Owner:** BA / PM
```

Owners should reflect the primary role responsible, using short role names:
- BA, PM, Architect, Developer, QA, DevOps, Security Engineer, Systems Engineer, etc.
- Use `/` for shared ownership: `BA / PM`, `BA / Sponsor`, `Architect / Tech Lead`

**Do NOT add an Owner column to tables.** The user rejected this — it makes tables too wide and the owner is usually shared across a section. Section-level blockquotes are the preferred format.

Owner mappings per BOK:

| BOK | Owner Pattern |
|---|---|
| BABOK | One per KA: BA / PM, BA / Sponsor, BA, BA / PO, etc. |
| SWEBOK | One per SDLC phase + one per cross-cutting domain |
| PMBOK | One per process group + governance/procurement |
| SEBOK | One per lifecycle stage + sub-disciplines |
| CyBOK | One per security domain (6 sections): CISO / Risk Manager, Threat Intel Analyst / SOC Lead, SOC Manager / SecOps Lead, AppSec Engineer / DevSecOps Lead, Network Security Engineer, Security Architect / Cryptography Engineer |
| DMBOK | One per data management KA (11 sections): CDO / Data Governance Council, Data Architect, Data Modeler, DBA, Data Security Officer, Data Integration Architect, ECM Manager, MDM Architect, BI Architect, Metadata Manager, Data Quality Manager |
| UX/UI | One per design phase: UX Researcher / PM (Research), UX Designer / IA (UX Design), UI Designer / Visual Designer (UI Design), UX Researcher / QA (Testing), UI Designer / Frontend Dev (Handoff) |

### 6. Sort by priority

**Every table must be sorted 🔴→🟡→🟢.** Within each priority band, sort alphabetically by document name (the bold `**Name**` part). The user explicitly requested this — unsorted tables are a rejection-worthy defect.

To sort reliably, use the bundled script (emoji Unicode escapes work correctly in .py files, NOT in `-c` one-liners):

```
python3 <skill-dir>/scripts/sort_priority_tables.py <path-to-.md-file>
```

This finds all markdown tables in the file, sorts rows within each by priority (🔴→🟡→🟢, then alphabetically by document name), and writes back. It's safe for files containing non-table content (headings, paragraphs between tables are preserved).

### 7. Add integration diagram

At the end, add a section showing how this BOK fits with the others already in the vault. For BABOK→SWEBOK, show which BA outputs feed which SE phases. Match the format of existing integration diagrams.

### 8. Write to the Essential Document folder

Output path pattern:
```
F:\projects\orlita_md\software-engineering-note\Essential Document\<BOK-ACRONYM> Essential Documents.md
```

Naming must match existing convention: `SWEBOK Essential Documents.md`, `BABOK Essential Documents.md`, etc.

**Frontmatter must include:**
```yaml
---
tags: [overview, <domain>, <bok-acronym-lowercase>, essential-documents]
---
```

**Header must include:**
- Source attribution with wikilink to the BOK overview
- Organization summary (phases or KAs)
- Warning block pointing to the full BOK source folder
- Priority legend table

### 9. Update the Essential Documents overview

After writing the new BOK file, **always update** `Essential Documents - Overview.md`:
- Bump the discipline count (e.g. "three" → "four")
- Add the new BOK row to the summary table
- Add a new column to the Quick Comparison table showing equivalent outputs per stage
- Add the new BOK to the "Which Checklist Do I Need?" section
- Add the BOK overview wikilink to Related Vaults
- Update the tags frontmatter to include the new domain

### 10. Clean up transient files

If the combined content was written to a temporary location before splitting, restore that file to its original state (index-only for `Software Engineering Note Content.md`).

## Creating Project-Type Profiles (Cross-BOK)

When the user wants tailored document templates for different project sizes (e.g. Small/Startup, Medium/Enterprise, Large/Safety-Critical), create **separate profile files** that cherry-pick from all BOKs with adjusted priorities.

### Workflow

1. **Read all 6 BOK essential document files** from `Essential Document/` to understand available documents
2. **Define 3 profiles** based on team size, timeline, methodology, and regulatory exposure:
   - 🚀 **Small/Startup** (1-5 devs, Agile, weeks-months) — ~25-30 docs, 🔴 only covers shipping essentials
   - 🏢 **Medium/Enterprise** (10-50, Hybrid, 6-18mo) — ~80-110 docs, adds governance + formal QA
   - 🏗️ **Large/Safety-Critical** (50+, V-Model, 18+mo, regulated) — ~150+ docs, full formal coverage
3. **Assign priorities per profile** — the same document can be 🔴 in one profile and 🟢 in another (e.g. SEMP is 🟢 for Small but 🔴 for Large)
4. **Structure each file** with: Profile blockquote → When to Use → Sources → Priority Legend → Phase tables → Quick-Start Checklist → Related
5. **Quick-Start Checklist** at the end: compact table with Phase | Document | ✓ columns, 🔴 items only, no descriptions — meant to be printed
6. **Parallel subagent creation** — each profile file is large (150-600 lines), so delegate to parallel subagents for speed
7. **Post-creation wikilink audit** — verify all Related sections use consistent `[[BOK Essential Documents]]` format
8. **Update Overview** — add a "Project-Type Profiles" section with comparison table linking all profiles

### File naming convention

```
Profile-Small-Startup.md
Profile-Medium-Enterprise.md
Profile-Large-Safety-Critical.md
```

### Source BOK mapping per profile

| Profile | BABOK | PMBOK | SWEBOK | SEBOK | CyBOK | DMBOK |
|---|---|---|---|---|---|---|
| Small | Minimal (objectives, user stories) | Minimal (sprint board, risk list) | Core only (no formal reviews) | Skip (no HW) | Basic threat model | Backup only |
| Medium | Strategy + requirements lifecycle | Full planning + M&C | Full SDLC + QA + security | Light (ConOps, ICD, V&V) | AppSec (SAST/DAST, pen test) | Data models + quality |
| Large | Full strategy analysis | Full PMBOK + procurement | Full + formal reviews | Full SEBoK (SEMP, safety case) | Full CyBOK (ISMS, SOC, forensics) | Full DMBOK (governance, MDM) |

### UX/UI sections in project profiles

When adding UX/UI sections to project profiles, scale the document count by project size:

| Profile | UX/UI Section Name | Docs | Key Documents |
|---|---|---|---|
| 🚀 Small/Startup | 2b. UX/UI Design | 3 | Wireframes, Prototype, Style Guide (basic) |
| 🏢 Medium/Enterprise | 4b. UX/UI Design | 12 | Personas, Journey Map, IA, Wireframes, Mockups, Design System, Usability Test, Accessibility Audit |
| 🏗️ Large/Safety-Critical | 6b. UX/UI Design | 20 | Full UX/UI process with ISO 9241 references |

Owner blockquotes for UX/UI sections:
- Small: `> **Owner:** Designer / Developer`
- Medium: `> **Owner:** UX Researcher / UI Designer`
- Large: `> **Owner:** UX Researcher / UI Designer`

Source column should use `UX/UI` (not a BOK acronym). Add `[[UX UI Essential Documents]]` to the Sources section of each profile.

## Common Pitfalls

1. **File corruption during sort.** Running a Python sort script with a `write_file` call that replaces content can corrupt the file if the script fails mid-write. Always read→sort→write atomically, and verify the output file size and structure after every write.

2. **Emoji detection in `-c` one-liners.** Python `-c` scripts handle Unicode escapes inconsistently on Windows. Use a .py temp file (write_file + terminal run + rm) instead of inline `-c`.

3. **Unsorted tables.** The user explicitly wants 🔴→🟡→🟢 sort. An unsorted table is the most common rejection. Verify each section after writing.

4. **Missing priority or reference column.** The user asked for BOTH priority and a reference column. A table with only Description is incomplete. All 4 columns are mandatory.

5. **Wrong destination.** The user may not specify the destination upfront. Default to `Essential Document/` following the existing naming convention. If the file was written elsewhere first, move it — don't duplicate.

6. **Combining BOKs in one file.** Each BOK gets its own file. The `Software Engineering Note Content.md` file is an index, not a container for extracted documents.

7. **Using `skill_manage` for in-repo creation.** When creating this skill, `skill_manage(action='create')` writes to `~/.hermes/skills/`, which is correct for user-local skills.

8. **Wrong reference column format.** The column is `ISO/IEEE Reference` for ALL BOKs — not `BABOK Task`, not `SWEBOK Task`. Even for BABOK, map each document to the closest ISO/IEEE standard (29148 for requirements, 31000 for risk, 25010 for SQuaRE, etc.). The user explicitly corrected this.

9. **Forgetting the overview update.** Adding a new BOK checklist without updating `Essential Documents - Overview.md` leaves the vault inconsistent. The overview must reflect the new discipline count, summary table, comparison column, and navigation links.

10. **Owner in tables vs section header.** The user explicitly rejected an Owner table column (too wide, clutter). Use `> **Owner:** BA / PM` blockquotes under each `## ` header instead. Every section should have one, even if it's the same owner as the previous section.

11. **Double-processing corrupts columns.** When running multiple Python scripts that modify table structure (add column, remove column, sort), NEVER run a second script on output that was already processed by the first. Each script that splits on `|` and manipulates column indices will shift indices on already-modified rows. After any structural edit, verify the column count and header labels before running another script.

12. **Header-only fixes leave data behind.** When fixing a problem with a script that only targets header rows (looking for keywords like `Owner` or `---`), data rows can pass through unchanged if their cell values don't match the detection condition. Always verify BOTH headers and data rows after structural fixes — the rendering can look correct (data merges into adjacent columns) while the raw markdown is broken.

13. **Subagent wikilink inconsistency.** When creating multiple profile files via parallel subagents, each agent independently chooses a wikilink format for Related sections (e.g. `[[BABOK v3]]` vs `[[BABOK — Business Analysis Body of Knowledge]]` vs `[[BABOK Essential Documents]]`). Always run a post-creation audit: grep all Related sections across the batch and enforce a single convention (`[[<BOK-ACRONYM> Essential Documents]]`). Fix with targeted edits before declaring done.

14. **Missing Overview update after profile creation.** Creating profile files without updating `Essential Documents - Overview.md` leaves the vault without navigation to the new content. The overview needs a "Project-Type Profiles" section with a comparison table (profile name, team size, timeline, methodology, doc count, focus).

15. **UX/UI in non-BOK vaults.** UX/UI Design content doesn't come from a single BOK — it's synthesized from industry standards (ISO 9241, Nielsen Norman Group, Lean UX). When the user asks for UX/UI essential documents, check if they already have HCI/UX/UI content in their vault (e.g., `Software Design/Human Computer Interaction/`). If so, integrate rather than duplicate. The UX/UI Essential Documents file goes in `Essential Document/` alongside the BOK files, and the HCI overview should link to it.

## Verification Checklist

- [ ] All KA files read and processed
- [ ] Every table has **exactly 4 columns**: Document, Description, Priority, ISO/IEEE Reference — verify with `l.count('|')` == 5 on data rows (4 visible cols + leading empty)
- [ ] Reference column contains `ISO/IEEE` standards (not BOK-specific task numbers)
- [ ] **After any structural edit, re-verify:** spot-check header row, separator row, and 2-3 data rows for consistent column count
- [ ] **No double-processing artifacts:** verify no rows have merged/overflow data from a partially-removed column
- [ ] Every table sorted 🔴→🟡→🟢 within each priority band, then alphabetically by document name
- [ ] File written to `Essential Document/<BOK-ACRONYM> Essential Documents.md`
- [ ] Owner blockquote (`> **Owner:** ...`) under each section heading
- [ ] No Owner column in any table (section-level only)
- [ ] Frontmatter has correct tags
- [ ] Priority legend table present
- [ ] Integration diagram included
- [ ] File size reasonable (8-30KB for a full BOK)
- [ ] Source BOK overview wikilinked in header
- [ ] Old combined/transient files cleaned up
- [ ] **Essential Documents - Overview.md updated** (discipline count, summary table, comparison column, navigation)

### Profile creation verification (additional)

- [ ] All 3 profile files created with consistent naming (`Profile-<Name>.md`)
- [ ] Each profile has: Profile blockquote, When to Use, Sources, Priority Legend, Phase tables, Quick-Start Checklist, Related
- [ ] Quick-Start Checklists contain only 🔴 items with Phase | Document | ✓ columns
- [ ] **Wikilinks in Related sections are consistent across ALL profile files** — same format for BOK links, same format for cross-profile links
- [ ] Overview updated with "Project-Type Profiles" section and comparison table
- [ ] Cross-links between profiles verified (each profile links to the other two)
