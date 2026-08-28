---
title: Flowero Gate & Guard — Startup Recovery Runbook
tags: [homelab, incident, keycloak, gateway, oauth2, docker]
created: 2026-08-28
---

# Flowero Gate & Guard — Startup Recovery Runbook

> What to do when `flowero-guard` (Keycloak) and/or `flowero-gate` (Spring Cloud
> Gateway) are down. First hit: 2026-08-28 — both containers had been `Exited`
> for ~5 days.
>
> Compose: `~/platform/docker-compose.platform.yml` · Related: [[keycloak]] · [[gateway]] · [[discovery]]

---

## TL;DR of the 2026-08-28 incident

| Container | State | Real cause |
|-----------|-------|-----------|
| `flowero-guard` | `Exited (127)` | Bind-mount source `panomete-realm.json` went missing → Docker auto-created it as an **empty directory** → OCI init refuses to mount a dir onto a file path. |
| `flowero-gate` | `Exited (1)` | **Cascade.** On boot it does OIDC discovery against `https://auth.panomete.com/realms/panomete`. Keycloak was down (+ a transient DNS failure during the restart storm) → Spring context fails → exit 1. |

**Fix applied:** dropped `--import-realm` and the realm-file volume mount from the
`flowero-guard` service. The `panomete` realm already lives in the `keycloak`
Postgres DB, so the import file is dead weight and was the only thing blocking
startup. Removed the bogus directories, recreated both containers. Both healthy.

---

## Why the mount breaks (root mechanism)

The old `flowero-guard` service had:

```yaml
command:
- start
- --import-realm
volumes:
- ./keycloak/flowero-guard/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
```

Docker bind-mount rule: **if the host source path does not exist, the daemon
creates it — as a directory.** Once `panomete-realm.json` (the file) is deleted,
moved, or was never placed there:

1. `docker compose up` recreates `panomete-realm.json` on the host as an empty
   **directory** (owned `root:root`, since the daemon runs as root).
2. Container init tries to mount that directory onto the container's file path
   `/opt/keycloak/data/import/panomete-realm.json` → fails with:
   ```
   not a directory: Are you trying to mount a directory onto a file (or vice-versa)?
   ```
   → exit **127**.
3. You `sudo rm -rf` the directory, run `up` again → back to step 1. Infinite loop.
   (The 2026-08-28 `.bash_history` shows ~15 rounds of exactly this.)

The realm JSON file was **never actually version-controlled on the server** —
`~/platform` is not a git repo, despite what [[keycloak]] claims. There is no
copy of it on the box. That's why the loop was unwinnable without either
recreating the file by hand or removing the dependency.

---

## The decision: drop `--import-realm` permanently

`--import-realm` only imports a realm **if it does not already exist** in the
database. Check:

```bash
docker exec local-postgres psql -U keycloak -d keycloak -tc "select name,enabled from realm;"
# Expect:
#  master   | t
#  panomete | t
```

If `panomete` is there and enabled, the import file does nothing on startup
except log "import skipped" — so the mount is pure liability. Removing it:

```yaml
# flowero-guard service — after
command:
- start
# (no volumes: block)
```

Keycloak boots straight from Postgres. Realm config (clients, roles, scopes,
token lifespans) is unaffected — it's all in the DB.

> If you ever genuinely need to re-seed the realm from JSON (fresh DB, disaster
> recovery), see **Re-importing the realm** below — but do it as a deliberate
> one-off, not as a permanent compose flag.

---

## Recovery procedure

### 1. Triage

```bash
ssh flowero@remote.panomete.com

docker ps -a --format "table {{.Names}}\t{{.Status}}" | grep -E "flowero-|NAMES"
docker inspect flowero-guard --format 'Exit={{.State.ExitCode}} Err={{.State.Error}}'
docker logs --tail 40 flowero-guard 2>&1
docker logs --tail 40 flowero-gate  2>&1
```

Match the symptom:

| Signal | Meaning | Go to |
|--------|---------|-------|
| `guard` Exit 127, `Error` mentions `not a directory` / `mount` | The realm-file mount bug | Step 2 |
| `guard` logs: `password authentication failed` / `Connection refused` | Postgres / creds | [[keycloak]] → "Other startup errors" |
| `guard` healthy, `gate` Exit 1, logs: `UnknownHostException: auth.panomete.com` | DNS during boot | Step 4 |
| `gate` Exit 1, logs: `Unable to resolve Configuration with the provided Issuer` but host reachable | Keycloak was down when gate booted | Fix guard first, then Step 3 |

### 2. Fix `flowero-guard` (the realm-mount bug)

```bash
cd ~/platform
cp docker-compose.platform.yml docker-compose.platform.yml.bak.$(date +%F)

# Remove --import-realm and the realm volume from the flowero-guard service.
# Target block to delete:
#     - --import-realm
#     volumes:
#     - ./keycloak/flowero-guard/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
nano docker-compose.platform.yml

docker compose -f docker-compose.platform.yml config >/dev/null && echo "compose OK"

# Nuke the Docker-created junk dirs (they're empty; rmdir is safe, no sudo rm -rf needed)
sudo rmdir platform/keycloak/flowero-guard/panomete-realm.json \
           platform/keycloak/flowero-guard \
           platform/keycloak 2>/dev/null || sudo rm -rf ~/platform/keycloak

docker compose -f docker-compose.platform.yml up -d flowero-guard
```

Wait ~40s (first boot after image/config change rebuilds the Quarkus augmentation),
then verify:

```bash
docker ps --format "{{.Names}}\t{{.Status}}" | grep flowero-guard   # want: Up ... (healthy)
curl -s -o /dev/null -w "internal %{http_code}\n" http://127.0.0.1:8001/realms/panomete/.well-known/openid-configuration
curl -s -o /dev/null -w "public   %{http_code}\n" https://auth.panomete.com/realms/panomete/.well-known/openid-configuration
```

Both should be `200`.

### 3. Bring up `flowero-gate`

Only after `guard` is **healthy** and the public issuer returns 200 — the
gateway does blocking OIDC discovery at startup and will exit 1 if the issuer
isn't ready.

```bash
cd ~/platform
docker compose -f docker-compose.platform.yml up -d flowero-gate
sleep 35
docker ps --format "{{.Names}}\t{{.Status}}" | grep flowero-gate
docker logs flowero-gate 2>&1 | grep -E "Started FlowerogateApplication|UnknownHost|ERROR" | tail
curl -s http://127.0.0.1:8000/actuator/health          # {"status":"UP"}
curl -s -o /dev/null -w "%{http_code}\n" https://api.panomete.com/actuator/health   # 200
```

`https://api.panomete.com/` returning **401** is correct — that's the gateway
demanding auth, not an error.

### 4. If `gate` still throws `UnknownHostException: auth.panomete.com`

The container can't resolve the public hostname. `auth.panomete.com` is
Cloudflare-fronted; from inside `db-network` it should fall back to Cloudflare's
A records (`172.67.x` / `104.21.x`).

```bash
# Test resolution from the network the gateway lives on:
docker run --rm --network db-network alpine sh -c "getent ahosts auth.panomete.com"
```

- **No output / only IPv6** → `db-network` has no external DNS. This is the
  [[2026-08-24-searxng-dns-outage-fix]] failure mode. Check the host's
  `/etc/resolv.conf` is a real file (`nameserver 127.0.0.1` + a public fallback),
  not a dangling symlink, and that the `adguard` container is up.
- **Resolves fine now** → it was a boot-order race (gateway started before
  AdGuard/DNS was ready). `restart: unless-stopped` should have recovered it;
  if `RestartCount` maxed out and it gave up, just `docker compose up -d
  flowero-gate` again now that DNS is healthy.

---

## Re-importing the realm (deliberate, one-off)

Only needed if the `panomete` realm is genuinely gone from Postgres (fresh DB,
`DROP DATABASE keycloak`, etc.).

**Option A — export from a running Keycloak, keep the file somewhere real:**

```bash
docker exec flowero-guard /opt/keycloak/bin/kc.sh export \
  --dir /tmp/export --realm panomete --users same_file
docker cp flowero-guard:/tmp/export/panomete-realm.json ./panomete-realm.json
# then commit it to an actual repo — NOT a loose file under ~/platform
```

**Option B — one-shot import container (doesn't touch the long-running service):**

```bash
docker run --rm --network db-network \
  -e KC_DB=postgres \
  -e KC_DB_URL=jdbc:postgresql://local-postgres:5432/keycloak \
  -e KC_DB_USERNAME=keycloak -e KC_DB_PASSWORD='<from .env>' \
  -v "$PWD/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro" \
  ghcr.io/oat431/flowero-guard:latest \
  import --file /opt/keycloak/data/import/panomete-realm.json
```

Then start `flowero-guard` normally (still no `--import-realm` flag).

A minimal fallback realm JSON (roles + token lifespans, clients re-registered by
hand afterward) is preserved in [[keycloak]] under "Troubleshooting → panomete-realm.json content".

---

## Prevention / follow-ups

- [x] `--import-realm` + volume mount removed from `flowero-guard` — the loop
      can't recur.
- [ ] **Export the live `panomete` realm and commit it to a real git repo.**
      Right now there is zero backup of the realm config outside the Postgres DB
      (which *is* covered by `~/backups/postgres/pg_dumpall_*.sql.gz`, nightly).
- [ ] `~/platform/` is not a git repo. Consider `git init` so compose changes are
      tracked (the `.env` has secrets — add `.gitignore`).
- [ ] `KC_DB_PASSWORD` and `KC_BOOTSTRAP_ADMIN_PASSWORD` are hardcoded as
      `${VAR:-<default>}` fallbacks in the compose file. Move the real values
      into `~/platform/.env` (chmod 600) and drop the inline defaults.
- [ ] `flowero-gate` depends on `flowero-guard` + `flowero-discover` at boot but
      has no `depends_on`. Consider adding
      `depends_on: { flowero-guard: { condition: service_healthy } }` so a full
      `docker compose up` orders them correctly. (Won't help across host reboots
      if guard's own healthcheck lags — the manual "guard first, then gate" order
      above is still the safe play.)

---

## Quick reference

```bash
# Full platform status
docker compose -f ~/platform/docker-compose.platform.yml ps

# Restart the pair in the correct order
cd ~/platform
docker compose -f docker-compose.platform.yml up -d flowero-guard
sleep 40
docker compose -f docker-compose.platform.yml up -d flowero-gate

# Health
curl -sf http://127.0.0.1:8001/health/ready && echo " guard OK"
curl -s  http://127.0.0.1:8000/actuator/health
```

| Thing | Value |
|-------|-------|
| Keycloak internal | `http://127.0.0.1:8001` (`:9000` = management/metrics) |
| Keycloak public | `https://auth.panomete.com` |
| Gateway internal | `http://127.0.0.1:8000` |
| Gateway public | `https://api.panomete.com` |
| Keycloak DB | `keycloak` on `local-postgres` (user `keycloak`) |
| Realm | `panomete` — clients: `flowero-gateway`, `account`, `admin-cli`, `broker`, `realm-management`, `security-admin-console` |
| Keycloak version | 26.7.0 (Quarkus 3.33) |
| Compose backup | `~/platform/docker-compose.platform.yml.bak.2026-08-28` |

---

## Related

- [[keycloak]] — full Keycloak setup + the older 502 / realm-import troubleshooting
- [[gateway]] — Spring Cloud Gateway config, OAuth2 client, routes
- [[discovery]] — Eureka (`flowero-discover`); gateway registers with it at boot
- [[2026-08-24-searxng-dns-outage-fix]] — the `db-network` external-DNS failure mode
- [[db-network-integration-guide]] — shared infra networking
- Index: [[Homelab-Infra-Checklist]]
