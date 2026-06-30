---
tags:
- linux
- os
- programming
---

# 02 File Systems

The OS organizes raw disk blocks into files and directories. Understanding inodes, journaling, and permissions helps you debug "permission denied" and "disk full" errors.

---

## Inodes — The Heart of Unix File Systems

> An inode stores metadata about a file: size, permissions, timestamps, and pointers to data blocks. The filename is NOT in the inode — it's in the directory.

```
Inode #12345:
  Type: regular file
  Permissions: rw-r--r--
  Owner: 1000 (alice) Group: 1000 (developers)
  Size: 14200 bytes
  Timestamps: atime, mtime, ctime
  Blocks: [2048, 2049, 3072]
```

### Direct vs Indirect Blocks

```
Inode:
  [Direct block 0] ──────────▶ [Data]
  [Direct block 1] ──────────▶ [Data]
  ...
  [Direct block 11] ─────────▶ [Data]
  [Single indirect] ─────────▶ [Block of pointers] → [Data] × 256
  [Double indirect] ─────────▶ [Block of ptrs] → [Block of ptrs] → [Data]
  [Triple indirect] ─────────▶ [...three levels deep...]
```

```bash
# Check inode usage (different from disk space!)
df -i
# If inodes are full → can't create new files — even if disk has space!
```

---

## Journaling — Crash Recovery

> Before modifying the file system, write your INTENT to a journal. After a crash, replay the journal.

| Mode | What's Journaled | Safety vs Speed |
|------|-----------------|:---:|
| **Writeback** | Metadata only. Data may be lost. | Fastest |
| **Ordered** (default ext4) | Metadata. Data written before metadata. | Balanced |
| **Data** | Metadata + data (full journaling) | Safest. Slowest. |

---

## Common File Systems

| FS | Where Used | Key Feature |
|----|-----------|------------|
| **ext4** | Linux default | Journaling, large volumes (1EB), extents |
| **XFS** | RHEL/CentOS default | Parallel I/O, excellent for large files |
| **NTFS** | Windows | ACLs, compression, journaling |
| **ZFS** | FreeBSD, Ubuntu | Copy-on-write, snapshots, checksums, RAID-Z |
| **NFS** | Network | Remote mount. Stateless. |

---

## Hard Links vs Symbolic Links

| | Hard Link | Symbolic (Soft) Link |
|---|:---:|:---:|
| **What it is** | Second name for same inode | Pointer to a path |
| **Cross filesystem** | ❌ | ✅ |
| **Survives original deletion** | ✅ (inode lives while any links exist) | ❌ (broken link) |
| **Can link to directory** | ❌ (usually) | ✅ |
| **Created with** | `ln target linkname` | `ln -s target linkname` |

```bash
ln file.txt hardlink.txt      # Same inode
ln -s /var/log/app.log log    # Points to path
ls -li                         # Shows inode numbers
```

---

## Permissions

```
-rwxr-xr--  1 alice  developers  4096 Jun 24 14:32 script.sh
 │├┘├┘├┘    │   │        │
 │ │ │ │    │   │        └── Group
 │ │ │ │    │   └── Owner
 │ │ │ │    └── Link count
 │ │ │ └── Others (r--)
 │ │ └── Group (r-x)
 │ └── Owner (rwx)
 └── Type: - (file), d (dir), l (link)
```

| Octal | Symbolic | Meaning |
|:-----:|----------|---------|
| 7 | rwx | Read, write, execute |
| 6 | rw- | Read, write |
| 5 | r-x | Read, execute |
| 4 | r-- | Read only |
| 0 | --- | No permissions |

```bash
chmod 755 script.sh    # rwxr-xr-x
chmod 600 secret.key   # rw-------
chown appuser:appgroup file.log
```

---

## Sources

- `man inode`, `man ext4`, `man chmod`
- McKusick et al. *The Design and Implementation of the FreeBSD Operating System.*
