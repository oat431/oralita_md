# 02 — SSH Hardening

> Disable password auth, block root login, whitelist users.

---

## Step 1: Create hardened SSH config

```bash
sudo nano /etc/ssh/sshd_config.d/hardened.conf
```

Add these lines:

```
PasswordAuthentication no
PermitRootLogin no
AllowUsers flowero
```

| Setting | What it does |
|---------|-------------|
| `PasswordAuthentication no` | Only key-based login allowed. Brute-force attacks become impossible |
| `PermitRootLogin no` | Blocks direct root SSH access. Use `sudo` instead |
| `AllowUsers flowero` | Whitelist. Only this user can SSH in. Add more users separated by spaces |

**Why:** After confirming key auth works, lock down SSH so passwords and root login are disabled. This is the #1 server hardening step.

---

## Step 2: Restart SSH

```bash
sudo systemctl restart sshd
```

---

## Step 3: Verify (from another terminal)

```bash
# Should work (key auth)
ssh flowero@192.168.1.121 "echo ok"

# Should fail (password auth disabled)
ssh -o PubkeyAuthentication=no flowero@192.168.1.121 "echo ok"
```
