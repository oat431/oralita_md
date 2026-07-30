# Cloudflare Tunnel Setup — Full Workflow

> Step-by-step for creating a Cloudflare Tunnel from scratch. Covers auth, tunnel creation, config, DNS routing, and service installation.

## Prerequisites

- Cloudflare account (free tier)
- Domain added to Cloudflare (nameservers pointed to CF)

## 1. Install cloudflared

On Ubuntu 26.04+, the apt repo may not exist yet. Use binary install:

```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared
rm /tmp/cloudflared
cloudflared version
```

## 2. Authenticate

```bash
cloudflared tunnel login
```

Opens a browser URL. Select the domain to authorize. Saves cert to `~/.cloudflared/cert.pem`.

**Note:** The command blocks until auth completes. If running over SSH, it will timeout — the user must visit the URL while cloudflared waits.

## 3. Create tunnel

```bash
cloudflared tunnel create homelab
```

Outputs:
- Tunnel credentials JSON: `~/.cloudflared/<tunnel-id>.json`
- Tunnel ID

## 4. Configure

```bash
nano ~/.cloudflared/config.yml
```

```yaml
tunnel: <tunnel-id>
credentials-file: /home/<user>/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: '*.example.com'
    service: http://localhost:80
  - hostname: example.com
    service: http://localhost:80
  - service: http_status:404
```

**Key points:**
- Wildcard `*.example.com` catches all subdomains — no per-subdomain DNS needed
- All traffic routes to Nginx on `localhost:80` — Nginx handles subdomain routing
- Last rule MUST be the catch-all `http_status:404`
- Validate with: `cloudflared tunnel ingress validate`

## 5. Route DNS

```bash
cloudflared tunnel route dns homelab '*.example.com'
cloudflared tunnel route dns homelab example.com
```

**Pitfall:** If `example.com` already has an A/CNAME record (e.g., old public IP), the route command fails. Delete the old record in Cloudflare dashboard first, then re-run.

## 6. Install as systemd service

cloudflared's service installer looks for config in `/etc/cloudflared/`, NOT `~/.cloudflared/`:

```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<tunnel-id>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

## 7. Verify

```bash
cloudflared tunnel list
sudo systemctl status cloudflared
sudo journalctl -u cloudflared -n 10
```

Tunnel should show connections (e.g., `1xsin11, 1xsin13`).

## DNS Cleanup (Migration from Public IP)

When migrating from public IP to tunnel:

1. Delete all old A records pointing to the public IP
2. Delete old MX, SPF, DMARC records (if mail server is being removed)
3. Delete service-specific verification TXT records (GitHub Pages, etc.)
4. Keep NS records (Cloudflare manages these)
5. Run `cloudflared tunnel route dns` for root domain and wildcard
6. The wildcard CNAME covers all subdomains automatically — no per-subdomain DNS changes needed

**MVP DNS after cleanup:**

| Type | Name | Value |
|------|------|-------|
| NS | example.com | Cloudflare nameservers |
| CNAME | *.example.com | <tunnel-id>.cfargotunnel.com |
| CNAME | example.com | <tunnel-id>.cfargotunnel.com |

## Adding a New Service Later

No DNS changes needed (wildcard covers it). Just:

1. Add Nginx config for the subdomain
2. Start the Docker container on the right port

The tunnel and wildcard CNAME handle everything else.
