---
tags:
- linux
- os
- programming
---

# 02 Memory Management

The OS gives every process the illusion of having its own private, contiguous memory — even though physical RAM is shared, fragmented, and limited.

---

## Virtual Memory

> Every process sees its own address space. The OS maps virtual addresses to physical addresses behind the scenes.

```
Virtual Address Space (process view):
┌──────────┐ 0xFFFFFFFF
│  Stack   │ ← grows down
│    ↓     │
│          │
│    ↑     │
│  Heap    │ ← grows up
│  .bss    │ ← uninitialized globals
│  .data   │ ← initialized globals
│  .text   │ ← code
└──────────┘ 0x00000000

Physical RAM (actual hardware):
[ Page 0 ][ Page 1 ][ Page 2 ][ Page 3 ][ Page 4 ]...
   ↑ process A .text      ↑ process B stack
```

---

## Paging

> Memory is divided into fixed-size blocks: pages (virtual) and frames (physical). The page table maps one to the other.

```
Virtual Page # → Page Table → Physical Frame #
      5              │              3
      8         [mapping]          12
     15              │             99
```

### Page Table Entry

| Field | Purpose |
|-------|---------|
| **Frame number** | Which physical frame |
| **Present bit** | 1 = in RAM, 0 = on disk (page fault!) |
| **Dirty bit** | 1 = modified since loaded. Must write back on eviction. |
| **Accessed bit** | Used by page replacement algorithms |
| **Protection bits** | Read/Write/Execute |

---

## TLB — Translation Lookaside Buffer

> A hardware cache for page table entries. Without it, EVERY memory access would require TWO lookups (page table, then memory).

```
CPU → TLB (fast, hit ~99%) → Page Table (slow, on miss)
     └── 1 cycle              └── 100+ cycles
```

---

## Page Replacement — When RAM Is Full

| Algorithm | How | Notes |
|-----------|-----|-------|
| **FIFO** | Evict oldest page | Simple. Bad — may evict frequently used page. |
| **LRU** (Least Recently Used) | Evict page unused longest | Good. Expensive to track. |
| **NRU** (Not Recently Used) | Evict pages not accessed recently | Practical approximation. |
| **Second Chance** (Clock) | FIFO + check accessed bit. Give one more chance. | Linux uses a variant. |
| **LFU** (Least Frequently Used) | Evict page with fewest accesses | New pages (few accesses) may be evicted unfairly. |

---

## Thrashing

> System spends more time swapping pages than doing useful work.

```
Cause: Too many processes fighting for too little RAM.
Symptom: High disk I/O, low CPU utilization (CPU waiting on disk).
Fix: Add RAM. Reduce processes. Kill memory hogs.
```

```bash
# Check for thrashing
vmstat 1
# si (swap in), so (swap out) consistently > 0 = potential thrashing
```

---

## Java & Memory

| Component | What | Tuning |
|-----------|------|--------|
| **Heap** (-Xmx, -Xms) | Objects live here. GC manages. | `-Xmx2g -Xms2g` (same = no resizing) |
| **Metaspace** | Class metadata (replaced PermGen) | `-XX:MaxMetaspaceSize=256m` |
| **Thread stacks** (-Xss) | Per-thread stack | `-Xss1m` (default). 1000 threads = 1GB! |
| **Direct memory** | Off-heap. NIO buffers. | `-XX:MaxDirectMemorySize=512m` |
| **Code Cache** | JIT-compiled native code | `-XX:ReservedCodeCacheSize=256m` |

```bash
# Check JVM memory
jcmd <PID> VM.native_memory summary
# Example output:
# Java Heap: 2.0 GB
# Thread: 150 MB (150 threads × 1MB stack)
# Code: 80 MB
# GC: 50 MB
```

---

## Sources

- Silberschatz et al. *Operating System Concepts*, Chapters 8–9.
- Oracle JVM Memory Management — https://docs.oracle.com/javase/8/docs/technotes/guides/vm/
