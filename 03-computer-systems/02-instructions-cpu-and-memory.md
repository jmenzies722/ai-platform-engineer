# Instructions, CPU, and Memory

A processor repeatedly executes machine instructions while registers and memory hold the current state.

## Why it matters

A hot function may spend most of its time waiting for data even though its machine instructions are individually fast. Deciding between algorithm changes, compiler work, and memory-layout changes requires separating language bytecode, native instructions, and the storage hierarchy feeding the processor. “The CPU is slow” is not yet a performance diagnosis.

## How it works

An instruction set defines operations, registers, and addressing visible to machine code. Compilers translate higher-level operations into instructions. Loads bring data toward registers; stores send results toward memory. The CPU uses pipelines and caches to avoid waiting for slower main memory.

An instruction-set architecture defines programmer-visible instructions, registers, addressing, and control transfer. A compiler or runtime emits native instructions for that contract; CPython instead evaluates its own bytecode using a native interpreter. The processor fetches and decodes instructions, executes operations through functional units, and retires results in architectural order even when internal work overlaps. Loads and stores name virtual addresses, which hardware translates before cache lookup and possible main-memory access. Pipelines gain throughput from overlap but must handle dependencies, branches, and exceptions. Interrupts and system calls transfer control to privileged code while preserving enough state to resume. The operating system schedules threads, but the processor executes whichever native stream the selected thread and kernel provide.

## See it yourself

**Tiny Proof:** predict that `dis` shows Python virtual-machine operations for `add`, while `objdump`—when present—shows architecture-specific instructions from a native executable. The two listings should not use the same instruction vocabulary.

```bash
python3 - <<'PY2'
import dis
def add(a, b): return a + b
dis.dis(add)
PY2
command -v objdump >/dev/null && objdump -d "$(command -v true)" | sed -n '1,12p' || true
```

Expected observation: Python bytecode describes work for CPython; disassembly of a native executable shows architecture-specific machine instructions.

Limits of the instructions, cpu, and memory observation: Neither listing reports which instructions actually executed, how many cycles they took, whether they missed cache, or whether the compiler removed work. Static disassembly is a map of possible code, not a profile of one run.

## Where it shows up

Numerical libraries show the boundary in production. A Python call may spend little time in bytecode before entering compiled vector code that processes contiguous arrays with specialized instructions. A Python profiler can attribute time to the extension call without explaining cache misses or instruction throughput; a native profiler and hardware counters answer those deeper questions. Rewriting the call in Python would cross the boundary in the wrong direction.

## When it breaks

Illegal-instruction crashes often mean a binary targets unsupported ISA features; high CPU with slow progress may indicate inefficient instructions or cache behavior; low CPU points toward scheduling or waits instead. First obtain a stack profile and identify whether samples land in runtime, application, library, or kernel code. Only then inspect disassembly or counters around the hot region, preserving compiler flags and input shape for reproducibility.

## Practice

**Build:** compile or inspect a tiny native addition function and compare it with Python `dis` output. **Break:** run a bounds-heavy and a contiguous-array version over equivalent data, without claiming cause from timing alone. **Explain back:** describe what the Python interpreter, OS scheduler, virtual-memory hardware, and CPU each own. Success combines equivalent-result tests, repeated timing, and a profile locating the dominant execution boundary.

## Check yourself

1. How does Python bytecode differ from an ISA instruction?
2. Why is main-memory latency relevant when CPUs execute instructions?

## Sources

### REQUIRED

- [RISC-V ISA specifications](https://riscv.org/technical/specifications/)

### RECOMMENDED

- [Intel software developer manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

### DEEP DIVE

- [Computer Architecture: A Quantitative Approach](https://www.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1)

## Next

Continue to [Caches, Locality, and Measurement](./03-caches-locality-and-measurement.md).
