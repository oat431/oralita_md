# SOUL.md Adaptation: OpenClaw → Hermes

Worked example from adapting `miguelsalva/openclaw-personal-trainer-templates` for a Hermes gym profile.

## Source

```
https://raw.githubusercontent.com/miguelsalva/openclaw-personal-trainer-templates/master/workspace/SOUL.md
```

## Mapping Table

| OpenClaw concept | Hermes equivalent | Why |
|---|---|---|
| `~/.openclaw/state/coach/` file reads | `memory` tool | Hermes auto-injects memory entries into every session |
| `memory/YYYY-MM-DD.md` daily journal | `memory` tool + `session_search` | No file journaling needed — memory persists, session_search recalls past conversations |
| `MEMORY.md` long-term storage | Durable memory entries | Same persistence, tool-based instead of file-based |
| "I look in the files" | "Check Hermes memory, check Obsidian vault" | Agent shouldn't reference non-existent paths |
| No tool availability section | Added "Tools Available" section | Hermes agents need to know which tools they have |
| Generic "my human" | Named "Panomete" | Personalization based on user profile |

## Sections Added (Hermes-specific)

These don't exist in OpenClaw SOULs but are standard in Hermes:

1. **Tools Available** — `memory`, `web`, `file`, `terminal`, `session_search`, `clarify`, `todo`
2. **Memory & Continuity** — explains memory tool persistence model instead of file-based journaling
3. **Self-update footer** — Hermes convention: update SOUL.md and notify user when it evolves
4. **Profile-aware paths** — references `~/AppData/Local/hermes/profiles/gym/` not `~/.hermes/`

## Sections Preserved (domain-specific, transportable)

- Operating Philosophy ("active balance") and signal/action table — kept verbatim
- Boundaries — kept with Hermes-appropriate wording
- Vibe — data-driven, no cheerleading, concise
- Core Principles — rewritten but same spirit

## Sections Removed (OpenClaw-specific)

- `Continuity` section referencing `memory/YYYY-MM-DD.md` and `MEMORY.md` files → replaced with Hermes memory model
- Any paths starting with `~/.openclaw/`
- Agent-specific commands that don't exist in Hermes
