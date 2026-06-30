---
tags:
- cybersecurity
- programming
- security
---

# 04 Monitoring & Incident Response

You will be breached. The question is whether you detect it in minutes or months. Monitoring catches attacks. Incident response contains the damage.

---

## What to Monitor

| Category | What to Log | Alert When |
|----------|------------|------------|
| **Authentication** | Login success/failure, MFA events, password resets | 5+ failures in 5 min |
| **Authorization** | Access denied events | Spike in 403s |
| **API** | Request count, error rate, response time | 5xx > 1%, p95 > 1s |
| **Infrastructure** | CPU, memory, disk, network | > 80% utilization |
| **Data** | DB query count, slow queries | Sudden 10x increase |

---

## Log Everything (Except Secrets)

```java
// Structured logging — JSON format
log.info("{}", Json.of(
    "event", "order.created",
    "userId", userId,
    "orderId", orderId,
    "amount", total,
    "ip", request.getRemoteAddr()
));
// Output: {"event":"order.created","userId":"123","orderId":"456",...}
```

### What Every Log Entry Should Have

| Field | Example |
|-------|---------|
| **timestamp** | `2024-06-24T14:32:00.000Z` (ISO 8601, UTC) |
| **service** | `order-service` |
| **traceId** | `abc123...` (links across services) |
| **userId** | `user-456` (or `anonymous`) |
| **event** | `order.created`, `payment.failed` |
| **outcome** | `SUCCESS`, `DENIED`, `ERROR` |
| **sourceIp** | `203.0.113.42` |

---

## Incident Response

### The SANS 6-Step Process

```
1. Preparation  → Have a plan BEFORE the incident
2. Identification → Detect and confirm
3. Containment   → Stop the bleeding
4. Eradication   → Remove the threat
5. Recovery      → Restore normal operations
6. Lessons Learned → Post-mortem. Fix root cause.
```

### First 15 Minutes — Playbook

| Minute | Action |
|--------|--------|
| 0–5 | **Confirm** the incident. Is this a real breach or a false alarm? |
| 5–10 | **Contain**. Revoke compromised keys. Isolate affected systems. Block attacker IPs. |
| 10–15 | **Communicate**. Notify security lead. Start incident log (who, what, when). |

```bash
# Immediate containment — revoke access
# 1. Rotate all secrets that may be compromised
vault lease revoke -prefix database/creds/
# 2. Block attacker IP
iptables -A INPUT -s 198.51.100.23 -j DROP
# 3. Isolate affected pod
kubectl cordon affected-node
```

---

## SIEM (Security Information & Event Management)

Aggregates logs from all systems, correlates events, alerts on threats.

| Tool | Type |
|------|------|
| **ELK Stack** (Elastic) | Open-source. Build your own. |
| **Splunk** | Enterprise. Most features. |
| **Datadog Security** | SaaS. Integrated with APM. |
| **Wazuh** | Open-source XDR. |

---

## Post-Mortem Template

```
Incident: [Title]
Date: [When]
Duration: [Detection → Resolution]
Impact: [What was affected? Data exposed? Users impacted?]

Timeline:
  - 14:32 UTC — Alert fired: 500 error spike
  - 14:35 — Engineer on-call acknowledged
  - 14:42 — Root cause identified: expired DB certificate
  - 14:50 — Certificate renewed, services restored

Root Cause: Expired TLS cert on RDS. No expiry monitoring.

Action Items:
  - [ ] Add cert expiry alerting (30-day warning)
  - [ ] Auto-renew certificates via cert-manager
  - [ ] Update runbook with renewal procedure
```

---

## Sources

- NIST SP 800-61 — Computer Security Incident Handling Guide
- SANS Incident Handler's Handbook
- ELK Stack — https://www.elastic.co/
