# Memory Cleanup: Worked Example

From session 2026-06-29 with Panomete (default profile).

## Before

| Store | Usage | Issue |
|-------|-------|-------|
| Memory | 81% (1,793/2,200) | Near limit, procedural entries, stale counts |
| User Profile | 74% (1,024/1,375) | Duplication with memory, verbose structure |

### Entries removed (procedural, don't belong in memory)

1. **"Task Management Rules"** — _"...tasks should be created with clear titles, concise descriptions..."_ → procedural, belongs in SOUL.md
2. **"Analysis Patterns"** — _"...pull data locally when user asks...skip accounting of alternatives unless asked..."_ → procedural, belongs in SOUL.md

### Entries consolidated (duplicated across memory + user profile)

3. **Obsidian vaults** — had stale completion counts: _"Math (12), English Skill (27), HCI/UI/UX (29), Design Patterns (23), Microservices (19), API Design (10)"_ → collapsed to just path + pattern since Obsidian is source of truth
4. **Homelab URL** — duplicated in both stores → kept in memory only, trimmed from user profile
5. **Security tiers** — verbose data-tier listing → tightened to essentials

## After

| Store | Usage | Freed |
|-------|-------|-------|
| Memory | 44% (973/2,200) | 820 chars |
| User Profile | 47% (647/1,375) | 377 chars |

## Operations used

Single atomic batch via `memory(operations=[...])`:

```json
[
  {"action": "remove", "old_text": "Task Management Rules"},
  {"action": "remove", "old_text": "Analysis Patterns: Pull data locally"},
  {"action": "replace", "old_text": "Obsidian vaults at F:\\projects\\orlita_md\\...", "content": "Obsidian vaults: F:\\projects\\orlita_md\\ — numbered folders + files. Prefers Mermaid."},
  {"action": "replace", "old_text": "Security: PII redaction active for emails...", "content": "Security: PII redaction active. Never share credentials unless explicitly asked."}
]
```

Same pattern applied to user profile target.

## Key takeaway

When Obsidian (or any external system) is the source of truth, memory should hold **path + pattern** — not current completion state. Completion counts rot within days.
