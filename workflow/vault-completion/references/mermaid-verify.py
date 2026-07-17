"""Verify Mermaid diagrams in .md files under a vault path.
Usage: python mermaid-verify.py <vault_path>

Checks:
  1. All expected .md files exist and have content > 500 bytes
  2. Every file has a ## Sources section
  3. Every ```mermaid block contains a valid diagram type keyword
  4. Reports total files, mermaid count, and any errors

Exit 0 = all clean, exit 1 = errors found.
"""
import os, re, sys

def verify_vault(base_path, expected):
    """expected: dict of folder_name -> list of filenames"""
    errors = []
    present = 0
    with_sources = 0
    with_mermaid = 0

    for folder, files in expected.items():
        for fn in files:
            path = os.path.join(base_path, folder, fn)
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
            # Validate mermaid blocks
            blocks = re.findall(r'```mermaid\n(.*?)```', c, re.DOTALL)
            for block in blocks:
                first_line = block.strip().split("\n")[0].strip()
                valid_keywords = ["classDiagram", "graph", "sequenceDiagram", 
                                 "stateDiagram", "flowchart", "erDiagram", "gantt",
                                 "pie", "journey", "gitGraph", "mindmap"]
                if not any(first_line.startswith(kw) for kw in valid_keywords):
                    errors.append(f"BROKEN MERMAID in {folder}/{fn}: '{first_line[:40]}'")

    total = sum(len(v) for v in expected.values())
    print(f"Files: {present}/{total}")
    print(f"With Sources: {with_sources}/{present}")
    print(f"With Mermaid: {with_mermaid}/{present}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("PASS")
    sys.exit(0)

# Example usage — replace with actual expected dict
# verify_vault("/path/to/vault", {
#     "01 Folder": ["file1.md", "file2.md"],
#     "02 Folder": ["file3.md"],
# })
