---
name: pptx-deck-series
description: "Build multi-deck presentation series from structured content (vaults, outlines, docs). Folder-per-project, consistent naming, per-deck build scripts, shared design system."
triggers:
  - "create presentation series"
  - "build slides from vault"
  - "multiple decks"
  - "chapter slides"
  - "overview + topic decks"
---

# PPTX Deck Series Builder

Build a set of related .pptx decks from structured source content (Obsidian vaults, markdown outlines, documentation). Each deck gets its own build script; the series shares a design system.

## When to Use

- User wants multiple related presentations from a content vault or outline
- Building course materials with an overview deck + per-chapter decks
- Converting structured markdown (with sections, tables, lists) into slides

## Folder Structure

```
F:\projects\<project>/
├── <Topic A>/
│   ├── build_overview.js      ← CH00 deck
│   ├── build_ch01.js          ← per-chapter builds
│   ├── CH00_Overview.pptx
│   ├── CH01_<Name>.pptx
│   └── node_modules/          ← local install (one per folder)
├── <Topic B>/
│   ├── build_overview.js
│   ├── CH00_Overview.pptx
│   └── node_modules/
```

**Naming convention:** `CH00_Overview.pptx`, `CH01_<TopicName>.pptx`, etc. Match the vault's chapter numbering.

## Template

See [templates/build_template.js](templates/build_template.js) for a ready-to-copy skeleton with all helpers (darkSlide, lightSlide, addCard, mkShadow) and the standard color/font system.

## Setup Per Folder

```bash
mkdir -p "F:/projects/<project>/<folder>"
cd "F:/projects/<project>/<folder>"
npm init -y > /dev/null 2>&1
npm install pptxgenjs
```

Each subfolder needs its own `node_modules` — node resolves upward, but one per topic folder keeps things clean and avoids stale cross-references.

## Workflow

### 1. Read Source Content

Read the vault's overview/index file to understand structure. Then read each chapter's content files for detail.

### 2. Design System (one per series, copy across decks)

Define a consistent palette + helper functions at the top of each build script. Each topic in a series should use a **different palette** so decks are visually distinct.

```javascript
// Pick palette based on topic domain
const C = {
  darkBg: "0D1117", primary: "238636", secondary: "2EA043", accent: "3FB950",
  lightBg: "F0F7F0", white: "FFFFFF", dark: "1B1F23", muted: "656D76",
  cardBg: "FFFFFF", tableBg: "DAFBE1", tableHead: "238636",
};
```

**Palette mapping (proven):**
- Language/Communication → Teal Trust (`#028090`)
- Math/Science → Indigo (`#3730A3`)
- Programming/Code → GitHub Green (`#238636`)

### 3. Reusable Helpers (paste into each build script)

```javascript
const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

function darkSlide(title, sub) {
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
  s.addText(title, { x: 0.8, y: 1.5, w: 8.4, h: 1.2, fontSize: 40, fontFace: HF, color: C.white, bold: true });
  if (sub) s.addText(sub, { x: 0.8, y: 2.8, w: 8.4, h: 0.8, fontSize: 18, fontFace: BF, color: C.accent });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.4, w: 10, h: 0.225, fill: { color: C.accent } });
  return s;
}

function lightSlide(title) {
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.08, h: 5.625, fill: { color: C.primary } });
  s.addText(title, { x: 0.5, y: 0.25, w: 9, h: 0.6, fontSize: 26, fontFace: HF, color: C.primary, bold: true, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 0.9, w: 3, h: 0, line: { color: C.accent, width: 2 } });
  return s;
}
```

### 4. Slide Patterns

**Overview deck (CH00):** 6-7 slides
1. Title (dark) — series name + tagline
2. About — who it's for, stats (topics, files, sources)
3-4. Topic cards — 2×2 or 3×2 card grids per slide, with bullets
5. Learning path / teaching routes (if applicable)
6. Vault relationship diagram (if content links to another vault)
7. Closing (dark) — motivational one-liner

**Chapter deck (CH01+):** varies
1. Title (dark) — chapter name
2. Overview — what we'll cover
3-N. Content slides — tables, cards, examples, callouts
N+1. Thai Speaker Traps / Common Mistakes (orange accent, table format)
N+2. Quick Test / Quiz
N+3. Section divider for next topic (if multi-topic chapter)

### 5. Build & Verify

```bash
cd "F:/projects/<project>/<folder>"
node build_overview.js
node build_ch01.js
```

## QA Without LibreOffice

When soffice/pdftoppm aren't available, extract text with python-pptx:

```python
import sys
sys.path = [p for p in sys.path if 'hermes' not in p]  # avoid PIL conflicts with hermes venv
from pptx import Presentation
prs = Presentation('output.pptx')
for i, slide in enumerate(prs.slides):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                t = para.text.strip()
                if t: texts.append(t)
    print(f'--- Slide {i+1} ---')
    for t in texts: print(t)
```

Also run a code-level pitfall check:
- No `#` prefix in hex colors
- No 8-char hex (corruption risk)
- No unicode bullets (`•`)
- No negative shadow offsets
- No ROUNDED_RECTANGLE with accent bars

## Pitfalls

- **8-char hex corrupts files.** `"FFFFFFCC"` is not valid — use `"FFFFFF"` and set `transparency` separately. pptxgenjs will warn but still produce a broken file.
- **Global npm installs may not resolve.** Always `npm install pptxgenjs` locally in the build folder.
- **PIL conflict with hermes venv.** When importing python-pptx, filter hermes paths from sys.path or use the system Python directly.
- **Don't declare success without QA.** Even if `node build.js` exits 0, extract and verify content.
- **Color palettes must differ per topic** in a series — otherwise all decks look the same.
