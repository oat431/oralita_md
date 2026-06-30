---
tags:
- database
- nosql
- programming
- sql
---

# 01 Normalization

Normalization eliminates data redundancy. Done right, your database is consistent and efficient. Done wrong, you get update anomalies and wasted storage.

---

## Why Normalize?

### The Problem: Update Anomalies

```sql
-- Unnormalized: courses table stores instructor info per row
course_id | course_name | instructor_name | instructor_email
CS101     | Intro to CS | Dr. Smith       | smith@univ.edu
CS102     | Data Struct | Dr. Smith       | smith@univ.edu
CS103     | Algorithms  | Dr. Smith       | smit@univ.edu     ← Typo! Inconsistent!
```

When Dr. Smith's email changes, you must update EVERY row. Miss one = inconsistency. This is an **update anomaly.**

---

## The Normal Forms

| Form | Rule | What It Prevents |
|:----:|------|-----------------|
| **1NF** | Atomic values. Each cell holds one value. No repeating groups. | Multi-valued columns |
| **2NF** | 1NF + no partial dependencies (non-key columns depend on the WHOLE primary key) | Redundancy from composite keys |
| **3NF** | 2NF + no transitive dependencies (non-key doesn't depend on another non-key) | Indirect dependencies |
| **BCNF** | Stronger 3NF — every determinant must be a candidate key | Edge cases 3NF misses |
| **4NF** | No multi-valued dependencies | Independent multi-valued facts |
| **5NF** | No join dependencies | Can't be decomposed further without loss |

> **In practice:** 3NF or BCNF is the sweet spot. 4NF/5NF are rarely needed. Sometimes you deliberately **denormalize** for performance.

---

## 1NF — Atomic Values

```sql
-- ❌ NOT 1NF — multiple phone numbers in one field
customer_id | name  | phone_numbers
1           | Alice | "555-0100, 555-0101"

-- ✅ 1NF — separate table or separate rows
customer_id | name
1           | Alice

customer_id | phone_number
1           | 555-0100
1           | 555-0101
```

---

## 2NF — No Partial Dependencies

Only applies to tables with **composite primary keys.**

```sql
-- ❌ NOT 2NF
-- Primary key: (order_id, product_id)
-- product_name depends only on product_id (PART of the key), not the whole key
order_id | product_id | product_name | quantity
1        | P100       | Widget       | 5
1        | P200       | Gadget       | 3

-- ✅ 2NF — split into two tables
-- order_items: (order_id, product_id, quantity)
-- products: (product_id, product_name)
```

---

## 3NF — No Transitive Dependencies

```sql
-- ❌ NOT 3NF
-- department_name depends on department_id, which depends on employee_id
-- employee_id → department_id → department_name (transitive)
employee_id | name  | department_id | department_name
1           | Alice | D01           | Engineering
2           | Bob   | D01           | Engineering

-- ✅ 3NF — split into two tables
-- employees: (employee_id, name, department_id)
-- departments: (department_id, department_name)
```

---

## When to Denormalize

| Scenario | Why Denormalize |
|----------|----------------|
| Read-heavy reporting | Avoid expensive joins |
| Materialized pre-computation | Store calculated values (order totals) |
| Audit/history | Store snapshot of data at a point in time |
| High-scale reads with eventual consistency | Duplicate data across services (CQRS) |

```sql
-- Denormalized: order_total stored in orders table
-- Avoids joining with order_items and summing every time
orders: id | customer_id | total | status
order_items: id | order_id | product_id | quantity | price
```

> **The rule:** Normalize by default. Denormalize when you've **measured** a performance problem and proven that normalization is the bottleneck.

---

## Sources

- Codd, E.F. "A Relational Model of Data for Large Shared Data Banks," 1970.
- SWEBOK v4, Section 6.4: RDBMS and Normalization
