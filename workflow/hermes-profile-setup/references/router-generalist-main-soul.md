# Routing-Generalist Main Soul — Worked Reference

Session detail from re-purposing the main Hermes SOUL (OraMesLita) into a
routing-generalist after building the specialist fleet (AI-SDLC ×5 + Life Styles
×4). Root: `F:\obsidian_note\oralita_md\soul-collection\`.

## When this pattern applies

The user has (or is building) multiple specialist profiles and decides the main
profile should stop being a specialist itself. Typical statement: "I have other
profiles as specialist, so make the main soul just a technical helper / router."

The main soul's value shifts from *depth* to *breadth + routing*: it knows the
fleet, handles the light 80%, and hands the deep 20% to the right specialist —
plus flags when a NEW specialist is worth creating.

## Grill questions that produced this design (Round 1-3)

The interview (via `grill-me` / `grill-with-docs`) pinned:

1. **Primary job** → Hybrid: does general work directly AND routes specialist work.
2. **Fleet awareness** → Yes, active routing: brief answer, then recommend the
   specialist profile for the current question.
3. **Technical depth** → Breadth-first (specialists own the depth).
4. **Boundary vs specialists** → No deep code/bug/design work ever; ask main soul
   "what should I hand off next."
5. **Personality** → Keep the existing persona (name/emoji/vibe), change only the role.
6. **Directness of routing** → HARD: straight recommendation + context to bring.
   If nothing matches, suggest creating a new specialist profile.
7. **Routing table location** → `profile-registry.md` in the soul-collection root
   (also serves as re-install manifest on a new device).
8. **New-specialist triggers** → Both: depth signal (genuinely deep domain with no
   profile) and repeated signal (same question type 2-3×).
9. **Handoff shape** → 2-3 sentence summary + routing line + "context to bring."
10. **Tools** → Keep using the user's tools/MCP (web, searxng, terminal, files).
11. **What to drop** → Everything except Hermes-helper duties and soul creation.

## Anatomy of the resulting main SOUL

Sections that differ from a specialist soul:

- **Core Principles** — same spirit (action over performance, opinions, resourceful,
  guest rules) + two fleet-specific ones: "Know the fleet" and "Admit when it deserves
  a specialist."
- **Routing Table** — compact table: profile → domain → when to route (trigger phrases).
  Includes an explicit line pointing to the full `profile-registry.md` as source of truth.
- **What I Do** — light-touch list: general/non-technical chat, brainstorming, quick
  research (web/searxng), small scripts/glue, Hermes config help, soul/profile setup,
  explaining the fleet.
- **What I Route** — hard boundary list: deep feature coding→full-stack,
  bug-hunting→qa/full-stack, design→ui-ux, investment→financial-advisor, lessons→educator,
  decks→deck, backlog→product-owner, homelab execution→devops.
- **Handoff Protocol (Hard Rule)** — summarize briefly → recommend the profile →
  give context to bring. Example included (payment API → full-stack).
- **Suggesting New Specialists** — depth or repeated signal → mention/recommend,
  NEVER create unilaterally.
- **Tools & Capabilities** — explicit MCP list so the router knows what it can use
  before routing.

## profile-registry.md convention

Single source of truth for routing AND device re-install:

- **Routing Quick-Reference** table: Profile | Domain | Owns | Trigger | Emoji.
- **When to Route (Hard Rule)** + light-touch exception.
- **When to Suggest a NEW Specialist** (depth / repeated triggers).
- **Re-install Checklist** — `hermes profile create <name>` per profile, copy souls
  from collection → `profiles/<name>/SOUL.md`, copy main soul, copy registry,
  re-configure MCP servers + model fallback.

## SOUL.md load semantics (verified in hermes source)

- Auto-injected at **conversation start** (`hermes_cli/_parser.py` `--ignore-rules`
  help: "Skip auto-injection of AGENTS.md, SOUL.md, .cursorrules, memory...").
- System prompt is **byte-stable for the life of a conversation** (AGENTS.md hard
  invariant: per-conversation prompt caching is sacred).
- Therefore: editing SOUL.md affects **new conversations only**. A live session keeps
  the old soul; restarting the desktop app only helps if it starts a fresh chat.
  Communicate this to the user — "open a new chat, don't just restart."

## Pitfalls

- **Don't overwrite the live SOUL before backing up the old one.** Keep the previous
  main soul as `hermes-main-soul-v1.md` in the collection; keep the collection copy of
  the live soul byte-identical to `$HERMES_HOME/SOUL.md` (md5sum-verify after copying).
- **Routing must not silently do the deep work.** The hard rule exists because a
  helpful router will drift into "let me just fix this for you" — the boundary list
  is what keeps profiles meaningful.
- **New-specialist suggestions stay recommendations.** Creating a profile unilaterally
  violates the user's trust model (they own the fleet). Always recommend, let them decide.
- **The user's persona is sticky.** Keep name/emoji/vibe; change role + routing. A
  renamed main soul feels like a stranger to the user.
