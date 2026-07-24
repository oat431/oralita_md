# Keycloak

> Identity provider (IAM). OAuth2 / OIDC server for the Panomete Platform.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-23 | **Verified:** Healthy
>
> - Container: `flowero-guard` — Up, healthy
> - Image: `ghcr.io/oat431/flowero-guard:latest` (GHCR)
> - OIDC Discovery: `https://auth.panomete.com/realms/panomete/.well-known/openid-configuration` ✅
> - JWKS: 2 RSA keys ✅
> - Admin Console: `https://auth.panomete.com/admin` — HTTP 302 (redirect to login) ✅
> - Realm: `panomete` imported ✅
> - Permanent admin: Created via Post Install procedure ✅
> - Metrics: `/metrics` on management port 9000 ✅

---

## What & Why

Keycloak is the identity backbone for all Panomete Platform services. It handles:
- User authentication (login, SSO)
- OAuth2 / OIDC token issuance (JWT)
- Role-based access control (RBAC)
- Client management (registering which services can use auth)

In the platform architecture, Keycloak **IS** Flowero Guard — there is no wrapper service.

---

## Setup

**Compose:** `/home/flowero/platform/docker-compose.platform.yml`

| Item | Value |
|------|-------|
| Image | `quay.io/keycloak/keycloak:latest` |
| Container | `flowero-guard` |
| Port | `127.0.0.1:8001` (Keycloak internal `:8080`) |
| Network | `db-network` |
| Database | `keycloak` on shared PostgreSQL 18 (`local-postgres`) |
| Domain | `auth.panomete.com` (via Nginx → Cloudflare) |
| Realm | `panomete` |

---

## Prerequisites (Run Once)

### 1. Create `keycloak` role + database on PostgreSQL

```bash
docker exec -it local-postgres psql -U postgres << 'SQL'
CREATE ROLE keycloak WITH LOGIN PASSWORD 'YOUR_PASSWORD';
CREATE DATABASE keycloak
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
GRANT ALL ON SCHEMA public TO keycloak;
SQL
```

### 2. Add Nginx server block

```bash
sudo tee /etc/nginx/sites-available/auth.panomete.com > /dev/null << 'NGINX'
server {
    server_name auth.panomete.com;
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

sudo ln -s /etc/nginx/sites-available/auth.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

> No DNS changes needed — `*.panomete.com` wildcard already routes to the Cloudflare tunnel.

---

## Deploy

### Compose service definition

```yaml
services:
  flowero-guard:
    image: quay.io/keycloak/keycloak:latest
    container_name: flowero-guard
    ports:
      - "127.0.0.1:8001:8080"
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
      KC_DB_USERNAME: ${KC_DB_USERNAME}
      KC_DB_PASSWORD: ${KC_DB_PASSWORD}
      KC_BOOTSTRAP_ADMIN_USERNAME: ${KC_BOOTSTRAP_ADMIN_USERNAME}
      KC_BOOTSTRAP_ADMIN_PASSWORD: ${KC_BOOTSTRAP_ADMIN_PASSWORD}
      KC_HOSTNAME: auth.panomete.com
      KC_HTTP_ENABLED: "true"
      KC_PROXY_HEADERS: xforwarded
      KC_CACHE: local
    command: ["start", "--import-realm"]
    volumes:
      - ./keycloak/flowero-guard/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
    networks:
      - shared-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G

networks:
  shared-network:
    external: true
    name: db-network
```

### .env file (`~/platform/.env`)

```env
KC_BOOTSTRAP_ADMIN_USERNAME=admin
KC_BOOTSTRAP_ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=YOUR_DB_PASSWORD
```

```bash
chmod 600 ~/platform/.env
cd ~/platform
docker compose -f docker-compose.platform.yml up -d flowero-guard
```

> First boot takes 15-30 seconds — Keycloak runs Liquibase migrations to create its schema.

---

## Access

| Resource | URL |
|----------|-----|
| Admin Console | `https://auth.panomete.com/admin` |
| Account Console | `https://auth.panomete.com/realms/panomete/account` |
| OIDC Discovery | `https://auth.panomete.com/realms/panomete/.well-known/openid-configuration` |
| JWKS (public key) | `https://auth.panomete.com/realms/panomete/protocol/openid-connect/certs` |

**Admin login:** username + password from `.env` file

---

## Common Commands

```bash
# Health check
curl -sf http://localhost:8001/health/ready

# Connect to PostgreSQL keycloak DB
docker exec -it local-postgres psql -U postgres -d keycloak

# View Keycloak logs
docker logs -f flowero-guard

# Restart Keycloak
cd ~/platform && docker compose -f docker-compose.platform.yml restart flowero-guard

# Export realm config (after changes)
# Admin Console → panomete realm → Realm Settings → Action → Partial Export
```

---

## Post Install

> One-time setup after first deployment. Do this before using Keycloak for anything else.

### Create a permanent admin user

`KC_BOOTSTRAP_ADMIN_USERNAME` / `KC_BOOTSTRAP_ADMIN_PASSWORD` always create a **temporary** admin — this is by design in Keycloak 26+ ([GitHub #34768](https://github.com/keycloak/keycloak/issues/34768)). You need to create a permanent admin through the Admin Console.

1. Log in to `https://auth.panomete.com/admin` with the temporary admin credentials
2. Go to **Users** in the left sidebar (under the `master` realm)
3. Click **Create new user**
4. Fill in:
   - Username: your permanent admin username (e.g., `oat431`)
   - Email, First name, Last name
5. Click **Create**
6. Go to the **Credentials** tab → **Set password**
   - Enter your password
   - Toggle **Temporary: OFF** ← important, otherwise you'll be asked to change it on next login
   - Click **Save**
7. Go to the **Role mapping** tab → **Assign role**
   - Search for `admin`
   - Assign the `admin` realm role
8. **Log out** from the temporary admin
9. **Log in** with your new permanent admin
10. Go back to **Users** → find the temporary `admin` user → **Delete** it

> The warning "You are logged in as a temporary admin user" disappears once you log in as the permanent admin.

### Update .env after creating permanent admin

Once you've created the permanent admin, update your `.env` to document the new username (password should NOT be in `.env` — keep it in your password manager):

```env
# Bootstrap admin (temporary — used only for first boot)
KC_BOOTSTRAP_ADMIN_USERNAME=admin
KC_BOOTSTRAP_ADMIN_PASSWORD=<temporary-password>

# Permanent admin (created via Admin Console — see Post Install above)
# Username: oat431 (example)
# Password: stored in password manager, NOT in this file
```

---

## Realm Configuration

The `panomete` realm is version-controlled as JSON at `flowero-guard/panomete-realm.json`. Keycloak imports it on startup via `--import-realm`.

| Item | Value |
|------|-------|
| Realm name | `panomete` |
| Roles | `admin`, `user`, `viewer` |
| Access token lifespan | 5 minutes (300s) |
| SSO session idle timeout | 30 minutes (1800s) |

> After ANY realm change in the Admin Console, export the JSON and commit it to the repo.

---

## Registering a New OAuth2 Client

When onboarding a new service (e.g., Cute Gufo blog):

1. Admin Console → `panomete` realm → Clients → Create client
2. Client ID: `cute-gufo` (service name)
3. Client type: Confidential
4. Standard flow: Enabled (browser login)
5. Service accounts: Enabled (S2S calls)
6. Save → Credentials tab → Copy secret → Add to `~/platform/.env`

---

## Troubleshooting

### 502 Bad Gateway on `auth.panomete.com`

**Most common cause:** Keycloak container is crash-looping, so Nginx has nothing to proxy to.

#### Step 1 — Check if the container is actually running

```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}' | grep flowero-guard
```

If it shows `Restarting` or a high `RestartCount`, it's crash-looping. Check the logs.

#### Step 2 — Check the logs

```bash
docker logs --tail 30 flowero-guard
```

#### Most common root cause: `panomete-realm.json (Is a directory)`

If you see this error in the logs:

```
ERROR: /opt/keycloak/bin/../data/import/panomete-realm.json (Is a directory)
ERROR: Failed to run import
ERROR: Failed to start server in (production) mode
```

**What happened:** When the container started, the `panomete-realm.json` file **didn't exist yet** on the host. Docker's bind mount behavior: if the host path doesn't exist, it **auto-creates a directory** instead of failing. Keycloak then tries to import a directory and crashes.

**Verify:**

```bash
docker exec flowero-guard ls -la /opt/keycloak/data/import/
# If you see: drwxr-xr-x ... panomete-realm.json  ← it's a DIRECTORY (wrong)
# Should be:  -rw-r--r-- ... panomete-realm.json  ← it's a FILE (correct)
```

**Fix:**

```bash
# 1. Stop the container
docker stop flowero-guard && docker rm flowero-guard

# 2. Remove the auto-created directory
rm -rf /home/flowero/platform/keycloak/flowero-guard/panomete-realm.json

# 3. Create the actual JSON file
nano /home/flowero/platform/keycloak/flowero-guard/panomete-realm.json
# Paste the realm JSON below, save

# 4. Verify it's a file now
ls -la /home/flowero/platform/keycloak/flowero-guard/panomete-realm.json
# Should show: -rw-r--r-- ... NOT drwxr-xr-x ...

# 5. Redeploy
cd ~/platform
docker compose -f docker-compose.platform.yml up -d flowero-guard
```

**`panomete-realm.json` content:**

```json
{
    "id": "panomete",
    "realm": "panomete",
    "displayName": "Panomete Platform",
    "enabled": true,
    "sslRequired": "external",
    "registrationAllowed": false,
    "loginWithEmailAllowed": true,
    "duplicateEmailsAllowed": false,
    "resetPasswordAllowed": false,
    "editUsernameAllowed": false,
    "bruteForceProtected": true,
    "roles": {
        "realm": [
            {
                "name": "admin",
                "description": "Full access administrator",
                "composite": false,
                "clientRole": false,
                "containerId": "panomete",
                "attributes": {}
            },
            {
                "name": "user",
                "description": "Standard platform user",
                "composite": false,
                "clientRole": false,
                "containerId": "panomete",
                "attributes": {}
            },
            {
                "name": "viewer",
                "description": "Read-only access",
                "composite": false,
                "clientRole": false,
                "containerId": "panomete",
                "attributes": {}
            },
            {
                "name": "default-roles-panomete",
                "description": "default-roles-panomete",
                "composite": true,
                "composites": {
                    "realm": ["user"]
                },
                "clientRole": false,
                "containerId": "panomete"
            }
        ]
    },
    "clients": [
        {
            "clientId": "account",
            "name": "Account Console",
            "rootUrl": "${authBaseUrl}",
            "baseUrl": "/realms/panomete/account/",
            "surrogateAuthRequired": false,
            "enabled": true,
            "alwaysDisplayInConsole": false,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["/realms/panomete/account/*"],
            "webOrigins": [],
            "notBefore": 0,
            "bearerOnly": false,
            "consentRequired": false,
            "standardFlowEnabled": true,
            "implicitFlowEnabled": false,
            "directAccessGrantsEnabled": false,
            "serviceAccountsEnabled": false,
            "publicClient": false,
            "frontchannelLogout": false,
            "protocol": "openid-connect",
            "attributes": {},
            "authenticationFlowBindingOverrides": {},
            "fullScopeAllowed": false,
            "nodeReRegistrationTimeout": 0,
            "defaultClientScopes": ["web-origins", "profile", "roles", "email"],
            "optionalClientScopes": ["address", "phone", "offline_access", "microprofile-jwt"]
        },
        {
            "clientId": "admin-cli",
            "name": "Admin CLI",
            "surrogateAuthRequired": false,
            "enabled": true,
            "alwaysDisplayInConsole": false,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": [],
            "webOrigins": [],
            "notBefore": 0,
            "bearerOnly": false,
            "consentRequired": false,
            "standardFlowEnabled": false,
            "implicitFlowEnabled": false,
            "directAccessGrantsEnabled": true,
            "serviceAccountsEnabled": false,
            "publicClient": true,
            "frontchannelLogout": false,
            "protocol": "openid-connect",
            "attributes": {},
            "authenticationFlowBindingOverrides": {},
            "fullScopeAllowed": false,
            "nodeReRegistrationTimeout": 0,
            "defaultClientScopes": ["web-origins", "profile", "roles", "email"],
            "optionalClientScopes": ["address", "phone", "offline_access", "microprofile-jwt"]
        }
    ],
    "clientScopes": [
        {
            "name": "web-origins",
            "description": "OpenID Connect scope for add allowed web origins to the access token",
            "protocol": "openid-connect",
            "attributes": {"include.in.token.scope": "true", "display.on.consent.screen": "false"},
            "protocolMappers": [
                {
                    "name": "allowed-origins",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-allowed-origins-mapper",
                    "consentRequired": false,
                    "config": {}
                }
            ]
        },
        {
            "name": "profile",
            "description": "OpenID Connect built-in scope: profile",
            "protocol": "openid-connect",
            "attributes": {"include.in.token.scope": "true", "display.on.consent.screen": "true"},
            "protocolMappers": [
                {"name": "full name", "protocol": "openid-connect", "protocolMapper": "oidc-full-name-mapper", "consentRequired": false, "config": {"id.token.claim": "true", "access.token.claim": "true"}},
                {"name": "family name", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-property-mapper", "consentRequired": false, "config": {"userinfo.token.claim": "true", "user.attribute": "lastName", "id.token.claim": "true", "access.token.claim": "true", "claim.name": "family_name", "jsonType.label": "String"}},
                {"name": "given name", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-property-mapper", "consentRequired": false, "config": {"userinfo.token.claim": "true", "user.attribute": "firstName", "id.token.claim": "true", "access.token.claim": "true", "claim.name": "given_name", "jsonType.label": "String"}},
                {"name": "username", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-property-mapper", "consentRequired": false, "config": {"userinfo.token.claim": "true", "user.attribute": "username", "id.token.claim": "true", "access.token.claim": "true", "claim.name": "preferred_username", "jsonType.label": "String"}}
            ]
        },
        {
            "name": "email",
            "description": "OpenID Connect built-in scope: email",
            "protocol": "openid-connect",
            "attributes": {"include.in.token.scope": "true", "display.on.consent.screen": "true"},
            "protocolMappers": [
                {"name": "email", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-property-mapper", "consentRequired": false, "config": {"userinfo.token.claim": "true", "user.attribute": "email", "id.token.claim": "true", "access.token.claim": "true", "claim.name": "email", "jsonType.label": "String"}}
            ]
        },
        {
            "name": "roles",
            "description": "OpenID Connect scope for add user roles to the access token",
            "protocol": "openid-connect",
            "attributes": {"include.in.token.scope": "true", "display.on.consent.screen": "true"},
            "protocolMappers": [
                {"name": "realm roles", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-realm-role-mapper", "consentRequired": false, "config": {"user.attribute": "foo", "access.token.claim": "true", "claim.name": "realm_access.roles", "jsonType.label": "String", "multivalued": "true"}}
            ]
        }
    ],
    "accessTokenLifespan": 300,
    "accessTokenLifespanForImplicitFlow": 300,
    "ssoSessionIdleTimeout": 1800,
    "ssoSessionMaxLifespan": 36000,
    "eventsEnabled": true,
    "adminEventsEnabled": true,
    "adminEventsDetailsEnabled": false
}
```

> **Prevention:** Always create the `panomete-realm.json` file on the host **before** starting the container. Docker creates directories for non-existent bind mount sources.

---

### Other startup errors

| Log message | Cause | Fix |
|-------------|-------|-----|
| `Connection refused` or `password authentication failed` | Wrong `KC_DB_URL`, `KC_DB_PASSWORD`, or PostgreSQL not running | Verify PostgreSQL is healthy: `docker exec local-postgres pg_isready -U postgres`. Check `.env` credentials. |
| `Liquibase: Update has been unsuccessful` | Corrupted or partial migration | Last resort: `DROP DATABASE keycloak; CREATE DATABASE keycloak OWNER keycloak;` then redeploy. Realm re-imports from JSON. |
| `WARN: Hostname v1 options [proxy] are still in use` | `KC_PROXY=edge` is deprecated in newer Keycloak | Remove `KC_PROXY=edge`, add `KC_PROXY_HEADERS=xforwarded` instead. |
| `WARN: Likely misconfiguration detected. With HTTPS not enabled, proxy-headers unset` | Missing `KC_PROXY_HEADERS` — Keycloak doesn't know it's behind Nginx/Cloudflare | Add `KC_PROXY_HEADERS: xforwarded` to compose env. This tells Keycloak to trust `X-Forwarded-For/Proto/Host` headers. |
| `JOIN sent to xxx timed out` (repeated many times) | JGroups trying to form a distributed cluster on a single-node deployment | Add `KC_CACHE: local` to compose env. Disables distributed caching, cuts startup from ~60s to ~15s. |
| `Unable to find composite client role: view-profile` | Realm JSON references client roles that weren't defined in the JSON. The `default-roles-panomete` composite role tries to reference `account` client roles (`view-profile`, `manage-account`) that don't exist yet. | Remove the client role references from the composite role definition, or drop the DB and re-import with the fixed JSON (see "Database cleanup" below). |
| `KEYCLOAK_ADMIN is deprecated, use KC_BOOTSTRAP_ADMIN_USERNAME instead` | Keycloak 26+ renamed the admin bootstrap env vars | Replace `KEYCLOAK_ADMIN` → `KC_BOOTSTRAP_ADMIN_USERNAME`, `KEYCLOAK_ADMIN_PASSWORD` → `KC_BOOTSTRAP_ADMIN_PASSWORD` in compose. |
| `HTTPS required` (403 on external access) | Keycloak rejects HTTP requests from Nginx because it doesn't know the original request was HTTPS (Cloudflare handles TLS) | Fix Nginx: hardcode `proxy_set_header X-Forwarded-Proto https;` instead of `$scheme`. Since Cloudflare terminates TLS, Nginx always receives HTTP — `$scheme` would be `http`. |

### Recommended compose environment (single-node homelab)

These are the **correct env vars** for running Keycloak behind Nginx + Cloudflare on a single server:

```yaml
environment:
  KC_DB: postgres
  KC_DB_URL: jdbc:postgresql://local-postgres:5432/keycloak
  KC_DB_USERNAME: ${KC_DB_USERNAME}
  KC_DB_PASSWORD: ${KC_DB_PASSWORD}
  KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN}
  KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
  KC_HOSTNAME: auth.panomete.com
  KC_HTTP_ENABLED: "true"
  KC_PROXY_HEADERS: xforwarded   # Trust X-Forwarded-* from Nginx (replaces deprecated KC_PROXY=edge)
  KC_CACHE: local                 # No distributed caching — single node only
```

---

### Database cleanup (drop + recreate)

When the realm import fails partway through (e.g., missing client roles), the database has corrupted/partial data. The safest fix is to drop and recreate it. Keycloak will re-run Liquibase migrations and re-import the realm from scratch.

```bash
# 1. Stop Keycloak
docker stop flowero-guard

# 2. Drop and recreate the keycloak database
docker exec -it local-postgres psql -U postgres << 'SQL'
DROP DATABASE IF EXISTS keycloak;
CREATE DATABASE keycloak
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    OWNER keycloak;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
GRANT ALL ON SCHEMA public TO keycloak;
SQL

# 3. Restart Keycloak (fresh Liquibase + realm import)
cd ~/platform
docker compose -f docker-compose.platform.yml up -d flowero-guard

# 4. Wait and verify
sleep 20
curl -sf http://localhost:8001/health/ready && echo " ✅"
```

> **Note:** This wipes all Keycloak data (users, clients, sessions). The realm will be re-imported from the JSON file. Admin user is recreated from the `KEYCLOAK_ADMIN` env vars.

---

### Quick diagnostic checklist

```bash
# Is the container up?
docker ps | grep flowero-guard

# Is port 8001 bound?
ss -tlnp | grep 8001

# Does Keycloak respond internally?
curl -sf http://localhost:8001/health/ready

# Is Nginx routing correctly?
curl -sf -o /dev/null -w '%{http_code}' -H 'Host: auth.panomete.com' http://localhost

# Does it work externally?
curl -sf -o /dev/null -w '%{http_code}' https://auth.panomete.com/
```

If `curl localhost:8001` returns nothing but the container shows "Up", Keycloak may still be starting (Liquibase + realm import takes 15-30s on first boot).

---

## Related

- [[postgresql]] — Database backend
- [[valkey]] — Used by Gate, not Guard
- [[08.1-Add-Subdomain]] — How the Nginx block works
- [[docker-network]] — Why container names are used for connections
