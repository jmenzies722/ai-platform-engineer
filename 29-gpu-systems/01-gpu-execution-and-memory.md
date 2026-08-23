# GPU execution and memory

GPUs run many similar operations concurrently, but performance depends on feeding those operations without excessive movement or divergence.

## Why it matters

Peak FLOPS describe an upper bound, not application speed. Memory traffic and execution shape often dominate.

## How it works

Threads execute in warps grouped into blocks. Blocks occupy streaming multiprocessors subject to register and shared-memory limits. Global memory is large and slow; caches, shared memory, and registers are progressively smaller and faster. Coalesced accesses combine adjacent requests. Branch divergence serializes paths within a warp.

The scheduler hides memory latency by switching among ready warps; it does not make memory free. Occupancy describes resident warps relative to a limit, while achieved utilization depends on whether those warps have useful work. Blocks cannot share ordinary synchronization, so decomposition also sets communication boundaries. Host-device transfers cross a much slower boundary and should be amortized.

## See it yourself

Have 32 threads read adjacent four-byte values: a 128-byte region can satisfy the warp with a small number of transactions. Give thread \(i\) address \(i\times128\): useful bytes remain 128, but requests span 32 regions. Expect dramatically lower effective bandwidth. This proves address pattern, not arithmetic count, controls transaction efficiency.

## Where it shows up

In an embedding lookup, irregular indices cause scattered global reads and little reuse. Batching improves parallelism but does not guarantee coalescing. A profiler showing low compute utilization with high memory throughput points toward bandwidth limits; low values for both can indicate launch overhead or dependency stalls.

## When it breaks

Small kernels underfill the device, transfers dominate, divergence wastes lanes, and excess registers reduce occupancy. First capture a timeline plus achieved occupancy, memory throughput, warp-stall reasons, and transfer time. Do not infer “GPU is slow” from wall time alone. Compare a known contiguous kernel to separate layout problems from environment or clock limits.

## Practice

**Build:** profile contiguous and strided elementwise kernels and reconcile useful bytes with measured bandwidth. **Break:** add a data-dependent branch and a host copy per iteration; identify their distinct timeline signatures. **Explain back:** distinguish occupancy, utilization, and coalescing using profiler evidence, not peak specifications.

## Check yourself

1. What is coalescing?
2. Why can high occupancy still be slow?
3. What causes warp divergence?

## Sources

### REQUIRED

- [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

### RECOMMENDED

- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)

### DEEP DIVE

- [NVIDIA GPU architecture whitepapers](https://www.nvidia.com/en-us/data-center/resources/gpu-architecture/)

## Next

Continue to [Kernels, precision, and performance](02-kernels-precision-and-performance.md).
