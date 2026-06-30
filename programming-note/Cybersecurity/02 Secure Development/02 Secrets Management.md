---
tags:
- cybersecurity
- programming
- security
---

# 02 Secrets Management

Secrets are credentials that grant access: passwords, API keys, tokens, certificates, private keys, connection strings. A single leaked secret can compromise your entire system.

---

## The Golden Rules

| Rule | Why |
|------|-----|
| **Never in source code** | Git history is forever. `git revert` doesn't delete. |
| **Never in logs** | Logs are often less secured than code. |
| **Never in environment variables alone** | Too easy to leak (`env` command, `/proc`, crash dumps). |
| **Rotate regularly** | Assume secrets WILL leak. Limit the damage window. |
| **Least privilege** | Each secret grants minimum necessary access. |

---

## Where Secrets Go WRONG

```java
// ❌ Hardcoded in source
String apiKey = "sk_live_abc123def456";
String dbPassword = "admin123";

// ❌ In application.properties (committed to git)
database.password=SuperSecret123

// ❌ In logs
log.info("Connecting with API key: {}", apiKey);

// ❌ In Dockerfile
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG...

// ❌ In docker-compose.yml
environment:
  - DB_PASSWORD=admin123
```

---

## Secrets Management Tools

| Tool | Best For |
|------|----------|
| **HashiCorp Vault** | Enterprise. Dynamic secrets, auto-rotation, audit logging. |
| **AWS Secrets Manager** | AWS-native. Auto-rotation for RDS. |
| **Kubernetes Secrets** | K8s-native. Base64 (NOT encrypted at rest by default — enable!). |
| **SOPS (Mozilla)** | Encrypt secrets in git. Good for GitOps. |
| **.env + .gitignore** | Development only. NEVER for production. |

---

## HashiCorp Vault Example

```java
// Application authenticates to Vault, fetches secrets at runtime
VaultTemplate vault = new VaultTemplate(
    VaultEndpoint.from(new URI("https://vault.internal:8200")),
    new TokenAuthentication("s.abc123...")
);

// Read dynamic database credentials
VaultResponseSupport<DbCredentials> response = vault.read(
    "database/creds/readonly", DbCredentials.class);
DbCredentials creds = response.getData();
// username, password — auto-generated, short-lived, auto-revoked
```

---

## Kubernetes Secrets (with Encryption at Rest)

```yaml
# Enable encryption at rest — cluster-level config
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
```

```yaml
# Mount secret as file (not env var — more secure)
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: db-credentials
```

---

## Git Security

```bash
# Scan repo for accidentally committed secrets
# GitGuardian, TruffleHog, Gitleaks
trufflehog git file://. --since-commit HEAD~100

# If you accidentally committed a secret:
# 1. Rotate the secret IMMEDIATELY (revoke old, issue new)
# 2. THEN clean git history (BFG Repo-Cleaner, git filter-branch)
# 3. Force push

# .gitignore — never committed
.env
*.pem
*.key
secrets/
credentials.json
```

---

## Secret Rotation

| Secret Type | Rotation Cadence | Automation |
|------------|:---------------:|------------|
| Database credentials | 30 days | Vault dynamic secrets |
| API keys | 90 days | Manual + reminder |
| TLS certificates | 90 days (Let's Encrypt: 60d) | cert-manager |
| JWT signing keys | 90 days | Key rotation with grace period |

---

## Sources

- HashiCorp Vault — https://www.vaultproject.io/
- SOPS — https://github.com/getsops/sops
- OWASP Secrets Management Cheat Sheet
