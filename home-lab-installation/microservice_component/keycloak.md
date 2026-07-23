# Keycloak

> Identity provider (IAM). OAuth2 / OIDC server for the Panomete Platform.
> Last updated: 2026-07-23

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
      KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN}
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
      KC_HOSTNAME: auth.panomete.com
      KC_PROXY: edge
      KC_HTTP_ENABLED: "true"
    command: ["start", "--import-realm"]
    volumes:
      - ./flowero-guard/panomete-realm.json:/opt/keycloak/data/import/panomete-realm.json:ro
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
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD
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

## Related

- [[postgresql]] — Database backend
- [[valkey]] — Used by Gate, not Guard
- [[08.1-Add-Subdomain]] — How the Nginx block works
- [[docker-network]] — Why container names are used for connections
