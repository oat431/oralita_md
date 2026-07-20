# rclone OneDrive on Headless Server

## The Problem

`rclone authorize "onedrive"` starts a local web server at `http://127.0.0.1:53682` for OAuth. On a headless server, this URL is inaccessible from your browser.

## Solution: Authorize on Local Machine, Paste Token to Server

1. Install rclone on your local machine (Windows/Mac/Linux)
2. Run: `rclone authorize "onedrive"`
3. Browser opens → log in with Microsoft account
4. Copy the JSON token it outputs
5. Paste token into server's `~/.config/rclone/rclone.conf`

## Config Format (v1.74+)

```ini
[onedrive]
type = onedrive
token = {"access_token":"...","token_type":"Bearer","refresh_token":"...","expiry":"...","expires_in":3599}
drive_id = XXXXXXXXXXXX
drive_type = personal
```

⚠️ **drive_id is required** in v1.74+. The token alone gives "unable to get drive_id and drive_type".

## Fetching drive_id

Use the access token to query Microsoft Graph API:

```bash
ACCESS_TOKEN="your-access-token-here"
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  'https://graph.microsoft.com/v1.0/me/drive' | python3 -m json.tool
```

Response contains `"id": "XXXXXXXXXXXX"` — use this as `drive_id` in the config.

## Installing Latest rclone

Ubuntu's apt package is often outdated. Install from official source:

```bash
sudo apt install -y unzip
curl -fsSL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
cd /tmp && unzip rclone.zip
sudo cp rclone-*-linux-amd64/rclone /usr/local/bin/
sudo chmod +x /usr/local/bin/rclone
rm -rf /tmp/rclone*
```

## Usage

```bash
rclone lsd onedrive:                    # list directories
rclone copy /path/to/backup onedrive:backups/  # upload
rclone ls onedrive:backups/             # list files
```
