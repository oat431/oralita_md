# 06 — Tailscale

> Zero-config mesh VPN for remote access. No port forwarding needed.

---

## Step 1: Install

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

---

## Step 2: Authenticate

```bash
sudo tailscale up
```

This opens a browser link. Log in with your Tailscale account (Google/GitHub/etc). The server joins your tailnet.

---

## Step 3: Verify

```bash
tailscale status
tailscale ip
```

**Why:** Access your server from anywhere — SSH, Portainer, Grafana — without exposing any ports to the internet. Works behind CGNAT, double NAT, anything. Free for personal use.
