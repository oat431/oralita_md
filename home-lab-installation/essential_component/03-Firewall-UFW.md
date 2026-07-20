# 03 — Firewall (UFW)

> Default deny all inbound. Only allow what's needed.

---

## Step 1: Enable UFW with default rules

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

| Command | What it does |
|---------|-------------|
| `ufw default deny incoming` | Block all inbound connections by default |
| `ufw default allow outgoing` | Allow all outbound connections (server needs to reach the internet) |
| `ufw allow ssh` | Allow port 22 (SSH). Without this, you lock yourself out |
| `ufw enable` | Activate the firewall. Will ask for confirmation |

---

## Step 2: Verify

```bash
sudo ufw status verbose
```

**Why:** Defense in depth. Even if a service accidentally binds to `0.0.0.0`, the firewall blocks external access. Only SSH is exposed — everything else goes through Cloudflare Tunnel later.
