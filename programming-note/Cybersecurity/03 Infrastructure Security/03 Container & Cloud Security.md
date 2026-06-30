---
tags:
- cybersecurity
- programming
- security
---

# 03 Container & Cloud Security

Containers and cloud shift the security boundary. Misconfigured S3 buckets and privileged Docker containers have caused more breaches than exotic zero-days.

---

## Docker Security

```dockerfile
# ❌ Common mistakes
FROM ubuntu:latest                    # Use specific version, not :latest
USER root                             # Never run as root
COPY . /app                           # Copies .env, .git, secrets

# ✅ Secure Dockerfile
FROM eclipse-temurin:17-jdk-alpine@sha256:abc123...  # Digest pinning
RUN addgroup -S app && adduser -S app -G app         # Non-root user
COPY --chown=app:app target/app.jar /app/app.jar      # Minimal copy
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:8080/actuator/health || exit 1
```

| Rule | How |
|------|-----|
| **No root** | `USER` directive. Containers can still escape to host. Root makes it worse. |
| **Read-only filesystem** | `docker run --read-only`. Immutable in production. |
| **Minimal base image** | `alpine`, `distroless`. Smaller = fewer CVEs. |
| **No secrets in image** | Secrets at runtime via Vault, K8s Secrets, env. |
| **Scan images** | Trivy, Snyk Container. Every build, every push. |

```bash
# Scan image before pushing
trivy image myapp:latest
# Fail build if CRITICAL CVEs found
trivy image --severity CRITICAL --exit-code 1 myapp:latest
```

---

## Kubernetes Security

### Pod Security

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    readOnlyRootFilesystem: true
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]            # Drop all Linux capabilities
      seccompProfile:
        type: RuntimeDefault     # Restrict syscalls
```

### RBAC — Least Privilege

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: order-service-role
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
  resourceNames: ["order-service-config", "order-db-credentials"]
# Only what order-service NEEDS — not wildcards
```

---

## Cloud Security (AWS)

| Service | Common Misconfig | Fix |
|---------|-----------------|-----|
| **S3** | Public bucket (`s3:GetObject` → `*`) | Block public access. Use bucket policies. |
| **IAM** | Overly permissive roles (`*:*`) | Least privilege. Resource-level permissions. |
| **RDS** | Publicly accessible DB | VPC-only. Bastion for access. |
| **Security Groups** | `0.0.0.0/0` on all ports | Restrict to specific IPs/services. |
| **CloudTrail** | Not enabled | Enable everywhere. Log all API calls. |

---

## IAM — The Hardest Cloud Skill

```json
// ❌ Too broad
{
    "Effect": "Allow",
    "Action": "s3:*",
    "Resource": "*"
}

// ✅ Least privilege
{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::my-app-uploads/*"
}
```

| Best Practice | Why |
|--------------|-----|
| **Roles over users** | Temporary credentials, no long-lived access keys |
| **MFA for root** | Non-negotiable |
| **Permission boundaries** | Limit what roles can delegate |
| **SCP** (Service Control Policies) | Organization-wide guardrails |

---

## Sources

- Docker Security — https://docs.docker.com/engine/security/
- Kubernetes Security — https://kubernetes.io/docs/concepts/security/
- AWS Well-Architected — Security Pillar
