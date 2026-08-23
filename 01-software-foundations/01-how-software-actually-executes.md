# How Software Actually Executes

## In One Sentence

Your source code becomes running behavior only because a language runtime, the operating system, memory machinery, and the CPU cooperate to produce an observable result.

## Why This Exists

**Prerequisite:** [Why Software Exists](../00-history/02-why-software-exists.md) gives the gentlest explanation of software as changeable instructions. [Evolution of Operating Systems](../00-history/05-evolution-of-operating-systems.md) is helpful but not required.

Typing `python3 hello.py` feels like one action. It is actually a chain of translations and resource decisions. Without that chain, phrases such as “the code is slow,” “the process is stuck,” and “nothing printed” are too vague to debug.

Without a layered execution model, “the code is slow” or “Python did not print” is too vague to debug. The source may be waiting on an import, the process may be sleeping, the scheduler may not be giving it CPU time, memory pages may be faulting in, a syscall may be blocked, or output may still be in a user-space buffer.

The model in this lesson turns a symptom into testable questions:

1. Did source become a valid code object?
2. Is the expected process alive and in the expected state?
3. Is its address space mapped and resident as expected?
4. Is it running on a CPU, runnable, sleeping, or blocked?
5. Did it request an OS operation, and what happened?
6. Where is output directed, and has buffering delayed it?

## Picture This

Imagine sending a handwritten recipe to a restaurant:

1. the recipe must be readable;
2. a trained cook interprets each instruction;
3. the kitchen manager assigns a workstation and controls shared equipment;
4. ingredients and intermediate dishes need places to live;
5. hands and machines perform the physical work;
6. a server carries the result to the right table.

Source code is the recipe. CPython is the trained cook. The operating system is the kitchen manager. A process is this particular order in progress. Memory is its labeled workspace. The CPU performs the physical steps. Standard output is one delivery route.

The analogy gives us roles. The engineering model gives us exact boundaries and evidence.

## The Real Definition

Software execution is a sequence of state changes performed by a physical CPU under the coordination of a language implementation and an operating system.

Use this causal chain:

**Source Code → Interpreter/Compiler → OS → Process → Memory → CPU → Output**

The arrows are not a one-time conveyor belt. Execution moves back and forth:

- CPython asks the OS for memory, files, clocks, and I/O.
- The OS schedules and pauses the process many times.
- The CPU alternates between user-mode interpreter instructions and kernel-mode instructions.
- A read, page fault, timer, signal, or device event can change what happens next.

The most important distinction is between an abstraction and its implementation. “Compiled” and “interpreted” describe useful execution strategies, not mutually exclusive language identities. Python source is commonly compiled to Python bytecode; CPython interprets that bytecode; CPython itself is compiled native code; and alternative Python implementations may use just-in-time or ahead-of-time compilation.

### Program, executable, and process

A **program** is code and data stored somewhere. An **executable** is a file format the OS loader can map and start directly, such as an ELF binary on Linux. A **process** is a running OS-managed instance with an identity, virtual address space, threads, file descriptors, credentials, and execution state.

A `.py` file is usually data consumed by the Python executable; Linux does not directly execute Python syntax. With a shebang such as `#!/usr/bin/env python3`, the kernel uses the named interpreter to run the script.

### Compiler and interpreter

A **compiler** translates one representation into another before or during execution. An **interpreter** directly implements the semantics of an input representation. CPython uses both ideas:

1. tokenize and parse source;
2. build an abstract syntax tree (AST);
3. compile the AST to a code object containing Python bytecode;
4. evaluate bytecode instructions in the CPython interpreter loop.

Cached `.pyc` files may avoid recompiling unchanged imported modules, but they are not native machine-code executables.

### Kernel and system calls

The OS **kernel** controls protected resources. User code cannot directly ask a disk controller to write bytes or arbitrarily map physical memory. It requests services through **system calls** such as `read`, `write`, `mmap`, and `execve`. Python APIs often pass through CPython C code and the C library before reaching a syscall.

### Virtual memory and pages

Each process sees a private **virtual address space** divided into pages. Page tables map virtual pages to physical memory or other backing, with permissions such as readable, writable, and executable. Mappings can represent the Python executable, shared libraries, heap, thread stacks, anonymous memory, and files.

A mapping does not mean every byte is currently in RAM. Access can trigger a **page fault**, allowing the kernel to establish a mapping, load file-backed data, allocate a zero-filled page, or reject invalid access.

### Scheduling and CPU execution

Threads are the units Linux schedules. A runnable thread waits in a run queue until the scheduler selects it for a logical CPU. The CPU then executes native instructions, updates registers and caches, and may be interrupted or preempted.

For ordinary CPython, the CPU is executing machine instructions from the CPython binary and its libraries—not Python bytecode directly. Those native interpreter instructions inspect the next Python opcode and implement its semantics. Native extension modules can execute their own machine code.

### File descriptors, streams, and output

Linux processes conventionally begin with file descriptors `0`, `1`, and `2` for standard input, output, and error. They may point to a terminal, regular file, pipe, socket, or other object. Python’s `print` writes through a buffered text stream. That stream eventually causes one or more OS writes. A successful write means the kernel accepted bytes; it does not always mean a physical device or remote consumer has durably processed them.

The three layers are:

1. **Intuition:** source describes intent; several systems turn it into visible behavior.
2. **Mechanism:** CPython parses and compiles source to bytecode, interprets that bytecode, and requests protected services from Linux.
3. **Engineering:** process state, mappings, scheduling, syscalls, file descriptors, and buffering provide evidence when behavior differs from intent.

## Mental Model

```mermaid
flowchart TD
    A["Python source (.py)"] --> B["Tokenizer + parser"]
    B --> C["AST + symbol analysis"]
    C --> D["Compiler"]
    D --> E["Code object + Python bytecode"]
    E --> F["CPython evaluation loop"]
    F --> G["Native CPython instructions"]
    G --> H["CPU executes user-mode instructions"]
    F --> I["Runtime objects in virtual memory"]
    I <--> J["Page tables / physical memory"]
    H --> K["System-call boundary"]
    K --> L["Linux kernel"]
    L --> M["Scheduler, files, pipes, terminal, devices"]
    M --> N["Observable output"]
    L --> H
```

The diagram separates language-level bytecode from native CPU instructions and shows that the kernel participates at controlled boundaries rather than executing every Python operation.

Narrate the main path as:

**Source → Runtime/Compiler → OS → Process → Memory → CPU → Output**

Do not picture a one-way conveyor belt. While the program runs, the runtime repeatedly touches memory, the OS pauses and resumes threads, the CPU crosses into kernel code for protected operations, and output may wait in buffers.

## How It Actually Works

Consider:

```python
message = "hello"
print(message.upper())
```

### 1. The shell starts Python

After the shell resolves `python3` using its command-search rules, it typically creates a child and invokes an `exec`-family operation. On Linux, `execve` replaces the calling process image with the Python executable. The kernel validates the executable format, creates memory mappings, prepares arguments and environment data, and transfers control through the program loader.

This is the OS executing the **Python executable**, not parsing the `.py` file.

### 2. CPython initializes

Startup code initializes the runtime, memory allocators, built-in types, import machinery, standard streams, and interpreter state. Shared libraries and modules may be mapped or loaded. This explains why even a tiny program has significant startup time and memory use.

### 3. CPython reads and parses source

CPython obtains source bytes through file operations, determines source encoding, tokenizes the text, applies the Python grammar, and creates an AST. Syntax errors occur here, before the module body begins executing.

### 4. CPython compiles to bytecode

The compiler validates and transforms the AST, builds symbol-table information, and emits a **code object**. The code object contains bytecode plus constants, names, variable metadata, and source-position information. `dis.dis()` exposes a human-readable view of bytecode, but exact opcodes vary by Python version.

### 5. The evaluation loop executes the code object

CPython creates a frame holding execution state such as local variables, references, and the instruction position. Its evaluation machinery dispatches bytecode operations. In recent CPython versions, adaptive specialization may replace general operations with forms optimized for observed types. This is still an implementation detail; source semantics remain defined by the language reference.

For `message.upper()`, CPython resolves a name, looks up an attribute, performs a call, and creates or retrieves Python objects. Reference counting handles most object-lifetime updates in CPython, while cyclic garbage collection handles certain reference cycles.

### 6. Memory accesses resolve through virtual memory

The frame, string objects, interpreter state, native stacks, executable code, and shared-library code occupy virtual addresses. CPU memory accesses are translated using page tables, usually accelerated by a translation lookaside buffer. Missing translations or unavailable pages can fault into the kernel.

### 7. Linux schedules the executing thread

The Python thread alternates among running, runnable, and sleeping states. It can be preempted after a scheduling interval or block while waiting for I/O. CPython’s global interpreter lock also affects when multiple Python threads may execute Python bytecode in a standard build, although version and build configuration matter.

### 8. The CPU executes native instructions

The CPU fetches and retires machine instructions belonging to CPython, libraries, extension modules, and—during kernel entry—the OS. Python bytecode such as a call instruction is data interpreted by those native instructions. It is not the CPU’s instruction set.

### 9. Output crosses the syscall boundary

`print` converts values to text and writes to `sys.stdout`. The text layer encodes characters into bytes and buffering may retain them. When flushed, CPython eventually requests a write to file descriptor `1`. The kernel routes those bytes to whatever fd `1` references. If that is a terminal, a terminal subsystem and emulator render the visible characters.

### 10. The process exits

On normal completion, Python flushes standard streams, runs defined shutdown machinery, and returns an exit status. The kernel releases process resources and retains a small exit record until the parent collects it. Open file descriptors are closed; memory mappings do not survive the process.

### Boundaries that sharpen the model

### `exec` does not create a new process

This common shortcut is inaccurate. On POSIX systems, `execve` replaces the current process image while preserving the process identity across the transition. A shell commonly uses `fork` or a related creation mechanism first, then the child performs `execve`. The combination appears to “start a new program.”

### Bytecode caches

Imported Python modules may produce cache files under `__pycache__`. CPython checks cache metadata or hashes before reusing them. A cache improves module loading but does not remove runtime interpretation. The main script is not generally cached in the same way as imported modules.

### Virtual memory measurements

Tools report different quantities:

- **VSZ/VmSize:** virtual address space reserved or mapped.
- **RSS/VmRSS:** pages currently resident in physical memory, with caveats around sharing.
- **PSS:** shared pages divided proportionally among mapping processes.
- **Heap:** one region used for dynamic allocation; Python can also allocate through anonymous mappings.

Therefore “the process has 500 MB of virtual memory” does not imply it owns 500 MB of physical RAM.

### Syscalls are observable boundaries

Many Python operations are entirely in user space. Integer operations, attribute lookup, and most bytecode dispatch do not make a syscall each time. Opening a file, waiting on a socket, or writing flushed output eventually crosses into the kernel. On Linux, `strace` can observe many of these boundaries, though tracing changes timing and carries overhead.

### Buffering changes visibility

When stdout is connected to an interactive terminal it is commonly line-buffered; when redirected to a pipe or file it is commonly block-buffered. `print(..., flush=True)` or `python3 -u` requests more immediate stream behavior. Buffering explains why logs can appear promptly in a terminal but arrive late in a container pipeline.

## Tiny Proof

The smallest useful proof has two parts. The first shows that Python source becomes bytecode before execution:

```bash
python3 - <<'PY'
import dis

source = 'print("hello".upper())'
code = compile(source, "<tiny-proof>", "exec")
dis.dis(code)
exec(code)
PY
```

You should see bytecode instructions and then `HELLO`. Exact opcode names vary by Python version. The stable claim is that CPython produced a code object and executed it; the CPU did not execute the source text or Python bytecode directly.

The second proves that source, executable, and process are different things:

```bash
python3 -c 'import os, time; print(os.getpid(), flush=True); time.sleep(15)' &
pid=$!
ps -o pid,ppid,stat,vsz,rss,comm,args -p "$pid"
readlink "/proc/$pid/exe"
wait "$pid"
```

The command line includes Python source, `/proc/.../exe` points to the Python executable, and `ps` reports one running process. That observation makes three often-confused concepts visible.

## In Production

Suppose a worker logs `starting batch`, performs work, and logs `done`, but a dashboard shows neither line for a minute.

1. `ps` shows the worker process exists, so startup reached the OS process layer.
2. Its state is `S`, indicating interruptible sleep rather than current CPU execution.
3. `/proc/<pid>/fd/1` points to a pipe, not a terminal.
4. The worker’s stdout is block-buffered because it is redirected.
5. Running with `python3 -u` or using configured, flushed logging makes records visible promptly.

The source was executing correctly; output visibility was delayed between Python’s stream layer and the pipe. Adding random retries would not address the cause.

- **Containers:** PID namespaces change which processes are visible, while cgroups constrain CPU and memory. A container is not a process model replacement.
- **Web servers:** worker count, thread scheduling, socket syscalls, and buffering shape latency and throughput.
- **Serverless functions:** runtime startup, module imports, page population, and connection setup contribute to cold starts.
- **Data and AI jobs:** virtual mappings, resident pages, native numerical libraries, CPU scheduling, and accelerator transfers all affect performance.
- **Observability:** profiles sample user-space execution; syscall traces show kernel boundaries; process metrics summarize scheduling and memory state.
- **Incident response:** exit codes, signals, OOM termination, blocked I/O, and file-descriptor destinations provide evidence beyond application logs.

Use the chain to ask better questions:

| Layer | Production question |
|---|---|
| Source/runtime | Did parsing, import, allocation, or bytecode/native execution fail? |
| OS/process | Does the expected process exist, and what state is it in? |
| Memory | Is address space merely mapped, actually resident, or constrained by a cgroup? |
| CPU | Is the thread running, runnable, throttled, or waiting? |
| Output | Where does file descriptor `1` point, and has buffering delayed visibility? |

## How It Breaks

| Symptom | Likely layer | Useful evidence |
|---|---|---|
| `SyntaxError` before any expected output | Parser/compiler | traceback and source location |
| `ModuleNotFoundError` | Runtime/import environment | `sys.path`, active interpreter, environment |
| Process exists but CPU stays near zero | Scheduler wait or blocked I/O | `ps` state, wait channel, syscall trace |
| Process uses high CPU with little output | User-space runtime/native code | profiler, thread/process CPU metrics |
| Memory value looks unexpectedly large | Virtual-memory interpretation | compare VSZ, RSS, mappings, PSS |
| Output appears late after redirection | Stream buffering | fd target, `flush=True`, `-u` experiment |
| `PermissionError` opening a file | OS policy/filesystem | credentials, path permissions, syscall error |
| Exit status `137` in common shells | Usually signal 9 (`128 + 9`) | orchestrator events, kernel/cgroup OOM evidence |

Do not infer an OOM kill from `137` alone; an administrator or orchestrator can also send `SIGKILL`.

The table is a starting hypothesis map, not a lookup oracle. A process can be sleeping for healthy reasons; status `137` can result from any `SIGKILL`; high virtual size is not automatically a leak.

## Debug It

1. **State the symptom precisely.** Include time, command, exit status, missing or present output, and environment.
2. **Locate the last proven layer.** A syntax traceback proves parsing began; a PID proves process creation; an fd target proves output routing.
3. **Form one falsifiable hypothesis.** Example: “stdout is buffered because fd 1 is a pipe.”
4. **Choose minimally invasive evidence.** Start with `ps`, `/proc`, Python introspection, logs, and exit status.
5. **Run a controlled comparison.** Change one variable, such as adding `-u`, while preserving the workload.
6. **Account for observation effects.** Tracing and profiling add overhead; debuggers can change scheduling.
7. **Explain the full causal chain.** Record why the evidence supports the conclusion and what alternatives remain.

The transferable move is **last proven boundary**. A PID proves that the OS created an execution context. It does not prove useful work. A successful `write` proves the kernel accepted bytes. It does not prove a remote consumer processed them.

## Build / Break Exercises

### Guided lab

Complete [Inspect a Python Process on Linux](../labs/01-software-execution/README.md). The lab starts from copyable commands, pauses for predictions, and ends with an explanation you can give without notes.

### Build

Create `execution_story.py` that:

1. prints its PID, parent PID, and Python executable;
2. prints whether stdout is attached to a terminal;
3. allocates a configurable amount of memory;
4. sleeps briefly so another shell can inspect it;
5. writes one message to stdout and one to stderr with explicit flushing.

Then produce a one-page evidence note connecting each observation to **Source Code → Interpreter/Compiler → OS → Process → Memory → CPU → Output**. Include at least one claim you initially made but revised after inspecting evidence.

**Success criteria:** another learner can run your program, identify each layer from evidence, and reproduce your explanation without guessing.

### Break

Make one controlled change at a time:

- introduce a syntax error and identify why no module statement runs;
- redirect stdout and remove explicit flushing to observe buffering;
- request a nonexistent file and record the exception plus OS error;
- allocate additional memory gradually and compare VSZ with RSS.

Do not intentionally exhaust machine memory, create an unbounded loop, inspect unrelated users’ processes, or send signals to processes you did not start.

**Success criteria:** for each controlled failure, record the prediction, symptom, evidence, responsible layer, correction, and one tempting but unsupported conclusion.

### No-AI challenge

Without an AI assistant:

1. Write a Python program that prints its PID and sleeps for 30 seconds.
2. Use only `python3`, `ps`, `/proc`, and shell built-ins to identify its parent PID, executable path, process state, stdout destination, virtual memory, and resident memory.
3. Draw the execution chain from source to output.
4. Explain in 150 words why Python bytecode is not CPU machine code.
5. Predict what changes when stdout is redirected to a file, then test the prediction.

Documentation and local manual pages are allowed. Save commands and outputs as evidence.

## Explain It to Anybody

### 1. To a smart non-engineer

“A source file is a set of instructions, not a moving thing. Python reads and prepares those instructions. The operating system creates a protected running workspace and takes turns giving it the processor. The processor performs the real physical work, and the result travels through an output route such as the terminal. If nothing appears, we can inspect each handoff instead of saying only ‘the code is broken.’”

### 2. To a junior engineer

“With CPython, source is parsed into an AST and compiled into a code object containing Python bytecode. A Linux process runs the native CPython executable in a virtual address space. Linux schedules its threads; the CPU executes native interpreter and kernel instructions. Operations needing protected resources cross the syscall boundary. `print` passes through text encoding and buffering before bytes reach file descriptor 1.”

### 3. In an interview (60–90 seconds)

“When I run `python3 app.py`, the shell starts the Python executable—commonly by creating a child that calls `execve`. Linux maps the executable and libraries into a process address space. CPython initializes, reads the source, parses an AST, and compiles a code object with bytecode. Its evaluation loop implements those bytecode operations using native CPU instructions. Linux schedules the thread and maps its virtual memory pages. For protected operations, CPython enters the kernel through syscalls. `print` converts values to text, encodes and buffers bytes, and eventually writes to file descriptor 1. This layered model gives me a debugging sequence: prove parsing, process state, memory, CPU or wait state, syscall behavior, fd destination, and buffering with evidence appropriate to each boundary.”

Do not memorize these scripts. Rebuild them around one concrete program such as `print("hello")`.

## Knowledge Check

1. Does Linux execute Python bytecode directly?
2. Why can Python reasonably be described as both compiled and interpreted?
3. What does `execve` do to the calling process?
4. What is the difference between virtual size and resident set size?
5. Why might a runnable process not execute immediately?
6. Which layer translates a Python `print` into bytes before an OS write?
7. Why can redirected output appear later than terminal output?
8. Does a page fault always indicate a bug?
9. What evidence would distinguish a blocked process from a CPU-bound one?
10. Why is exit status `137` insufficient by itself to prove an OOM kill?

<details>
<summary>Answer guide</summary>

1. No. A CPU executes native instructions from CPython; CPython interprets Python bytecode.
2. CPython compiles source to bytecode and then interprets that bytecode.
3. It replaces the current process image with a new program image; it does not itself create a new PID.
4. Virtual size measures mapped/reserved address space; RSS estimates currently resident physical pages.
5. Other runnable threads may be selected, CPU quota may constrain it, or scheduler policy and priority may delay it.
6. Python’s text I/O and encoding layers, implemented by CPython, produce bytes; buffering may precede the syscall.
7. Stream buffering policy commonly changes when stdout is not a terminal.
8. No. Demand paging routinely uses page faults to establish valid mappings.
9. Process state, CPU-time change, wait channel, stack/profile samples, and syscall tracing.
10. Signal 9 produces that conventional shell status regardless of who or what sent it.

</details>

### Interview stretch

1. Walk from `python3 app.py` to the first line appearing in a terminal.
2. What is the difference between a program and a process?
3. If Python is interpreted, why does `dis` show bytecode?
4. What does the CPU execute while a CPython function runs?
5. Explain virtual memory to an engineer who thinks it is “disk pretending to be RAM.”
6. A Python service has high VSZ but stable RSS. What would you investigate before calling it a leak?
7. A worker is alive, has near-zero CPU, and produces no logs. How do you narrow the cause?
8. Why might `print` behavior differ between local execution and a container log collector?
9. Where do syscalls fit into Python execution, and why is not every bytecode operation a syscall?
10. How would you prove that a production process was killed by a memory limit rather than merely observing status `137`?

Strong answers distinguish model from implementation, name evidence, and state what cannot be concluded from one metric.

## Vocabulary

- **AST:** Tree representation of parsed source structure.
- **Bytecode:** Intermediate instructions for a language virtual machine, not generally native CPU instructions.
- **Code object:** CPython runtime object containing bytecode and execution metadata.
- **Compiler:** System that translates one code representation into another.
- **File descriptor:** Per-process integer handle referring to an open kernel-managed object.
- **Interpreter:** System that directly implements the semantics of an input representation.
- **Kernel:** Privileged OS component managing hardware and protected resources.
- **Page:** Fixed-size unit used in virtual-memory mapping.
- **Page fault:** CPU exception raised when a memory translation needs kernel handling or is invalid.
- **Process:** OS-managed execution context with an identity and resources.
- **Resident set size (RSS):** Estimate of a process’s currently resident physical pages.
- **Scheduler:** Kernel subsystem that selects runnable threads for CPUs.
- **System call:** Controlled request from user space to the kernel.
- **Virtual address space:** Process-visible address range translated through page tables.
- **VSZ:** Total virtual memory size reported for a process.

Use a term only after you can point to its place in the execution chain. The curriculum-wide [Glossary](../GLOSSARY.md) includes both plain and precise definitions.

## References

### REQUIRED

- [Python Language Reference — Execution model](https://docs.python.org/3/reference/executionmodel.html) — the language-level execution contract.
- [Python Library Reference — `ast`](https://docs.python.org/3/library/ast.html) — the parsed tree used in the Tiny Proof.
- [Python Library Reference — `dis`](https://docs.python.org/3/library/dis.html) — the supported way to inspect CPython bytecode.
- [Linux man-pages — `execve(2)`](https://man7.org/linux/man-pages/man2/execve.2.html) — the process-image replacement boundary.
- [Linux man-pages — `proc(5)`](https://man7.org/linux/man-pages/man5/proc.5.html) — the process evidence used in the lab.
- [Linux man-pages — `write(2)`](https://man7.org/linux/man-pages/man2/write.2.html) — the kernel output boundary.

### RECOMMENDED

- [CPython Developer Guide — Compiler design](https://devguide.python.org/internals/compiler/) — source, AST, code object, and bytecode pipeline.
- [Python C API — Code objects](https://docs.python.org/3/c-api/code.html) — precise CPython representation details.
- [Linux kernel documentation — Process addresses](https://docs.kernel.org/mm/process_addrs.html) — virtual-memory mappings and address spaces.
- [Linux kernel documentation — Scheduler](https://docs.kernel.org/scheduler/index.html) — how Linux shares CPUs.

### DEEP DIVE

- [CPython source — bytecode definitions](https://github.com/python/cpython/blob/main/Python/bytecodes.c) — implementation-level opcode behavior; version-specific by design.
- [Linux man-pages — `proc_pid_status(5)`](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html) — exact meanings and limits of process status fields.

## Next

Open [labs/01-software-execution/README.md](../labs/01-software-execution/README.md) and make the execution chain visible on a Linux machine. After the lab, continue to [Module 02: Python](../02-python/README.md); Module 01’s remaining lessons are intentionally not yet published.
