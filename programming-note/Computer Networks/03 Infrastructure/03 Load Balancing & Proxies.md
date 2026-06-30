---
tags:
- networking
- programming
- protocols
---

# 03 Load Balancing & Proxies

Distributing traffic across multiple servers. Reverse proxies sit in front. Load balancers distribute. CDNs cache at the edge.

---

## Reverse Proxy vs Load Balancer

| | Reverse Proxy | Load Balancer |
|---|:---:|:---:|
| **Primary role** | Protect backend. Terminate TLS. Cache. | Distribute traffic. High availability. |
| **Scope** | One backend service | Many backend instances |
| **Examples** | NGINX, Apache, Traefik | NGINX, HAProxy, AWS ALB |
| **Often combined** | ✅ Most load balancers ARE reverse proxies | |

```
Internet → Load Balancer → App Server 1
                         → App Server 2
                         → App Server 3
```

---

## L4 vs L7 Load Balancing

| | Layer 4 (Transport) | Layer 7 (Application) |
|---|:---:|:---:|
| **Works at** | TCP/UDP level | HTTP level |
| **Routing based on** | IP, port | URL path, headers, cookies |
| **TLS Termination** | ❌ (pass-through) | ✅ |
| **Sticky Sessions** | ❌ | ✅ (cookie-based) |
| **Speed** | Faster (less processing) | Slightly slower (more logic) |
| **Use Case** | Simple TCP services | Web applications, APIs |

---

## Load Balancing Algorithms

| Algorithm | How It Works | Best For |
|-----------|-------------|----------|
| **Round Robin** | Each request → next server in list | Equal-capacity servers |
| **Least Connections** | Request → server with fewest active connections | Uneven request durations |
| **IP Hash** | Hash(client IP) → same server every time | Sticky sessions without cookies |
| **Weighted** | Servers with more capacity get more requests | Mixed-capacity servers |
| **Random** | Pick one at random | Simple, surprisingly effective |

---

## NGINX Configuration

```nginx
# Reverse proxy + load balancing
upstream backend {
    least_conn;                    # Algorithm
    server 10.0.1.10:8080 weight=3;  # More capacity
    server 10.0.1.11:8080 weight=2;
    server 10.0.1.12:8080 backup;    # Only if others fail
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # TLS
    ssl_certificate /etc/ssl/certs/api.example.com.pem;
    ssl_certificate_key /etc/ssl/private/api.example.com.key;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health checks
    location /health {
        return 200 "OK";
    }
}
```

---

## Health Checks

> Don't send traffic to dead servers.

| Type | How |
|------|-----|
| **Passive** | Monitor responses. If 5xx → mark unhealthy. |
| **Active** | Periodically GET /health → expect 200. |
| **Graceful shutdown** | Before stopping, signal LB to drain connections. |

```java
// Spring Boot Actuator health endpoint
// GET /actuator/health → {"status":"UP"}
management:
  endpoint:
    health:
      show-details: always
  health:
    db:
      enabled: true      # Check DB connection
    diskspace:
      enabled: true      # Check disk space
```

---

## CDN — Content Delivery Network

> Cache static (and dynamic) content at edge locations close to users.

```
User in Bangkok → CDN Edge (Bangkok) → Origin Server (US East)
                 └─── 20ms ───┘        └──── 200ms ─────┘
```

| CDN | Best For |
|-----|----------|
| **Cloudflare** | All-in-one: CDN, WAF, DDoS, DNS |
| **AWS CloudFront** | AWS-native. Lambda@Edge for custom logic. |
| **Fastly** | Real-time purging. VCL for custom caching. |

---

## Sources

- NGINX Admin Guide — https://nginx.org/en/docs/
- HAProxy Documentation — https://www.haproxy.org/
