---
tags:
- networking
- programming
- protocols
---

# 01 DNS Deep Dive

DNS is the phonebook of the internet. When it breaks, "the internet is down" — even though it's just name resolution failing.

---

## How DNS Resolution Works

```
Browser asks: "What's the IP for api.example.com?"

1. Check browser cache → Not found
2. Check OS cache (hosts file) → Not found
3. Ask DNS Resolver (ISP / 8.8.8.8):
   Resolver: "Hey Root Server, where's .com?"
   Root: "Ask .com TLD at 192.5.6.30"
   Resolver: "Hey .com TLD, where's example.com?"
   TLD: "Ask ns1.example.com at 203.0.113.10"
   Resolver: "Hey ns1.example.com, where's api.example.com?"
   Authoritative: "api.example.com = 198.51.100.42"
4. Resolver returns 198.51.100.42 to browser
5. Resolver caches result for TTL seconds
```

---

## DNS Record Types

| Type | What It Maps | Example |
|:----:|-------------|---------|
| **A** | Domain → IPv4 | `example.com → 93.184.216.34` |
| **AAAA** | Domain → IPv6 | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Domain → Domain (alias) | `www.example.com → example.com` |
| **MX** | Domain → Mail server | `example.com → mail.example.com (priority 10)` |
| **NS** | Domain → Name server | `example.com → ns1.dnsprovider.com` |
| **TXT** | Arbitrary text | SPF records, domain verification |
| **SOA** | Start of Authority | Administrative info about the zone |
| **PTR** | IP → Domain (reverse) | `34.216.184.93.in-addr.arpa → example.com` |
| **SRV** | Service location | `_sip._tcp.example.com → sipserver:5060` |

---

## TTL — Time to Live

> How long a resolver can cache the record before asking again.

| Short TTL (60–300s) | Long TTL (3600–86400s) |
|:---:|:---:|
| Records that change often | Records that rarely change |
| Load-balanced services | MX, NS records |
| CDN with frequent origin changes | TXT verification records |

---

## DNS Tools

```bash
# Look up A record
dig example.com A

# Look up all records
dig example.com ANY

# Reverse lookup
dig -x 93.184.216.34

# Query specific DNS server
dig @8.8.8.8 example.com

# Trace the resolution path
dig +trace example.com

# Check propagation
dig example.com +short
```

---

## Common DNS Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| **Wrong A record** | Traffic goes to wrong IP | Update A record. Wait for TTL expiry. |
| **Missing CNAME** | Subdomain doesn't resolve | Add CNAME record. |
| **Stale cache** | Changes not visible | `dig` with `@1.1.1.1` to bypass ISP cache. |
| **DNSSEC failure** | Domain doesn't resolve | Fix DNSSEC signing. Check DS record at registrar. |
| **NXDOMAIN** | Domain doesn't exist | Check spelling. Check domain hasn't expired. |

---

## DNSSEC — Preventing Spoofing

> Normal DNS: no authentication. Anyone can spoof a response. DNSSEC cryptographically signs records.

```
Without DNSSEC: Attacker can send fake DNS response pointing to their server.
With DNSSEC:    Responses are signed. Fake responses fail validation.
```

---

## Spring Boot — DNS Caching

```java
// Java caches DNS by default — can cause issues with dynamic DNS
// Disable or reduce cache for services with changing IPs
// In $JAVA_HOME/conf/security/java.security:
networkaddress.cache.ttl=60        // Default: -1 (cache forever!)
networkaddress.cache.negative.ttl=10
```

---

## Sources

- RFC 1034/1035 — DNS Specification
- RFC 4033-4035 — DNSSEC
- dig man page — `man dig`
