# GitHub Stats Extended — Self-Hosted Deployment

> **Date:** 2026-08-31
> **Service:** GitHub Stats Extended (successor to `github-readme-stats`)
> **Repo:** <https://github.com/stats-organization/github-stats-extended>
> **Server:** `flowero@remote.panomete.com`
> **Port:** `7010` (host) → `9000` (container)
> **Subdomain:** `ghstatus.panomete.com` (pending DNS A record)

---

## Overview

Self-hosted instance of **GitHub Stats Extended** — a TypeScript/Express.js service that dynamically generates SVG stats cards for GitHub READMEs (fork of `anuraghazra/github-readme-stats`).

**Why self-host:**
- Own GitHub PAT → no shared rate limits
- Custom cache duration (24h default)
- Whitelist control (restrict to specific usernames)
- No reliance on public Vercel instance

---

## Architecture

```
                    ┌──────────────────────┐
 Internet ────────▶│  Nginx (443/80)      │
  ghstatus.        │  ghstatus.panomete.com│
  panomete.com     └────────┬─────────────┘
                            │ proxy_pass
                            ▼
                    ┌──────────────────────┐
                    │  localhost:7010      │
                    │  Docker container    │
                    │  Node 24 + Express   │
                    └────────┬─────────────┘
                             │ GitHub GraphQL API
                             ▼
                    ┌──────────────────────┐
                    │  api.github.com      │
                    │  (PAT authenticated) │
                    └──────────────────────┘
```

| Component | Detail |
|---|---|
| Image | `node:24-alpine` (build + runtime) |
| Build tool | pnpm 10.34.1, `pnpm deploy --legacy` |
| Source | `release` branch of upstream repo |
| Container name | `github-stats-extended` |
| Reverse proxy | Nginx (`ghstatus.panomete.com`) |
| Secrets | `.env` file, `chmod 600` |

---

## File Layout

```
~/application/github-stats-extended/
├── .env                    # Secrets (PAT_1, WHITELIST, etc.)
├── .env.example            # Template
├── docker-compose.yml      # Compose config
├── Dockerfile              # Multi-stage build
├── apps/
│   └── backend/            # Express.js API server
└── packages/
    └── core/               # Card generation library (TypeScript)
```

---

## Dockerfile

Multi-stage build using `pnpm deploy` to flatten the workspace monorepo into a standalone deployment bundle:

```dockerfile
# Build stage
FROM node:24-alpine AS builder
RUN corepack enable && corepack prepare pnpm@10.34.1 --activate
WORKDIR /app

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/core/package.json packages/core/
COPY apps/backend/package.json apps/backend/
COPY tsconfig.base.json tsconfig.json ./
RUN pnpm install --frozen-lockfile

COPY packages/core packages/core
COPY apps/backend apps/backend
RUN pnpm --filter @stats-organization/github-readme-stats-core build
RUN pnpm --filter ./apps/backend/ --legacy deploy ./deployment/

# Production stage
FROM node:24-alpine AS runner
WORKDIR /app
COPY --from=builder /app/deployment ./deployment
ENV NODE_ENV=production
ENV PORT=9000
EXPOSE 9000
WORKDIR /app/deployment
CMD ["node", "express.js"]
```

### Build pitfalls encountered

| Issue | Root cause | Fix |
|---|---|---|
| `ERR_MODULE_NOT_FOUND: axios` | Manual `COPY node_modules` doesn't resolve pnpm workspace symlinks | Use `pnpm deploy --legacy` |
| `ERR_MODULE_NOT_FOUND: express` | `express` is a `devDependency` in backend; `--prod` strips it | Remove `--prod` from deploy command |
| `.env` changes not picked up on `restart` | Docker Compose `restart` doesn't reload `.env` | Must `docker compose down && docker compose up -d` |

---

## docker-compose.yml

```yaml
services:
  github-stats:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: github-stats-extended
    restart: unless-stopped
    ports:
      - "7010:9000"
    env_file:
      - .env
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:9000/api/status/up"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
```

---

## Environment Variables (.env)

| Variable | Value | Purpose |
|---|---|---|
| `PAT_1` | `ghp_***` (secret) | GitHub Personal Access Token |
| `CACHE_SECONDS` | `86400` | 24h cache for generated cards |
| `UPDATE_AFTER_HOURS` | `11` | Proactively regenerate after 11h |
| `DELETE_AFTER_HOURS` | `192` | Stop regenerating unused cards after 8d |
| `WHITELIST` | `floweroloveflower,anuraghazra,oat431` | Allowed usernames |
| `FETCH_MULTI_PAGE_STARS` | `true` | Fetch all stars for accurate counts |

### PAT requirements

Classic token scopes: `repo`, `read:user`
Or fine-grained: read-only on commits, issues, PRs, metadata, commit statuses.

---

## Nginx Configuration

File: `/etc/nginx/sites-available/ghstatus.panomete.com`

```nginx
server {
    server_name ghstatus.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:7010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 8 8k;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }
}
```

**DNS pending:** A record for `ghstatus` → server IP.
Once DNS propagates + Certbot SSL, the subdomain will serve HTTPS.

---

## API Endpoints

Base URL (until DNS): `http://remote.panomete.com:7010`
After DNS: `https://ghstatus.panomete.com`

> ⚠️ **No trailing slashes** on the path — the router uses exact string matching.

| Endpoint | Description | Example |
|---|---|---|
| `/api` | Stats card | `?username=oat431&show_icons=true&theme=radical` |
| `/api/top-langs` | Top languages | `?username=oat431&theme=tokyonight` |
| `/api/pin` | Pin a repo | `?username=oat431&repo=my-repo` |
| `/api/gist` | Pin a gist | `?id=<gist_id>` |
| `/api/wakatime` | WakaTime stats | `?username=<waka_user>` |
| `/api/status/up` | Health check | Returns `true` |
| `/api/status/pat-info` | PAT status | JSON with valid/expired/exhausted |

### Common themes

`radical`, `tokyonight`, `merko`, `gruvbox`, `dark`, `dracula`, `onedark`, `cobalt`, `synthwave`, `transparent`

### README embedding example

```markdown
![GitHub Stats](https://ghstatus.panomete.com/api?username=oat431&show_icons=true&theme=radical)
![Top Languages](https://ghstatus.panomete.com/api/top-langs?username=oat431&theme=tokyonight&langs_count=6)
![Pinned Repo](https://ghstatus.panomete.com/api/pin?username=oat431&repo=my-repo)
```

---

## Operations

### Health check

```bash
curl http://localhost:7010/api/status/up
# Returns: true

curl http://localhost:7010/api/status/pat-info | python3 -m json.tool
# Shows validPATs, remaining quota
```

### Adding a user to whitelist

```bash
cd ~/application/github-stats-extended
nano .env                          # edit WHITELIST=... line
docker compose down && docker compose up -d   # full cycle required (restart won't reload .env)
```

### Updating to latest release

```bash
cd ~/application/github-stats-extended
git fetch origin && git checkout release && git pull origin release
docker compose build --no-cache
docker compose down && docker compose up -d
```

### Rebuilding after Dockerfile changes

```bash
cd ~/application/github-stats-extended
docker compose build --no-cache
docker compose down && docker compose up -d
```

### Logs

```bash
docker logs github-stats-extended --tail 50
```

---

## Monitoring

**Uptime Kuma** monitor configured:
- **Name:** GitHub Stats Extended
- **Type:** HTTP(s)
- **URL:** `http://127.0.0.1:7010/api/status/up`
- **Keyword:** `true`
- **Interval:** 60s
- **Retries:** 3

Visible at <https://status.panomete.com/dashboard>

---

## Related

- [[2026-08-28-uptime-kuma-dns-outage-fix]] — Kuma DNS/SQLite notes
- [[db-network-integration-guide]] — db-network shared across services
