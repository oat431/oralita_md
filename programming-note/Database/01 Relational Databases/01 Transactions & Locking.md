---
tags:
- database
- nosql
- programming
- sql
---

# 01 Transactions & Locking

Transactions keep your data consistent when things go wrong. Locking keeps concurrent transactions from stepping on each other.

---

## ACID — The Four Guarantees

| Property | Meaning | Example |
|----------|---------|---------|
| **Atomicity** | All or nothing. A transaction either fully completes or fully rolls back. | Transfer $100 from A to B: debit A AND credit B — or neither. |
| **Consistency** | Transaction moves DB from one valid state to another. Constraints hold. | After transfer, total money in system is unchanged. |
| **Isolation** | Concurrent transactions don't interfere with each other. | Two transfers at the same time don't create or destroy money. |
| **Durability** | Committed data survives crashes, power loss, etc. | After "transaction committed," the data is safe. |

---

## Isolation Levels — The Trade-Off

Higher isolation = less concurrency. Lower isolation = more anomalies.

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Concurrency |
|:------|:---:|:---:|:---:|:---:|
| **Read Uncommitted** | ✅ Yes | ✅ Yes | ✅ Yes | Maximum |
| **Read Committed** | ❌ No | ✅ Yes | ✅ Yes | High *(PostgreSQL default)* |
| **Repeatable Read** | ❌ No | ❌ No | ✅ Yes | Medium |
| **Serializable** | ❌ No | ❌ No | ❌ No | Low *(safest)* |

### Anomaly Examples

```sql
-- Dirty Read: Transaction A reads uncommitted data from B. B rolls back. A has phantom data.

-- Non-Repeatable Read: Same query in same transaction returns different rows
-- T1: SELECT balance WHERE id=1 → 100
-- T2: UPDATE balance SET balance=200 WHERE id=1; COMMIT
-- T1: SELECT balance WHERE id=1 → 200 (different!)

-- Phantom Read: Same query returns different SET of rows
-- T1: SELECT * WHERE balance > 100 → 5 rows
-- T2: INSERT new row with balance=150; COMMIT
-- T1: SELECT * WHERE balance > 100 → 6 rows (phantom appeared!)
```

---

## Pessimistic vs Optimistic Locking

| | Pessimistic | Optimistic |
|---|:---:|:---:|
| **How** | Lock row before reading. Others wait. | Read row, check version before update. |
| **Use When** | High contention. Conflicts common. | Low contention. Conflicts rare. |
| **Implementation** | `SELECT ... FOR UPDATE` | `version` column or timestamp |
| **Downside** | Blocks other transactions. Deadlock risk. | Wasted work if conflict detected. |

### Pessimistic (Database Lock)

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT a FROM Account a WHERE a.id = :id")
Optional<Account> findByIdForUpdate(@Param("id") Long id);
// Row is locked until transaction ends. Other transactions WAIT.
```

### Optimistic (Application-Level Version Check)

```java
@Entity
public class Account {
    @Version
    private Long version;  // Auto-incremented on each update
    // ...
}

// If two transactions read version=1,
// first to commit updates to version=2.
// Second gets OptimisticLockException — must retry.
```

---

## Deadlocks

> Transaction A holds lock on row X, wants lock on row Y.
> Transaction B holds lock on row Y, wants lock on row X.
> **Neither can proceed. Both wait forever.**

### Prevention

| Strategy | How |
|----------|-----|
| **Consistent order** | Always lock resources in the same order (alphabetical, by ID) |
| **Short transactions** | Acquire locks late, release early. Don't hold locks across user input. |
| **Timeout** | Set lock timeout. Fail fast, don't hang. |
| **Retry** | Application catches deadlock exception and retries |

```java
@Retryable(value = {CannotAcquireLockException.class}, maxAttempts = 3, backoff = @Backoff(delay = 100))
@Transactional
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    // Always lock in consistent order (lower ID first)
    Long first = Math.min(fromId, toId);
    Long second = Math.max(fromId, toId);
    Account a1 = accountRepo.findByIdForUpdate(first);
    Account a2 = accountRepo.findByIdForUpdate(second);
    // ... perform transfer ...
}
```

---

## Sources

- PostgreSQL Concurrency Control — https://www.postgresql.org/docs/current/mvcc.html
- Java Persistence Locking — https://jakarta.ee/specifications/persistence/
