# Fill KA Gaps Directly (No PDF Source)

## When to Use

When the user has an existing SWEBOK Knowledge Area Overview with a "What's Missing" section, and the missing topics are well-documented, standardized concepts that can be written from domain knowledge without a source PDF.

## Indicators

- Overview file has a "What's Missing" section listing 5-10 specific topics
- Topics are standard SWEBOK concepts (not proprietary models)
- User asks "can we just fill the gaps without a book?"

## Process

### 1. Read the Overview

Read the existing Overview to understand:
- What's in the "What's Missing" section
- Existing note structure (what subfolders/files already exist)
- Style conventions (YAML frontmatter format, wikilink patterns)

### 2. Check for Overlap

Verify the proposed gaps don't duplicate existing content. Check:
- Existing subfolders (Clean Code, Clean Architecture, Design Pattern, etc.)
- Related KAs that might already cover the topic

### 3. Map Gaps to Files

Present a gap-filling plan to the user:

| Gap | Can Fill? | Notes |
|---|---|---|
| Design Fundamentals | ✅ | Abstraction, modularization, coupling/cohesion |
| Design Processes | ✅ | High-level vs detailed design |
| ... | ... | ... |

### 4. Write Files Directly

Use `write_file` to create each file with:
- YAML frontmatter with appropriate tags
- Source attribution (usually "SWEBOK v4 Chapter XX")
- Professional, structured content with tables and sections
- `## Related` section with [[wikilinks]] to existing notes

**File sizes:** 4-6 KB each is appropriate for these theoretical overviews.

### 5. Update the Overview

- Add new files to the "My Notes" section (grouped under a meaningful heading)
- Remove the "What's Missing" section (or replace with "All major topics now covered")
- Preserve existing subfolder links

## Proven On

- **Software Design KA Gaps** — 6 files (33.8 KB) filling Design Fundamentals, Design Processes, Design Qualities, Recording Designs, Design Strategies, and Design Quality Analysis. All written directly from SWEBOK knowledge in ~5 minutes. No PDF or web search required.
