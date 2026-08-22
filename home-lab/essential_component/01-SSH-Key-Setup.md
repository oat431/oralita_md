# 01 — SSH Key Setup

> Key-based authentication to the server. More secure than passwords and enables automation.

---

## Prerequisites

- SSH client installed (built-in on macOS/Linux, use Git Bash on Windows)
- Access to the remote server (username + password for initial setup)

---

## Step 1: Create the `.ssh` directory

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

| Part | What it does |
|------|-------------|
| `mkdir -p ~/.ssh` | Creates the `.ssh` directory in your home folder. `-p` means "don't error if it already exists" |
| `chmod 700` | Sets permissions to **owner-only** (read/write/execute). SSH refuses to work if this directory is world-readable |

**Why:** SSH looks for keys and config in `~/.ssh/`. If it doesn't exist, key generation and SSH connections will fail.

---

## Step 2: Generate a new SSH key pair

```bash
ssh-keygen -t ed25519 -C "flowero@panomete" -f ~/.ssh/id_homelab -N ""
```

| Flag | What it does |
|------|-------------|
| `-t ed25519` | Key type. Ed25519 is the modern standard — faster, shorter, more secure than RSA |
| `-C "flowero@panomete"` | Comment/label. Helps you identify which key is for what. Put the server name or purpose here |
| `-f ~/.ssh/id_homelab` | Output file path. Use a descriptive name like `id_homelab`, `id_work`, `id_friendserver` |
| `-N ""` | Empty passphrase. No password on the key — required for automation (scripts, cron, CI/CD). If you omit this flag, it will prompt for a passphrase |

**Why:** This creates two files:
- `~/.ssh/id_homelab` — **Private key** (never share this, never leave the machine)
- `~/.ssh/id_homelab.pub` — **Public key** (copy this to every server you want to access)

---

## Step 3: Copy the public key to the server

```bash
ssh-copy-id -i ~/.ssh/id_homelab flowero@192.168.1.121
```

| Part | What it does |
|------|-------------|
| `ssh-copy-id` | Built-in tool that appends your public key to the server's `~/.ssh/authorized_keys` file |
| `-i ~/.ssh/id_homelab` | Which key to copy. Points to the `.pub` file automatically |
| `flowero@192.168.1.121` | Username@server-address (IP or hostname) |

**Why:** The server needs your public key in its `authorized_keys` file to recognize you. This command handles it in one step — it will ask for the server password once, then never again.

---

## Step 4: Verify key-based auth works

```bash
ssh -o BatchMode=yes flowero@192.168.1.121 "echo 'key auth works ✅'"
```

| Flag | What it does |
|------|-------------|
| `-o BatchMode=yes` | Disables all interactive prompts (password, passphrase). If the key doesn't work, it fails immediately instead of falling back to password |

**Why:** This confirms the key is working. If it says "Permission denied", the key wasn't copied correctly — go back to Step 3.

---

## Step 5: Enable passwordless sudo (for automation)

Run this **on the server** (SSH in first):

```bash
echo 'flowero ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/flowero
```

| Part | What it does |
|------|-------------|
| `echo '...' \| sudo tee /etc/sudoers.d/flowero` | Creates a sudoers drop-in file that lets `flowero` run any sudo command without entering a password |
| `/etc/sudoers.d/flowero` | Drop-in file. Keeps your custom rule separate from the main sudoers file. Easy to remove later |

**Why:** Automation tools (Ansible, scripts, SSH commands) can't enter interactive passwords. This lets the setup process run sudo commands over SSH without manual input.

**To revoke later:** `sudo rm /etc/sudoers.d/flowero`

---

## Multiple Servers Workflow

```bash
# Generate a key per server (use a descriptive name)
ssh-keygen -t ed25519 -C "friend-server" -f ~/.ssh/id_friendserver -N ""

# Copy to server
ssh-copy-id -i ~/.ssh/id_friendserver flowero@<server-ip>

# Verify
ssh -o BatchMode=yes -i ~/.ssh/id_friendserver flowero@<server-ip> "echo ok"
```

---

## SSH Config shortcut (`~/.ssh/config`)

Create `~/.ssh/config` to avoid typing flags every time:

```
Host homelab
    HostName 192.168.1.121
    User flowero
    IdentityFile ~/.ssh/id_homelab

Host friendserver
    HostName 192.168.1.50
    User flowero
    IdentityFile ~/.ssh/id_friendserver
```

Then just: `ssh homelab` or `ssh friendserver`

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Saving key failed: No such file or directory` | `~/.ssh/` directory doesn't exist | `mkdir -p ~/.ssh && chmod 700 ~/.ssh` |
| `Permission denied (publickey,password)` | Key not in server's `authorized_keys` | Re-run `ssh-copy-id` |
| Key auth works but `BatchMode=yes` fails | Key has a passphrase and agent isn't loaded | Use `-N ""` for automation keys, or `ssh-add` for passphrase keys |
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` | Key file permissions too open | `chmod 600 ~/.ssh/id_homelab` |
