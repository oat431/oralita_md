"""
Find and fix broken [[wikilinks]] across an Obsidian vault.
Usage: python fix-wikilinks.py <vault_root> [--dry-run]
"""
import os, re, sys

# === CONFIGURE FIX MAPPINGS ===
# broken_link_text → correct_replacement
# Obsidian resolves by filename (without .md), not path
FIXES = {
    # Add your broken→correct mappings here.
    # Examples from Panomete's vaults:
    
    # Combined files — link to the file that absorbed them
    "03 Migration & Versioning": "03 Migration Backup & Scaling",
    "03 Backup & Recovery": "03 Migration Backup & Scaling",
    "03 Scaling Strategies": "03 Migration Backup & Scaling",
    "03 Complexity Analysis": "03 Patterns & Strategies",
    "02 Email, FTP & Supporting Protocols": "02 Supporting Protocols",
    
    # Renamed files
    "02 SOAP, MQTT & AMQP": "02 SOAP MQTT AMQP",
    "Code Smell Overview": "Code Smells Catalog",
    "Backend Launch": "API Launch",
    
    # Cross-vault links (Obsidian format)
    "software-engineering-note": "../software-engineering-note/Software Engineering Note Content",
    
    # Folder links → filename links
    "01 Gestalt Laws/": "01 Law of Proximity",
    "02 UI Design/": "06 Mobile First Design",
    "03 UX Laws/": "10 Aesthetic Usability Effect",
    "04 UX Principles/": "25 User-Centered Design",
}


def build_existing_index(base_dir):
    """Build set of all resolvable filenames."""
    files = set()
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                rel = os.path.join(root, fn).replace(base_dir, "").lstrip("\\/").replace("\\", "/")
                files.add(rel.lower())
                files.add(fn[:-3].lower())  # without .md
    return files


def fix_file(filepath, existing_files, fixes, dry_run=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Apply known fix mappings
    for broken, correct in fixes.items():
        pattern = re.escape(broken)
        content = re.sub(rf'\[\[{pattern}\]\]', f'[[{correct}]]', content)
        content = re.sub(rf'\[\[{pattern}\|([^\]]+)\]\]', f'[[{correct}|\\1]]', content)
    
    if content == original:
        return False
    
    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return True


def find_broken(base_dir, existing_files):
    """Scan all files and return {filepath: [broken_links]}."""
    broken = {}
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            links = re.findall(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]', content)
            for link in links:
                link = link.strip()
                if "http" in link or "://" in link:
                    continue
                target = link.lower()
                if target in existing_files or (target + ".md") in existing_files:
                    continue
                rel = fp.replace(base_dir, "").lstrip("\\/").replace("\\", "/")
                broken.setdefault(rel, []).append(link)
    return broken


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else r"F:\projects\orlita_md"
    dry_run = "--dry-run" in sys.argv
    
    existing = build_existing_index(base)
    print(f"Indexed {len(existing)} files")
    
    # Show broken links
    broken = find_broken(base, existing)
    if broken:
        total = sum(len(v) for v in broken.values())
        print(f"\n{total} broken links in {len(broken)} files:")
        for fp, links in sorted(broken.items()):
            print(f"  {fp}")
            for link in links[:5]:
                print(f"    ❌ [[{link}]]")
    else:
        print("No broken links found.")
    
    # Apply fixes
    if not dry_run:
        fixed = 0
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(root, fn)
                if fix_file(fp, existing, FIXES):
                    rel = fp.replace(base, "").lstrip("\\/")
                    print(f"  Fixed: {rel}")
                    fixed += 1
        print(f"\nFixed {fixed} files")
    else:
        print("\nDry run — no changes made. Remove --dry-run to apply fixes.")
