---
tags:
- database
- nosql
- overview
- programming
- sql
---

# 02 NoSQL Overview

NoSQL doesn't mean "no SQL." It means "not only SQL" — databases designed for use cases where relational databases struggle: massive scale, flexible schemas, specialized data models.

---

## CAP Theorem — Pick Two

> A distributed database can provide at most two of: **C**onsistency, **A**vailability, **P**artition Tolerance.

```
       Consistency
          /\
         /  \
        /    \
       / CP   \  CA
      /        \
     /__________\
Availability    Partition Tolerance
         AP
```

| Choice | Databases | Use Case |
|--------|----------|----------|
| **CP** (Consistency + Partition) | HBase, MongoDB (configurable) | Banking, financial systems |
| **AP** (Availability + Partition) | Cassandra, DynamoDB, CouchDB | Social media, IoT, shopping carts |
| **CA** (Consistency + Availability) | Traditional RDBMS (single node) | Systems that don't need to partition |

> In practice: network partitions happen. You're really choosing between **CP** and **AP.**

---

## ACID vs BASE

| | ACID (RDBMS) | BASE (NoSQL) |
|---|-------------|-------------|
| **Strategy** | Consistency first | Availability first |
| **State** | Always consistent | Eventually consistent |
| **Transactions** | Full ACID transactions | Limited or no transactions |
| **Use Case** | Banking, orders, anything with money | Social feeds, analytics, caching |

> **BASE:** **B**asically **A**vailable, **S**oft state, **E**ventual consistency.

---

## When to Choose NoSQL

| Scenario | Why NoSQL |
|----------|----------|
| **Massive horizontal scaling** | RDBMS struggles beyond ~100 nodes. NoSQL (Cassandra, DynamoDB) scales to thousands. |
| **Flexible/evolving schema** | Document stores don't require schema migrations for new fields. |
| **High write throughput** | Cassandra, DynamoDB optimize for writes. RDBMS optimizes for reads. |
| **Specialized queries** | Full-text (Elasticsearch), graph traversal (Neo4j), time-series (InfluxDB). |
| **Low-latency caching** | Redis: sub-millisecond reads. PostgreSQL: ~1ms minimum. |

---

## When to STAY with SQL

| Scenario | Why RDBMS |
|----------|----------|
| **ACID transactions across multiple rows/tables** | NoSQL typically lacks cross-collection transactions. |
| **Complex ad-hoc queries** | SQL is unmatched for joins, aggregations, window functions. |
| **Data integrity constraints** | Foreign keys, check constraints, unique constraints — enforced by DB, not app. |
| **Mature tooling** | ORMs, migration tools, monitoring, backup — decades of ecosystem. |
| **Your data IS relational** | Don't force a graph model onto relational data, or vice versa. |

---

## The Polyglot Persistence Pattern

> Use the right database for the right job — multiple databases in one application.

```
E-Commerce Platform:
├── PostgreSQL  → Orders, customers, inventory (ACID required)
├── Redis       → Shopping cart, session cache, rate limiting
├── Elasticsearch → Product search, full-text
├── Cassandra   → Clickstream analytics, event logging
└── Neo4j       → Product recommendations (graph)
```

---

## Sources

- CAP Theorem — Brewer, Eric. "Towards Robust Distributed Systems," 2000.
- SWEBOK v4, Section 6: Database Management
