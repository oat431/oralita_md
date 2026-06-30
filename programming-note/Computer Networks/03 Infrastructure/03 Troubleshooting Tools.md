---
tags:
- networking
- programming
- protocols
---

# 03 Troubleshooting Tools

When something breaks between client and server, these tools tell you where and why. Every backend developer should be fluent in all of them.

---

## The Troubleshooting Flow

```
1. Can the client reach the server at all?         → ping
2. Is DNS resolving correctly?                     → dig / nslookup
3. Is the port open and listening?                  → netstat / ss / telnet
4. Is the HTTP request/response correct?            → curl
5. What's happening on the wire?                    → tcpdump / Wireshark
6. What path does the packet take?                  → traceroute
```

---

## ping — Is It Alive?

```bash
ping api.example.com
# PING api.example.com (198.51.100.42): 56 data bytes
# 64 bytes from 198.51.100.42: icmp_seq=0 ttl=54 time=12.3 ms
# --- api.example.com ping statistics ---
# 5 packets transmitted, 5 received, 0% loss

# Key metrics:
# - Packet loss > 0% → network problem
# - High/varying time → congestion or distance
# - No response → firewall blocking ICMP, or host down
```

---

## dig / nslookup — DNS Resolution

```bash
dig example.com
# ANSWER SECTION:
# example.com.  86400  IN  A  93.184.216.34

dig example.com MX          # Mail servers
dig -x 93.184.216.34        # Reverse lookup
dig +short example.com       # Just the answer
dig @8.8.8.8 example.com    # Query Google's DNS (bypass ISP cache)

nslookup example.com         # Simpler, less detailed
```

---

## netstat / ss — What's Listening?

```bash
# netstat (older, widely available)
netstat -tlnp     # TCP listening ports + process names
netstat -an | grep 8080   # Everything on port 8080

# ss (modern replacement, faster)
ss -tlnp          # TCP listening ports
ss -s             # Summary statistics

# Check if your app is actually listening
ss -tlnp | grep 8080
# LISTEN  0  100  *:8080  *:*  users:(("java",pid=12345,fd=42))
```

---

## curl — The HTTP Swiss Army Knife

```bash
# Basic GET
curl https://api.example.com/health

# POST with JSON
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"customer_id": 42, "items": [{"product": "Widget"}]}'

# Show response headers
curl -I https://api.example.com/

# Verbose — show headers, TLS handshake, timing
curl -v https://api.example.com/

# Timing breakdown
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -o /dev/null -s https://api.example.com/

# Follow redirects
curl -L https://short.link/abc
```

---

## telnet / nc — Raw TCP Connection

```bash
# Test if port is open
telnet api.example.com 443
# Trying 198.51.100.42...
# Connected to api.example.com.  ← Port is open!

# nc (netcat) — more powerful
nc -zv api.example.com 443    # Scan: is port open?
nc -zv api.example.com 80-90  # Scan range
```

---

## traceroute — What Path?

```bash
traceroute api.example.com
# 1  192.168.1.1 (router)  2.3 ms
# 2  10.0.0.1 (ISP gateway)  5.1 ms
# 3  203.0.113.1 (ISP backbone)  12.4 ms
# ...
# 10 198.51.100.42 (api.example.com)  45.2 ms

# * * * = no response (firewall blocking ICMP, router not responding)
```

---

## tcpdump — What's on the Wire?

```bash
# Capture traffic on port 443
tcpdump -i eth0 port 443

# Capture HTTP headers
tcpdump -A -i eth0 port 80

# Capture to file for Wireshark analysis
tcpdump -i eth0 -w capture.pcap

# Capture specific host
tcpdump -i eth0 host 198.51.100.42
```

---

## Wireshark — GUI Deep Dive

> Graphical packet analyzer. Capture or open `.pcap` files. Filter, follow TCP streams, inspect TLS handshakes.

Key filters:
```
http                        # Only HTTP traffic
tcp.port == 8080            # Specific port
ip.addr == 198.51.100.42    # Specific IP
tls.handshake.type == 1     # Client Hello (TLS handshake)
```

---

## Sources

- `man` pages for each tool
- Wireshark User Guide — https://www.wireshark.org/docs/
