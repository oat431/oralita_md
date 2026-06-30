---
tags:
- database
- nosql
- programming
- sql
---

# 01 SQL Fundamentals

SQL is the universal language of relational databases. Every backend developer needs it — regardless of what ORM they use.

---

## The Four SQL Sublanguages

| Sublanguage | What It Does | Keywords |
|------------|-------------|----------|
| **DDL** (Data Definition) | Defines and modifies structure | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** (Data Manipulation) | Reads and modifies data | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** (Data Control) | Manages permissions | `GRANT`, `REVOKE` |
| **TCL** (Transaction Control) | Manages transactions | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

---

## DDL — Building the Structure

```sql
CREATE TABLE orders (
    id          BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id),
    status      VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total       DECIMAL(10,2) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_status CHECK (status IN ('PENDING', 'CONFIRMED', 'SHIPPED', 'CANCELLED'))
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status = 'PENDING';  -- Partial index
```

---

## DML — The Core Operations

### SELECT — The 80/20

```sql
-- Basic
SELECT * FROM orders WHERE customer_id = 42;

-- Join types
-- INNER: only matching rows in both tables
SELECT o.*, c.name FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT: all rows from left table, matching from right (NULL if no match)
SELECT c.*, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;

-- Subquery: query inside query
SELECT * FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE created_at > '2024-01-01'
);

-- Window functions: calculate across related rows without grouping
SELECT 
    customer_id,
    total,
    RANK() OVER (PARTITION BY customer_id ORDER BY total DESC) AS rank,
    SUM(total) OVER (PARTITION BY customer_id) AS customer_total
FROM orders;
```

### INSERT, UPDATE, DELETE

```sql
-- INSERT
INSERT INTO orders (customer_id, total) VALUES (42, 99.99);
INSERT INTO orders (customer_id, total) VALUES 
    (1, 50.00), (2, 75.00), (3, 120.00);              -- Multi-row

-- UPDATE
UPDATE orders SET status = 'CONFIRMED' WHERE id = 123;

-- DELETE
DELETE FROM orders WHERE status = 'CANCELLED' AND created_at < NOW() - INTERVAL '90 days';
```

---

## The 5 Essential Joins

```
INNER JOIN      → rows that match in BOTH tables
LEFT JOIN       → ALL rows from left + matching from right
RIGHT JOIN      → ALL rows from right + matching from left (rare — use LEFT instead)
FULL OUTER JOIN → ALL rows from both (PostgreSQL only among major DBs)
CROSS JOIN      → Cartesian product (every row × every row)
```

---

## Window Functions — The Power Tool

| Function | What It Does |
|----------|-------------|
| `ROW_NUMBER()` | Unique sequential number per partition |
| `RANK()` | Rank with gaps (1, 1, 3) |
| `DENSE_RANK()` | Rank without gaps (1, 1, 2) |
| `LAG(column, n)` | Value from n rows before |
| `LEAD(column, n)` | Value from n rows after |
| `SUM() OVER()` | Running total |

```sql
-- Running balance
SELECT 
    transaction_date,
    amount,
    SUM(amount) OVER (ORDER BY transaction_date) AS running_balance
FROM transactions
WHERE account_id = 42;
```

---

## Common Table Expressions (CTEs)

```sql
-- Make complex queries readable
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', created_at) AS month,
        SUM(total) AS revenue
    FROM orders
    WHERE status != 'CANCELLED'
    GROUP BY 1
)
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / 
          LAG(revenue) OVER (ORDER BY month) * 100, 1) AS growth_pct
FROM monthly_sales
ORDER BY month;
```

---

## ORM vs Raw SQL

| Use ORM When... | Use Raw SQL When... |
|----------------|-------------------|
| Simple CRUD operations | Complex reporting queries |
| You need type safety | Performance is critical |
| Rapid development | Window functions, CTEs, recursive queries |
| Cross-DB portability | Database-specific features |

> **The rule:** Know SQL first. Use ORM for convenience. Never let the ORM be a crutch that prevents you from understanding what queries are actually running.

---

## Sources

- PostgreSQL Documentation — https://www.postgresql.org/docs/current/sql.html
- SWEBOK v4, Section 6: Database Management
