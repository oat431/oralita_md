# Rename & Fix Backlinks Workflow

When renaming a vault folder or files within a vault, follow this systematic approach to avoid broken links.

## Steps

### 1. Rename the folder
```bash
cd "parent_dir" && mv Old_Name New_Name
```

### 2. Rename files with old name in their title
Use `mcp_filesystem_move_file` to rename overview files.

### 3. Find all references to old name
Use `search_files` with pattern `Old_Name|OldFolder` across the vault.

### 4. Fix references with `patch()`
Replace old name with new name in each file.

### 5. Fix broken wikilinks
Scan for `[[wikilinks]]` that don't match actual filenames. Fix with `patch()`.

### 6. Verify
Python script checking no old name references remain.

## Proven Example

- **Algorithm_v2 → Algorithm_advance**: 3 references fixed (2 internal in overview, 1 external in v1 overview), plus 7 broken wikilinks corrected (wrong v1 file names like `[[04_Binary_Heaps]]` → `[[01 Heaps & Priority Queues]]`). All verified clean.
