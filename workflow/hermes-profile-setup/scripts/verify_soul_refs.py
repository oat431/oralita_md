#!/usr/bin/env python3
"""Verify that every vault path referenced in SOUL files resolves.

Usage:
    python verify_soul_refs.py <soul-dir> [vault-root]

Extracts document-template paths from backtick-wrapped code spans inside
SOUL.md files and checks each resolves under the vault root. Handles both
backslash and forward-slash references.

Defaults:
    soul-dir   = current directory
    vault-root = F:/obsidian_note/swe-knowledge
"""
import os
import re
import sys

DEFAULT_VAULT = "F:/obsidian_note/swe-knowledge"


def extract_refs(text: str):
    # Backtick-wrapped vault paths (forward or back slashes)
    pat = re.compile(
        r"`((?:body-of-knowledge|software-engineering-note|computing-foundation-note"
        r"|career-path|document-template)[^`]*?\.md)`"
    )
    return [m.group(1).replace("\\", "/") for m in pat.finditer(text)]


def main():
    soul_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    vault = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VAULT
    vault = vault.replace("\\", "/")

    refs, missing = set(), set()
    for name in sorted(os.listdir(soul_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(soul_dir, name)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        refs.update(extract_refs(text))

    for r in sorted(refs):
        full = os.path.join(vault, r)
        if not os.path.exists(full):
            missing.add(r)

    print(f"unique vault refs: {len(refs)}")
    if missing:
        print("MISSING:")
        for m in sorted(missing):
            print("  ", m)
        sys.exit(1)
    print("ALL VAULT REFS RESOLVE")


if __name__ == "__main__":
    main()
