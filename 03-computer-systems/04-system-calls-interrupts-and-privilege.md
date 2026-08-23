# System Calls, Interrupts, and Privilege

Applications execute with restricted authority. System calls and asynchronous events let the operating-system kernel mediate hardware, isolation, time, and shared resources.

## Why it matters

A function named `read` may copy from a language buffer without entering the kernel, while one logical write may become several system calls. Performance tuning and incident diagnosis fail when library operations, syscalls, interrupts, and context switches are treated as synonyms. Security also depends on knowing where untrusted code loses direct authority.

## How it works

Processors provide privilege levels. The kernel runs with authority to configure memory translation, devices, and scheduling; ordinary application code runs in user mode. A system call uses an architecture-defined entry mechanism, validates arguments and permissions, performs or begins kernel work, and returns a result or error. The C library often wraps this interface, and a language runtime may add buffering and object conversion above it.

Exceptions are synchronous events caused by the current instruction, such as a page fault or invalid operation. Hardware interrupts are asynchronous notifications from devices or timers. Both transfer control through protected handlers. A context switch changes the executing thread and its relevant state; mode can switch during a syscall without necessarily scheduling another thread. Blocking I/O can remove a thread from the runnable set until data or readiness arrives. Nonblocking and event-driven APIs change how waiting is represented, not the fact that device and kernel work must complete.

## See it yourself

**Tiny Proof:** when `strace` is available, predict at least one `write` syscall even though Python executes one `print` call. Without `strace`, the program still demonstrates the language operation but cannot prove kernel entry.

```bash
if command -v strace >/dev/null; then
  strace -e trace=write python3 -c 'print("hello")' 2>&1
else
  python3 -c 'print("hello")'
  printf '%s\n' 'strace unavailable; no syscall claim made'
fi
```

Expected observation: tracing normally shows a write to fd 1 containing `hello`; tracer setup and runtime version may add detail.

Limits of this proof: tracing perturbs timing, reports the traced process scope only, and does not show device completion or durable storage. One syscall does not imply one physical I/O.

## Where it shows up

A high-throughput server can spend substantial time entering the kernel for tiny reads and writes. Buffering, batched operations, or readiness APIs may reduce overhead, but only after profiles and syscall counts locate the cost. Separately, a sandbox reduces process authority with credentials, namespaces, syscall policy, and resource limits. Each mechanism controls a different boundary; running as a non-root user alone is not complete isolation.

## When it breaks

`EPERM` or `EACCES` indicates a policy or credential denial; `EINTR` means an operation was interrupted and its retry contract must be checked; many tiny syscalls suggest missing batching; sleeping threads may be blocked in kernel waits. First capture the exact operation, arguments without secrets, return value, error number, process identity, and stack location. Use focused tracing on a disposable or approved process because syscall arguments can expose sensitive data.

## Practice

**Build:** write through a buffered Python file, flush it, and use focused tracing to count relevant open, write, and close calls. **Break:** open an inaccessible path in a temporary tree and preserve exception plus syscall error. **Explain back:** distinguish function call, runtime operation, syscall, mode switch, interrupt, and context switch. Success means every claim is tied to a trace line or documented limitation.

## Check yourself

1. Why is a system call not necessarily a context switch?
2. How can one language-level I/O operation differ from kernel I/O operations?

## Sources

### REQUIRED

- [syscalls(2)](https://man7.org/linux/man-pages/man2/syscalls.2.html)

### RECOMMENDED

- [The Linux kernel: system calls](https://linux-kernel-labs.github.io/refs/heads/master/lectures/syscalls.html)

### DEEP DIVE

- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)

## Next

Continue to [Virtual Memory and Address Translation](./05-virtual-memory-and-address-translation.md).
