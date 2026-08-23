# Unix, C, and Linux

Unix, C, and Linux made small composable tools and portable systems software a durable foundation for modern infrastructure.

## Why it matters

**Prerequisite:** [Evolution of Operating Systems](./05-evolution-of-operating-systems.md).

Large operating systems were difficult to move between machines and their tools rarely composed cleanly. Unix paired a small set of interfaces with processes, files, and pipes; C made much of the system portable without hiding the machine completely.

That design made systems easier to extend and reuse. Its interfaces now anchor Linux, the common host for cloud and accelerator workloads, along with decades of compatibility, security, and kernel complexity.

## How it works

Unix is a graph of processes connected by byte streams and named resources; Linux is a kernel implementing and extending that model.

The shell parses commands, forks processes, wires descriptors, and executes programs. The kernel tracks identities and permissions, moves bytes through descriptors, and delivers signals. C maps efficiently to machine and OS interfaces.

Pipes decouple producers from consumers but carry untyped bytes, so protocols remain necessary. “Mechanism, not policy” encourages flexible primitives, yet secure defaults and fleet-wide consistency must be layered above them.

## Vocabulary

- **Unix:** The operating-system family and interface tradition built around processes, files, and composition.
- **C:** A compiled systems language closely associated with portable Unix implementation.
- **Linux:** A Unix-like open-source kernel used by most modern server infrastructure.
- **POSIX:** Standards defining portable operating-system interfaces.
- **Shell:** A program that interprets commands and composes processes.
- **Fork:** Creating a new process based on the calling process.
- **Exec:** Replacing a process image with a new program.
- **Pipe:** A kernel buffer connecting one process's output to another's input.
- **File descriptor:** A process-local integer handle for an open kernel object.
- **Signal:** An asynchronous notification delivered to a process or thread.
- **PID 1:** The first process in a Linux PID namespace, with special lifecycle responsibilities.
- **User space:** Unprivileged execution outside the kernel.

## See it yourself

```bash
printf '%s\n' error ok error | sort | uniq -c
printf 'hello\n' | wc -c
id; umask
printf '%s\n' "$$" "$PPID"
```

Predict the two counts and whether `$$` and `$PPID` will differ. The pipeline should count two `error` lines and one `ok`, while the identifiers show shell process ancestry. This supports Unix composition through processes and byte streams. It does not show that text protocols are unambiguous or that every command in a pipeline succeeded.

## Where it shows up

A container entrypoint is still a Linux process, and the first process in its PID namespace has lifecycle duties. If it does not forward `SIGTERM`, children keep running until the orchestrator's grace period expires; if it does not reap exited children, zombies accumulate. Deployment settings can be correct while process behavior is wrong. Process ancestry, signal handling, and exit status are the useful facts.

## When it breaks

A deployment that hangs during termination often points to process behavior, not orchestration. PID 1 may ignore or fail to forward `SIGTERM`, a child may retain a descriptor, or shutdown may block on I/O. First inspect the process tree, delivered signals, open descriptors, and exit statuses inside the same namespace.

## Practice

### Observe

Build a three-command pipeline, redirect stderr separately, send termination signals, and inspect exit statuses and process trees.

### Build

Write a small C or systems-language program that opens a file, forks, connects a pipe, and executes a child command.

### Break

Remove execute permission, close the wrong descriptor, ignore `SIGTERM`, and omit quoting. Explain each observed failure.

### Say it out loud

Explain what the shell and kernel each do for a pipeline.

**Success:** Your listener should be able to predict descriptor wiring, process relationships, and one signal-related failure.

## Check yourself

1. Why did C improve OS portability?
2. What does a pipe abstract and omit?
3. Why is PID 1 special on Linux?

### Interview stretch

- Debug a container that will not terminate.
- Explain file descriptors to an application engineer.
- Which Unix principles scale well, and which need stronger contracts?

## Sources

### REQUIRED

- “The UNIX Time-Sharing System” — Dennis Ritchie and Ken Thompson. [ACM Digital Library](https://dl.acm.org/doi/10.1145/361011.361061). Primary account of Unix’s goals and design.

### RECOMMENDED

- “The Development of the C Language” — Dennis Ritchie. [Bell Labs archive](https://www.bell-labs.com/usr/dmr/www/chist.html). Explains the co-evolution of C and Unix.

### DEEP DIVE

- “The Linux man-pages Project” — Michael Kerrisk and contributors. [Official site](https://www.kernel.org/doc/man-pages/). Canonical userspace interface documentation.

## Next

Continue with [./07-networking-and-the-internet.md](./07-networking-and-the-internet.md).
