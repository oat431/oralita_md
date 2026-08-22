# GitHub Actions — Tailscale Setup

> How to let GitHub Actions runners reach the homelab server behind Tailscale.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-24 | **Verified:** Working
>
> - CI workflows: ✅ All 3 repos (`ci.yml` + `deploy.yml`)
> - CI runs: ✅ All 3 pass (compile + test + push to GHCR)
> - GHCR images: ✅ `ghcr.io/oat431/flowero-guard`, `flowero-discovery`, `flowero-gateway`
> - Tailscale auth key: ✅ Configured in GitHub secrets
> - SSH deploy key: ✅ Configured in GitHub secrets
> - Manual deploy: ✅ `workflow_dispatch` only (per DEC-007)

---

## Why This Is Needed

The homelab server (`remote.panomete.com`) resolves to a Tailscale IP (`100.73.143.25`). GitHub Actions runners are on the public internet and **cannot reach Tailscale IPs directly**.

To deploy from GitHub Actions, the runner must temporarily join the Tailnet using [`tailscale/github-action`](https://github.com/tailscale/github-action).

```
GitHub Actions Runner (public internet)
  → tailscale/github-action (joins Tailnet)
  → SSH to remote.panomete.com (now reachable)
  → deploy
  → disconnects when job ends (ephemeral node)
```

---

## Prerequisites

- Tailscale account with admin access
- Homelab server already on the Tailnet (`remote.panomete.com` → `100.73.143.25`)
- GitHub repository (will store the secret)

---

## Step 1: Generate a Tailscale Auth Key

1. Go to **https://login.tailscale.com/admin/settings/keys**
2. Click **Generate auth key**
3. Configure:
   - **Description:** `GitHub Actions Deploy`
   - **Reusable:** ✅ Yes (one key for all deploys)
   - **Ephemeral:** ✅ Yes (auto-removes the node after job ends — prevents clutter)
4. Click **Generate**
5. **Copy the key** (starts with `tskey-auth-...`) — you won't see it again

> **Ephemeral** is important: Without it, every deploy creates a permanent Tailscale node entry that you'd have to clean up manually.

---

## Step 2: Add the Auth Key to GitHub Secrets

1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Configure:
   - **Name:** `TS_AUTH_KEY`
   - **Secret:** paste the `tskey-auth-...` key from Step 1
4. Click **Add secret**

---

## Step 3: Generate an SSH Key for Deploy

```bash
# On your PC (or server) — generate a dedicated deploy key
ssh-keygen -t ed25519 -f ~/.ssh/github_actions_deploy -C "github-actions-deploy"

# When prompted for passphrase: press Enter (empty — GitHub can't enter passphrases)
```

This creates:
- `~/.ssh/github_actions_deploy` (private key — goes to GitHub)
- `~/.ssh/github_actions_deploy.pub` (public key — goes to server)

---

## Step 4: Authorize the Public Key on the Server

```bash
# Copy the public key to the homelab server
ssh-copy-id -i ~/.ssh/github_actions_deploy.pub flowero@remote.panomete.com

# Or manually:
cat ~/.ssh/github_actions_deploy.pub | ssh flowero@remote.panomete.com 'cat >> ~/.ssh/authorized_keys'
```

Verify it works:

```bash
# Should connect without password prompt
ssh -i ~/.ssh/github_actions_deploy flowero@remote.panomete.com 'echo SSH OK'
```

---

## Step 5: Add the Private Key to GitHub Secrets

1. Open the private key file and copy the **entire contents**:
   ```bash
   cat ~/.ssh/github_actions_deploy
   ```
   (Must include `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`)

2. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Configure:
   - **Name:** `HOMELAB_SSH_KEY`
   - **Secret:** paste the entire private key
5. Click **Add secret**

---

## Step 6: Verify in a Workflow

Test that both secrets work by adding this to any workflow:

```yaml
jobs:
  test-deploy-access:
    runs-on: ubuntu-latest
    steps:
      - name: Connect to Tailscale
        uses: tailscale/github-action@v3
        with:
          auth-key: ${{ secrets.TS_AUTH_KEY }}
          hostname: github-actions-test

      - name: Test SSH
        uses: appleboy/ssh-action@v1
        with:
          host: remote.panomete.com
          username: flowero
          key: ${{ secrets.HOMELAB_SSH_KEY }}
          script: |
            echo "SSH OK from GitHub Actions"
            docker ps --format '{{.Names}}' | head -5
```

Expected output: `SSH OK from GitHub Actions` followed by container names.

---

## GitHub Secrets Summary

| Secret Name | What | Where It Came From |
|-------------|------|-------------------|
| `TS_AUTH_KEY` | Tailscale auth key (`tskey-auth-...`) | Tailscale admin console → Settings → Keys |
| `HOMELAB_SSH_KEY` | SSH private key (full contents) | `ssh-keygen` on PC → public key added to server |

---

## How It Works in the Deploy Workflow

```yaml
steps:
  # 1. Join Tailnet (GitHub runner → Tailscale network)
  - name: Connect to Tailscale
    uses: tailscale/github-action@v3
    with:
      auth-key: ${{ secrets.TS_AUTH_KEY }}
      hostname: github-actions-deploy

  # 2. SSH to server (now reachable via Tailnet)
  - name: Deploy via SSH
    uses: appleboy/ssh-action@v1
    with:
      host: remote.panomete.com    # Resolves to 100.73.143.25
      username: flowero
      key: ${{ secrets.HOMELAB_SSH_KEY }}
      script: |
        cd ~/platform
        docker compose -f docker-compose.platform.yml pull flowero-gate
        docker compose -f docker-compose.platform.yml up -d flowero-gate

  # 3. Tailscale auto-disconnects when the job ends (ephemeral node removed)
```

---

## Troubleshooting

### "dial tcp: lookup remote.panomete.com: no such host"

**Cause:** Tailscale step failed or hasn't connected yet.

**Fix:** Check that `TS_AUTH_KEY` is correct and not expired. Verify the Tailscale step ran before the SSH step.

### "Permission denied (publickey)"

**Cause:** SSH key not authorized on the server.

**Fix:**
```bash
# Check the public key is in authorized_keys
cat ~/.ssh/authorized_keys
# If missing, re-add:
echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys
```

### "tskey-auth-... is not valid"

**Cause:** Auth key expired or was revoked.

**Fix:** Generate a new auth key from the Tailscale admin console and update the GitHub secret.

### Tailscale nodes piling up

**Cause:** Auth key was not set to **Ephemeral**.

**Fix:** Regenerate the key with "Ephemeral: Yes" checked. Old nodes can be removed from the Tailscale admin console → Machines.

---

## Related

- [[../essential_component/06-Tailscale]] — Original Tailscale server setup
- [[../microservice_component/gateway]] — Gateway deployment (uses this)
- [[../microservice_component/discovery]] — Discover deployment (uses this)
- [[../microservice_component/keycloak]] — Guard deployment (uses this)
