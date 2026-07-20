# Windows Git Bash SSH Workarounds

## Problem: Password-based SSH from Git Bash/MSYS2

Git Bash on Windows doesn't have `sshpass`. Interactive password input doesn't work in automation.

## Solution: SSH_ASKPASS

```bash
# 1. Create password script
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'your-password'
SCRIPT
chmod +x /tmp/ssh_pass.sh

# 2. Use SSH_ASKPASS for commands
export SSH_ASKPASS="/tmp/ssh_pass.sh" SSH_ASKPASS_REQUIRE="force" DISPLAY=":0"
ssh -o StrictHostKeyChecking=no user@server "command"
```

**Clean up after:** `rm /tmp/ssh_pass.sh` (password in plaintext)

## Problem: Ed25519 key with passphrase fails to sign

```
debug1: Server accepts key: ...
debug3: sign_and_send_pubkey: signing using ssh-ed25519 ...
debug2: we did not send a packet, disable method
```

The Windows SSH client (Git Bash) fails to sign with passphrase-protected ed25519 keys even when the agent should handle it.

## Solution: Generate RSA key without passphrase

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "automation"
```

RSA without passphrase works reliably from Windows Git Bash for automation. Keep your passphrase-protected ed25519 key for daily personal use.
