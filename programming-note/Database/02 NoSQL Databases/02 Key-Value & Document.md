---
tags:
- database
- nosql
- programming
- sql
---

# 02 Key-Value & Document Databases

Key-value is the simplest NoSQL model — a giant distributed hash map. Document stores extend that to semi-structured JSON documents with query capabilities.

---

## Key-Value — Redis

Redis stores everything in memory. Blazing fast. Not just a cache — a data structure server.

### Core Data Structures

| Structure | Operations | Use Case |
|-----------|-----------|----------|
| **String** | GET, SET, INCR, EXPIRE | Caching, counters, rate limiting |
| **Hash** | HSET, HGET, HGETALL | User sessions, object storage |
| **List** | LPUSH, RPOP, LRANGE | Message queues, activity feeds |
| **Set** | SADD, SINTER, SUNION | Tags, unique visitors, friends |
| **Sorted Set** | ZADD, ZRANGE, ZRANK | Leaderboards, priority queues |

### Common Patterns

```java
// Rate limiter — 100 requests per minute per user
String key = "ratelimit:" + userId;
Long count = redis.opsForValue().increment(key);
if (count == 1) redis.expire(key, 60, TimeUnit.SECONDS);  // First request sets TTL
if (count > 100) throw new RateLimitExceededException();

// Cache with TTL
String cacheKey = "user:" + userId;
User cached = redis.opsForValue().get(cacheKey);
if (cached != null) return cached;
User user = userRepo.findById(userId);
redis.opsForValue().set(cacheKey, user, 10, TimeUnit.MINUTES);

// Distributed lock
Boolean locked = redis.opsForValue()
    .setIfAbsent("lock:order:" + orderId, "locked", 30, TimeUnit.SECONDS);
if (Boolean.TRUE.equals(locked)) {
    try { /* process order */ }
    finally { redis.delete("lock:order:" + orderId); }
}
```

---

## Document — MongoDB

Stores JSON-like documents (BSON). Schema is flexible — each document can have different fields.

### When MongoDB Excels

| ✅ Good Fit | ❌ Bad Fit |
|-----------|-----------|
| Rapid iteration (changing schemas) | Complex transactions across collections |
| Nested, hierarchical data (product catalogs) | Highly relational data with many JOINs |
| Read-heavy, few writes | Write-heavy with strict consistency needs |
| Content management, user profiles, IoT data | Banking, ledger, anything with money |

### Document Design — Embed vs Reference

```json
// ✅ EMBED: One-to-few, read together
{
    "_id": "order_123",
    "customer": {"name": "Alice", "email": "alice@email.com"},
    "items": [
        {"product": "Widget", "qty": 2, "price": 9.99},
        {"product": "Gadget", "qty": 1, "price": 24.99}
    ]
}

// ✅ REFERENCE: One-to-many, independently accessed
// orders collection
{"_id": "order_123", "customer_id": "cust_42", "total": 44.97}
// customers collection
{"_id": "cust_42", "name": "Alice", "email": "alice@email.com"}
```

### Indexing in MongoDB

```javascript
// Single field
db.orders.createIndex({ customer_id: 1 })

// Compound
db.orders.createIndex({ customer_id: 1, status: 1 })

// Text search
db.products.createIndex({ name: "text", description: "text" })
db.products.find({ $text: { $search: "wireless headphones" } })
```

---

## Comparison: Redis vs MongoDB

| | Redis | MongoDB |
|---|:---:|:---:|
| **Storage** | In-memory (with persistence options) | Disk-based |
| **Data Model** | Key-value + data structures | JSON documents |
| **Queries** | Simple key lookups + operations | Rich query language |
| **Speed** | Sub-millisecond | Milliseconds |
| **Durability** | Optional (RDB/AOF snapshots) | Journaled, replication |
| **Best For** | Cache, sessions, counters, queues | Content, catalogs, profiles |

---

## Sources

- Redis Documentation — https://redis.io/docs/
- MongoDB Documentation — https://www.mongodb.com/docs/
