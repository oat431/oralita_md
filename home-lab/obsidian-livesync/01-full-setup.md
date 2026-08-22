# Obsidian LiveSync — Complete Setup Guide (Zero → Working)

> Full journey: CouchDB deployment → Nginx → user/database → CORS → Obsidian plugin.
> All steps were executed and verified on the Panomete homelab, 2026-08-13.
> Server: `flowero@remote.panomete.com` · Subdomain: `obsync.panomete.com`

---

## Architecture Overview

```
Obsidian (desktop/mobile)
    │  HTTPS (native fetch — needs CORS)
    ▼
Cloudflare Tunnel (obsync.panomete.com)
    │
    ▼
Nginx (host-level reverse proxy)
    │  127.0.0.1:5984
    ▼
CouchDB 3.5.2 (container: local-couchdb, db-network)
    │
    ├── obsidian-livesync  ← the sync database
    └── _users             ← user accounts
```

- **CouchDB speaks HTTP** — no database driver needed, the plugin talks REST directly.
- **CORS is handled by CouchDB itself** (Nginx stays a clean pass-through proxy).
- MongoDB **cannot** be used — LiveSync is built on the CouchDB replication protocol (PouchDB).

---

## Step 1 — Deploy CouchDB

### 1.1 Create the compose directory

```bash
ssh flowero@remote.panomete.com
mkdir -p ~/database/couchdb
```

### 1.2 Generate secrets

```bash
COUCHPASS=$(openssl rand -hex 16)
COUCHSECRET=$(openssl rand -hex 32)
cat > ~/database/couchdb/.env << EOF
COUCHDB_USER=admin
COUCHDB_PASSWORD=$COUCHPASS
COUCHDB_SECRET=$COUCHSECRET
EOF
```

### 1.3 Compose file

`~/database/couchdb/compose.yml`:

```yaml
services:
  couchdb:
    container_name: local-couchdb
    image: couchdb:3
    environment:
      COUCHDB_USER: ${COUCHDB_USER:-admin}
      COUCHDB_PASSWORD: ${COUCHDB_PASSWORD:-couchdb}
      COUCHDB_SECRET: ${COUCHDB_SECRET}
    volumes:
      - couchdb_data:/opt/couchdb/data
      - couchdb_config:/opt/couchdb/etc/local.d
    ports:
      - "127.0.0.1:5984:5984"
    restart: unless-stopped
    networks:
      - shared-network
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:5984/ || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3

volumes:
  couchdb_data:
  couchdb_config:

networks:
  shared-network:
    external: true
    name: db-network
```

### 1.4 Start & verify

```bash
cd ~/database/couchdb
docker compose config --quiet   # validate
docker compose up -d            # start
docker ps --filter "name=couchdb"   # expect: (healthy)
curl http://127.0.0.1:5984/          # expect: {"couchdb":"Welcome",...}
```

---

## Step 2 — Nginx Reverse Proxy

`/etc/nginx/sites-available/obsync.conf`:

```nginx
server {
    listen 80;
    server_name obsync.panomete.com;
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5984;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;

        # LiveSync uses the long-poll _changes feed
        proxy_buffering off;
        proxy_read_timeout 120s;
    }
}
```

Apply:

```bash
sudo ln -s /etc/nginx/sites-available/obsync.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

> ⚠️ **Do NOT add CORS headers in Nginx.** CouchDB emits them natively (once enabled, Step 4).
> Duplicated `Access-Control-*` headers from two sources break browsers.

Then create the Cloudflare Tunnel route for `obsync.panomete.com` → local HTTP (as done for the other subdomains).

**Verify:** open `https://obsync.panomete.com/` → should show the CouchDB welcome JSON.

---

## Step 3 — Create Database & Users

### 3.1 Create system + sync databases

```bash
ADMIN="admin"; ADMINPASS="<from ~/database/couchdb/.env>"

# System databases (required for users/security)
curl -X PUT -u $ADMIN:$ADMINPASS http://127.0.0.1:5984/_users
curl -X PUT -u $ADMIN:$ADMINPASS http://127.0.0.1:5984/_replicator
curl -X PUT -u $ADMIN:$ADMINPASS http://127.0.0.1:5984/_global_changes

# The LiveSync database
curl -X PUT -u $ADMIN:$ADMINPASS http://127.0.0.1:5984/obsidian-livesync
```

### 3.2 Create a non-admin user

Never give the plugin the admin account. Create a dedicated user:

```bash
curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '{"_id": "org.couchdb.user:obsidian", "name": "obsidian",
       "type": "user", "roles": [], "password": "obsidian-livesync"}' \
  http://127.0.0.1:5984/_users/org.couchdb.user:obsidian
```

### 3.3 Grant database access (critical — users are DB-isolated by default)

```bash
curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '{"admins":{"names":[],"roles":[]},"members":{"names":["obsidian"],"roles":[]}}' \
  http://127.0.0.1:5984/obsidian-livesync/_security
```

> ⚠️ `_security` PUT **replaces the whole list** — include ALL existing members when adding one.

### 3.4 Verify the user works

```bash
curl -u obsidian:obsidian-livesync http://127.0.0.1:5984/_session
# → {"ok":true,"userCtx":{"name":"obsidian",...}}

curl -u obsidian:obsidian-livesync http://127.0.0.1:5984/obsidian-livesync
# → {"db_name":"obsidian-livesync",...}
```

---

## Step 4 — Enable CORS (THE gotcha step)

### The three rules learned the hard way

1. **Master switch:** `[chttpd] enable_cors = true` — defaults to **false**. Without it, CouchDB silently ignores all `[cors]` settings and returns no CORS headers at all.
2. **`origins = *` + `credentials = true` is invalid** — CouchDB silently disables credentials when origins is `*`. Use an explicit origin list.
3. **No spaces after commas** in the origin list — CouchDB doesn't trim.

### 4.1 Set via API (applies immediately)

```bash
BASE="http://127.0.0.1:5984/_node/_local/_config"

# Master switch
curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '"true"' $BASE/chttpd/enable_cors

# CORS rules
curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '"app://obsidian.md,capacitor://localhost,http://localhost,https://localhost,https://obsync.panomete.com"' \
  $BASE/cors/origins

curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '"true"' $BASE/cors/credentials

curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '"accept,authorization,content-type,origin,referer,x-requested-with"' \
  $BASE/cors/headers

curl -X PUT -u $ADMIN:$ADMINPASS -H "Content-Type: application/json" \
  -d '"GET,PUT,POST,HEAD,DELETE"' \
  $BASE/cors/methods
```

### 4.2 Persist in docker.ini (survives restarts)

The official image regenerates `/opt/couchdb/etc/local.d/docker.ini` from runtime config on graceful shutdown — but write it explicitly to be safe:

```ini
[chttpd]
enable_cors = true

[cors]
origins = app://obsidian.md,capacitor://localhost,http://localhost,https://localhost,https://obsync.panomete.com
credentials = true
headers = accept,authorization,content-type,origin,referer,x-requested-with
methods = GET,PUT,POST,HEAD,DELETE
```

> ⚠️ If you edit docker.ini from outside the container (docker cp), **chown it back** to `5984:5984` (the couchdb user) or every config write fails with `eacces`:
> ```bash
> docker exec local-couchdb chown 5984:5984 /opt/couchdb/etc/local.d/docker.ini
> ```

### 4.3 Verify CORS works

```bash
# Preflight (the one that matters)
curl -si -X OPTIONS \
  -H "Origin: app://obsidian.md" \
  -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: authorization" \
  https://obsync.panomete.com/obsidian-livesync | grep -i access-control
```

Expected:
```
HTTP/1.1 204 No Content
access-control-allow-credentials: true
access-control-allow-headers: authorization
access-control-allow-methods: GET, PUT, POST, HEAD, DELETE
access-control-allow-origin: app://obsidian.md
access-control-max-age: 600
```

---

## Step 5 — Connect Obsidian (First Device)

1. Install **Self-hosted LiveSync** from Community Plugins → Enable
2. Click the **"Welcome to Self-hosted LiveSync"** notice
3. Choose **I am setting this up for the first time** → confirm
4. Connection Method → **Configure a remote manually** (NOT Setup URI — that's for additional devices)
5. Choose **CouchDB** → enter:

   | Field | Value |
   |-------|-------|
   | CouchDB URL | `https://obsync.panomete.com` |
   | Username | `obsidian` |
   | Password | `obsidian-livesync` |
   | Database | `obsidian-livesync` |

6. Enable **End-to-End Encryption** → set a strong vault passphrase (store it safely!)
7. Click **Check server requirements** → **Create or connect to database and continue**
8. **Restart and Initialise Server** → confirm the overwrite warning (first device pushes local vault)
9. If asked: **No Synchronisation Settings Found** → **Use this device's settings**
10. Keep Obsidian open until progress indicators clear

### Compatibility Review Pause

On an existing vault, LiveSync pauses with *"No previously acknowledged internal database version was found"*. This is a **safety gate, not an error** — click acknowledge/resume. It records the current version and starts replication.

---

## Step 6 — Add More Devices (Setup URI)

1. On the working first device: Command Palette → **Self-hosted LiveSync: Copy settings as a new Setup URI** → set a URI passphrase → copy link
2. On the new device: install plugin → onboarding → **I am adding a device** → paste URI + URI passphrase → **Restart and Fetch Data**
3. Store the Setup URI and its passphrase **separately** (different channels)

Two distinct passphrases exist:
- **Vault encryption passphrase** — encrypts your note data (same on all devices)
- **Setup URI passphrase** — decrypts the connection-settings link (per-URI, can differ)

---

## Operations Reference

### Container lifecycle

```bash
cd ~/database/couchdb
docker compose up -d          # start
docker compose down           # stop (data preserved in volumes)
docker logs local-couchdb     # logs
docker exec -it local-couchdb bash   # shell
```

### Fauxton admin UI

```
https://obsync.panomete.com/_utils/
```
Login with the admin credentials from `~/database/couchdb/.env`.

### Backups

CouchDB data lives in the Docker volume `couchdb_couchdb_data`.
```bash
# Quick backup (all DBs → file)
docker exec local-couchdb couchdb-dump http://admin:PASS@localhost:5984 > couchdb-backup.json
```

### Monitoring

Uptime Kuma can monitor `https://obsync.panomete.com/` — expect HTTP 200 (or 401 without auth, still healthy).

---

## Troubleshooting Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| No CORS headers at all | `[chttpd] enable_cors` missing | Set to `true` (Step 4.1) |
| `credentials` silently off | `origins = *` + `credentials = true` conflict | Explicit origin list |
| Origin never matches | Spaces after commas in origins | No spaces: `a,b,c` |
| `eacces` on config PUT | docker.ini owned by wrong UID | `chown 5984:5984` |
| OPTIONS returns 401 | Preflight origin not in list | Add the origin, re-test |
| "native fetch API failed" | Any of the above | Work through Step 4.3 |
| "You are not allowed" | User not in DB `_security` members | Step 3.3 |
| "Database not found" | DB not created | Step 3.1 |
| Config lost after restart | Not persisted in docker.ini | Step 4.2 |

---

## Related Notes

- [[03-couchdb-user-management]] — creating/removing users, permissions
- [[02-connection-guide]] — end-user connection guide + troubleshooting
