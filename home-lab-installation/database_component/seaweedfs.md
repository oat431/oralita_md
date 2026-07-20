# SeaweedFS

> S3-compatible object storage. Free and open source (Apache 2.0).
> Last updated: 2026-07-20

---

## Why SeaweedFS over MinIO?

MinIO changed to AGPLv3 licensing with commercial restrictions. SeaweedFS is Apache 2.0 — truly free for any use.

## Architecture

```
Master (metadata) → Volume (data storage) → S3 API (S3 protocol)
                        ↓
                    Filer (web UI / file system interface)
```

## Setup

**Compose:** `/home/flowero/database/seaweedfs/compose.yml`

| Service | Container | Port | Access |
|---------|-----------|------|--------|
| Master | `seaweedfs-master` | `0.0.0.0:9333` | Tailscale only |
| Volume | `seaweedfs-volume` | internal | — |
| Filer | `seaweedfs-filer` | `0.0.0.0:8888` | Tailscale only |
| S3 API | `seaweedfs-s3` | `127.0.0.1:8333` | Via Nginx (`s3.panomete.com`) |

## Access

| Method | URL |
|--------|-----|
| Filer UI | `http://100.73.143.25:8888` |
| Master UI | `http://100.73.143.25:9333` |
| S3 API | `http://s3.panomete.com` (public) or `http://127.0.0.1:8333` (local) |

## S3 Credentials

Config: `/home/flowero/database/seaweedfs/s3.json`

| Key | Value |
|-----|-------|
| Access Key | `oralita` |
| Secret Key | `Saha_6462` |

## Access via rclone

```bash
# Configure
rclone config
# n → s3 → Other → http://127.0.0.1:8333 → access_key → secret_key

# Upload
rclone copy /path/to/file s3:mybucket/

# List
rclone ls s3:mybucket/
```

## Access via Go (AWS SDK)

```go
cfg, _ := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1"))
client := s3.NewFromConfig(cfg, func(o *s3.Options) {
    o.BaseEndpoint = aws.String("http://127.0.0.1:8333")
    o.UsePathStyle = true
})
```

## Access via Nginx (public)

`http://s3.panomete.com` → Nginx → `127.0.0.1:8333`

Nginx config: `/etc/nginx/sites-enabled/s3.conf`

⚠️ **S3 API is public** — credentials required. Filer/Master UI are Tailscale-only (no auth).

## Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `wrong jwt` on Filer | `security.toml` enforcing JWT | Remove `security.toml`, don't use `-s3` flag on filer |
| `maximum recursion depth` (AWS CLI) | Python 3.14 bug in AWS CLI v2.36 | Use rclone or MinIO client (`mc`) instead |
| S3 IAM warning in logs | Missing signing key | Warning only — basic S3 still works |
| S3 `AccessDenied` on root | No credentials provided | Normal — use credentials to access |
