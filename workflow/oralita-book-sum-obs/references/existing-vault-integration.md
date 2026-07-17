# Existing Vault Integration

When the user asks for new content in an area that may already have partial coverage in their vault.

## When to Use

- User says "I need X" where X might overlap with existing folders
- User mentions a topic area without specifying where to put it
- Before creating any new top-level folder in the vault

## Checklist

1. **Scan the vault first** — `mcp_filesystem_directory_tree` on the parent directory
2. **Check for related subfolders** — look for names that cover similar territory
3. **Read existing overviews** — understand what's already there
4. **Integrate, don't duplicate** — add new files to existing structure with sequential numbering
5. **Update existing overviews** — add new entries to the overview tables
6. **Remove empty folders** — if you created a duplicate, clean it up

## Example: UX/UI Design → HCI Integration

**Problem:** User asked for UX/UI design content. Created `UX UI Design/` folder with 6 files.

**Discovery:** User had `Software Design/Human Computer Interaction/` with 29 existing files covering Gestalt laws, UX laws, UI principles (theory).

**Solution:**
- Moved 6 files into HCI folder with sequential numbering (30-34)
- Updated HCI overview to include new "UX/UI Process" section
- Updated UX Overview and UI Overview to link to new process files
- Removed empty `UX UI Design/` folder
- Updated Essential Documents link to point to HCI

**Result:** 35 files in one cohesive folder (theory + practice) instead of two fragmented folders.

## File Numbering Convention

When integrating into an existing numbered structure:
- Continue the existing numbering (if files are 01-29, new files start at 30)
- Don't renumber existing files
- Use descriptive names: `30 User Research Methods.md` not `30_Methods.md`

## Cross-Link Updates Required

After integration, update these links:
- [ ] Parent overview → add new entries to section table
- [ ] Related overviews → add new process sections
- [ ] Essential Documents → update "Which Checklist" links
- [ ] BOK overview → if relevant, add to relationship diagram
