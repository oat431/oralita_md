---
tags:
- networking
- programming
- protocols
---

# 02 Supporting Protocols

Beyond HTTP: the other protocols that keep the internet running. Email, file transfer, and network management.

---

## SMTP — Sending Email

> Simple Mail Transfer Protocol. Push-only. Sends mail to a mail server.

```java
// Spring Boot — JavaMailSender
@Autowired
private JavaMailSender mailSender;

public void sendOrderConfirmation(Order order) {
    MimeMessage message = mailSender.createMimeMessage();
    MimeMessageHelper helper = new MimeMessageHelper(message);
    helper.setTo(order.getCustomerEmail());
    helper.setSubject("Order #" + order.getId() + " Confirmed");
    helper.setText("<h1>Thank you!</h1><p>Your order has been confirmed.</p>", true);
    mailSender.send(message);
}
```

```yaml
spring:
  mail:
    host: smtp.gmail.com
    port: 587
    username: ${MAIL_USERNAME}
    password: ${MAIL_PASSWORD}
    properties:
      mail.smtp.auth: true
      mail.smtp.starttls.enable: true
```

---

## POP3 / IMAP — Reading Email

| | POP3 | IMAP |
|---|:---:|:---:|
| **Model** | Download and delete | Server-side storage |
| **Multi-device** | ❌ (emails on one device) | ✅ (syncs across devices) |
| **Offline access** | ✅ | ❌ (needs connection) |
| **Port** | 110 (995 SSL) | 143 (993 SSL) |

---

## FTP / SFTP — File Transfer

| | FTP | SFTP |
|---|:---:|:---:|
| **Protocol** | FTP (plain text) | SSH File Transfer Protocol |
| **Encryption** | ❌ (unless FTPS) | ✅ (via SSH) |
| **Ports** | 21 (control), 20 (data) | 22 (same as SSH) |
| **Firewall-friendly** | ❌ (dynamic data ports) | ✅ (single port) |

> **Never use plain FTP in production.** Use SFTP or SCP.

---

## DHCP — Automatic IP Assignment

> "Hey, I'm new here. I need an IP address."

```
Client (DHCP Discover) → Broadcast: "I need an IP!"
Server (DHCP Offer)    → "Here: 192.168.1.100"
Client (DHCP Request)  → "I'll take 192.168.1.100"
Server (DHCP ACK)      → "Confirmed. Lease: 24 hours."
```

### DHCP Lease Process
- Client requests renewal at 50% of lease time
- If no response, retries at 87.5%
- If lease expires, must start over with Discover

---

## SNMP — Network Monitoring

> Simple Network Management Protocol. Polls devices for status. Sends traps on events.

```bash
# Query router uptime
snmpget -v2c -c public 192.168.1.1 sysUpTime.0

# Walk all interfaces
snmpwalk -v2c -c public 192.168.1.1 IF-MIB::ifDescr
```

---

## ICMP — Internet Control Message Protocol

> Not for data transfer. For diagnostics and error reporting.

| Type | Code | Purpose |
|:----:|:----:|---------|
| 0 | 0 | Echo Reply (ping response) |
| 8 | 0 | Echo Request (ping) |
| 3 | 1 | Destination Host Unreachable |
| 3 | 3 | Destination Port Unreachable |
| 11 | 0 | TTL Exceeded (traceroute) |

---

## Sources

- RFC 5321 — SMTP
- RFC 3501 — IMAPv4
- RFC 2131 — DHCP
