# rclone OneDrive Setup

## Install rclone (latest from official)
```bash
curl -fsSL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
cd /tmp && unzip -o rclone.zip
sudo cp rclone-*-linux-amd64/rclone /usr/local/bin/
sudo chmod +x /usr/local/bin/rclone
```

## Get OAuth token (on PC, not server)
```bash
rclone authorize "onedrive"
# Browser opens → login → terminal prints token JSON
```

## Get drive_id from Microsoft API
```bash
curl -s -H "Authorization: Bearer <access_token>" \
  'https://graph.microsoft.com/v1.0/me/drive' | python3 -m json.tool | grep '"id"'
```

## Config (`~/.config/rclone/rclone.conf`)
```ini
[onedrive]
type = onedrive
token = {"access_token":"...","token_type":"Bearer","refresh_token":"...","expiry":"...","expires_in":3599}
drive_id = XXXXXXXXXXXX
drive_type = personal
```

## Usage
```bash
rclone lsd onedrive:                          # list folders
rclone copy /path/file onedrive:backups/      # upload
rclone copy onedrive:backups/ /tmp/restore/   # download
```

## Pitfalls
- `unable to get drive_id and drive_type` → must add `drive_id` manually (fetch from API)
- `Failed to start auth webserver` → old rclone process holding port, `killall rclone`
- Token alone isn't enough — v1.74 requires `drive_id` in config
- apt version may be outdated DEV build — install from official site
- Token auto-refreshes via `refresh_token` — no manual action needed
