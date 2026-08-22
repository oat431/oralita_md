# 07 — Cloudflare Tunnel

> Expose web services to the internet without opening ports.

---

## Step 1: Install cloudflared

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install -y cloudflared
```

---

## Step 2: Authenticate

```bash
cloudflared tunnel login
```

Opens a browser. Select your domain. Cloudflare stores credentials in `~/.cloudflared/`.

---

## Step 3: Create a tunnel

```bash
cloudflared tunnel create homelab
```

---

## Step 4: Configure the tunnel

```bash
sudo nano ~/.cloudflared/config.yml
```

```yaml
tunnel: <tunnel-id>
credentials-file: /home/flowero/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: gateway.panomete.com
    service: http://localhost:8000
  - hostname: "*.panomete.com"
    service: http://localhost:80
  - service: http_status:404
```

| Part | What it does |
|------|-------------|
| `tunnel` | Your tunnel ID (from the create command) |
| `credentials-file` | Path to the tunnel credentials JSON |
| `ingress` | Route rules — which domain goes where. `*.panomete.com` catches all subdomains |
| `service: http_status:404` | Catch-all. Required last rule. Returns 404 for unmatched requests |

---

## Step 5: Route DNS

```bash
cloudflared tunnel route dns homelab "*.panomete.com"
cloudflared tunnel route dns homelab gateway.panomete.com
```

---

## Step 6: Run as a service

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

---

## Step 7: Verify

```bash
sudo systemctl status cloudflared
# Then visit https://gateway.panomete.com
```

**Why:** Zero open ports on your router. Cloudflare handles TLS, DDoS protection, and CDN. Your server only makes outbound connections to Cloudflare's edge. No public IP needed.
