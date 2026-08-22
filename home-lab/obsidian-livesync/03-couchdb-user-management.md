# CouchDB — Creating Users for Obsidian LiveSync

> Admin guide for adding new users to the `obsidian-livesync` database.
> Each person sharing a vault needs their own account.
> Prerequisite: access to **Fauxton** at `https://obsync.panomete.com/_utils/`

---

## Method 1: Fauxton Web UI (Recommended)

### Step 1 — Log in to Fauxton

1. Go to `https://obsync.panomete.com/_utils/`
2. Log in with the **admin** account
   - Username: `admin`
   - Password: see `~/database/couchdb/.env` on the homelab server

### Step 2 — Create the user

1. Click the **wrench icon** (⚙️) in the left sidebar → **Configuration**
2. Or navigate directly to: `https://obsync.panomete.com/_utils/#database/_users/_all_docs`
3. Click **+ Create Document**
4. Paste this JSON (replace `USERNAME` and `PASSWORD`):

```json
{
  "_id": "org.couchdb.user:USERNAME",
  "name": "USERNAME",
  "type": "user",
  "roles": [],
  "password": "PASSWORD"
}
```

5. Click **Create Document**
6. Verify: the new user appears in the `_users` document list

### Step 3 — Grant database access

1. Go to the `obsidian-livesync` database
   - `https://obsync.panomete.com/_utils/#database/obsidian-livesync/_all_docs`
2. Click **Permissions** (lock icon in the top bar)
3. In the **Members** section, under the **Names** column:
   - Type `USERNAME` and press Enter
4. The user now has read/write access to this database

### Step 4 — Verify the user can connect

Test with curl (optional):

```bash
curl -u USERNAME:PASSWORD https://obsync.panomete.com/_session
```

Should return `"ok": true` with the user's name.

### Step 5 — Give credentials to the user

Tell the person to enter these in their Obsidian LiveSync plugin settings:

```
URI:      https://obsync.panomete.com
Username: USERNAME
Password: PASSWORD
Database: obsidian-livesync
```

---

## Method 2: API (curl — for bulk/scripted creation)

If you need to create many users quickly, use the CouchDB REST API. Run from the homelab server.

### Create a user

```bash
# Set credentials
ADMIN_USER="admin"
ADMIN_PASS="<from ~/database/couchdb/.env>"

curl -X PUT \
  -u ${ADMIN_USER}:${ADMIN_PASS} \
  -H "Content-Type: application/json" \
  -d '{
    "_id": "org.couchdb.user:USERNAME",
    "name": "USERNAME",
    "type": "user",
    "roles": [],
    "password": "PASSWORD"
  }' \
  https://obsync.panomete.com/_users/org.couchdb.user:USERNAME
```

### Grant database access (add to members list)

```bash
# Fetch current security doc
CURRENT_SEC=$(curl -s -u ${ADMIN_USER}:${ADMIN_PASS} \
  https://obsync.panomete.com/obsidian-livesync/_security)

# Add the new user to members and PUT it back
curl -X PUT \
  -u ${ADMIN_USER}:${ADMIN_PASS} \
  -H "Content-Type: application/json" \
  -d "{
    \"admins\": {\"names\": [], \"roles\": []},
    \"members\": {\"names\": [\"obsidian\", \"USERNAME\"], \"roles\": []}
  }" \
  https://obsync.panomete.com/obsidian-livesync/_security
```

> ⚠️ **Important:** When updating `_security`, you must include ALL existing member usernames — the PUT replaces the entire list. You can't append a single user via API without re-sending the full list.

---

## Deleting a User

### Via Fauxton

1. Go to `_users` database
2. Find the document `org.couchdb.user:USERNAME`
3. Click the **trash icon** → confirm deletion
4. Go to `obsidian-livesync` → **Permissions** → remove from members list

### Via API

```bash
# Get the revision first
REV=$(curl -s -u ${ADMIN_USER}:${ADMIN_PASS} \
  https://obsync.panomete.com/_users/org.couchdb.user:USERNAME | python3 -c "import sys,json;print(json.load(sys.stdin)['_rev'])")

# Delete with revision
curl -X DELETE \
  -u ${ADMIN_USER}:${ADMIN_PASS} \
  "https://obsync.panomete.com/_users/org.couchdb.user:USERNAME?rev=${REV}"
```

---

## Security Notes

| Account type | Purpose | Access |
|-------------|---------|--------|
| `admin` | Server management | All databases, config, users |
| Regular user (`obsidian`, etc.) | LiveSync only | Only `obsidian-livesync` DB |

- Regular users **cannot** create other users
- Regular users **cannot** access `_users`, `_replicator`, or server config
- If a vault needs to be isolated per-person, create separate databases (e.g. `obsidian-livesync-personA`) and restrict each user to their own DB
- The `_security` doc controls who can read/write. Without it, the DB is **admin-only** by default
- Always use HTTPS (`https://obsync.panomete.com`) — never expose port 5984 directly
