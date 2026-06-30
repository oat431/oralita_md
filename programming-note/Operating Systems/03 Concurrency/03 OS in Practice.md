---
tags:
- linux
- os
- programming
---

# 03 OS in Practice — Linux Tools for Developers

The tools every backend developer needs to diagnose OS-level problems. Not the theory — the practice.

---

## Process Inspection

```bash
# Top processes by CPU/memory
top
htop  # Prettier, interactive

# Process tree — who spawned what
pstree -p

# Detailed process info
ps -eo pid,ppid,user,%cpu,%mem,comm | sort -k4 -rn | head -20

# Thread-level view
ps -eLf | grep java  # -L shows threads
top -H -p <PID>      # Per-thread CPU
```

---

## Memory Analysis

```bash
# System memory overview
free -h

# Virtual memory stats
vmstat 1
# Key columns: si (swap in), so (swap out), bi (block in), bo (block out)

# Per-process memory
pmap <PID>       # Memory map
smem -k          # PSS (Proportional Set Size) — shared memory divided fairly

# JVM-specific
jcmd <PID> GC.heap_info
jcmd <PID> VM.native_memory summary
jmap -heap <PID>
```

---

## I/O Analysis

```bash
# Disk I/O — per device
iostat -x 1
# %util > 80% = bottleneck. await > 10ms = slow.

# Per-process I/O
iotop -oP         # -o: only active, -P: only processes
pidstat -d 1      # Per-process read/write

# What files is this process accessing?
lsof -p <PID>     # All open files
lsof -i :8080     # What's listening on port 8080?
```

---

## CPU & Scheduling

```bash
# CPU usage breakdown
mpstat -P ALL 1
# %usr (user), %sys (system), %iowait (waiting for I/O), %idle

# Context switch rate
vmstat 1         # cs column
pidstat -w 1     # Per-process context switches

# What's the scheduler doing?
perf top          # Live CPU profiling
perf record -p <PID> -g -- sleep 30  # Capture 30s
perf report       # Analyze
```

---

## Network

```bash
# Connection states
ss -s            # Summary
ss -tlnp         # TCP listening
ss -tan state time-wait | wc -l  # Count TIME_WAIT

# Socket stats
netstat -s       # Protocol statistics

# Bandwidth per process
nethogs           # Like top for network
iftop             # Per-connection bandwidth
```

---

## System-Wide Stats

```bash
# Everything at once
dstat -c -d -m -n --top-cpu --top-io --top-mem 1

# System resource limits
ulimit -a        # Current limits
cat /proc/<PID>/limits  # Per-process limits

# Common limit fixes
ulimit -n 65536            # Increase file descriptors
ulimit -u 4096             # Increase max processes
```

---

## Java-Specific Tools

```bash
jps -l                     # List Java processes
jstack <PID>               # Thread dump — what's each thread doing?
jcmd <PID> Thread.print    # Same, modern
jstat -gc <PID> 1000       # GC stats every second
jmap -histo <PID> | head   # Object histogram — what's eating memory?
```

### Common Thread States in jstack

| State | Meaning |
|-------|---------|
| **RUNNABLE** | Thread is running or ready to run |
| **BLOCKED** | Waiting for a monitor lock |
| **WAITING** | `Object.wait()` — waiting to be notified |
| **TIMED_WAITING** | `Thread.sleep()`, `Lock.tryLock(timeout)` |
| **TERMINATED** | Thread finished |

> Many threads in BLOCKED state = lock contention. Check your synchronized blocks.

---

## Sources

- `man` pages for each tool
- Brendan Gregg. *Systems Performance: Enterprise and the Cloud.*
