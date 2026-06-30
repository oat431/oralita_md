---
tags:
- linux
- os
- programming
---

# 01 CPU Scheduling

The OS decides which thread gets the CPU next. Understanding scheduling helps you reason about latency, fairness, and why your thread isn't running.

---

## Scheduling Algorithms

| Algorithm | How It Works | Pros | Cons |
|-----------|-------------|------|------|
| **FCFS** (First Come First Served) | Run in arrival order | Simple | Convoy effect — long job blocks short ones |
| **SJF** (Shortest Job First) | Run shortest job next | Optimal avg wait time | Must know job length in advance |
| **SRTF** (Shortest Remaining Time) | Preemptive SJF — new shorter job preempts | Better response time | Starvation of long jobs |
| **Round Robin** | Each thread gets a time slice (~10-100ms) | Fair. Good for interactive. | Higher context switch overhead |
| **Priority** | Higher priority runs first | Critical tasks get CPU | Starvation of low priority |
| **Multi-Level Queue** | Separate queues per priority class | Mixes batch + interactive | Complex |

---

## Linux CFS — Completely Fair Scheduler

> The default Linux scheduler since 2.6.23 (2007).

```
Key idea: Each runnable thread gets a "fair share" of CPU time.
CFS tracks virtual runtime (vruntime) — how long each thread has run,
weighted by priority (nice value).

Lower vruntime → runs next.
Higher priority (lower nice) → vruntime accumulates slower → gets more CPU.
```

### Nice Values

```
-20 (highest priority) ←→ 19 (lowest priority)
Default: 0
Only root can set negative nice values.
```

```bash
# Check process priority
ps -eo pid,ni,comm | grep java

# Launch with specific priority
nice -n 10 java -jar app.jar    # Lower priority
nice -n -5 java -jar app.jar    # Higher priority (needs root)
```

---

## Preemptive vs Non-Preemptive

| | Preemptive | Non-Preemptive |
|---|:---:|:---:|
| **Interrupts** | ✅ Can force thread off CPU | ❌ Thread runs until it yields |
| **Responsiveness** | Good for interactive | Good for batch |
| **Examples** | Round Robin, SRTF, Linux CFS | FCFS, cooperative multitasking |

> Modern OSes are **preemptive.** The kernel can interrupt any thread at any time.

---

## CPU Affinity

> Pin a thread to specific CPU cores. Reduces cache misses from migration.

```java
// Java doesn't expose CPU affinity directly (JVM abstracts it)
// But you can set it at the OS level:
// taskset -c 0,1 java -jar app.jar   # Pin to cores 0 and 1
```

```bash
# Check CPU affinity
taskset -p <PID>

# View per-CPU interrupts and scheduling
mpstat -P ALL 1
```

---

## Real-Time Scheduling

| Policy | Behavior |
|--------|----------|
| **SCHED_FIFO** | Highest priority runs to completion. No time slicing. |
| **SCHED_RR** | Like FIFO but with time slices for equal priorities. |
| **SCHED_DEADLINE** | Tasks specify runtime, deadline, period. Earliest deadline first. |

> ⚠️ Real-time threads can starve the entire system. Use sparingly. Reserved for audio, robotics, industrial control — not web servers.

---

## Sources

- Linux CFS Documentation — `Documentation/scheduler/sched-design-CFS.txt`
- `man sched`, `man nice`, `man chrt`
