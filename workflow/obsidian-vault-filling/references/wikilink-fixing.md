# Wikilink Fixing — Batch Repair of Broken `[[links]]`

After filling a vault, moving files, or renaming topics, many `[[wikilinks]]` may point to non-existent files. Use this pipeline to find and fix them.

## Step 1: Build the Index

```python
existing_files = set()
for root, dirs, files in os.walk(base):
    for fn in files:
        if fn.endswith(".md"):
            existing_files.add(fn[:-3].lower())  # Without .md
            existing_files.add(fn.lower())        # With .md
```

## Step 2: Find Broken Links

```python
links = re.findall(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]', content)
for link in links:
    if link.lower() not in existing_files:
        broken[filepath].append(link)
```

## Step 3: Create Fix Mapping

Map broken link text → correct target filename:

```python
fixes = {
    # Wrong chapter numbers
    "06_Software_Configuration_Management": "08_Software_Configuration_Management",
    # Case-sensitive names  
    "SOLID Principles": "solid-principles",
    # Renamed files
    "Backend Launch": "API Launch",
}
```

## Step 4: Batch Replace

```python
for broken, correct in fixes.items():
    content = re.sub(rf'\[\[{re.escape(broken)}\]\]', f'[[{correct}]]', content)
    content = re.sub(rf'\[\[{re.escape(broken)}\|([^\]]+)\]\]', f'[[{correct}|\\1]]', content)
```

## Common Patterns

- **SWEBOK chapter renumbering**: Body of Knowledge files often have wrong chapter numbers in cross-references
- **Design pattern cross-refs**: `[[Factory Method]]` → `factory-method` (filename is lowercase with hyphens)
- **HCI folder links**: `[[01 Gestalt Laws/]]` → filename-only: `[[01 Law of Proximity]]` (Obsidian resolves by filename)
- **Combined files**: If you merged Migration + Backup + Scaling into one file, update all references
- **Cross-vault links**: `[[software-engineering-note]]` → relative path `[[../software-engineering-note/Note Name]]`

## Verification

After fixing, re-run Step 2 to confirm zero remaining broken links.
