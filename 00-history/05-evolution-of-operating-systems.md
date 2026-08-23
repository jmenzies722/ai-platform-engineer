# Evolution of Operating Systems

An operating system safely shares one machine among many programs and gives those programs simpler ways to use hardware.

## Why it matters

**Prerequisite:** [Evolution of Programming Languages](./04-evolution-of-programming-languages.md).

Early operators loaded one job at a time, leaving expensive hardware idle while programs waited for input and output. Multiprogramming and time-sharing kept the machine busy, but required a trusted layer to isolate users and allocate resources.

Operating systems supplied durable abstractions such as processes, files, users, and virtual memory. Linux still uses those abstractions to share a host among services, containers, and AI workloads, so contention and protection remain central engineering concerns.

## How it works

The kernel is a privileged mediator: it turns finite physical resources into controlled virtual resources and records policy at boundaries.

Programs enter the kernel through system calls. The scheduler assigns CPU time; page tables translate virtual addresses; filesystems map names to blocks; drivers operate devices; interrupts report asynchronous events. Permissions constrain resource access.

Virtual memory gives each process a private address space, not unlimited RAM. Pages can fault, be shared, or be reclaimed. Scheduling optimizes competing goals—latency, fairness, throughput—so overload appears as queues and tail latency before total failure.

## Vocabulary

- **Kernel:** The privileged OS core that manages protected resources.
- **System call:** A controlled request from user space to the kernel.
- **Process:** An OS-managed execution context and resource container.
- **Thread:** A schedulable execution stream within a process.
- **Context switch:** Saving one execution context and restoring another.
- **Virtual memory:** Process-visible addresses translated to physical or other backing.
- **Page fault:** A CPU exception requesting kernel handling for a memory access.
- **Interrupt:** An event that transfers CPU control to a privileged handler.
- **Scheduler:** The subsystem that chooses which runnable thread gets CPU time.
- **IPC:** Inter-process communication between separate process contexts.
- **Driver:** Software that controls a device through an OS-defined interface.

## See it yourself

```bash
ps -eo pid,ppid,stat,%cpu,%mem,comm
cat /proc/self/status
ulimit -a
strace -f -e trace=file,network true
```

Predict which command will show scheduling state, resource limits, and file-related system calls. On Linux, each should expose a different kernel contract. The observations support the claim that processes use protected OS abstractions rather than hardware directly. A snapshot of `/proc` or `ps` does not establish why a process is slow without changes over time and workload context.

## Where it shows up

A containerized service can remain alive yet stop making progress. The kernel may consider its threads runnable while CPU throttling limits execution, reclaim may stall them under memory pressure, or storage I/O may leave them blocked. An application health endpoint sees only selected behavior. Process states, pressure metrics, cgroup counters, faults, and I/O latency connect the symptom to the shared host.

## When it breaks

A host can show high load average while CPU utilization remains low. Threads may be waiting in uninterruptible I/O, memory reclaim, or a device driver rather than competing for execution. First inspect process states and wait channels, then correlate run queues, pressure, faults, and I/O latency over time; load alone does not identify the constrained resource.

## Practice

### Observe

Run CPU-bound and I/O-bound jobs; inspect process states and timing. Constrain memory safely and observe allocation failure or reclaim behavior.

### Build

Implement a cooperative round-robin scheduler simulation with arrival times, blocking, and per-task metrics.

### Break

Create descriptor exhaustion and a CPU hog inside a disposable environment. Add limits and verify the blast radius.

### Say it out loud

Explain how an OS can make one machine look private to many programs.

**Success:** Include protection, scheduling, virtual memory, one leak of the abstraction, and the first evidence you would inspect.

## Check yourself

1. Why are process and virtual memory separate abstractions?
2. What happens on a page fault?
3. Why is scheduling a policy trade-off?

### Interview stretch

- Diagnose high load with low CPU utilization.
- Explain an OOM kill versus an allocation failure.
- What kernel resources do containers share?

## Sources

### REQUIRED

- “The Compatible Time-Sharing System” — MIT. [MIT CSAIL](https://multicians.org/thvv/7094.html). Shows why interactive resource sharing emerged.

### RECOMMENDED

- “Operating Systems: Three Easy Pieces” — Arpaci-Dusseau and Arpaci-Dusseau. [Official book site](https://pages.cs.wisc.edu/~remzi/OSTEP/). Builds mechanisms around virtualization, concurrency, and persistence.

### DEEP DIVE

- “Linux Kernel Documentation” — Linux kernel community. [Official documentation](https://docs.kernel.org/). Canonical source for modern kernel mechanisms.

## Next

Continue with [./06-unix-c-linux.md](./06-unix-c-linux.md).
