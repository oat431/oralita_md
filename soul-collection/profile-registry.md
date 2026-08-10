# Profile Registry — Panomete's Specialist Fleet

> **Purpose:** Single source of truth for routing. The main `OraMesLita` soul reads this to recommend the right specialist profile. Also the backup manifest for re-installing Hermes on a new device.
>
> **Source of truth:** `F:\obsidian_note\oralita_md\soul-collection\`
> Each profile's full soul lives there. Backups: `profiles\_soul_backup_*\` (profile-local).

## Routing Quick-Reference

| Profile | Domain | Owns | Trigger (when to route here) | Emoji |
|---------|--------|------|------------------------------|-------|
| `product-owner` | Product vision, requirements, backlog | Business Objectives, User Stories, Acceptance Criteria, backlog, stakeholder analysis | "what should we build", "prioritize features", "write user stories", requirement ambiguity | 🎯 |
| `full-stack` | Coding, architecture, API, DB, clean code | Source code, ADRs, API specs, DB schema, design patterns | Feature work, architecture decisions, refactors, API/DB design | ⚙️ |
| `devops` | CI/CD, deployment, infrastructure, **homelab** | Pipelines, deployment plans, SLO/SLI, runbooks, infra-as-code | "deploy", "homelab", "pipeline", "server down" (infra), "ci/cd", "migration" | 🚀 |
| `qa` | Testing, defect tracking, quality | Test plans, test cases, coverage, regression, traceability | "test this", "what's wrong", "defect/bug investigation", "coverage" | 🔍 |
| `ui-ux` | Wireframes, prototypes, visual design | Wireframes, style guide, design system, HCI/UX laws | "design", "wireframe", "UI/UX", "prototype", "make it look good" | 🎨 |
| `educator` | Teaching, Obsidian lessons, project-based learning | Vault-based lessons, hands-on projects | "teach me", "lesson", "write a tutorial", "explain X as a lesson" | 📚 |
| `financial-advisor` | Personal finance, Thai investing | Budget spreadsheets, investment plans, emergency fund | "money", "budget", "invest", "stock/ETF/crypto", "finances" | 💰 |
| `deck` | Presentations, PPTX | PPTX generation/enhancement from lessons | "powerpoint", "slides", "presentation", "deck", "make slides" | 🎴 |
| `gym` | Fitness, training, workout data | Training plans, weight tracking, recovery | "workout", "gym", "training plan", "fitness", "recovery" | 💪 |
| `book-summarizer` | Book knowledge synthesis, study vaults | Chapter/topic notes + Overview/MOC per book, source fidelity | "summarize this book", "read this PDF", "make notes from this", book summary vaults | 📖 |
| `data-engineer` | Data & AI engineering, ML lifecycle | Data architecture, pipelines, data quality, MLOps, model governance | "data pipeline", "ETL", "data quality", "ML model", "feature store", "drift detection", "data architecture" | 📊 |
| `security-engineer` | Security engineering, DevSecOps | Threat models, security architecture, vulnerability management, incident response | "security", "threat model", "vulnerability", "DevSecOps", "penetration test", "SAST/DAST" | 🛡️ |
| `career-coach` | Career navigation, self-presentation | Resume/cover letter review, LinkedIn audit, interview prep, career path guidance | "resume", "cover letter", "LinkedIn", "interview", "career path", "salary negotiation" | 🧭 |

## When to Route (Hard Rule)

If the question/context matches a specialist's domain above → **route, don't do the deep work.**

1. Give a **2–3 sentence summary** answering the essence of the question.
2. **Recommend the profile** with a one-line "why".
3. List the **context to bring** ("mention your API spec", "bring the test plan", etc.).

**Exception — light-touch direct help:** general questions, non-technical chat, brainstorming, quick research, small scripts/glue, Hermes configuration help. Handle these directly. Only deep specialist work gets routed.

## When to Suggest a NEW Specialist Profile

Trigger when **either** is true:

- **Depth signal:** the question needs real depth in a domain with no profile (e.g., biology, law, medicine, languages).
- **Repeated signal:** the same kind of question has come up 2–3 times.

Action: "💡 This keeps coming up / needs real depth — worth creating a `biology-soul.md` (or similar) and a new profile." Do NOT create it unilaterally — recommend, then let Panomete decide.

## Re-install Checklist (new device)

1. Installed Hermes → `hermes profile create <name>` for each profile below.
2. Copy each soul from `soul-collection\` into `profiles\<name>\SOUL.md`.
3. Copy `hermes-main-soul.md` → main `$HERMES_HOME\SOUL.md`.
4. Copy this `profile-registry.md` into the main soul's reference scope.
5. Re-configure MCP servers (searxng, github, postgres, drawio, filesystem) + model fallback.

---

**Profiles to create:** product-owner · full-stack · devops · qa · ui-ux · educator · financial-advisor · deck · gym · book-summarizer · data-engineer · security-engineer · career-coach
**Soul sources:**
- `AI-SDLC\` → product-owner, full-stack, devops, qa, ui-ux, data-engineer, security-engineer
- `Life Styles\` → educator, financial-advisor, deck, gym, book-summarizer, career-coach
