---
tags:
- linux
- os
- programming
---

# 01 System Calls & Kernel

System calls are the interface between your application and the OS kernel. Every file read, network send, and thread creation is a system call.

---

## User Mode vs Kernel Mode

```
┌──────────────────────┐
│    User Mode          │ ← Your application code
│  (unprivileged)       │
├──────────────────────┤
│   System Call ───────▶│
├──────────────────────┤
│    Kernel Mode        │ ← OS code
│  (privileged)         │    Access to hardware, memory, devices
└──────────────────────┘
```

> User mode: can't access hardware directly. Kernel mode: can do anything. System calls bridge the gap.

---

## Common System Calls

| Category | Calls | Java Equivalent |
|----------|-------|----------------|
| **Process** | `fork`, `exec`, `exit`, `wait` | `ProcessBuilder`, `Runtime.exec()` |
| **File I/O** | `open`, `read`, `write`, `close` | `FileInputStream`, `Files.readAllBytes()` |
| **Network** | `socket`, `bind`, `listen`, `accept`, `connect` | `ServerSocket`, `HttpURLConnection` |
| **Memory** | `mmap`, `brk`, `sbrk` | NIO `MappedByteBuffer` |
| **Thread** | `clone` (Linux), `pthread_create` | `new Thread()` |

---

## How a System Call Works

```
1. Application calls read(fd, buf, size)
2. C library (glibc) sets up registers: syscall number, arguments
3. Software interrupt / syscall instruction (sysenter/syscall)
4. CPU switches to kernel mode
5. Kernel looks up syscall number in syscall table
6. Kernel executes sys_read()
7. Result returned. CPU switches back to user mode.
8. Application continues.
```

> Each system call = context switch to kernel mode. Cost: ~100-500ns. Batching operations saves these switches.

---

## Signals

> OS notifications to a process. Like interrupts for software.

| Signal | Number | Meaning | Default Action |
|--------|:------:|---------|---------------|
| **SIGINT** | 2 | Ctrl+C — interrupt | Terminate |
| **SIGKILL** | 9 | Force kill (can't be caught) | Terminate |
| **SIGTERM** | 15 | Graceful shutdown (can be caught) | Terminate |
| **SIGSTOP** | 19 | Pause (can't be caught) | Stop |
| **SIGSEGV** | 11 | Segmentation fault | Core dump + terminate |
| **SIGHUP** | 1 | Terminal closed | Terminate |

```java
// Graceful shutdown — catch SIGTERM
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    log.info("Shutting down...");
    // Close connections, flush buffers, finish in-flight requests
    connectionPool.close();
}));
```

---

## strace — Trace System Calls

```bash
# Trace all syscalls
strace java -jar app.jar

# Count syscalls by type
strace -c java -jar app.jar

# Trace specific syscall
strace -e trace=open,read,write java -jar app.jar

# Attach to running process
strace -p <PID>
```

### What strace Reveals

| Finding | What It Means |
|---------|--------------|
| Thousands of `read(1,...)` | Reading 1 byte at a time. Buffer your I/O! |
| Repeated `open`/`close` of same file | Cache file handles. Use connection pooling. |
| `futex` calls dominating | Heavy thread synchronization. Could be contention. |

---

## Sources

- `man 2 syscalls` — Linux system call table
- `man 7 signal` — Signal overview
- `man strace`
