# Vault Verification Script

Python script to verify all files in a filled vault are complete and valid. Run after batch-creating topic notes.

```python
import os, re, sys

base = r"F:\projects\orlita_md\your-vault-name"
errors = []

# 1. Check overview exists and has wikilinks
overview_path = os.path.join(base, "Overview.md")
if os.path.exists(overview_path):
    with open(overview_path, "r", encoding="utf-8") as f:
        c = f.read()
    links = re.findall(r'\[\[(.*?)\]\]', c)
    print(f"  Overview: {len(links)} wikilinks")

# 2. Check all expected subdirs and files
# Define your expected structure:
expected = {
    "01 Category": ["01 File.md", "02 File.md"],
    "02 Category": ["03 File.md"],
}

present = 0
with_sources = 0
with_mermaid = 0

for folder, files in expected.items():
    for fn in files:
        path = os.path.join(base, folder, fn)
        if not os.path.exists(path):
            errors.append(f"MISSING: {folder}/{fn}")
            continue
        if os.path.getsize(path) < 500:
            errors.append(f"TOO SMALL: {folder}/{fn}")
            continue
        present += 1
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        if "## Sources" in c:
            with_sources += 1
        if "```mermaid" in c:
            with_mermaid += 1
        # Check no broken mermaid (text in mermaid block without diagram keyword)
        blocks = re.findall(r'```mermaid\n(.*?)```', c, re.DOTALL)
        for block in blocks:
            if not any(kw in block for kw in ["classDiagram", "graph", "sequenceDiagram", "stateDiagram"]):
                errors.append(f"BROKEN MERMAID: {folder}/{fn}")

# 3. Check for stray ASCII art
ascii_chars = "┌└├┐┘┤─│┬┴┼"
for folder in expected:
    for fn in os.listdir(os.path.join(base, folder)):
        path = os.path.join(base, folder, fn)
        with open(path, "r", encoding="utf-8") as f:
            if any(c in f.read() for c in ascii_chars):
                print(f"  ⚠ ASCII art still in: {folder}/{fn}")

total = sum(len(v) for v in expected.values())
print(f"Files: {present}/{total}")
print(f"With Sources: {with_sources}/{present}")
print(f"With Mermaid: {with_mermaid}/{present}")

if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)
else:
    print("PASS")
    sys.exit(0)
```
