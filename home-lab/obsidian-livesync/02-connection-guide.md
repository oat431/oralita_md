# Connecting to Obsidian LiveSync

> Step-by-step guide for connecting an Obsidian vault to the self-hosted LiveSync server.
> Prerequisite: you received your **username** and **password** from the vault admin.

---

## Step 1 — Install the Plugin

1. Open **Obsidian** (desktop or mobile)
2. Go to **Settings** (⚙️) → **Community plugins**
3. If restricted mode is on, click **Turn on community plugins**
4. Click **Browse** → search: **Self-hosted LiveSync** → **Install** → **Enable**

> ⚠️ **Before you start:** disable Obsidian Sync, iCloud, OneDrive, or any other sync service writing to the same vault. Two sync systems running together will cause conflicts.

---

## Step 2 — Open the Setup Wizard

1. After enabling, a notice appears: **"Welcome to Self-hosted LiveSync"**
2. Click it to open the onboarding wizard
3. Choose your scenario:

| Scenario | What to select |
|----------|---------------|
| **First device** (server is empty, you have existing notes) | `I am setting this up for the first time` |
| **Additional device** (another device already synced) | `I am adding a device to an existing synchronisation setup` |

---

## Step 3A — First Device: Manual Configuration

> Use this when connecting to a **fresh CouchDB** for the first time.

1. Confirm: "I want to set up a new synchronisation"
2. On **Connection Method**, select:
   ```
   ❌  Use a Setup URI (Recommended)     ← NOT this (we don't have one yet)
   ✅  Configure a remote manually        ← Choose THIS
   ```
3. Click **Proceed with manual configuration**

### End-to-End Encryption

4. Choose whether to encrypt your synced data:
   - **Enable E2E Encryption** (recommended) → enter a strong **Vault encryption passphrase**
   - Store this passphrase safely — **losing it means your synced data is unrecoverable**
   - Optional: enable **Obfuscate Properties** to hide document metadata too

### CouchDB Connection

5. On **Choose a synchronisation remote**, select **CouchDB** → **Continue**
6. Enter the connection details:

   | Field | Value |
   | ------- | ------- | 
   | **CouchDB URL** | `https://obsync.panomete.com` |
   | **Username** | *(your username, e.g. `obsidian`)* |
   | **Password** | *(your password, e.g. `obsidian-livesync`)* |
   | **Database name** | `obsidian-livesync` |

7. Click **Check server requirements** (optional but recommended — verifies the connection)
8. Click **Create or connect to database and continue**
9. You should see **Setup Complete: Preparing to Initialise Server**

### Initialise the Server

10. Click **Restart and Initialise Server**
11. Read the overwrite warning carefully → click **I Understand, Overwrite Server**
    *(This is expected for a first device — it pushes your local vault to the empty server)*
12. If prompted **"No Synchronisation Settings Found"** → select **Use this device's settings**
13. Acknowledge **"All optional features are disabled"** → let it finish

> **Keep Obsidian open** until all progress indicators clear. Large vaults may take several minutes.

### Test

14. Create a test note → wait for it to sync
15. Check the status bar shows 🟢 **LiveSync**

---

## Step 3B — First Device: Setup URI Method (Alternative)

> If the admin generated a Setup URI for you (instead of manual config), use this path.

1. Choose `I am setting this up for the first time`
2. On **Connection Method**, select **Use a Setup URI (Recommended)**
3. **Paste the Setup URI** (starts with `obsidian://setuplivesync?settings=`)
4. Enter the **Setup URI passphrase** (decrypts the URI — different from the vault encryption passphrase)
5. Click **Test Settings and Continue**
6. Follow steps 9-13 above (Restart, Initialise Server, Overwrite warning)

---

## Step 4 — Generate a Setup URI (for Other Devices)

> Once the **first device** is working, generate a Setup URI to quickly configure additional devices.

1. On the **working first device**, open the Command Palette (`Ctrl/Cmd + P`)
2. Run: **Self-hosted LiveSync: Copy settings as a new Setup URI**
3. Enter a **new passphrase** to protect this Setup URI → click OK
4. The Setup URI is copied to your clipboard → click OK

> ⚠️ **Store the Setup URI and its passphrase separately.** The URI is encrypted but contains credentials — protect both. Send them through different channels.

---

## Step 5 — Add Another Device

> For any device AFTER the first one is synced.

1. Install & enable **Self-hosted LiveSync**
2. Open the **"Welcome to Self-hosted LiveSync"** notice
3. Choose **I am adding a device to an existing synchronisation setup**
4. On **Device Setup Method**, select **Use a Setup URI (Recommended)**
5. **Paste the Setup URI** from the first device
6. Enter the **Setup URI passphrase** → click **Test Settings and Continue**
7. Review **Setup Complete: Preparing to Fetch Synchronisation Data**
8. Click **Restart and Fetch Data**
9. When prompted how to handle data:
   - **Empty/new vault** → select **Overwrite all with remote files**
   - **Vault with existing local notes** → choose carefully (see warning below)
10. When asked about extra local files → **Keep local files even if not on remote** (safest)
11. Let it finish — keep Obsidian open until progress indicators clear

> ⚠️ If the vault already has notes that aren't on the server yet, do NOT choose "Overwrite all" — this deletes local-only files. Use the merge strategy instead.

---

## Understanding the Two Passphrases

| Passphrase | What it protects | When you need it |
|------------|-----------------|-----------------|
| **Vault encryption passphrase** | Your synced note data (E2EE) | Configured on first device; same on all devices |
| **Setup URI passphrase** | The Setup URI link itself | Only when using Setup URI to add devices |

These are **two different passwords** — don't confuse them:
- The Setup URI passphrase decrypts the *connection settings link*
- The Vault passphrase decrypts your *actual note content on the server*

---

## Status Indicators

| Icon | Meaning |
|------|---------|
| 🟢 **LiveSync** | Connected, real-time sync active |
| 🟡 **Periodic** | Syncing on a timer |
| 🔴 **Error** | Connection issue |

---

## Troubleshooting

### "The native fetch API failed! Please check CORS settings"
This is a CORS problem on the server. It was fixed once on this homelab (2026-08-13) — the CouchDB config now includes:

```ini
[chttpd]
enable_cors = true

[cors]
origins = app://obsidian.md,capacitor://localhost,http://localhost,https://localhost,https://obsync.panomete.com
credentials = true
headers = accept,authorization,content-type,origin,referer,x-requested-with
methods = GET,PUT,POST,HEAD,DELETE
```

If it recurs, check on the server:
```bash
curl -s -u admin:<pass> http://127.0.0.1:5984/_node/_local/_config/chttpd/enable_cors
curl -s -u admin:<pass> http://127.0.0.1:5984/_node/_local/_config/cors
```
Verify the preflight works:
```bash
curl -si -X OPTIONS -H "Origin: app://obsidian.md" \
  -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: authorization" \
  https://obsync.panomete.com/obsidian-livesync | grep -i access-control
```
Should return `HTTP/1.1 204` + `access-control-allow-origin: app://obsidian.md`.

**Gotchas learned:** `[chttpd] enable_cors = true` is the master switch (default false — CORS silently does nothing without it). Config values with `origins = *` and `credentials = true` conflict; use explicit origins. CouchDB doesn't trim spaces in comma lists — no spaces after commas.

### "Database not found" or "You are not allowed"
The admin hasn't added your username to the database members list yet. Ask them to add you via Fauxton → `obsidian-livesync` → Permissions.

### Sync seems stuck
1. Command Palette → **Self-hosted LiveSync: Rebuild the entire database** (re-uploads everything)
2. Or: **Fetch reboot DB** (re-downloads everything)
3. Check server: `https://obsync.panomete.com/_utils/` should be accessible

### Conflicts (same note edited on two devices)
LiveSync keeps both versions. You'll see a ` (conflict copy)` suffix — manually merge and delete the duplicate.

### Mobile-specific
- Keep Obsidian open during first full sync (iOS kills background apps aggressively)
- Enable **Background sync** in LiveSync settings
- Android: disable battery optimization for Obsidian

---

## Quick Reference

```
Server:    https://obsync.panomete.com
Username:  <your-username>
Password:  <your-password>
Database:  obsidian-livesync
```

For admins, see: [[03-couchdb-user-management]]
