---
tags:
- linux
- os
- programming
---

# 03 Synchronization & Deadlocks

When multiple threads share data, you need synchronization. When synchronization goes wrong, you get deadlocks.

---

## The Race Condition

```java
// ❌ Race condition — two threads increment counter
public class Counter {
    private int count = 0;
    
    public void increment() {
        count++;  // NOT atomic! Read → Increment → Write (3 steps)
    }
}
// Thread A reads 0. Thread B reads 0.
// Thread A writes 1. Thread B writes 1.
// Result: 1 (should be 2). One update LOST.
```

---

## Synchronization Primitives

### Mutex (Mutual Exclusion)

> Only ONE thread can hold the lock at a time.

```java
// Java — synchronized
public synchronized void increment() {
    count++;  // Only one thread at a time
}

// Or explicit lock
private final ReentrantLock lock = new ReentrantLock();
public void increment() {
    lock.lock();
    try {
        count++;
    } finally {
        lock.unlock();  // ALWAYS unlock in finally!
    }
}
```

### Semaphore

> Allows N threads simultaneously. Counter-based.

```java
// Connection pool — max 10 connections
Semaphore semaphore = new Semaphore(10);

public Connection getConnection() throws InterruptedException {
    semaphore.acquire();  // Block if all 10 in use
    try {
        return pool.borrowConnection();
    } finally {
        // Return to pool, then:
        semaphore.release();
    }
}
```

| Mutex | Semaphore |
|-------|-----------|
| Binary (locked/unlocked) | Counter (0 to N) |
| Ownership — only locker unlocks | Any thread can signal |
| One thread at a time | N threads at a time |

### ReadWriteLock

> Many readers OR one writer. Readers don't block each other.

```java
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();

public String read() {
    rwLock.readLock().lock();
    try { return data; }
    finally { rwLock.readLock().unlock(); }
}

public void write(String newData) {
    rwLock.writeLock().lock();
    try { data = newData; }
    finally { rwLock.writeLock().unlock(); }
}
```

### Condition Variables

> Wait for a condition. Signal when it changes. Used for producer-consumer.

```java
private final Lock lock = new ReentrantLock();
private final Condition notEmpty = lock.newCondition();
private final Condition notFull = lock.newCondition();

// Producer
lock.lock();
try {
    while (queue.isFull()) {
        notFull.await();  // Wait until there's space
    }
    queue.add(item);
    notEmpty.signal();  // Wake up waiting consumers
} finally { lock.unlock(); }

// Consumer
lock.lock();
try {
    while (queue.isEmpty()) {
        notEmpty.await();  // Wait until there's data
    }
    Item item = queue.remove();
    notFull.signal();  // Wake up waiting producers
    return item;
} finally { lock.unlock(); }
```

---

## Deadlocks — The Four Conditions

> A deadlock requires ALL four conditions. Break ANY one → no deadlock.

| Condition | Meaning | How to Break |
|-----------|---------|-------------|
| **Mutual Exclusion** | Resource can't be shared | Use lock-free data structures |
| **Hold and Wait** | Holding one resource while waiting for another | Acquire all resources at once |
| **No Preemption** | Can't force a thread to release | Use `tryLock()` with timeout |
| **Circular Wait** | A → waits → B → waits → C → waits → A | Always acquire locks in consistent order |

```java
// ❌ Deadlock-prone — inconsistent lock order
// Thread 1: lock(A) → lock(B)
// Thread 2: lock(B) → lock(A)  ← Circular wait!

// ✅ Consistent order — always lock lower ID first
Long first = Math.min(id1, id2);
Long second = Math.max(id1, id2);
synchronized(first) {
    synchronized(second) {
        // transfer money
    }
}
```

### tryLock with Timeout

```java
// ✅ Back off instead of deadlocking
if (lock1.tryLock(1, TimeUnit.SECONDS)) {
    try {
        if (lock2.tryLock(1, TimeUnit.SECONDS)) {
            try {
                // do work
            } finally { lock2.unlock(); }
        }
    } finally { lock1.unlock(); }
}
// If either lock times out, release and retry
```

---

## Lock-Free Programming

> `AtomicInteger`, `AtomicReference`, `ConcurrentHashMap` — use hardware CAS (Compare-And-Swap) instead of locks.

```java
// ✅ Lock-free counter
private final AtomicInteger count = new AtomicInteger(0);
public void increment() {
    count.incrementAndGet();  // Atomic. No lock. Hardware CAS.
}
```

| Locking | Lock-Free |
|---------|----------|
| Threads block and wait | Threads retry on conflict |
| Deadlock possible | No deadlocks |
| Priority inversion possible | No priority inversion |
| Slower under low contention | Faster under low contention |

---

## Sources

- Goetz, Brian. *Java Concurrency in Practice.*
- Silberschatz et al. *Operating System Concepts*, Chapters 6–7.
