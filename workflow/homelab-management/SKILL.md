---
name: homelab-management
description: "Homelab infrastructure management — server audits, security hardening, Docker stack setup, Cloudflare Tunnel, Tailscale, monitoring, backups. For remote server assessment against checklists, use the audit workflow below."
triggers:
  - homelab audit or checklist
  - remote server health check
  - server security review
  - infrastructure planning or architecture
  - Docker stack setup on a server
  - Cloudflare Tunnel or Tailscale setup
  - self-hosted services management
---

# Homelab Management

## Audit Workflow

When the user asks to check/audit a remote server against a checklist:

1. **Read the checklist first** — load the full checklist file before SSH-ing anywhere
2. **Gather in parallel batches** — group SSH commands by concern (hardware, Docker, security, networking) and run them concurrently. SSH timeouts are common with sudo-heavy commands — break those into smaller calls
3. **Handle `sudo` carefully** — SSH commands with `sudo` hang waiting for a password prompt. Options: (a) ask the user to set up `NOPASSWD` sudoers entry, (b) use the user's own permissions and note what needs root, (c) pipe password via `sudo -S` if the tool allows it
4. **Compile findings in section-by-section tables** — match the checklist structure, one table per section with ✅/⚠️/❌/❓ status indicators
5. **Prioritize findings** — use 🔴 Critical, ⚠️ Priority, ✅ OK severity levels
6. **End with a ranked action list** — top 5 actions, numbered by priority, with concrete next steps

## Report Format

The user prefers:
- **Status tables** per checklist section (| Item | Status | Notes |)
- **Emoji indicators**: ✅ pass, ⚠️ needs attention, ❌ fail, ❓ cannot verify from SSH
- **Priority callouts** before each section's critical findings
- **Code blocks** for exact fixes (SSH config, compose YAML, commands)
- **Top N actions list** at the end — concrete, numbered, actionable
- **Concise notes** — no fluff, just what's wrong and how to fix it

## Common Findings Reference

Load `references/ssh-audit-commands.md` for the SSH command patterns used for server audits. These cover hardware info, Docker inspection, security config, networking, and backup status checks.

## Architecture Diagrams

When the user wants a visual architecture plan for their homelab:
- Use **Mermaid** format (Obsidian-compatible)
- Structure: `flowchart TB` with subgraphs for layers (Edge, Infrastructure, Applications, Data, Backup)
- Use cylinder shapes `[(...)]` for databases, standard shapes for services
- Include emoji in subgraph labels for visual clarity
- Append to the relevant checklist/note file, not a separate file

## Security Hardening Checklist

Common issues found in homelab audits:

| Finding | Why it's bad | Fix |
|---------|-------------|-----|
| SSH `PasswordAuthentication` commented out | Defaults to `yes` on Ubuntu — brute-forceable | Set explicit `no` in sshd_config.d/ |
| Containers bound to `0.0.0.0` | Bypasses reverse proxy, directly accessible from LAN/internet | Bind to `127.0.0.1` in compose ports |
| No firewall (UFW not configured) | All ports open by default | `ufw default deny incoming`, allow 22/80/443 only |
| No backups | Data loss on disk failure | Compose files in git + DB dumps + rclone to B2 |
| No UPS | Filesystem corruption on power loss | Small APC UPS + auto-shutdown script |
| `fail2ban` not installed/active | No brute-force protection | `apt install fail2ban`, enable service |
| Containers with no restart policy | Don't survive reboots | `restart: unless-stopped` in compose |
| No resource limits on containers | One bad container OOM-kills everything | `mem_limit` and `cpus` in compose |
| Nginx proxying HTTP to HTTPS service | "Client sent HTTP request to HTTPS server" error | Use `proxy_pass https://` + `proxy_ssl_verify off` |

## Adding New Services (Nginx + Cloudflare Tunnel)

No DNS changes needed — wildcard `*.domain.com` in tunnel config catches all subdomains. Just add Nginx config and reload.

### HTTP services (most common)

```nginx
server {
    server_name service.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTPS services (Portainer, Keycloak, etc.)

When a service runs on HTTPS internally (self-signed cert):

```nginx
server {
    server_name container.panomete.com;
    location / {
        proxy_pass https://127.0.0.1:PORT;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Pitfall:** "Client sent an HTTP request to an HTTPS server" → add `proxy_pass https://` and `proxy_ssl_verify off`.

## Key Decisions Pattern

When the user wants to "set zero" and rebuild infra:
1. Understand what they're building (read project specs)
2. Propose a target architecture diagram (Mermaid)
3. Ask clarifying questions (hardware, DB needs, backup preferences)
4. Let them confirm before building anything
5. Don't rush to implementation — planning first is the user's stated preference

## SSH from Windows (Git Bash / MSYS2)

When `sshpass` is not available on Windows, use the `SSH_ASKPASS` trick for password-based SSH:

```bash
# Create password script (clean up after key-based auth is set up!)
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'PASSWORD_HERE'
SCRIPT
chmod +x /tmp/ssh_pass.sh

# Connect using SSH_ASKPASS
export SSH_ASKPASS="/tmp/ssh_pass.sh" SSH_ASKPASS_REQUIRE="force" DISPLAY=":0"
ssh -o StrictHostKeyChecking=no user@host "command" < /dev/null
```

**Critical pitfalls:**
- **stdin must be `/dev/null`** — otherwise SSH tries to read password from stdin instead of ASKPASS
- **`DISPLAY=:0` is required** — SSH_ASKPASS only activates when DISPLAY is set (even on Windows/MSYS2)
- **Clean up the password script** after switching to key-based auth: `rm /tmp/ssh_pass.sh`

### ed25519 Key Failure (Windows OpenSSH 9.9 ↔ Ubuntu 26.04 OpenSSH 10.2)

Windows Git Bash ships OpenSSH 9.9 which uses `publickey-hostbound-v00@openssh.com` extension. Ubuntu 26.04's OpenSSH 10.2 accepts the key but the signing step fails silently ("we did not send a packet, disable method").

**Symptoms:** `ssh -vvv` shows "Server accepts key" followed by "Permission denied"

**Workaround:** Generate and use an **RSA 4096** key instead of ed25519:
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "description"
```

### Sudo over Non-Interactive SSH

`sudo` requires a TTY for password prompt. Non-interactive SSH (`ssh user@host "sudo ..."`) hangs or fails with "A terminal is required to authenticate".

**Fix:** Ask the user to set up NOPASSWD sudo on the server:
```bash
echo 'username ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/username
```

This is needed for audit workflows that probe root-only configs (`ufw status`, `sshd -T`, `iptables -L`). Revoke after the task with `sudo rm /etc/sudoers.d/username`.

## Anonymization for Team-Shared Diagrams

When the user shares architecture diagrams in a **team knowledge base** (not their private vault):
- Replace project code names with generic labels: **Service A, Service B, ...**
- Replace personal microservice names (e.g. "Flowero Gate") with generic terms: **API Gateway, Service Discovery, Load Balancer**
- Add a ⚠️ note: "Service names are anonymized — replace with actual project names in your private vault"
- Keep infrastructure tool names (Keycloak, Nginx, PostgreSQL) as-is — those are generic

## Infrastructure Stack Preferences (Panomete)

- **No public IP** — Cloudflare Tunnel for web, Tailscale for SSH/management
- **Multiple DBs** — PostgreSQL, MongoDB, Redis (possibly more)
- **Docker Compose** for service management (not Proxmox/VMs)
- **Nginx** as reverse proxy (already established)
- **Organized compose layout**: `application/`, `database/`, `storage/`, `mq/`
- **Certbot not needed with Cloudflare Tunnel** — TLS terminates at Cloudflare edge, Nginx listens on localhost HTTP only
- **OS: Ubuntu Server LTS** — user chose this over Debian for familiarity
