---
tags:
- database
- nosql
- programming
- sql
---

# 03 Migration, Backup & Scaling

Databases in production need care. Schema changes must be versioned. Data must be backed up. And when you grow, the database must scale.

---

## Schema Migration — Flyway & Liquibase

> Version control your database schema just like your code. No manual SQL in production. Ever.

### Flyway (Migration-based)

```sql
-- V1__create_users.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- V2__add_name_to_users.sql
ALTER TABLE users ADD COLUMN name VARCHAR(100);

-- V3__create_orders.sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id)
);
```

```yaml
# Spring Boot + Flyway
spring:
  flyway:
    enabled: true
    baseline-on-migrate: true
    locations: classpath:db/migration
```

### Migration Rules

| Rule | Why |
|------|-----|
| **Migrations are immutable** | Once applied, NEVER modify. Add a new migration instead. |
| **One change per migration** | `V3_add_column.sql` and `V4_add_index.sql` — not one mega-migration. |
| **Always reversible** | Write `V3__...sql` AND `U3__...sql` (undo). |
| **Test on copy of production** | Schema changes can lock tables. Test first. |
| **Backward-compatible** | Old app code must work with new schema during deployment. |

---

## Backup & Recovery

| Backup Type | What It Captures | Recovery Time |
|-----------|-----------------|:---:|
| **Full** | Entire database | Slow |
| **Differential** | Changes since last full | Medium |
| **Transaction Log** | Every transaction since last log backup | Fastest |
| **PITR** (Point-in-Time Recovery) | Full + all transaction logs → restore to any moment | Fast |

### PostgreSQL Backup Commands

```bash
# Logical backup (SQL dump) — portable, slower
pg_dump mydb > mydb_backup.sql
pg_restore -d mydb mydb_backup.sql

# Physical backup (file-level) — fast, not portable
pg_basebackup -D /backup/mydb -Ft -z -P

# Continuous archiving (PITR)
# wal_level = replica, archive_mode = on in postgresql.conf
# Replay WAL files to any point in time
```

### Backup Strategy (3-2-1 Rule)

- **3** copies of your data
- **2** different media types (disk + cloud)
- **1** copy off-site
- **Test your restores** — a backup you can't restore is not a backup

---

## Scaling Strategies

### Vertical Scaling (Scale Up)

> Bigger machine: more CPU, RAM, faster disks.

| ✅ Pros | ❌ Cons |
|--------|--------|
| Simple. No code changes. | Cost grows super-linearly. |
| No data distribution complexity. | Hard limit (largest available machine). |
| | Single point of failure. |

### Read Replicas

> Primary handles writes. Replicas handle reads.

```
         ┌──────────┐
  Writes │ Primary  │
  ──────▶│          │──────▶ Replication ──▶ ┌──────────┐
         └──────────┘                        │ Replica 1│ ← Reads
                                             ├──────────┤
                                             │ Replica 2│ ← Reads
                                             └──────────┘
```

```yaml
# Spring Boot — read/write split
spring:
  datasource:
    primary:
      url: jdbc:postgresql://primary:5432/mydb   # Writes
    replica:
      url: jdbc:postgresql://replica:5432/mydb    # Reads
```

### Sharding (Horizontal Partitioning)

> Split data across multiple independent databases by a shard key.

```
user_id % 4 == 0 → Shard 0
user_id % 4 == 1 → Shard 1
user_id % 4 == 2 → Shard 2
user_id % 4 == 3 → Shard 3
```

| ✅ Pros | ❌ Cons |
|--------|--------|
| Near-linear scalability | Complex queries across shards |
| Each shard is independent | Resharding is painful |
| | No cross-shard JOINs or transactions |

### Connection Pooling

```yaml
# HikariCP — default in Spring Boot
spring:
  datasource:
    hikari:
      maximum-pool-size: 20       # Don't exceed DB connection limit
      minimum-idle: 5
      idle-timeout: 300000        # 5 min
      connection-timeout: 30000   # 30 sec — fail fast, don't hang
      max-lifetime: 1800000       # 30 min
```

---

## Sources

- Flyway Documentation — https://flywaydb.org/documentation/
- PostgreSQL Backup Documentation — https://www.postgresql.org/docs/current/backup.html
