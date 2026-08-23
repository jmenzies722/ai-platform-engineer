# Origins of Computing

A computer is a machine that follows encoded instructions to transform information, one small state change at a time.

## Why it matters

**Prerequisite:** None. This is the gentlest entry point to the curriculum.

Manual calculation was slow, difficult to repeat, and limited by the person doing it. Early mechanical and electronic machines automated pieces of that work, but fixed wiring still tied a machine to one job.

Programmable control and stored instructions made the same hardware useful for many jobs. Modern CPUs and accelerators are vastly faster, but they still pay for computation, data movement, memory capacity, heat, and power.

## How it works

A computer is a state-transition engine: read encoded state and an instruction, apply logic, write new state, repeat. Performance is bounded not only by arithmetic but by moving bits among storage levels.

A clock coordinates register updates. The processor fetches an instruction, decodes its opcode and operands, executes logic, accesses memory if required, and commits results. Modern processors overlap these stages, predict branches, and cache data while preserving the observable instruction-set contract.

The von Neumann abstraction unifies code and data but creates a bandwidth bottleneck. Parallel accelerators address workloads with abundant similar operations, while caches exploit temporal and spatial locality. Neither removes physical constraints: latency, bandwidth, energy, and synchronization determine usable performance.

## Vocabulary

- **Bit:** A binary digit, usually represented as `0` or `1`.
- **Boolean logic:** Rules for combining true/false values with operations such as AND, OR, and NOT.
- **Transistor:** An electronic switch used to build digital logic.
- **Stored program:** Instructions encoded in addressable memory rather than fixed in wiring.
- **Instruction set architecture (ISA):** The machine-instruction contract visible to software.
- **Register:** Small, fast storage directly used by a processor.
- **Cache:** Small, fast storage that keeps likely-to-be-reused data near a processor.
- **Locality:** The tendency to reuse recently accessed or nearby data and instructions.
- **Bandwidth:** The amount of data transferable per unit of time.
- **Latency:** The delay before an operation or transfer completes.
- **Arithmetic intensity:** The amount of computation performed per byte of data moved.

## See it yourself

```python
# A tiny state transition: accumulator machine
program = [("LOAD", 7), ("ADD", 5), ("STORE", 0)]
acc, memory = 0, [0]
for op, value in program:
    if op == "LOAD": acc = value
    elif op == "ADD": acc += value
    elif op == "STORE": memory[value] = acc
print(memory[0])  # 12
```

Before running it, calculate the accumulator after each instruction. The expected printout is `12`: `LOAD` sets state, `ADD` changes it, and `STORE` copies it to memory. That observation supports the state-transition model used here. It says nothing about clocks, gates, caches, or how a physical CPU executes an instruction.

## Where it shows up

A model server can report low GPU utilization even while issuing billions of operations. If weights and activations arrive from memory more slowly than the arithmetic units consume them, kernels wait on data. Batching may reuse weights across requests, and quantization may move fewer bytes, but both change latency, memory use, or numerical behavior. The old physical constraints remain visible in a modern serving decision.

## When it breaks

A visible failure is high accelerator occupancy paired with low request throughput. The workload may be limited by memory bandwidth, cache misses, synchronization, or an input shape unlike the benchmark—not by insufficient arithmetic. First compare time and bytes moved per operation with hardware counters or a profiler; that evidence separates compute saturation from data starvation.

## Practice

### Observe

Run a large array sum twice and compare cold versus warm timings. Vary element width and working-set size. Record where caches stop hiding memory latency and explain the change.

### Build

Implement an 8-bit virtual accumulator with `LOAD`, `ADD`, `SUB`, `JUMP_IF_ZERO`, and `STORE`. Define overflow behavior and test every opcode.

### Break

Create a program that overflows, jumps forever, and reads an invalid address. Add traps and limits that turn each silent failure into explicit evidence.

### Say it out loud

Explain why more FLOPS may not increase model throughput.

**Success:** A listener should be able to identify the relevant state transition and choose one measurement that separates compute from memory limits.

## Check yourself

1. Why did stored programs change machine capability?
2. Why can memory bandwidth dominate arithmetic?
3. Which details does an instruction set hide, and which leak?

### Interview stretch

- Why does a GPU outperform a CPU for some workloads but not all?
- Explain locality to someone diagnosing low accelerator utilization.
- How would you distinguish compute-bound from memory-bound inference?

## Sources

### REQUIRED

- “First Draft of a Report on the EDVAC” — John von Neumann. [Computer History Museum](https://www.computerhistory.org/revolution/birth-of-the-computer/4/88/359). Documents the stored-program architecture that anchors the modern machine model.

### RECOMMENDED

- “The Computer History Timeline” — Computer History Museum. [Timeline](https://www.computerhistory.org/timeline/). Connects devices and ideas without reducing the history to one invention.

### DEEP DIVE

- “The Free Lunch Is Over” — Herb Sutter. [Dr. Dobb’s archive](http://www.gotw.ca/publications/concurrency-ddj.htm). Explains why power and concurrency changed software performance assumptions.

## Next

Continue with [./02-why-software-exists.md](./02-why-software-exists.md).
