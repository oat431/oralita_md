---
tags:
- database
- nosql
- programming
- sql
---

# 02 Columnar & Graph Databases

When relational doesn't fit: wide-column for massive scale writes, graph for deeply connected data.

---

## Wide-Column — Cassandra

Optimized for **write-heavy, append-only** workloads at massive scale. Think: time-series, event logs, sensor data.

### Data Model

```sql
-- Cassandra Query Language (CQL) — looks like SQL, isn't SQL
CREATE TABLE user_events (
    user_id UUID,
    event_time TIMESTAMP,
    event_type TEXT,
    metadata MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

| Concept | Relational | Cassandra |
|---------|-----------|-----------|
| **Primary Key** | Uniquely identifies a row | Partition key determines which node stores the data |
| **WHERE clause** | Any column with an index | Only partition key + clustering columns |
| **JOINs** | Yes | No — denormalize everything |
| **Transactions** | ACID | Row-level atomicity only |

### When to Use Cassandra

| ✅ Good Fit | ❌ Bad Fit |
|-----------|-----------|
| Write-heavy (thousands/sec) | Complex queries with many WHERE conditions |
| Known query patterns (design for queries first) | Ad-hoc exploration |
| Time-series data | Frequent updates to existing rows |
| Multi-region, always-on | Small datasets (< 100GB) |

```java
// Spring Data Cassandra
@Table("user_events")
public class UserEvent {
    @PrimaryKey
    private UserEventKey key;  // Composite: user_id + event_time
    private String eventType;
    private Map<String, String> metadata;
}

@Repository
public interface UserEventRepo extends CassandraRepository<UserEvent, UserEventKey> {
    @Query("SELECT * FROM user_events WHERE user_id = ?0")
    List<UserEvent> findByUserId(UUID userId);
}
```

---

## Graph — Neo4j

Data where **relationships** are as important as the data itself. Social networks, recommendations, fraud detection.

### Data Model

```
(Alice)-[:FRIEND]->(Bob)
(Alice)-[:PURCHASED]->(Product:Widget)
(Bob)-[:PURCHASED]->(Product:Gadget)
(Bob)-[:PURCHASED]->(Product:Widget)
→ Alice and Bob both bought Widget → recommend Gadget to Alice
```

### Cypher Query Language

```cypher
-- Find friends of friends (2 hops) who bought the same product
MATCH (me:Customer {name: 'Alice'})-[:FRIEND]->(:Customer)-[:FRIEND]->(fof:Customer)
MATCH (fof)-[:PURCHASED]->(p:Product)
WHERE NOT (me)-[:PURCHASED]->(p)
RETURN fof.name, p.name, COUNT(*) AS score
ORDER BY score DESC
LIMIT 5
```

### When to Use Neo4j

| ✅ Good Fit | ❌ Bad Fit |
|-----------|-----------|
| Social graphs, recommendations | Simple CRUD (overkill) |
| Fraud detection (ring patterns) | Tabular reporting |
| Network/IT topology | Bulk data processing |
| Bill of materials, dependency trees | High write-throughput logging |

---

## Comparison

| | Cassandra | Neo4j |
|---|:---:|:---:|
| **Model** | Wide-column | Graph (nodes + relationships) |
| **Strength** | Massive write scale | Deep relationship traversal |
| **Query** | CQL (restricted) | Cypher (expressive) |
| **Scale** | 1000+ nodes | Clustered (fewer nodes, more memory) |
| **Learning Curve** | Medium (query-first design) | Medium (graph thinking) |

---

## Sources

- Cassandra Documentation — https://cassandra.apache.org/doc/latest/
- Neo4j Documentation — https://neo4j.com/docs/
