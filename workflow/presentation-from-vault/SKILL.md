---
name: presentation-from-vault
description: "Generate .pptx presentations from Obsidian vault content using PptxGenJS. Covers multi-chapter project organization, educational slide design systems, and QA workflows."
platforms: [windows, linux, macos]
---

# Presentation from Vault

Generate PowerPoint presentations from Obsidian markdown content using PptxGenJS.

## When to Use

- User asks to create slides/deck/presentation from Obsidian vault notes
- User references vault chapters, topics, or book summaries for presentation
- Multi-chapter or multi-topic presentation series

## Prerequisites

- `pptxgenjs` installed **locally** in project dir (not global — global `npm install -g pptxgenjs` does NOT resolve with `require()`)
- Load the `powerpoint` skill for design guidelines, QA checklist, and pitfall list

```bash
cd <project-dir>
npm init -y && npm install pptxgenjs
```

## Project Structure

For multi-chapter series, organize like this:

```
F:\projects\oralita_pptx\
└── English Skill\
    ├── node_modules\          # shared deps
    ├── package.json
    ├── build_overview.js      # CH00 — overview/index
    ├── build_ch01.js          # CH01 — chapter 1
    ├── build_ch02.js          # CH02 — chapter 2
    ├── CH00_Overview.pptx     # output
    ├── CH01_Foundation.pptx   # output
    └── ...
```

- One `build_*.js` per presentation
- All build scripts in the same dir sharing one `node_modules`
- Output naming: `CH00_Overview.pptx`, `CH01_Foundation.pptx` (numbered, descriptive)

## Workflow

### 1. Read Source Content

Read all vault files for the chapter/topic first. Use `mcp__filesystem__read_multiple_files` for batch reads.

### 2. Plan Slide Structure

Before writing code, plan:
- How many slides per topic
- Which layout types (table, cards, section divider, comparison, trap slide)
- Content density — don't cram; split dense tables across slides

### 3. Design System

Define a reusable color/font system at the top of each build script:

```javascript
const C = {
  darkBg: "0A3D47", primary: "028090", secondary: "00A896", accent: "02C39A",
  lightBg: "F0F9F7", white: "FFFFFF", dark: "1E293B", muted: "64748B",
  cardBg: "FFFFFF", tableBg: "E8F6F3", tableHead: "028090",
  red: "DC2626", green: "16A34A",
  trapBg: "FFF7ED", trapAccent: "EA580C",
};
const HF = "Georgia", BF = "Calibri";
```

### 4. Build Helper Functions

Create reusable slide builders — don't repeat layout code per slide:

- `darkSlide(title, subtitle)` — title/closing slides with dark bg
- `lightSlide(title)` — content slides with left accent bar
- `sectionSlide(num, title, desc)` — chapter/topic intro with big number
- `contentSlide(title)` — standard content with header + divider
- `trapSlide(title, rows)` — Thai speaker traps table with orange accent
- `addCard(s, x, y, w, h, accentColor, items)` — shadow card with left accent bar

### 5. Write & Run

```bash
node build_ch01.js
```

### 6. QA

**Content QA** (always do this):

```python
# Use system Python, NOT Hermes venv Python (PIL conflict)
import sys
sys.path = [p for p in sys.path if 'hermes' not in p]
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

**Code-level QA checklist** — run against the build script:
- No `#` prefix in hex colors (causes file corruption)
- No 8-char hex (opacity in color string corrupts file)
- No unicode bullets (`•`) — use `bullet: true`
- No negative shadow offset (corrupts file)
- No reused option objects across calls (pptxgenjs mutates in-place)
- `breakLine: true` on all array text items except the last

**Visual QA** — convert to images and use subagent (see powerpoint skill). Requires LibreOffice.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Global pptxgenjs not found by require() | Install locally: `npm install pptxgenjs` in project dir |
| markitdown[pptx] fails to extract | Use python-pptx direct extraction (see QA script above) |
| PIL/_imaging import error from python-pptx | Filter hermes venv from sys.path before importing pptx |
| No LibreOffice for visual QA | Content QA + code-level checklist is sufficient; offer to install LibreOffice if user wants visual verification |
| Console.log message doesn't match output filename | Keep success message in sync with `fileName` param |
| `npm install -g` packages not in node_modules | Always install locally per project, not globally |

## Educational Presentation Patterns

For teaching/educational decks (language, skills, training):

- **Section divider slides** — big chapter number + title between topics
- **Comparison cards** — side-by-side (e.g., countable vs uncountable)
- **Trap slides** — dedicated slides for common mistakes with ❌/✅ formatting
- **Quick test slides** — interactive quiz content with answer reveals
- **Thai speaker trap pattern** — orange accent, 3-column table (Thai pattern | Wrong | Correct)
