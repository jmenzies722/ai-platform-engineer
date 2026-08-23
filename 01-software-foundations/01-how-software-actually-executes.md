# How Software Actually Executes

A source file is inert text. A language implementation and the operating system turn it into a process whose instructions a CPU can execute.

## Why it matters

A production worker can have valid source, a live PID, and no visible output. Deciding whether to change code, restart a process, or inspect an output pipe depends on knowing which stage has actually succeeded. This model turns “Python is stuck” into separate questions about parsing, runtime evaluation, scheduling, system calls, and stream buffering.

## How it works

When you run `python3 app.py`, the shell starts CPython. CPython parses source, compiles it to bytecode, and evaluates that bytecode. Linux supplies a process, virtual memory, scheduling, and file descriptors. The processor executes CPython machine instructions; it does not execute Python source.

The shell first resolves `python3` and asks the kernel to replace a child process image with that executable. CPython then initializes its runtime, reads the script, creates an abstract syntax tree, and compiles a code object. Its evaluation loop implements Python bytecode by executing native instructions from CPython and its libraries. Operations such as integer addition may stay in user space; opening a file or flushing output eventually crosses a system-call boundary. Linux can pause the thread between any of those operations, and virtual-memory faults can briefly return control to the kernel. A visible line therefore depends on several independently inspectable events: the module must compile, the frame must run, text must be encoded, a buffer must flush, and fd 1 must lead somewhere observable.

## See it yourself

Predict that disassembly appears before `hello`, and that opcode names may differ with the installed Python version. The important result is the ordering: a code object exists before `exec` evaluates it.

```bash
python3 - <<'PY2'
import dis
code = compile('print("hello")', '<demo>', 'exec')
dis.dis(code)
exec(code)
PY2
```

Expected observation: You should see version-specific bytecode followed by `hello`. The stable observation is that CPython created and executed a code object.

Limits of the how software actually executes observation: This proof does not show which native CPU instructions implement an opcode, whether output crossed the kernel in one write, or how a different Python implementation executes the same source. `dis` exposes CPython bytecode, not an architectural instruction trace.

## Where it shows up

Consider a containerized batch worker whose “started” line arrives several minutes late. The same image may print immediately in an interactive terminal because stdout is line-buffered there, then buffer larger blocks when fd 1 is a pipe connected to a log collector. Inspecting the process, fd target, and behavior under `python3 -u` can isolate visibility from computation. Rewriting the batch algorithm would be an expensive response to an output-boundary problem.

## When it breaks

A `SyntaxError` before the first application line points toward parsing; a live process with growing CPU time points toward active evaluation; a sleeping process with fd 1 aimed at a pipe makes waiting or buffering plausible. First capture the exact command, exit status, PID state, and fd destinations. Add `dis`, profiling, or syscall tracing only after that snapshot identifies the boundary worth observing; tracing everything first changes timing and produces noise.

## Practice

**Build:** write a script that prints its PID, executable, and whether stdout is a terminal, then sleeps for ten seconds. **Break:** add a syntax error and separately redirect an unflushed print to a file; record how the two symptoms differ. **Explain back:** narrate one successful run from source read through fd 1 without saying that the CPU executes Python source. Success is an evidence note containing the prediction, observed command output, responsible boundary, and one conclusion each observation cannot support.

## Check yourself

1. What does the CPU execute during ordinary CPython evaluation?
2. Why is Python reasonably called both compiled and interpreted?

## Sources

### REQUIRED

- [Python execution model](https://docs.python.org/3/reference/executionmodel.html)

### RECOMMENDED

- [CPython compiler design](https://devguide.python.org/internals/compiler/)

### DEEP DIVE

- [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html)

## Next

Continue to [Processes, Memory, and Files](./02-processes-memory-and-files.md).
