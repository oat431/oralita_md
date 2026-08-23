---
date: 2026-08-23
tags: [writing, template, quick-note, th-en]
---

# Quick Note Template (TH/EN)

> Master template for fast capture. Copy **one block** into a new note — total fill time under 30 seconds. A quick note's job is to *not lose the thought*; perfection comes later or never.

## Rules That Keep Quick Notes Useful

1. **Title = words future-you will search** — never `note1`, `misc`, `asdf`
2. **One note = one thought** — two ideas = two notes
3. **Tag intent at capture** — `#idea` `#task` `#link` `#quote` `#log`
4. **Mark the follow-up** — 🔁 line says where this should end up, or "none"
5. **Triage weekly** — promote to a real note / do the task / delete. Notes that skip triage become a graveyard (see: the old Quick Note folder, dissolved 2026-08-22 into career/projects/personal/hermes).

## EN Version

```markdown
---
date: YYYY-MM-DD
tags: [quick-note, idea]
---

# <Searchable Title — keywords you'd grep for>

<The thought. 1–5 lines, incomplete sentences welcome.>

🔁 Follow-up: <none | move to writing/review/ | research X | add to project Y>
```

**Example**

```markdown
---
date: 2026-08-23
tags: [quick-note, link]
---

# Obsidian LiveSync conflict resolution strategy

Reddit thread says: stop sync, keep newest mtime, resync. Try next time
the tablet and PC diverge. Thread URL saved in browser bookmarks "livesync".

🔁 Follow-up: test on dummy vault, then update home-lab/obsidian-livesync notes
```

## TH Version

```markdown
---
date: YYYY-MM-DD
tags: [quick-note, idea]
---

# <ชื่อที่ค้นหาเจอ — ใส่คำค้นหาสำคัญ>

<ความคิด 1–5 บรรทัด เขียนสบาย ๆ ไม่ต้องประโยคสมบูรณ์>

🔁 ตามต่อ: <ไม่มี | ย้ายไป writing/review/ | หาข้อมูล X | เพิ่มในโปรเจกต์ Y>
```

**ตัวอย่าง**

```markdown
---
date: 2026-08-23
tags: [quick-note, idea]
---

# แผนซ้อมวิ่งควบคุมจังหวะหายใจ

ลอง cadence breathing 2:2 ตอนเทรดกลาง แต่ถ้าหอบเกิน switch เป็น 3:3
อ้างอิงโซน HR จาก [[smart-watch-settings]]

🔁 ตามต่อ: ลองพฤหัสนี้ → ถ้า work เพิ่มใน run-walk-log.md
```

## Micro Version (no file — chat apps, sticky notes, phone)

```
YYYY-MM-DD | <topic>: <thought> | 🔁<follow-up or ->
2026-08-23 | docker network: host mode skips port mapping entirely | 🔁add to homelab cheatsheet
```

## Language Switching Rule (TH/EN)

Mix freely **inside** the note — Thai body with English technical terms is normal and correct. The one place discipline matters:

- **Title/tags must carry the keywords you'd search in EITHER language.** A note titled only `เรื่องการ deploy` is invisible when future-you greps "deployment"; only `docker networking` is invisible when you think in Thai. Put both languages' key terms in the title or first line.

⚠️ **Thai Speaker Trap:** never translate technical terms in notes (`การกระจายตัว` for cache, `โดเคอร์` for Docker) — translated terms break search against official docs and code. Thai prose, English terminology.

⚠️ **English Speaker Trap:** don't drop Thai particles/politeness in shared notes out of habit — tone leaks. Scratch notes for yourself can be bare; anything pasted into a team doc needs its register restored.

## Triage Checklist (weekly, 5 minutes)

```
For each quick note older than 7 days:
□ Still interesting?  NO → delete (deleting is success, not failure)
□ It grew up?         → promote: rewrite as proper note in its home folder
□ It's a task?        → move to your task system, then delete the note
□ Still raw?          → keep, but it now owes you an answer next week
```

## Related

- Practice areas: `writing/review/` `writing/short_story/` `writing/wishing/` — promoted notes land there
- Knowledge layer: [[00-Writing-Types]]
