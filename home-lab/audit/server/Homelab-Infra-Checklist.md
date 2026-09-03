---
tags: [homelab, moc, checklist]
---

# Homelab Infra Checklist

> Index of infrastructure audits for `flowero` (192.168.1.121 / Tailscale 100.73.143.25).
> Each audit is a dated snapshot; compare consecutive ones to see drift.

## Audit Log

| Date | Note | Focus |
|------|------|-------|
| 2026-07-19 | [[homelab-infra-audit-2026-07-19]] | First full audit |
| 2026-07-20 | [[homelab-infra-audit-2026-07-20]] | Follow-up fixes |
| 2026-07-21 | [[homelab-infra-audit-2026-07-21]] | Follow-up fixes |
| 2026-07-23 | [[homelab-infra-audit-2026-07-23-eod]] | EOD snapshot |
| 2026-07-24 | [[homelab-infra-audit-2026-07-24]] | Follow-up fixes |
| 2026-07-26 | [[homelab-infra-audit-2026-07-26]] | Latest full audit |
| 2026-07-27 | [[2026-07-27-db-network-migration-and-fixes]] | db-network migration log |
| 2026-08-24 | [[2026-08-24-searxng-dns-outage-fix]] | SearXNG DNS outage — host resolv.conf + AdGuard upstream fix |

## Standing Checklist (verified sections per audit)

1. Hardware & Base Platform
2. Networking
3. Remote Access & Exposure
4. Container Management
5. Storage & Backups
6. Monitoring & Observability
7. Security
8. Services Running (containers + Nginx sites)
9. Maintenance & Operations

## Related

- [[home-lab-installation]] — setup guides (how it was built)
- [[db-network-integration-guide]] — shared database network
- [[home-lab-apps]] — app/port registry
