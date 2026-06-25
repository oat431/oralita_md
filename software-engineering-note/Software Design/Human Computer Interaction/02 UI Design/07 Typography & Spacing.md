# 07 Typography & Spacing

Typography is 90% of web design. Get the fonts, weights, sizes, and spacing right and everything else falls into place. Get them wrong and no amount of color or animation saves you.

---

## Font Weight

Weight creates hierarchy without changing size or color.

```
Light (300)    — The quick brown fox
Regular (400)  — The quick brown fox
Medium (500)   — The quick brown fox
Semibold (600) — The quick brown fox
Bold (700)     — The quick brown fox
```

### Rules

| Rule | Why |
|------|-----|
| **2–3 weights max** per design | Regular + Bold is enough for most sites. Regular + Medium + Bold for content-heavy sites |
| **Body text = Regular (400)** | Medium or Bold body text is exhausting to read |
| **Headings = Bold/Semibold (600–700)** | Creates clear separation from body |
| **Never use Light (300) for body text** | Too thin — hard to read, especially on low-res screens |

---

## Font Size

| Element | Recommended Size | Notes |
|---------|:---------------:|-------|
| Body text | **16px minimum** | iOS Safari zooms on inputs < 16px — never go smaller |
| Small/captions | 12–14px | Only for secondary info |
| H3 | 18–24px | |
| H2 | 24–32px | |
| H1 | 32–48px | |
| Hero text | 48–72px | Use sparingly |

### Large Text = Better Readability

| ❌ | ✅ |
|----|-----|
| Body text at 14px — looks dense and intimidating | Body text at 16–18px — inviting and readable |
| Line length: 100+ characters | Line length: 50–75 characters (ideal for reading) |

---

## Line Height

Space between lines of text. Too tight = claustrophobic. Too loose = disconnected.

| Element | Recommended Line Height |
|---------|:----------------------:|
| Body text | **1.5–1.75** |
| Headings | **1.2–1.3** |
| Code blocks | **1.5** |
| Small/captions | **1.4** |

```
line-height: 1.0  ← Too tight. Lines crash into each other.
line-height: 1.0  ← Hard to track which line you're on.

line-height: 1.6  ← Comfortable. Each line has breathing room.
line-height: 1.6  ← Easy to scan. The eye flows naturally.
```

---

## Letter Spacing

| Element | Recommendation |
|---------|---------------|
| Body text | **0** (default) — never add letter-spacing to body |
| Headings | **-0.5px to -1px** — tightens large text, looks more professional |
| All-caps text | **+1px to +3px** — all-caps needs breathing room to be legible |
| Code | **0** (monospace already has natural spacing) |

---

## Putting It All Together

```
❌ Amateur Typography:
  Body: 14px, line-height: 1.2, letter-spacing: 0
  Headings: same weight as body, line-height: 1.2
  → Dense, hard to read, no hierarchy

✅ Professional Typography:
  Body: 16px, line-height: 1.6, font-weight: 400
  H3: 20px, font-weight: 600, letter-spacing: -0.5px
  H2: 28px, font-weight: 700
  H1: 40px, font-weight: 700, letter-spacing: -1px
  → Clear hierarchy, inviting to read
```

---

## Sources

- *Refactoring UI* by Adam Wathan & Steve Schoger
- *Better Web Typography* by Matej Latin
