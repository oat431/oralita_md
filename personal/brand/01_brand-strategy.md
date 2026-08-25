---
date: 2026-08-25
version: "1.0"
status: Locked
tags: [branding, strategy, positioning, panomete, locked]
---

# Brand Strategy — Panomete

> Phase 1 of [[00_brand-roadmap]]. **Status: LOCKED 2026-08-25.** This is a compressed strategy — not a full positioning exercise, because Panomete is a personal design system, not a funded product. Every value here exists because it drives a specific visual decision downstream in [[02_visual-identity]].

## 1. Audience

| Question | Answer |
| --- | --- |
| Who is it for? | **Myself (Sahachan / `flowero`).** A software engineer building personal projects and knowledge-base decks. Not a consumer audience. |
| What problem do we solve best? | **Eliminate second-guessing.** Every project under Panomete picks colors, type, and components without deliberation — the system is pre-decided. |
| Where do they meet the brand? | Homelab web dashboards (`*.panomete.com`), API docs, status pages, Obsidian knowledge-base decks, PowerPoint presentations. |

## 2. Competitor Visual Audit — Inspiration Anchor

No formal competitor audit was conducted (personal project, not a market entrant). Instead, a single inspiration source was chosen:

**daisyUI forest theme (v5.7.22)** — a dark, green-forward, understated dev-tool palette. Source values pulled directly from `daisyui@5/themes.css` CDN and converted to HEX/RGB/CMYK with WCAG verification. This is the locked color foundation.

| Direction observed | Why it fits |
| --- | --- |
| Dark primary surface | Dev tools and dashboards run dark; reduces eye strain for long sessions |
| Green-forward palette | "Forest" = calm, stable, organic — matches Technical/Confident/Understated personality |
| Semantic color system | daisyUI's token system (primary/secondary/accent/neutral/base + status colors) means components restyle instantly |
| Flat, no depth shadows | `--depth: 0` — clean, modern, not skeuomorphic |

## 3. Positioning Statement (locked)

```markdown
For a software engineer (myself) who builds personal projects and knowledge decks,
Panomete is the personal design system
that eliminates visual second-guessing.
Unlike ad-hoc per-project styling, every surface uses one locked token system.
```

## 4. Foundation Blocks (compressed)

| Block | Fill-in |
| --- | --- |
| **Mission** | Build a personal design system so every project ships with zero visual deliberation. |
| **Vision** | Every Panomete surface — dashboard, deck, doc — is instantly recognizable as mine. |
| **Values** | 1. Consistency over novelty 2. Technical precision 3. Understatement |
| **Promise** | Every time you see a Panomete surface, the colors, type, and spacing are already decided. |

## 5. Personality & Emotion (locked)

```markdown
Our brand is: Technical / Confident / Understated

If our brand were a person, they would:
- Speak like: a senior engineer — short, direct, no hype
- Dress like: dark, clean, functional — nothing decorative
- Never be caught: using gradients, drop shadows, or decorative imagery

Emotions we want people to feel (1): Confidence — "this person knows what they're doing"
```

**Slider calibration:**

```
Playful  ————————●—— Serious
Luxury   ————————●—— Mass
Bold     ——————●———— Quiet
Classic  ————●—————— Edgy
```

## 6. Voice & Tone

| Do say | Don't say |
| --- | --- |
| short, direct sentences | corporate filler ("synergy", "leverage") |
| active verbs | hype without proof |
| technical terms where precise | decorative adjectives |
| "deploy", "configure", "verify" | "unleash", "empower", "transform" |

Tone shifts by context, voice never does: same voice in a status page as in a presentation deck.

---

## Decision Log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-25 | Scope: personal design system, not a full brand | User explicitly stated "not a brand at all, just want a design system" |
| 2026-08-25 | daisyUI forest theme as color foundation | User chose it directly; provides a complete, tested semantic token system |
| 2026-08-25 | Sarabun as body/heading typeface | User chose it; Thai-optimized, covers both scripts, free on Google Fonts |
| 2026-08-25 | JetBrains Mono as monospace | User chose it; current dev-tool standard |
| 2026-08-25 | Wordmark only, no icon mark | User chose; honest scope — a weak mark is worse than no mark |
| 2026-08-25 | Animal submarks for each project | User chose; leverages existing code-name system |

---

**Gate:** ✅ Strategy locked 2026-08-25. Proceed to [[02_visual-identity]].
