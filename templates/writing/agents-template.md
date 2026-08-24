---
date: 2026-08-24
tags: [writing, template, agents, hermes, project-context]
---

# AGENTS.md Template

> Master template for project context files — the "what this project needs" layer. Grounded in the official docs: [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) and [Which File Does What](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what). Sibling to the identity file: `soul-template.md`.
>
> **One-line shorthand:** SOUL.md is *who the agent is* (applies everywhere) · AGENTS.md is *what the project needs* (applies to this repo).

## What AGENTS.md Is / Is Not

| ✅ AGENTS.md — project facts & rules | ❌ SOUL.md — identity & voice (never project facts) |
|---|---|
| repo structure, architecture, conventions | tone, personality, communication style |
| commands, ports, paths, workflows | how direct or warm the agent is |
| "never edit migrations directly" | what to avoid stylistically |
| "tests go in `tests/`" | how to relate to uncertainty/disagreement |

**Rule:** *if it belongs to one project → AGENTS.md. If it should apply everywhere → SOUL.md.*

## How Hermes Discovers It (know your terrain)

**Priority chain — first match wins at startup:** `.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`. SOUL.md loads independently, always.

- **Inside a git repo:** Hermes merges the chain from git root down to your working directory — root first, deeper files later (so more specific guidance wins). Identical copies are deduplicated; each file gets a provenance header.
- **Outside a git repo:** only the working directory is checked — parents never leak in.
- **Subdirectories:** files are discovered *progressively* as the agent navigates (at most once per session), so `backend/AGENTS.md` loads when backend code is touched — no system-prompt bloat.
- **`AGENTS.override.md`:** your personal, usually-gitignored override that loads *instead of* the committed file — for personal tweaks without touching the repo.
- **Size cap:** 20,000 characters per file; longer gets head+tail truncated with a `[...truncated...]` marker. Prefer multiple files/skills over one giant file.
- **Security:** content passes a threat-pattern scanner; injection-like text becomes `[BLOCKED: ...]` placeholders (the rest of the file still loads).

## Skeleton (docs' example structure)

```markdown
# Project Context

<One paragraph: what this project is — stack, purpose, shape>

## Architecture
- <Major components and where they live>
- <Data flow / dependencies>

## Conventions
- <How to write code / docs for this repo — the non-negotiables>
- <Formatting, naming, test placement, tooling>

## Important Notes
- <Never-do items: migrations, secrets, ports, deploy steps>
```

**Filled example** (modeled on a homelab-style repo):

```markdown
# Project Context

Personal homelab setup documentation — Docker Compose services
on a Hetzner VPS, proxied through a single Traefik entry.

## Architecture
- Compose stacks live in `services/<name>/docker-compose.yml`
- Traefik in `infra/traefik/` handles TLS + routing for all domains
- Config secrets stay in `.env` files, never in compose directly

## Conventions
- Every service gets a README.md with ports and health-check commands
- Use `docker compose -f services/<name>/docker-compose.yml` explicitly
- Document changes with a dated changelog entry

## Important Notes
- Never commit `.env` files — they contain live tokens
- Port 443 is managed by Traefik only; services bind 127.0.0.1
- `make deploy` must be run from the repo root
```

## Checklist Before Dropping It In

- [ ] No personality/voice content (→ `soul-template.md` instead)
- [ ] Commands, ports, paths stated exactly — agents execute them literally
- [ ] Negative rules phrased as actions ("Never X" + what to do instead)
- [ ] Under 20,000 chars — if bigger, split into skills
- [ ] Root copy holds repo-wide rules; subdirectory copies hold scoped ones
- [ ] Tested: run Hermes in the repo, ask it to summarize the project rules

## Iteration Workflow

```
1. Write the one-paragraph Project Context first (what is this thing?)
2. Add Architecture — the map an agent needs before touching anything
3. Add Conventions — the rules you keep re-stating in reviews
4. Add Important Notes — the scars: what broke before
5. Run one real task in the repo; fix what the agent got wrong
```

The test is behavioral: the file is good when an agent asked "what's the architecture here?" answers from AGENTS.md, not from guessing.

## Troubleshooting (docs)

- **"Agent doesn't see my AGENTS.md"** → wrong directory (check cwd — outside a git repo, only the exact cwd is read) · filename case (`AGENTS.md`/`agents.md`) · another context file won the chain (`.hermes.md` beats it)
- **"It sees the file but ignores parts"** → conflicting instructions (deeper file wins in git-repo chains) · content truncated past 20K · text flagged by the security scanner
- **"My repo rules leak into other projects"** → you're not in a git repo (parents never checked — that's the feature, not a bug) · or the rules are actually global → move to SOUL.md
- **"I want my own rules without editing the repo file"** → `AGENTS.override.md` next to it, gitignore it

## Related

- Identity counterpart: [[soul-template]]
- Prompt craft: [[05-Prompt-Writing-Guide]]
- Map: [[00-Writing-Types]] — section 6
- Official docs: [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) · [Which File Does What](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what)
