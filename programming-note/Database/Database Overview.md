---
tags:
- database
- nosql
- overview
- programming
- sql
---

# Database Design & Management — Overview

Databases are not just storage. They're the foundation that determines how fast, reliable, and scalable your application can be. This vault covers relational fundamentals, NoSQL alternatives, and production operations.

---

## Topics

### 01 Relational Databases

> [[01 SQL Fundamentals]] — DDL, DML, DCL, TCL, joins, subqueries, window functions
> [[01 Normalization]] — 1NF → BCNF, when to denormalize, trade-offs
> [[01 Indexing & Performance]] — B-trees, hash indexes, covering indexes, EXPLAIN plans
> [[01 Transactions & Locking]] — ACID, isolation levels, pessimistic vs optimistic, deadlocks

### 02 NoSQL Databases

> [[02 NoSQL Overview]] — CAP theorem, BASE, when to choose NoSQL over SQL
> [[02 Key-Value & Document]] — Redis (cache/session), MongoDB (flexible schema)
> [[02 Columnar & Graph]] — Cassandra (wide-column), Neo4j (graph relationships)
> [[02 Time-Series & Search]] — InfluxDB (metrics), Elasticsearch (full-text)

### 03 Database Operations

> [[03 Migration & Versioning]] — Flyway, Liquibase, version-controlled schema
> [[03 Backup & Recovery]] — Full, differential, PITR, disaster recovery
> [[03 Scaling Strategies]] — Replication, sharding, read replicas, connection pooling

---

## Quick Decision Matrix

| You Need... | Consider |
|------------|---------|
| Complex queries, transactions, data integrity | PostgreSQL, MySQL (RDBMS) |
| Flexible schema, rapid iteration, nested documents | MongoDB (Document) |
| High-throughput caching, sessions, rate limiting | Redis (Key-Value) |
| Time-series metrics, IoT data | InfluxDB, TimescaleDB |
| Full-text search | Elasticsearch |
| Highly connected data (social graphs, recommendations) | Neo4j (Graph) |
| Massive scale writes, append-heavy | Cassandra (Columnar) |

---

## Sources

- SWEBOK v4 — Chapter 16: Computing Foundations, Section 6: Database Management
- PostgreSQL Documentation — https://www.postgresql.org/docs/
