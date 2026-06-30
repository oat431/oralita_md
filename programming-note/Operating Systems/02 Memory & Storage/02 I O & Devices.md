---
tags:
- linux
- os
- programming
---

# 02 I/O & Device Management

Every disk read, network packet, and keystroke involves I/O. The OS manages devices through a layered architecture of drivers, buffers, and interrupts.

---

## I/O Device Categories

| Type | Examples | Access Pattern |
|------|----------|---------------|
| **Block devices** | HDD, SSD | Random access in fixed-size blocks. Seek + read. |
| **Character devices** | Keyboard, mouse, serial port | Sequential stream. Read one char at a time. |
| **Network devices** | Ethernet, Wi-Fi | Packet-based. Different OS interface (sockets). |

---

## I/O Communication Methods

| Method | How | CPU Usage |
|--------|-----|:---:|
| **Polling** | CPU repeatedly checks "are you ready?" | High — spins waiting |
| **Interrupts** | Device sends interrupt when ready. CPU notified. | Low — CPU does other work |
| **DMA** (Direct Memory Access) | Device writes directly to RAM. CPU sets up, walks away. | Minimal — only setup/teardown |

```
Without DMA: CPU reads from device → CPU writes to memory
With DMA:    CPU tells device "write to address 0x..." → device does it → interrupt on done
```

> DMA is why async I/O is fast. The CPU sets up the transfer and goes back to running your code.

---

## Buffering & Caching

| Purpose | Where | Example |
|---------|-------|---------|
| **Buffer** | Smooth out speed differences | `BufferedInputStream` — reads 8KB at a time, not 1 byte |
| **Cache** | Avoid repeated slow operations | OS page cache — recently read files served from RAM |

```java
// ❌ Unbuffered — system call per byte
FileInputStream fis = new FileInputStream("data.bin");
int b;
while ((b = fis.read()) != -1) { process(b); }  // read() syscall per byte!

// ✅ Buffered — 8KB reads
BufferedInputStream bis = new BufferedInputStream(new FileInputStream("data.bin"));
// Internally reads 8KB chunks. read() returns from buffer, not syscall.
```

---

## I/O Scheduling

> The OS reorders disk requests to minimize seek time (HDD) or maximize throughput (SSD).

| Scheduler | Best For |
|-----------|----------|
| **CFQ** (Completely Fair Queue) | General purpose. Fair per-process. |
| **Deadline** | Reads served within deadline. Good for databases. |
| **NOOP** | No reordering. Good for SSDs (no seek time). |

```bash
# Check current I/O scheduler
cat /sys/block/sda/queue/scheduler
# [mq-deadline] kyber bfq none
```

---

## Memory-Mapped I/O

> Treat a file as if it's in memory. The OS handles loading/storing pages.

```java
// mmap — zero-copy file access
try (RandomAccessFile file = new RandomAccessFile("data.bin", "rw");
     FileChannel channel = file.getChannel()) {
    
    MappedByteBuffer buffer = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, file.length());
    
    // Read/write like memory. OS handles paging.
    int value = buffer.getInt();
    buffer.putInt(0, 42);
}
// No read()/write() syscalls during access — just page faults
```

---

## I/O in Practice — Linux Tools

```bash
# Disk I/O stats
iostat -x 1
# await: average wait time (ms). > 10ms = disk bottleneck.
# %util: how busy the disk is. > 80% = near saturation.

# Per-process I/O
iotop -o    # Show only processes doing I/O
pidstat -d 1  # Per-process I/O stats

# Check if swap is being used
free -h     # "Swap" row. If used > 0 and I/O is high = potential problem.
```

---

## Sources

- `man iostat`, `man iotop`
- Corbet, Rubini, Kroah-Hartman. *Linux Device Drivers*, 3rd ed.
