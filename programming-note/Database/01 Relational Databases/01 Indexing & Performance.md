---
tags:
- database
- nosql
- programming
- sql
---

# 01 Indexing & Performance

Indexes are the #1 lever for database performance. A single index can turn a 30-second query into 5 milliseconds. A missing index can bring your production database to its knees.

---

## How B-Tree Indexes Work

The default index type in PostgreSQL, MySQL, Oracle. A balanced tree structure:

```
                    [50 | 80]
                   /    |    \
           [10|30]   [60|70]   [90|99]
           /  |  \    /  |  \    /  |  \
        ... leaf nodes with pointers to actual rows ...
```

- O(log n) lookup, insert, delete
- Supports equality (`=`) and range queries (`>`, `<`, `BETWEEN`)
- Supports prefix matching (`LIKE 'ABC%'` — but NOT `LIKE '%ABC'`)

---

## What to Index

| Index This | Don't Index This |
|-----------|-----------------|
| Primary keys (automatic) | Low-cardinality columns (boolean, status with 2 values) |
| Foreign keys | Columns never used in WHERE/JOIN/ORDER BY |
| Columns in WHERE clauses | Tables with heavy writes and few reads |
| Columns in JOIN conditions | Very small tables (< 1000 rows) |
| Columns in ORDER BY / GROUP BY | |
| Columns used for range queries | |

---

## Index Types

| Type | Best For | Database Support |
|------|----------|:---:|
| **B-Tree** | General purpose: =, >, <, BETWEEN, ORDER BY | All |
| **Hash** | Equality only (=). Faster than B-tree for =. NOT for range. | PostgreSQL |
| **GIN** (Generalized Inverted) | Full-text search, array containment, JSONB | PostgreSQL |
| **GiST** | Geometric data, full-text search | PostgreSQL |
| **BRIN** (Block Range) | Very large tables with natural sort order (time-series) | PostgreSQL |
| **Partial** | Index only rows matching a condition (WHERE status = 'active') | PostgreSQL, SQL Server |
| **Covering** | Index includes ALL columns needed for query — no table lookup | PostgreSQL, MySQL (InnoDB) |

---

## Reading EXPLAIN Plans

```sql
EXPLAIN ANALYZE
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'PENDING'
ORDER BY o.created_at DESC
LIMIT 50;
```

### What to Look For

| Plan Keyword | What It Means |
|-------------|--------------|
| `Seq Scan` | Full table scan. Slow on large tables. Needs index. |
| `Index Scan` | Using index + reading table rows. OK. |
| `Index Only Scan` | All data in index. No table access. **Best.** |
| `Bitmap Index Scan` | Combining multiple indexes. Good for complex WHERE. |
| `Nested Loop` | Join strategy: for each row in A, look up B. Good for small result sets. |
| `Hash Join` | Build hash table of one side. Good for medium-large joins. |
| `Merge Join` | Both sides sorted, merge like merge sort. Good for large ordered joins. |

---

## Common Performance Patterns

### 1. Missing Index on Foreign Key

```sql
-- ❌ Every DELETE on customers scans orders
DELETE FROM customers WHERE id = 42;

-- ✅ Add index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### 2. LIKE with Leading Wildcard

```sql
-- ❌ Can't use B-tree index — scans entire table
SELECT * FROM products WHERE name LIKE '%widget%';

-- ✅ Solution: Full-text search (GIN index)
CREATE INDEX idx_products_name_fts ON products USING gin(to_tsvector('english', name));
SELECT * FROM products WHERE to_tsvector('english', name) @@ to_tsquery('widget');
```

### 3. Function in WHERE

```sql
-- ❌ Can't use index on created_at — function prevents it
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';

-- ✅ Use range query
SELECT * FROM orders WHERE created_at >= '2024-01-15' 
                       AND created_at < '2024-01-16';
```

### 4. N+1 Queries (Application-Level)

```java
// ❌ N+1: 1 query for orders, then N queries for customers
List<Order> orders = orderRepo.findAll();           // 1 query
for (Order o : orders) {
    Customer c = customerRepo.findById(o.getCustomerId());  // N queries!
}

// ✅ JOIN FETCH: 1 query
@Query("SELECT o FROM Order o JOIN FETCH o.customer")
List<Order> findAllWithCustomer();
```

---

## Sources

- PostgreSQL Index Documentation — https://www.postgresql.org/docs/current/indexes.html
- use-the-index-luke.com — Visual SQL indexing tutorial
