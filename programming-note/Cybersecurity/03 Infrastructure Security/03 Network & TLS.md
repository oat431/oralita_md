---
tags:
- cybersecurity
- programming
- security
---

# 03 Network & TLS

Network security is the outermost layer. If an attacker can't reach your service, they can't exploit it. TLS ensures that if they can reach it, they can't read or modify the traffic.

---

## The Defense Layers

```
Internet → Firewall → WAF → Load Balancer → TLS Termination → App
```

| Layer | What It Does | Tool |
|-------|-------------|------|
| **Firewall** | Blocks/allows IPs, ports | AWS Security Groups, iptables |
| **WAF** (Web App Firewall) | Blocks SQLi, XSS at HTTP level | AWS WAF, Cloudflare, ModSecurity |
| **DDoS Protection** | Absorbs volumetric attacks | Cloudflare, AWS Shield |
| **TLS** | Encrypts traffic. Authenticates server. | TLS 1.3, Let's Encrypt |

---

## TLS 1.3 — Minimum Standard

```nginx
server {
    listen 443 ssl http2;
    
    # Only TLS 1.2 and 1.3
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Strong ciphers
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    
    # HSTS — enforce HTTPS for 1 year
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

---

## mTLS — Both Sides Authenticate

Standard TLS: client verifies server. mTLS: **both** verify each other. Essential for service-to-service in zero-trust.

```yaml
# Spring Boot mTLS
server:
  ssl:
    enabled: true
    key-store: classpath:server-keystore.p12
    key-store-password: ${KEYSTORE_PASSWORD}
    trust-store: classpath:server-truststore.p12
    trust-store-password: ${TRUSTSTORE_PASSWORD}
    client-auth: need  # Require client certificate
```

---

## Zero-Trust Architecture

> **Never trust, always verify.** No implicit trust based on network location.

| Traditional | Zero-Trust |
|------------|-----------|
| "Inside the network = trusted" | Every request authenticated |
| Perimeter firewall | Identity-based micro-segmentation |
| VPN for remote access | Identity-aware proxy |
| Once inside, lateral movement easy | Every hop verified |

---

## Common Ports — Know What's Open

| Port | Service | Should Be Public? |
|:----:|---------|:-----------------:|
| 22 | SSH | ❌ Internal only or VPN |
| 80/443 | HTTP/HTTPS | ✅ (but redirect 80 → 443) |
| 3306 | MySQL | ❌ Internal only |
| 5432 | PostgreSQL | ❌ Internal only |
| 6379 | Redis | ❌ Internal only |
| 8080 | App (Spring Boot) | ❌ Behind reverse proxy |
| 9090 | Prometheus | ❌ Internal or VPN |
| 27017 | MongoDB | ❌ Internal only |

```bash
# Scan your own server
nmap -sV your-server.com
# If ports 3306, 6379, 27017 show — CLOSE THEM NOW
```

---

## DNS Security

| Threat | Defense |
|--------|---------|
| **DNS spoofing / cache poisoning** | DNSSEC |
| **Domain hijacking** | Registry lock, MFA on DNS provider |
| **Subdomain takeover** | Remove DNS records when deleting cloud resources |

---

## Sources

- Mozilla SSL Configuration Generator — https://ssl-config.mozilla.org/
- Let's Encrypt — https://letsencrypt.org/
- NIST Zero Trust Architecture — SP 800-207
