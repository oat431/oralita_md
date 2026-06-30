---
tags:
- networking
- overview
- programming
- protocols
---

# Computer Networks — Overview

Networks are the backbone of every distributed system. Every backend developer needs to understand what happens between "the request left the browser" and "the database returned the result." This vault covers the essentials.

---

## Topics

### 01 Fundamentals

> [[01 OSI & TCP-IP Models]] — 7 layers, encapsulation, TCP/IP stack, what happens at each layer
> [[01 IP Addressing & Subnetting]] — IPv4, IPv6, CIDR, subnet masks, NAT, private/public addresses
> [[01 DNS Deep Dive]] — Resolution, record types, TTL, DNSSEC, troubleshooting

### 02 Protocols

> [[02 HTTP & HTTPS]] — Methods, status codes, headers, TLS handshake, HTTP/2, HTTP/3
> [[02 TCP & UDP]] — 3-way handshake, flow control, congestion, when to use UDP
> [[02 Supporting Protocols]] — SMTP, POP3, IMAP, FTP/SFTP, DHCP, SNMP

### 03 Infrastructure

> [[03 Network Security]] — Firewalls, WAF, DDoS, VPN, mTLS, zero-trust
> [[03 Troubleshooting Tools]] — ping, traceroute, netstat, tcpdump, Wireshark, curl, dig
> [[03 Load Balancing & Proxies]] — L4 vs L7, NGINX, HAProxy, reverse proxy, CDN

---

## The Request Journey

```
Browser → DNS lookup → TCP handshake → TLS handshake → HTTP request
  → Load Balancer → Reverse Proxy → App Server → Database
  → Response flows back through each layer
```

Every step in this journey has a protocol, a port, and potential failure modes. Understanding each one makes you a better backend engineer.

---

## Quick Reference

| Protocol | Port | Layer | Purpose |
|----------|:----:|:-----:|---------|
| HTTP | 80 | Application | Web traffic |
| HTTPS | 443 | Application | Secure web traffic |
| DNS | 53 | Application | Name resolution |
| SSH | 22 | Application | Secure shell |
| SMTP | 25 | Application | Email sending |
| FTP | 20/21 | Application | File transfer |
| MySQL | 3306 | Application* | Database |
| PostgreSQL | 5432 | Application* | Database |
| Redis | 6379 | Application* | Cache |

---

## Sources

- SWEBOK v4 — Section 7: Computer Networks and Communications
- Kurose & Ross. *Computer Networking: A Top-Down Approach.*
