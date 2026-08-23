# GPU architecture and instruction execution

A GPU is a throughput machine: many lanes share instruction delivery while hardware switches among ready warps to cover latency.

## Why it matters

Source code hides instruction count, dependency chains, and resource allocation. A kernel can expose thousands of threads yet leave execution units idle because its warps diverge, wait on memory, or exhaust registers.

## How it works

A launch creates a grid of thread blocks. Hardware assigns a whole block to one streaming multiprocessor (SM), allocates its registers and shared memory, and schedules its warps. In NVIDIA terminology a warp contains 32 threads. SIMT means lanes have independent data but usually execute one issued instruction together. A branch with both outcomes active is replayed under lane masks; it does not create two independent processors.

Occupancy is resident warps divided by the architectural maximum. If a block uses \(R\) registers per thread, \(T\) threads, and \(S\) bytes of shared memory, the SM can admit only the minimum block count allowed by registers, shared memory, thread slots, and block slots. More occupancy helps only until enough independent warps cover latency. Instruction-level parallelism within a warp can matter as much.

## See it yourself

Predict the result before calculating. An SM has 65,536 registers and a kernel launches 256-thread blocks using 96 registers per thread. Registers permit only \(\lfloor65536/(256\times96)\rfloor=2\) blocks, or 512 resident threads, before other limits. Recompile at 64 registers and the register bound permits four blocks. This proves a resource bound changed; it does not prove the lower-register binary is faster because spills may add memory traffic.

## Where it shows up

Attention and reduction kernels mix tensor operations, address calculations, barriers, and reductions. Shape-dependent branches can leave lanes inactive. Disassembly and profiler counters connect source regions to issued instructions, active-lane percentage, barriers, and dependency stalls.

## When it breaks

Low occupancy is not automatically a defect, and high occupancy is not utilization. Register caps can spill into local memory; oversized blocks can limit placement; divergent loops wait for the slowest lane; frequent barriers prevent ready work. Compare compiler resource reports, achieved occupancy, eligible warps, active lanes, and stall reasons on the same kernel. Change one launch or compilation parameter at a time.

## Practice

**Observe:** collect block size, registers, shared memory, theoretical occupancy, and achieved occupancy. **Build:** write a spreadsheet that computes the binding limit for three launch shapes. **Break:** cap registers until spills appear and identify the latency and byte-traffic change. Completion requires a prediction, profile, and explanation of any disagreement.

## Check yourself

1. Why can four times as many launched threads leave residency unchanged?
2. Which evidence separates branch divergence from a memory dependency?
3. When can lower occupancy produce higher throughput?

## Sources

### REQUIRED

- [CUDA C++ Programming Guide: hardware implementation](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

### RECOMMENDED

- [CUDA Occupancy Calculator documentation](https://docs.nvidia.com/cuda/cuda-occupancy-calculator/)

### DEEP DIVE

- [NVIDIA Ampere architecture whitepaper](https://www.nvidia.com/en-us/data-center/ampere-architecture/)

## Next

Continue to [Memory systems and data movement](05-memory-systems-and-data-movement.md).
