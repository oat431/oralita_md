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

# Clone config only (keeps provider setup, fresh memory/skills)
hermes profile create <name> --clone

# Clone everything (identical copy — rarely needed)
hermes profile create <name> --clone-all
```

**Recommendation:** use `--clone` for cross-domain profiles. It copies your API keys and provider config so you can chat immediately, but leaves memory and skills clean. Full `--clone-all` brings over MCP servers and skills you probably don't need.

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
