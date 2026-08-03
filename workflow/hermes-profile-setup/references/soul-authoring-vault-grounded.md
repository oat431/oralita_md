# Authoring Vault-Grounded SOULs — Worked Reference

Session detail from building/upgrading the AI-SDLC + Life Styles soul collections
(root: `F:\obsidian_note\oralita_md\soul-collection\`).

## The grill-me session pattern (before writing)

For every persona, run a Q&A loop. Round 1 pins identity; Round 2 pushes depth;
Round 3 closes behavior questions. Examples that produced sharper souls:

- **Educator**: teaches any subject from Obsidian vault as *reference* (not curriculum),
  project-based (mini-projects + capstone), Obsidian md output only, no formal
  assessment (user checks learners), asks audience level each lesson, English, technical
  (Mermaid/YAML/wikilinks). Personality: professional-but-direct.
- **Financial Advisor**: serves one client (Panomete), personal finance, Thai context
  (SET/RMF/SSF), **enforced sequence** (track expenses → emergency fund → invest),
  Excel formula output (not files), warm personality, behavior-fix mindset (user never
  tracked expenses, ~12k THB/mo surplus). Never discusses investing until emergency
  fund exists.
- **Deck**: creates + enhances PPTX, one concept per slide, data-heavy-but-minimalist,
  content/structure + light design (not VBA/macros), takes Educator's vault lessons the
  user manually selects. Warm personality.

Key takeaway: the SOUL file is written *after* these answers exist. The answers ARE
the content.

## Anatomy of a vault-grounded soul

1. **Core Principles** — 5-6 beliefs, each tied to a technique from their BOK.
2. **Identity** — Name, Role (exact job title + scope), Emoji, Vibe, Mission.
3. **Knowledge Base (Vault-Grounded)** — "I read these live" curriculum table:
   - BOK chapters: `body-of-knowledge/SWEBOK/05_Software_Testing.md` etc.
   - Domain notes: `software-engineering-note/04_Software_Construction/API/`
   - Career anchor: `career-path/07_SRE_and_Platform_Engineer/00_overview.md`
   - Templates owned: `document-template/16_Deployment_and_Operations/...`
4. **Core Techniques (Applied, Not Just Named)** — name the technique AND show the
   application. PO "uses the Perfect Technology Filter"; QA "respects the oracle
   problem"; DevOps "runs error budgets".
5. **Owned Documents** — 🔴 Must Have / 🟡 Nice / 🟢 Optional tables, each row with
   template path + depth (Heavy/Med/Light).
6. **Handoff Protocol** — outgoing (produces→consumers) and incoming (receives→from).
7. **Priority Protocol** — how the soul triages, matching 🔴→🟢 like a real worker.
8. **Execution Style** — per-document how-to.
9. **Collaboration Rules** — with other souls + the user.
10. **Quality Gates** — checkbox list before releasing a document.

## Key BOK → role mapping (observed in this vault)

- PO/Founder → BABOK v3 (Strategy Analysis), PMBOK v8, SWEBOK Requirements
- Full-Stack Dev → SWEBOK Arch/Design/Construction, Clean Architecture, Design Patterns
- DevOps → SWEBOK Operations (new KA), SRE practice, CyBOK
- QA → SWEBOK Testing (largest KA), ISO 25010/29119
- UI/UX → HCI notes (Gestalt, UX Laws), Nielsen heuristics, WCAG 2.1

## Upgrade pattern (existing souls → vault-grounded)

When a soul was built from a *profile summary* and the full knowledge base later grew,
upgrade by re-grounding, not rewriting:
1. Replace one-line BOK titles with real chapter paths + applied techniques.
2. Expand Owned Documents from the thin profile set to the full template catalog
   (with depth labels).
3. Add the vault path to the actual template category per soul role.
4. Verify all paths resolve (below).

## Path-verification pitfalls

- Template filenames drift: `Wireframes.md` is actually `Wireframes-Low-fi.md`
  (and `Wireframes-Mid-fi.md` exists too). `Defect-Log-Metrics.md` lives under
  `18_Quality_Assurance/`, not `13_Testing_and_Verification/`.
- The MCP `filesystem` tools may not be loaded in a session — fall back to
  `terminal` + Python, or `search_files`.
- When grepping backslash paths through bash, escaping mangles the pattern — use a
  Python script (see `scripts/verify_soul_refs.py`) instead of `grep -o`.

## Effort lesson

The refresh was fast *because* the skeletons were solid. First-time authoring is
deliberate (grill + write); upgrade work is mechanical (re-ground + verify).
