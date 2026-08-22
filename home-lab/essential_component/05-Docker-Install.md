# 05 — Docker + Docker Compose

> Container runtime for all services.

---

## Step 1: Install Docker

```bash
# Add Docker's official GPG key
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## Step 2: Add user to docker group

```bash
sudo usermod -aG docker flowero
```

**Why:** Without this, every `docker` command needs `sudo`. Adding your user to the `docker` group lets you run Docker as a normal user.

**Note:** Log out and back in for the group change to take effect.

---

## Step 3: Verify

```bash
docker --version
docker compose version
docker run hello-world
```

**Why:** Docker is the foundation — every service (Keycloak, databases, your apps) runs in containers. Docker Compose manages multi-container stacks.
