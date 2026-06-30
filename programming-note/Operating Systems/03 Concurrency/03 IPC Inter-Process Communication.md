---
tags:
- linux
- os
- programming
---

# 03 IPC — Inter-Process Communication

Processes are isolated by design. IPC is how they talk to each other. Understanding the options helps you choose the right communication pattern.

---

## IPC Methods Compared

| Method | Speed | Data Size | Complexity | Use Case |
|--------|:---:|:---:|:---:|----------|
| **Pipes** | Medium | Stream | Low | `ls | grep java` |
| **Named Pipes (FIFO)** | Medium | Stream | Low | Unrelated processes |
| **Shared Memory** | Fastest | Any | High | Cache, large data transfer |
| **Message Queues** | Medium | Messages | Medium | Async task distribution |
| **Sockets** | Slowest | Stream/Messages | Medium | Network services |
| **Signals** | Fast | None (notification) | Low | "Shutdown now!" |

---

## Pipes

> Unidirectional stream. Parent and child process (or shell pipes).

```bash
# Anonymous pipe (shell)
ps aux | grep java | wc -l

# Named pipe (FIFO) — any processes
mkfifo /tmp/myfifo
# Process A writes
echo "hello" > /tmp/myfifo
# Process B reads
cat /tmp/myfifo
```

---

## Shared Memory

> Multiple processes map the same physical memory. NO copying. Fastest IPC.

```java
// Java — MappedByteBuffer shared between processes
RandomAccessFile file = new RandomAccessFile("/tmp/shared.dat", "rw");
FileChannel channel = file.getChannel();
MappedByteBuffer buffer = channel.map(
    FileChannel.MapMode.READ_WRITE, 0, 4096);

// Process A writes
buffer.putInt(0, 42);

// Process B reads (maps same file)
int value = buffer.getInt(0);  // 42
```

⚠️ Shared memory needs synchronization (semaphores, mutexes). Two processes writing simultaneously = corruption.

---

## Sockets — Network IPC

> The universal IPC. Works across machines. Foundation of microservices.

```java
// TCP socket
ServerSocket server = new ServerSocket(9090);
Socket client = server.accept();
BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
String message = in.readLine();

// Unix Domain Socket — faster than TCP for local IPC
// Path: /tmp/app.sock
// Same API as TCP but never leaves the machine. No TCP overhead.
```

---

## Message Queues — POSIX & System V

> Messages placed in a queue. Receiver picks them up. Persistent across process restarts (depending on implementation).

| POSIX MQ | System V MQ |
|----------|------------|
| File-descriptor based | ID-based |
| Priorities | Message types |
| `mq_open`, `mq_send`, `mq_receive` | `msgget`, `msgsnd`, `msgrcv` |

> Modern alternative: Redis, RabbitMQ — application-level message queues. More features, slower.

---

## Signals — Simple IPC

> OS-level notifications. Limited data (signal number + optional value). Good for process lifecycle management.

```bash
kill -TERM <PID>     # Graceful shutdown
kill -HUP <PID>      # Reload configuration
kill -USR1 <PID>     # Custom signal (application-defined)

# List all signals
kill -l
```

---

## Sources

- `man 7 pipe`, `man 7 unix`, `man shm_overview`
- Stevens, W. Richard. *UNIX Network Programming, Volume 2: Interprocess Communications.*
