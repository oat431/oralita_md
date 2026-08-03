---
name: hermes-profile-setup
description: "Create and configure Hermes profiles for separate use cases — fitness, finance, creative, research. Adapt SOUL.md from other agents (OpenClaw, Claude Code). Maintain memory across profiles."
version: 1.0.0
author: OraMesLita
license: MIT
metadata:
  hermes:
    triggers:
      - "create a profile for"
      - "new profile"
      - "separate context"
      - "gym profile"
      - "health profile"
      - "adapt SOUL"
      - "memory cleanup"
      - "memory is full"
      - "clean up memory"
    related_skills: [hermes-agent]
---

# Hermes Profile Setup & Maintenance

When to create a separate profile, how to adapt foreign agent SOUL templates, and how to keep memory lean across profiles.

## When to Create a Profile

Create a **new profile** when any of these are true:

- The use case is a **different domain** than your current profile (programming → fitness, fitness → finance)
- You want **isolated memory** — health data shouldn't mix with code review context
- You want a **different persona/SOUL** — fitness coach vs DevOps engineer
- You want **different tools/skills** — gym profile doesn't need GitHub MCP or PostgreSQL
- You want a **cheaper model** for lightweight Q&A (health advice doesn't need deepseek-v4-pro)

Stay in the **same profile** when:

- The task is the same domain with a different project (Python backend → React frontend)
- You want shared memory and conventions across work

## Creating a Profile

```bash
# Fresh profile (recommended for new domains)
hermes profile create <name>

# Clone config + .env + SOUL.md AND ALL skills + memory (identical setup, fresh sessions)
hermes profile create <name> --clone

# Clone everything via --clone-all (same as --clone; --clone already brings skills)
hermes profile create <name> --clone-all
```

**Recommendation:** use `--clone` for cross-domain profiles — it copies API keys, provider config, SOUL.md, *and all installed skills* (observed output: "Cloned config, .env, SOUL.md, and skills from default"). It does NOT leave skills clean. Only session history and memory start fresh. **A `--clone` profile inherits every skill from the source profile — plan to prune.** Trim irrelevant skill categories after creation (e.g. a book-summarizer profile does not need `gym`, `smart-home`, `mlops`, `slidev`) so the new profile doesn't waste context on foreign skills. `hermes tools` / skill pruning manage this per profile.

### Smoke-test a new profile immediately
The generated `<name>.bat` shortcut in `~/.local/bin` is not on the git-bash PATH (it just wraps `hermes -p <name>`). Verify the soul is live with a one-shot query instead:

```bash
hermes -p <name> chat -q "Answer in one sentence: what is your name and core role?"
```

The reply must reflect the new SOUL.md (e.g. the book-summarizer profile answers as "Libri, the Book Summarizer..."). A wrong identity means the soul didn't install where expected.

### Review-first gate for new souls (Panomete's rule)
Do NOT create the profile the moment a soul is drafted. When authoring a new fleet specialist:
1. Write the soul to `soul-collection/<DOMAIN>/<position>-soul.md` only.
2. Let Panomete review the soul file and explicitly approve it becoming a profile.
3. Only after approval: `hermes profile create <name> --clone`, copy the soul in, hash-sync, then update `profile-registry.md` + main soul routing table.
This review-first gate keeps drafts out of `$HERMES_HOME/profiles/` until they're approved — approved and live = reviewed.

After creation, the profile auto-generates a CLI shortcut:
```bash
<name> chat       # start a session
<name> setup      # configure model/keys
```

## Adapting SOUL.md from Other Agents

Other agent frameworks (OpenClaw, Claude Code, Codex) have SOUL.md or AGENTS.md templates online. The adaptation process:

### 1. Fetch the source
```bash
curl -sL "https://raw.githubusercontent.com/<user>/<repo>/<branch>/path/to/SOUL.md"
```

### 2. Map foreign concepts to Hermes equivalents

| Foreign (OpenClaw/Claude Code) | Hermes equivalent |
|---|---|
| `~/.openclaw/state/` file paths | `memory` tool for durable facts, `session_search` for past conversations |
| `memory/YYYY-MM-DD.md` daily journal | Hermes memory auto-injects every session — no manual journaling |
| `MEMORY.md` long-term file | Persistent memory entries survive across sessions |
| `CLAUDE.md` project context | `.hermes.md` or `AGENTS.md` in project root |
| Local file-based state | `memory` tool + Obsidian vault if applicable |

### 3. Add Hermes-specific sections

Every Hermes SOUL.md should include:
- **Tools Available** — list which Hermes tools the profile uses (`memory`, `web`, `file`, `todo`, `clarify`)
- **Memory & Continuity** — explain how memory persists (tool-based, not file-based)
- **Self-update footer** — standard "If this SOUL evolves, update it and notify the user"
- **Profile-aware paths** — reference the profile's own memory, not `~/.hermes/` global

### 4. Write to the profile path

```
~/AppData/Local/hermes/profiles/<name>/SOUL.md    (Windows)
~/.hermes/profiles/<name>/SOUL.md                 (macOS/Linux)
```

### 5. Trim tools for the domain

Don't load a gym profile with `terminal`, `github`, `docker` skills. The profile inherits the `cli` platform toolsets by default — suggest trimming via `hermes tools` in the new profile's shell.

## Authoring Original SOULs from Scratch

When the user wants a **new persona from their own domain** (not adapted from a foreign agent) — e.g. AI-SDLC role souls, life-style souls (educator, financial advisor, deck-builder) — use this workflow. It differs from adaptation: there's no source template, so the persona must be *grilled into existence* before writing.

### 1. Grill first, write after (most important rule)
Never invent a persona. Run the interview (via `grill-me` / `grill-with-docs`, or manually if the user is mid-conversation) to pin:
- **Who** the persona serves and their boundaries (e.g. "serves only me", "any audience")
- **Philosophy** — teaching style, risk stance, design taste
- **Deliverables** — what they produce and in what format (Obsidian md? PPTX? Excel formulas?)
- **Expertise level** — "graduate of which BOK" (see below)
- **Priority awareness** — 🔴/🟡/🟢 behavior like a real worker
- **Personality** — warmth/terseness, tone, direct vs encouraging

Push back on vague answers; each follow-up question makes the SOUL sharper. A "sharp specialist" beats a "blurry generalist" every time.

### 2. Naming & layout convention
- `[position]-soul.md` (e.g. `product-owner-soul.md`, `educator-soul.md`)
- Collection root with domain subfolders:
  ```
  soul-collection/<DOMAIN>/          e.g. soul-collection/AI-SDLC/
    <position>-soul.md
  ```
- One person wearing several hats = one soul per *role*, not one per person.

### 3. Anatomy (borrows the AI-SDLC template)
Core Principles → Identity (name/role/emoji/vibe/mission) → Knowledge Base (vault-grounded) → Core Techniques (applied, not named) → Owned Documents (🔴/🟡/🟢 with template paths + depth) → Handoff Protocol (outgoing/incoming) → Priority Protocol → Execution Style → Collaboration Rules → Quality Gates.

### 4. Ground each soul in the user's BOK vault
Each soul is a "graduate" of the BOK(s) that own its documents. The knowledge is **live**, so point at real vault paths, not titles:
- `body-of-knowledge/<BOK>/<chapter>.md` — the curriculum the soul reads
- `document-template/<category>/<doc>.md` — the templates the soul owns (with Heavy/Med/Light depth)
- `career-path/<NN>_<Role>/00_overview.md` — competence anchor
- `software-engineering-note/<KA>/` — deep domain notes

**Verify every referenced path resolves** after writing — stale template names are the #1 error. See `references/soul-authoring-vault-grounded.md` and run `scripts/verify_soul_refs.py`.

## Syncing Profiles to the Soul Collection

When the collection is updated (soul upgraded, persona changed) and the user wants existing profiles updated, sync each `$HERMES_HOME/profiles/<name>/SOUL.md` to its collection counterpart. Do NOT assume a profile is stale — verify first.

### 1. Find stale profiles with a hash diff
```bash
cd "$HERMES_HOME/profiles" && md5sum */SOUL.md
md5sum ~/soul-collection/<DOMAIN>/*.md
```
A profile is stale when its `SOUL.md` hash ≠ the matching collection file's hash. Matching by content hash, not size or date — that's how you catch "same-ish but different" souls. Life-style souls that weren't touched stay in sync automatically; only the re-authored ones go stale.

### 2. Name-mapping pitfall
Profile dir name ≠ collection filename. Map manually:
```
product-owner      ↔ product-owner-soul.md
full-stack         ↔ full-stack-developer-soul.md        (NOT full-stack-soul.md)
devops             ↔ devops-engineer-soul.md
qa                 ↔ qa-engineer-soul.md
ui-ux              ↔ ui-ux-designer-soul.md
```
Writing a verification loop that guesses `<profile>-soul.md` will report false "MISMATCH" on every profile whose collection name has a middle token. Use an explicit `declare -A` map instead.

### 3. Back up before overwriting
Old souls are not recoverable once overwritten (the collection file was already replaced). Stash them first:
```bash
BK="$HERMES_HOME/profiles/_soul_backup_$(date +%Y%m%d)" && mkdir -p "$BK"
for d in <stale-profiles>; do cp "$d/SOUL.md" "$BK/${d}-SOUL.md.bak"; done
```

### 4. Copy, then re-verify
```bash
cp <collection>/<file>-soul.md <profile>/SOUL.md
# re-run md5sum: profile hash must now equal collection hash (byte-identical)
```

### 5. Tell the user the running-session caveat
Already-running sessions keep the old soul (Hermes never mutates a live system prompt). New sessions pick up the new SOUL.md. Recommend opening a fresh session per profile to see the change.

### 6. Remember the main soul
The default/main profile's SOUL lives at `$HERMES_HOME/SOUL.md` (not in `profiles/`). Back it up to the collection root (e.g. `soul-collection/hermes-main-soul.md`) when iterating on it — it's the file that governs the base agent.

## Routing-Generalist Main Soul (multi-profile fleets)

Once the user has specialist profiles, the **main soul's job changes**: it stops being another specialist and becomes the *router/operator* — the one who "knows lots of things AND knows lots of people." This pattern (full detail + worked example: `references/router-generalist-main-soul.md`):

- **Hard handoff protocol** — when a question matches a specialist domain: (1) 2-3 sentence summary, (2) direct routing line ("This is a `full-stack` task."), (3) context to bring. Be straight, not wishy-washy.
- **"What I Do / What I Route" split** — light work (chat, research, quick scripts, Hermes config, soul creation) done directly; deep work (code→full-stack, bugs→qa, design→ui-ux, homelab→devops, money→financial-advisor, lessons→educator, decks→deck) routed, never half-done.
- **New-specialist triggers** — depth signal (question needs real depth in a domain with no profile) or repeated signal (same kind of question 2-3×) → *recommend* creating a soul, never create unilaterally.
- **`profile-registry.md`** — a routing table (profile → domain → owns → trigger phrases → emoji) living in the soul-collection root. Single source of truth for routing AND the re-install manifest for a new device (profile list, soul sources, MCP servers).
- **Keep the old persona** when re-purposing: same name/emoji/vibe, changed role description + routing table. The user keeps their identity; the job changes.

### SOUL.md load semantics (verified in source)
SOUL.md is **auto-injected at conversation start** (the `--ignore-rules` flag: "Skip auto-injection of AGENTS.md, SOUL.md, .cursorrules, memory"). The system prompt is **byte-stable for the life of a conversation** — a live session keeps its old soul no matter what you edit. A **new conversation** picks up the new soul; **restarting the app only helps if it starts a fresh chat** (resuming an old session does nothing). Tell the user: open a new chat, don't just restart.

## Memory Maintenance

Memory fills up from procedural entries, stale stats, and duplication. Clean it periodically.

### Audit pattern

1. **Read current state:** check the memory and user profile percentages in the system prompt header
2. **Categorize entries:**
   - ✅ **Keep:** identity facts, preferences, paths, security rules
   - ❌ **Remove:** procedural rules (belong in SOUL.md or skills), stale completion stats, task logs
   - ⚠️ **Consolidate:** entries duplicated across memory + user profile
3. **Batch operations:** use `memory(operations=[...])` for atomic changes — never multiple single-operation calls
4. **Verify:** check new percentages after the batch completes

### What never belongs in memory

- Procedural rules ("always do X, never do Y") → SOUL.md or skill
- Task progress ("completed phase 3", "merged PR #42") → session_search
- Stale counts ("12 files done, 5 remaining") → they rot within days
- Environment-specific failures ("pip install failed") → fix the environment, don't memorialize the error

### What belongs in memory

- User identity, preferences, and style
- Persistent paths (Obsidian vaults, project roots)
- Security rules and boundaries
- Domain-specific context (homelab URL, tech stack)

### Cleaning stale entries

When Obsidian or another external system is the source of truth, memory should only hold the **path** and the **pattern** — not the current completion state. "Vault at F:\projects\orlita_md\, numbered folders" is durable. "Math (12 files), English (27 files)" is stale in a week.

## Configuration Audit for Specific Use Cases

When auditing a profile for a specific use case (e.g., programming):

### Priority order
1. **Safety nets:** fallback model (uncommented), checkpoints enabled, approval mode
2. **Cost:** model choice matches the domain (coding needs reasoning, health Q&A doesn't)
3. **Memory headroom:** under 60% is healthy, over 80% needs pruning
4. **Tools:** MCP servers and skills relevant to the domain
5. **UX:** streaming, cost display, reasoning effort tuned to the task

### Common misses
- Fallback model commented out → no automatic failover on 429/503
- `checkpoints.enabled: false` → no `/rollback` safety net during refactors
- `approvals.mode: manual` → excessive friction; `smart` uses LLM to auto-approve low-risk commands
- `reasoning_effort: medium` on coding profiles → bump to `high` for architecture decisions
- `terminal.timeout: 180` → too tight for docker builds or large test suites

## Pitfalls

- **Don't clone-all for cross-domain profiles.** GitHub MCP, PostgreSQL, and Docker skills in a fitness profile waste memory and confuse context.
- **Don't keep procedural rules in memory.** They get re-read as directives each session, creating self-imposed constraints. SOUL.md or skills are the right home.
- **Don't store completion stats in memory.** "Phase 3 done, 12 of 20 files" rots within days. Obsidian or session_search are better.
- **OpenClaw SOULs reference file paths that don't exist in Hermes.** Always map `~/.openclaw/state/` → `memory` tool, not literal file paths.
- **Profiles inherit API keys from the shell environment.** If `DEEPSEEK_API_KEY` is set in `.env`, the new profile picks it up. Only run `gym setup` if you want a different provider.
