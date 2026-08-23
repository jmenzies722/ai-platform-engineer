# Processes, Memory, and Files

A process is a running instance with an identity and a private view of memory plus handles to kernel-managed resources.

## Why it matters

A service can report “out of memory” while its large virtual size is mostly unmapped or shared, and a stale PID can point at an entirely different process after reuse. Capacity changes and emergency signals are unsafe when identity and memory measurements are vague. Engineers need to distinguish an address-space reservation from resident pages and a descriptor number from the resource it currently names.

## How it works

Linux identifies a process with a PID and gives it a virtual address space. Page tables translate virtual addresses to physical pages. File descriptors are small integers in a per-process table; they can refer to files, terminals, pipes, or sockets. Descriptors 0, 1, and 2 conventionally mean standard input, output, and error.

Process creation gives the kernel an object with credentials, a PID, one or more threads, and references to resources. Each process sees virtual addresses; page tables and memory mappings determine whether an access reaches anonymous memory, a file-backed page, shared code, or an invalid region. RSS estimates pages currently resident, while VSZ counts a much broader mapped address range. An open operation installs a reference in the process file-descriptor table and returns its small integer index. Duplication and redirection can make several indexes refer to the same open file description, including its offset and flags. On exit the kernel closes the process references and tears down mappings, but persistent file contents remain. `/proc/PID` is a live view of this kernel state rather than a historical record.

## See it yourself

**Tiny Proof:** before starting the command, predict that `/proc/PID/exe` names Python, fd 1 names the current terminal or capture pipe, and VSZ is larger than RSS. Compare both `ps` samples rather than treating one state letter as a timeline.

```bash
python3 -c 'import os,time; print(os.getpid(), flush=True); time.sleep(15)' &
pid=$!
ps -o pid,ppid,stat,vsz,rss,args -p "$pid"
readlink "/proc/$pid/fd/1"
wait "$pid"
```

Expected observation: The process has a parent and a state. VSZ normally exceeds RSS, and fd 1 names the destination of standard output.

Limits of the processes, memory, and files observation: The sample cannot assign every resident page uniquely to the process, prove that the process is healthy, or establish that bytes written to fd 1 reached a remote consumer. Shared-page accounting and rapidly changing state require more specific tools for those claims.

## Where it shows up

A web server under a memory limit illustrates why the distinctions matter. Its workers map the interpreter, shared libraries, application files, heaps, and anonymous arenas; a dashboard may add RSS values and double-count shared pages. At the same time, rotated logs can leave deleted files open through worker descriptors. Examining mappings, proportional memory where available, and `/proc/PID/fd` leads to different remediation than increasing the limit or deleting a pathname again.

## When it breaks

`PermissionError` on open suggests path traversal, credentials, or mode policy; steadily rising anonymous RSS suggests live allocations; a large stable VSZ alone is not a leak. First prove identity with PID, owner, start context, executable, and command line, then capture `status`, mappings, and descriptor targets. If disk space remains consumed after deletion, inspect open descriptors before searching for hidden files. Never signal from an old PID note without revalidating identity.

## Practice

**Build:** complete [Inspect One Python Process](../labs/01-software-execution/README.md) and add a controlled open file to a copy of the workload. **Break:** close that descriptor early and attempt one more write, then preserve the exception and descriptor listing. **Explain back:** distinguish program, process, virtual mapping, resident page, descriptor, and file in one concrete story. Success means another learner can reproduce your report and identify exactly which command supports each claim.

## Check yourself

1. How does a program differ from a process?
2. Why can two descriptors refer to the same kernel object?

## Sources

### REQUIRED

- [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)

### RECOMMENDED

- [proc_pid_status(5)](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)

### DEEP DIVE

- [The Linux Programming Interface](https://man7.org/tlpi/)

## Next

Continue to [Concurrency and Waiting](./03-concurrency-and-waiting.md).
