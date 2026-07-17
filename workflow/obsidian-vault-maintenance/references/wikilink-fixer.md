# Broken Wikilink Detection & Fixing

Multi-pass workflow: scan → fix → re-scan → fix again. Most vaults need 2-3 passes.

## Step 1: Diagnose (run before EVERY pass)

```python
import os, re

base = r"F:\projects\orlita_md"  # adjust to vault path
existing_files = set()
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"): continue
        rel = os.path.join(root, fn).replace(base, "").lstrip("\\/").replace("\\", "/")
        existing_files.add(rel.lower())
        existing_files.add(fn[:-3].lower())

broken = {}
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"): continue
        fp = os.path.join(root, fn)
        rel = fp.replace(base, "").lstrip("\\/").replace("\\", "/")
        with open(fp, "r", encoding="utf-8") as f: content = f.read()
        for link in re.findall(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]', content):
            link = link.strip()
            if "http" in link: continue
            if link.lower() in existing_files: continue
            if link.lower() + ".md" in existing_files: continue
            broken.setdefault(rel, []).append(link)

if not broken:
    print("No broken wikilinks found!")
else:
    total = sum(len(links) for links in broken.values())
    print(f"{total} broken wikilinks across {len(broken)} files")
    for f, links in sorted(broken.items()):
        print(f"  {f}")
        for l in sorted(set(links)):
            print(f"     [[{l}]]")
```

## Step 2: Build Fix Mapping

Common patterns found in real vaults:

| Pattern | Example | Fix |
|---------|---------|-----|
| **Off-by-one chapter numbers** | `[[02_Risk_Management]]` when file is `01_Risk_Management` | Remap numbers |
| **Wrong chapter numbers** | `[[06_Data_Security]]` when file is `05_Data_Security` | Remap to correct |
| **Path-qualified links** | `[[BABOK/Note Name]]` | Flatten: `[[Note Name]]` |
| **Relative path links** | `[[../dir/Note Name]]` | Flatten: `[[Note Name]]` |
| **Backslash in links** | `[[Note\|alias]]` or `[[Note\\|alias]]` | Strip backslash |
| **Folder-style links** | `[[02-Creational/]]` | Remove entirely |
| **Placeholder text** | `[[wikilinks]]`, `[[Related Topic]]` | Remove entirely |
| **Concept-only links** | `[[viruses]]`, `[[CRM]]` (no file exists) | Convert to `**bold**` |
| **Profile name mismatches** | `[[BABOK v3]]` when file is `BABOK v3 - Overview` | Correct name |
| **Alias with wrong target** | `[[wrong\|display]]` | Fix target, keep alias |

## Step 3: Apply Fixes — Multi-Pass Script

```python
import os, re

base = r"F:\projects\orlita_md"

# Build file index (case-insensitive)
all_filenames = set()
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"): continue
        all_filenames.add(fn[:-3].lower())

# === DEFINE FIX MAPPINGS (customize per vault) ===

numbered_cross_refs = {
    # "broken_link_text": "correct_link_text"
    # e.g. "02_Risk_Management_and_Governance": "01_Risk_Management_and_Governance",
}

profile_name_fixes = {
    # "Short Name": "Full Filename Without .md"
    # e.g. "BABOK v3": "BABOK v3 - Overview",
}

concept_to_bold = [
    # List of link texts that have no file — convert to bold
    # e.g. "viruses", "CRM", "IDS"
]

# === APPLY ===

def apply_fixes(content):
    changed = False

    # 1. Fix backslash before pipe (single or double)
    new = re.sub(r'\[\[([^\\\[\]]+?)\\+(\|)', r'[[\1\2', content)
    if new != content: content, changed = new, True

    # 2. Fix backslash before closing brackets
    new = re.sub(r'\[\[([^\\\[\]]+?)\\+\]\]', r'[[\1]]', content)
    if new != content: content, changed = new, True

    # 3. Remove placeholder text
    for placeholder in ['[[wikilinks]]', '[[wikilink]]']:
        if placeholder in content:
            content = content.replace(placeholder, '')
            changed = True

    # 4. Remove folder-style links
    new = re.sub(r'\[\[[^\]]*?/\]\]', '', content)
    if new != content: content, changed = new, True

    # 5. Flatten path-qualified links: [[A/B/Note]] -> [[Note]]
    new = re.sub(r'\[\[(?:[^/\[\]]+/)+([^\|\]]+)\]\]', r'[[\1]]', content)
    new = re.sub(r'\[\[(?:[^/\[\]]+/)+([^\|\]]+)\|([^\]]+)\]\]', r'[[\1|\2]]', new)
    if new != content: content, changed = new, True

    # 6. Apply numbered cross-ref fixes
    for broken, correct in numbered_cross_refs.items():
        p = re.escape(broken)
        new = re.sub(r'\[\[' + p + r'\]\]', '[[' + correct + ']]', content)
        new = re.sub(r'\[\[' + p + r'\|([^\]]+)\]\]', '[[' + correct + r'|\1]]', new)
        if new != content: content, changed = new, True

    # 7. Apply profile name fixes
    for broken, correct in profile_name_fixes.items():
        p = re.escape(broken)
        new = re.sub(r'\[\[' + p + r'\]\]', '[[' + correct + ']]', content)
        if new != content: content, changed = new, True

    # 8. Convert concept-only links to bold
    for concept in concept_to_bold:
        p = re.escape(concept)
        new = re.sub(r'\[\[' + p + r'\]\]', '**' + concept + '**', content)
        if new != content: content, changed = new, True

    # 9. Catch-all: convert any remaining broken links to bold
    def replace_broken(match):
        link = match.group(1).split('|')[0].strip()
        if link.lower() in all_filenames or link.lower() + '.md' in all_filenames:
            return match.group(0)
        if 'http' in link:
            return match.group(0)
        if '|' in match.group(1):
            alias = match.group(1).split('|', 1)[1]
            return '**' + alias + '**'
        return '**' + link + '**'

    new = re.sub(r'\[\[([^\]]+)\]\]', replace_broken, content)
    if new != content: content, changed = new, True

    return content, changed

# Run
files_fixed = 0
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"): continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8") as f: content = f.read()
        new_content, changed = apply_fixes(content)
        if changed:
            with open(fp, "w", encoding="utf-8") as f: f.write(new_content)
            files_fixed += 1

print(f"Fixed {files_fixed} files")
```

## Step 4: Re-Scan

**Always** re-run Step 1 after each fix pass. Some corrections reveal new breaks, or the catch-all missed edge cases. Repeat Steps 2-3 until the scan reports zero broken links.

## Pitfalls

- **Single vs double backslash**: Files may contain `\` (0x5C) or `\\`. Python `repr()` shows `\\` for a single backslash. Check raw bytes with `open(fp, 'rb').read()` if unsure. The regex `\\+` handles both.
- **Case sensitivity**: Obsidian is case-insensitive for link resolution but your fix scripts must compare `.lower()` on both sides.
- **Concept-only links are content**: Don't delete `[[viruses]]` — convert to `**viruses**` to preserve the semantic emphasis. Only remove truly meaningless placeholders like `[[wikilinks]]`.
- **Catch-all must be last**: The catch-all bold-conversion in step 9 must run AFTER all targeted fixes, or it will convert valid links that just haven't been fixed yet.
- **User personal notes**: Skip files in `Personal Project/`, `Quick Note/`, `memory/`, and files with date patterns like `2026-06-`. Only fix knowledge vaults.
- **Backslash regex gotcha**: `r'\[\[([^\\[\]]+?)\\\]\]'` — the character class `[^\\[\]]` already excludes backslash, so the `+?` won't eat the backslash. But if the link text itself contains a backslash (rare), this breaks. Use `r'\[\[(.+?)\\+\]\]'` with `re.DOTALL` as fallback.
