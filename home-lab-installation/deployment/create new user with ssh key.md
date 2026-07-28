# Create New Linux User with SSH Key Auth (Behind Tailscale)

> **Created:** 2026-07-28
> **Purpose:** Set up a dedicated user on the Panomete homelab, locked behind Tailscale. Reusable for any service (Minecraft, CI, monitoring, etc.).
> **Server:** `remote.panomete.com` (SSH: `flowero@remote.panomete.com`)

---

## Prerequisites

- SSH access to the server as an existing user (`flowero`)
- Tailscale installed and connected on the server
- `sudo` privileges on the server

---

## Step 1 — Create the New User

SSH in as your current user, then create a new one:

```bash
# SSH in as yourself
ssh flowero@remote.panomete.com

# Create the new user (replace <new-user> with your desired username)
sudo adduser <new-user>

# Add to docker group (so they can manage containers)
sudo usermod -aG docker <new-user>
```

> This sets up a home directory at `/home/<new-user>` and prompts for a password.
> Use `sudo adduser --disabled-password <new-user>` if you only want key auth (no password).

---

## Step 2 — Set Up SSH Key Auth

You have two options:

### Option A — Generate a NEW key pair (recommended, separate identity)

On your **local machine**:

```bash
# Generate a new RSA key pair for the new user
ssh-keygen -t rsa -b 4096 -C "<new-user>@panomete" -f ~/.ssh/<new-user>_rsa

# This creates:
#   ~/.ssh/<new-user>_rsa      (private key — keep safe)
#   ~/.ssh/<new-user>_rsa.pub  (public key — copy to server)
```

Then copy the public key to the server:

```bash
cat ~/.ssh/<new-user>_rsa.pub | ssh flowero@remote.panomete.com \
  "sudo -u <new-user> mkdir -p /home/<new-user>/.ssh && \
   sudo -u <new-user> tee -a /home/<new-user>/.ssh/authorized_keys > /dev/null && \
   sudo -u <new-user> chmod 700 /home/<new-user>/.ssh && \
   sudo -u <new-user> chmod 600 /home/<new-user>/.ssh/authorized_keys"
```

### Option B — Reuse your existing key

If you want to use the same RSA key you already have:

```bash
cat ~/.ssh/id_rsa.pub | ssh flowero@remote.panomete.com \
  "sudo -u <new-user> mkdir -p /home/<new-user>/.ssh && \
   sudo -u <new-user> tee -a /home/<new-user>/.ssh/authorized_keys > /dev/null && \
   sudo -u <new-user> chmod 700 /home/<new-user>/.ssh && \
   sudo -u <new-user> chmod 600 /home/<new-user>/.ssh/authorized_keys"
```

---

## Step 3 — Harden SSH (Disable Password Login)

On the server, edit sshd config:

```bash
sudo nano /etc/ssh/sshd_config
```

Ensure these are set (likely already configured since `flowero` uses key auth):

```
PubkeyAuthentication yes
PasswordAuthentication no          # global — disables password for ALL users
```

Or per-user only (add at the end of the file):

```
Match User <new-user>
    PasswordAuthentication no
    PubkeyAuthentication yes
```

Restart SSH:

```bash
sudo systemctl restart sshd
```

---

## Step 4 — Test the Connection

From your local machine:

```bash
# If you generated a new key (Option A):
ssh -i ~/.ssh/<new-user>_rsa <new-user>@remote.panomete.com

# If you reused your key (Option B):
ssh <new-user>@remote.panomete.com
```

Add this to your `~/.ssh/config` for convenience:

```
Host panomete-<short-name>
    HostName remote.panomete.com
    User <new-user>
    IdentityFile ~/.ssh/<new-user>_rsa
```

Then you can just:

```bash
ssh panomete-<short-name>
```

---

## Step 5 — Tailscale Lockdown (Service Port)

Since the server is already behind Tailscale, your service port is only reachable via Tailscale by default — **as long as you bind it to the Tailscale interface IP** (not `0.0.0.0`).

Find the Tailscale IP:

```bash
tailscale ip -4
```

When running the service container (Docker Compose), bind the port to that IP:

```yaml
ports:
  - "100.x.x.x:<port>:<port>"   # Replace with your server's Tailscale IPv4
```

This ensures the service is **only** accessible over Tailscale — not exposed to the public internet.

---

## Quick Reference

| Step | What | Where |
|------|-------|-------|
| 1 | Create user `<new-user>` | Server (as `flowero`) |
| 2 | Generate / copy SSH key | Local → Server |
| 3 | Disable password auth | Server `sshd_config` |
| 4 | Test SSH | Local |
| 5 | Bind service to Tailscale IP | Docker Compose |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Permission denied (publickey)` | Check file perms: `chmod 700 ~/.ssh`, `chmod 600 ~/.ssh/authorized_keys` on server |
| SSH key not being offered | Verify `IdentityFile` in `~/.ssh/config` or pass `-i` flag explicitly |
| `adduser` asks for password | Use `sudo adduser --disabled-password <new-user>` for key-only setup |
| Service port unreachable | Verify Tailscale IP with `tailscale ip -4` and check Docker port binding |
| Can't `docker` commands as new user | Run `sudo usermod -aG docker <new-user>` then re-login |
