---
tags:
- clean-code
- software-design
- software-engineering
---

# Concurrency

*Clean Code — Robert C. Martin (by Brett L. Schuchert), pp. 177–196*

> "Objects are abstractions of processing. Threads are abstractions of schedule."
> — James O. Coplien

---

## Why Concurrency?

Concurrency is a **decoupling strategy** — it decouples *what* gets done from *when* it gets done. In single-threaded code, what and when are tightly coupled; the stack backtrace reveals the entire state. Decoupling them improves **throughput** and **structure**: the application looks like many collaborating computers rather than one main loop.

Motivations:

- **Structural benefit** — The servlet model decouples request handling into independent executions.
- **Throughput** — Hit multiple web sites concurrently instead of sequentially waiting on I/O.
- **Responsiveness** — Handle many users concurrently instead of queuing them serially.
- **Parallel processing** — Partition large data sets across processors.

### Myths and Misconceptions

| Myth | Reality |
|---|---|
| Concurrency *always* improves performance | Only when there is significant wait time, sharable across threads or processors; nontrivial |
| Design doesn't change for concurrent programs | Decoupling *what* from *when* radically alters system structure |
| Container-managed concurrency means you don't need to understand it | You must know what your container does; deadlock and concurrent-update bugs still bite |

**Sound bites:**
- Concurrency incurs **overhead** in both performance and additional code.
- Correct concurrency is **complex**, even for simple problems.
- Concurrency bugs aren't repeatable; they get dismissed as one-offs.
- Concurrency often demands a **fundamental redesign**.

---

## Challenges

Consider a shared counter incremented by two threads:

```java
public class X {
    private int lastIdUsed;

    public int getNextId() {
        return ++lastIdUsed;
    }
}
```

Two threads calling `getNextId()` have **12,870 possible execution paths** at the bytecode level (int; 2,704,156 for `long`). Most paths produce valid results — but some don't. That's the problem: it works *nearly* all the time, until it doesn't.

---

## Concurrency Defense Principles

### **Single Responsibility Principle (SRP)**

Concurrency design is a *reason to change* on its own. Concurrency-related code has its own lifecycle, challenges, and failure modes. Embedding it in business logic is a mistake.

> **Keep concurrency-related code separate from other code.**

---

### **Limit the Scope of Data**

Every critical section that touches shared data is a liability. The more places shared data can be updated, the higher the odds you will:

- Forget to guard one (breaking **all** guarding)
- Violate DRY with duplicated guards
- Struggle to trace failures

> **Severely limit access to any data that may be shared.**

---

### **Use Copies of Data**

Avoid sharing in the first place. Copy objects, treat them as read-only, or collect results per-thread and merge in a single thread. The cost of extra object creation is often offset by savings from avoiding intrinsic locks and synchronization overhead.

```java
// BEFORE — shared mutable state with locking
public synchronized void accumulate(int value) {
    sharedTotal += value;
}

// AFTER — per-thread accumulation, merge once
// Thread-local copies eliminate synchronization entirely
```

> **Prefer copies over shared mutable state.**

---

### **Threads Should Be as Independent as Possible**

Design each thread to exist in its own world. It receives all required data from an unshared source, stores everything in local variables, and never touches shared state. HttpServlets are a natural example: `doGet`/`doPost` parameters are per-request; synchronization only becomes necessary when reaching shared resources like database connections.

> **Partition data into independent subsets operated on by independent threads.**

---

## Know Your Library

Java 5+ (`java.util.concurrent`) provides battle-tested concurrency primitives. Use them.

### **Thread-Safe Collections**

`ConcurrentHashMap` outperforms `HashMap` in nearly all situations and supports simultaneous concurrent reads/writes with safe composite operations. Key classes:

| Class | Purpose |
|---|---|
| `ConcurrentHashMap` | Thread-safe map; better than synchronized `HashMap` |
| `ReentrantLock` | Lock acquirable in one method, releasable in another |
| `Semaphore` | Classic counting semaphore |
| `CountDownLatch` | Releases all waiting threads after N events; fair-start guarantee |

Also study: `java.util.concurrent.atomic`, `java.util.concurrent.locks`.

> **Start with `ConcurrentHashMap`. Prefer nonblocking solutions. Use executors for unrelated tasks.**

---

## Know Your Execution Models

### Key Terminology

- **Bound Resource** — Fixed-size resource in a concurrent environment (e.g., DB connection pool, read/write buffers).
- **Mutual Exclusion** — Only one thread accesses shared data/resource at a time.
- **Starvation** — Thread(s) denied progress for an excessively long time or forever.
- **Deadlock** — Two+ threads each holding a resource the other needs; neither can proceed.
- **Livelock** — Threads in lockstep, each yielding to the other, making no progress.

### **Producer-Consumer**

Producers create work → place in a bounded queue → consumers acquire and complete it. Both sides signal each other: producers signal "not empty," consumers signal "not full." Coordination requires waiting for notification.

### **Readers-Writers**

Shared resource read frequently, written occasionally. Throughput vs. staleness vs. writer starvation trade-off. Naive strategy: writers wait for zero readers → continuous readers starve writers. Frequent priority-writers degrade throughput. Balance is the challenge.

### **Dining Philosophers**

N philosophers, N forks (one to the left of each). A philosopher needs both adjacent forks to eat. Maps to enterprise processes competing for resources. Without careful design → deadlock, livelock, throughput degradation.

Most real-world concurrency problems are variations of these three. **Study and implement them.**

---

## Beware Dependencies Between Synchronized Methods

Multiple `synchronized` methods on the same shared class invite subtle bugs. If you must call more than one, use one of three strategies:

1. **Client-Based Locking** — Client acquires the server's lock before the first method call and releases after the last.
2. **Server-Based Locking** — Server provides a method that locks, calls all methods, unlocks. Client calls that single method.
3. **Adapted Server** — Intermediary does the locking; used when the original server cannot be changed.

> **Avoid more than one synchronized method on a shared object. When unavoidable, pick one locking strategy and stick to it.**

---

## Keep Synchronized Sections Small

`Synchronized` blocks introduce lock contention — expensive in both delay and overhead. Making critical sections *larger* than necessary increases contention and degrades performance. Make them as small as possible while still guarding correctness.

```java
// BAD — overbroad lock
public synchronized void process() {
    expensiveSetup();          // doesn't need locking
    sharedCounter++;           // only this needs locking
    expensiveTeardown();       // doesn't need locking
}

// GOOD — minimal lock scope
public void process() {
    expensiveSetup();
    synchronized(this) {
        sharedCounter++;
    }
    expensiveTeardown();
}
```

> **Minimize critical section size. Lock only what must be locked.**

---

## Writing Correct Shut-Down Code Is Hard

Graceful shutdown creates its own deadlock risks. Common failure: a parent thread spawns children, waits for them all, but one child is deadlocked → parent waits forever. Or: a producer-consumer pair where the producer shuts down immediately but the consumer is blocked waiting for a message it will never receive.

> **Design shutdown early. Review existing algorithms. Expect it to take longer than you think.**

---

## Testing Threaded Code

Testing cannot prove correctness, but good testing minimizes risk — and threaded code multiplies that risk. Core testing commandments:

### **Treat Spurious Failures as Candidate Threading Issues**

A bug that appears once in a million executions is *still a bug*. "One-offs" and "cosmic rays" are usually threading defects waiting for the right interleaving. **Do not ignore non-reproducible failures.**

### **Get Nonthreaded Code Working First**

Test POJOs outside threads before layering concurrency on top. The more of your system in thread-ignorant POJOs, the more you can test deterministically.

```java
// POJO — testable without any threading
public class IdGenerator {
    private int lastId;
    public synchronized int nextId() { return ++lastId; }
}
```

### **Make Threaded Code Pluggable**

Run under multiple configurations:
- One thread → several threads → varying thread counts
- Real dependencies → test doubles (fast, slow, variable, configurable iterations)

### **Make Threaded Code Tunable**

Allow thread count to be easily adjusted — even at runtime. Consider self-tuning based on throughput and utilization metrics.

### **Run with More Threads Than Processors**

Task-swapping stress uncovers missing critical sections and deadlocks. The more frequently threads swap, the higher the chance of hitting a race condition.

### **Run on Different Platforms**

Different operating systems schedule threads differently. Code that passes tests on macOS may fail on Windows (or vice versa). **Run tests on every deployment environment early and often.**

### **Instrument to Force Failures**

Normal execution takes the safe path. Only a handful of thousands of possible interleavings actually trigger a bug. Increase the odds:

**Hand-coded instrumentation:**
```java
public synchronized String nextUrlOrNull() {
    if (hasNext()) {
        String url = urlGenerator.next();
        Thread.yield();           // injected to shake out race conditions
        updateHasNext();
        return url;
    }
    return null;
}
```

**Automated jiggling** (preferred):
```java
public class ThreadJigglePoint {
    public static void jiggle() { /* no-op in production */ }
}

// In test: randomly sleep, yield, or do nothing
public synchronized String nextUrlOrNull() {
    if (hasNext()) {
        ThreadJigglePoint.jiggle();
        String url = urlGenerator.next();
        ThreadJigglePoint.jiggle();
        updateHasNext();
        ThreadJigglePoint.jiggle();
        return url;
    }
    return null;
}
```

Swap `jiggle()` implementations: production no-op, testing random delay/yield. Combine with many iterations. Tools like IBM ConTest offer sophisticated versions of this.

> **Jiggle aggressively in testing. Broken code should fail as early and as often as possible.**

---

## Checklist: Clean Concurrency

- [ ] Concurrency code separated from business logic (SRP)
- [ ] Shared data access severely limited
- [ ] Copies used instead of shared mutable state where possible
- [ ] Threads designed to be as independent as possible
- [ ] `java.util.concurrent` collections used in preference to hand-rolled synchronization
- [ ] Producer-Consumer, Readers-Writers, Dining Philosophers understood
- [ ] At most one `synchronized` method per shared class (or a deliberate, consistent locking strategy)
- [ ] `synchronized` blocks kept as small as possible
- [ ] Shutdown logic designed and tested early
- [ ] Nonthreaded POJOs tested fully before adding threading
- [ ] Threaded code is pluggable and tunable (thread counts, test doubles, iterations)
- [ ] Tests run with more threads than processors, on all target platforms
- [ ] Code instrumented to force interleaving failures (hand-coded or automated jiggling)
- [ ] Spurious test failures never dismissed — treated as threading defects until proven otherwise

---

## Related

[[Clean Code Principles]] · [[Function Design]] · [[System Architecture]] · [[Code Smells Catalog]]
