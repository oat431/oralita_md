# Skill Backup Workflow

Recurring workflow for backing up Hermes skills to an Obsidian vault for restoration on new machines.

## Workflow Overview

```
Hermes Skills → Obsidian Vault → New Machine
     ↓              ↓                ↓
  Installed      Backup Copy     Restore
```

## Steps

### 1. Identify Skills to Backup

```bash
# List all installed user-created skills
ls -d ~/AppData/Local/hermes/skills/*/*/SKILL.md | sed 's|.*/skills/||' | sed 's|/SKILL.md||' | sort

# Compare with vault
ls -d /f/obsidian_note/oralita_md/workflow/*/SKILL.md | sed 's|.*/workflow/||' | sed 's|/SKILL.md||' | sort
```

### 2. Copy Skills to Vault

```bash
# Copy skill directory (SKILL.md + references/)
cp -r ~/AppData/Local/hermes/skills/<category>/<skill-name> /f/obsidian_note/oralita_md/workflow/

# Or copy entire category if multiple skills
cp -r ~/AppData/Local/hermes/skills/<category>/* /f/obsidian_note/oralita_md/workflow/
```

### 3. Update Overview.md

The vault's `Overview.md` should list all active skills organized by category:

```markdown
# Workflow Overview

> *Agent-created Hermes skills — copy to `~/.hermes/skills/` on any new machine.*

---

## Skills Map (N Active)

### 📚 Category Name

| Skill | Use when |
|-------|---------|
| **skill-name** | Description |
```

### 4. Handle Archived Skills

When skills are consolidated (absorbed into others):

```bash
# Move to archived subfolder
mkdir -p /f/obsidian_note/oralita_md/workflow/archived
mv /f/obsidian_note/oralita_md/workflow/<old-skill> /f/obsidian_note/oralita_md/workflow/archived/
```

Update Overview.md to note absorption:
```markdown
## Archived Skills (N)

| Archived Skill | Absorbed Into | Reason |
|----------------|---------------|--------|
| **old-skill** | new-skill | Merged — description |
```

### 5. Verify Backup

```bash
# Count skills in vault
echo "Active: $(ls -d /f/obsidian_note/oralita_md/workflow/*/SKILL.md | wc -l)"
echo "Archived: $(ls -d /f/obsidian_note/oralita_md/workflow/archived/*/SKILL.md 2>/dev/null | wc -l)"
```

## Restoring on New Machine

```bash
# Copy all skills into Hermes
cp -r F:/obsidian_note/oralita_md/workflow/* ~/AppData/Local/hermes/skills/

# Verify
hermes skills list | grep local

# Load any skill
hermes -s <skill-name>
```

## Skill Lifecycle

```
[Create] → [Prove on real task] → [Save as skill] → [Use across sessions]
                                                        ↓
                                              [Backup to Obsidian vault]
                                                        ↓
                                              [Restore on new machine]
                                                        ↓
                                          [Consolidate] → [Archive in vault]
```

## Pitfalls

- **Don't backup packaged skills.** Only backup user-created skills. Packaged skills are auto-available from the skills hub.
- **Don't forget references/.** Skills often have `references/` directories with supporting files. Copy the entire skill directory.
- **Don't skip Overview.md updates.** The Overview is the index for restoration. Keep it current.
- **Don't delete archived skills.** Move them to `archived/` subfolder. They may be useful for reference.

## Verification

After backup:

```bash
# Check vault structure
ls -la /f/obsidian_note/oralita_md/workflow/

# Verify all user-created skills are present
comm -23 <(ls -d ~/AppData/Local/hermes/skills/*/*/SKILL.md | sed 's|.*/skills/||' | sed 's|/SKILL.md||' | sort) <(ls -d /f/obsidian_note/oralita_md/workflow/*/SKILL.md | sed 's|.*/workflow/||' | sed 's|/SKILL.md||' | sort)
```

If the command returns any skills, they're missing from the vault backup.