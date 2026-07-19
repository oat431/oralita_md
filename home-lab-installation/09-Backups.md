# 09 — Backups

> Automated backups with rclone to Backblaze B2.

---

## Step 1: Install rclone

```bash
sudo apt install -y rclone
```

---

## Step 2: Configure Backblaze B2

```bash
rclone config
```

Follow the prompts:
- Choose `n` for new remote
- Name: `b2`
- Storage: `Backblaze B2`
- Enter your B2 Key ID and Application Key

---

## Step 3: Create backup script

```bash
sudo nano /opt/backup.sh
```

```bash
#!/bin/bash
# Backup compose files and databases to B2

BACKUP_DIR="/tmp/backups/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Backup compose files
tar czf "$BACKUP_DIR/compose-files.tar.gz" /home/flowero/application/*/compose.yml

# Backup PostgreSQL
docker exec postgres pg_dumpall -U postgres > "$BACKUP_DIR/postgres.sql"

# Backup MongoDB
docker exec mongodb mongodump --archive > "$BACKUP_DIR/mongodb.archive"

# Upload to B2
rclone copy "$BACKUP_DIR" b2:your-bucket-name/homelab/$(date +%Y-%m-%d)/

# Cleanup local
rm -rf "$BACKUP_DIR"
```

---

## Step 4: Schedule daily backups

```bash
sudo chmod +x /opt/backup.sh
sudo crontab -e
```

Add:

```
0 3 * * * /opt/backup.sh >> /var/log/backup.log 2>&1
```

**Why:** Runs at 3 AM daily. If the NVMe dies, your data is in B2 (~$0.27/month for 54GB).

---

## Step 5: Test a restore

```bash
rclone ls b2:your-bucket-name/homelab/
```

**Why:** Untested backups are assumptions, not backups.

_(TODO: Complete with actual B2 setup and restore testing)_
