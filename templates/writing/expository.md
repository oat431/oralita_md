---
date: 2026-08-24
tags: [writing, template, expository, technical-writing]
---

# Expository Templates

> Fill-in masters per form. Copy ONE block into place. Method & failure modes: [[06-Expository-Writing-Guide]]. Name live files `YYYYMMDD-<slug>.md`.
>
> **Language-neutral by design:** lead-with-the-point structure carries the explaining job in any language.

## 📘 Technical Documentation / Runbook

```markdown
---
date: YYYY-MM-DD
tags: [expository, technical-doc]
audience: 
---

# <Task Title>

**Prerequisites:** <access, tools, versions needed before starting>
**Time to complete:** ~X min

## Steps
1. <imperative verb — "Run", "Open", "Set"> `<command/action>`
   Expected output: <what success looks like>
2. ...

## Verification
<how to confirm it worked>

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
```

**Filled example**

```markdown
# Rotate the home-lab TLS cert

**Prerequisites:** SSH access to `caddy-01`, sudo rights
**Time to complete:** ~5 min

## Steps
1. Run `sudo certbot renew --cert-name homelab`
   Expected output: "Congratulations, all renewals succeeded"
2. Run `sudo systemctl reload caddy`
   Expected output: no error, exit code 0

## Verification
`curl -vI https://homelab.local 2>&1 | grep expire` shows a date 90 days out.

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| "rate limited" | too many renewals this week | wait 7 days, or use staging cert |
```

## 📰 Journalism / Incident Report (inverted pyramid)

```markdown
---
date: YYYY-MM-DD
tags: [expository, report]
---

# <Headline: the conclusion, in one line>

<LEDE: who/what/when/where/why/how in 1–2 sentences — the whole story in miniature>

## Key details
<the 3–5 facts that matter most, most important first>

## Background
<context a reader needs but could skip>

## Sources
<attribution for every claim above>
```

## ✍️ Explainer / Blog Post

```markdown
---
date: YYYY-MM-DD
tags: [expository, blog]
---

# <The reader's actual question, as the title>

<Open by restating their question — confirm you understood it>

## Short answer
<the answer in 1–3 sentences, for skimmers>

## Why / how it works
<the explanation — analogy first, then mechanism>

## Example
<one concrete worked example>

## Edge cases / gotchas
<nuance that would mislead if stated first>
```

## 🎓 Academic / Whitepaper Section

```markdown
---
date: YYYY-MM-DD
tags: [expository, academic]
---

# <Working title>

**Thesis:** <the one claim this piece supports>

## Context / prior work
<what's already known, cited>

## Method
<how you investigated / built the case>

## Findings
<what you found — precision over style>

## Limitations
<what this does NOT show — state scope honestly>
```

## Related

- Method & failure modes: [[06-Expository-Writing-Guide]]
- Reviews open with an expository "what it is" section before the verdict: [[01-Review-Writing-Guide]]
