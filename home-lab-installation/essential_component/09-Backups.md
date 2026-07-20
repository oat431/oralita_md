# 09 — Backups

> Automated backups with rclone to OneDrive.
> Last updated: 2026-07-20

---

## What We Set Up

rclone connects your server to OneDrive for offsite backups. No paid service needed — uses your existing Microsoft account.

---

## Step 1: Install rclone

```bash
# Install from apt (may be outdated)
sudo apt install -y rclone

# Or install latest from official site
curl -fsSL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
cd /tmp && unzip -o rclone.zip
sudo cp rclone-*-linux-amd64/rclone /usr/local/bin/
sudo chmod +x /usr/local/bin/rclone
rm -rf /tmp/rclone* rclone-*-linux-amd64
```

**Why:** rclone is a CLI tool that supports 40+ cloud storage providers. OneDrive is built-in.

---

## Step 2: Get the OAuth token (on your PC)

Since the server is headless, authorize on your Windows PC:

```bash
# Run on Windows (need rclone installed locally)
rclone authorize "onedrive"
```

This opens a browser → log in with your Microsoft account → terminal prints a **token**. Copy it.

**Why:** The server has no browser. The token contains the OAuth credentials needed to access OneDrive.

---

## Step 3: Get your Drive ID

The token alone isn't enough — rclone needs your OneDrive drive ID. Get it from Microsoft's API:

```bash
# On the server, use your access_token
curl -s -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  'https://graph.microsoft.com/v1.0/me/drive' | python3 -m json.tool | grep '"id"'
```

This returns something like `"id": "7AF14124B96CA208"`. Save it.

---

## Step 4: Write the config on the server

```bash
mkdir -p ~/.config/rclone
nano ~/.config/rclone/rclone.conf
```

```ini
[onedrive]
type = onedrive
token = {"access_token":"...","token_type":"Bearer","refresh_token":"...","expiry":"...","expires_in":3599}
drive_id = 7AF14124B96CA208
drive_type = personal
```

| Field | What it does |
|-------|-------------|
| `token` | The OAuth token from Step 2 (full JSON, escaped for single line) |
| `drive_id` | Your OneDrive drive ID from Step 3 |
| `drive_type` | `personal` for consumer OneDrive, `business` for work/school |

---

## Step 5: Verify

```bash
rclone lsd onedrive:
```

Should list your OneDrive folders. If it works, you're connected.

---

## Usage

```bash
# Upload a file
rclone copy /path/to/file.txt onedrive:homelab-backups/

# Upload a directory
rclone copy /home/flowero/application onedrive:homelab-backups/compose-files/

# List backups
rclone ls onedrive:homelab-backups/

# Download/restore
rclone copy onedrive:homelab-backups/ /tmp/restore/

# Sync (mirror — deletes remote files not in local)
rclone sync /path/to/data onedrive:homelab-backups/data/
```

---

## Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `unable to get drive_id and drive_type` | Config missing `drive_id` | Fetch from Microsoft API (Step 3) |
| `Failed to start auth webserver` | Old rclone process holding port | `sudo killall rclone` and retry |
| Token expired | Access tokens expire in 1 hour | rclone auto-refreshes using `refresh_token` — no action needed |
| `unzip: command not found` | Not installed | `sudo apt install -y unzip` |

---

## Next: Automated Backup Script

Once databases are running, create a cron job that:
1. Dumps PostgreSQL: `docker exec postgres pg_dumpall -U postgres > backup.sql`
2. Dumps MongoDB: `docker exec mongodb mongodump --archive > mongodb.archive`
3. Tars compose files
4. Uploads to OneDrive via `rclone copy`

_(Add script here after databases are deployed)_
