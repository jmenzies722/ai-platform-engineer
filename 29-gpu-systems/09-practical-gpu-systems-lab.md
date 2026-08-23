# Practical lab: simulate a GPU performance investigation

This lab turns architecture, memory, profiling, topology, scheduling, and OOM claims into calculations that run without a GPU.

## Why it matters

GPU access is scarce, but sound investigations begin with falsifiable bounds and resource ledgers. The same notebook can later ingest real profiler measurements.

## How it works

Create a Python program with three pure functions: `roofline(flops, bytes_moved, peak_flops, bandwidth)`, `ring_time(ranks, message_bytes, link_bytes_s)`, and `can_fit(capacity, allocations, request)`. Return intermediate values, not only verdicts. Add an allocator model whose free list can be fragmented, plus a scheduler model with two eight-GPU nodes and topology labels.

Use a fixed scenario: 30 TFLOP of work, 600 GB moved, 120 TFLOP/s compute, and 1.5 TB/s memory; eight ranks reducing 1 GiB over 25 GiB/s links; and a 40 GiB heap. Emit JSON records containing inputs, predicted bound, observed synthetic duration, and hypothesis.

## See it yourself

Predict each result. Arithmetic intensity is 50 operations per byte, so the bandwidth roof is 75 TFLOP/s and predicted kernel time is at least 0.4 seconds. Ring communication has a 70 ms serialization lower bound. Split 8 GiB free into eight 1 GiB holes and show that a 4 GiB request fails in a contiguous allocator. Assertions make each claim executable while documenting assumptions.

## Where it shows up

Replace synthetic duration with exported profiler data and replace topology constants with measured bandwidth. The artifact becomes an incident appendix: another engineer can rerun the assumptions, challenge a byte count, and compare the predicted bound with reality.

## When it breaks

Peak specifications are not sustained rates; caches change byte counts; collectives have startup and contention; real allocators may coalesce or use virtual memory. Label these as model errors rather than silently tuning constants. Reject negative sizes, zero bandwidth, impossible rank counts, and allocations from unknown owners.

## Practice

**Build:** implement all functions, twelve unit tests, and a command that emits deterministic JSON. **Break:** inject strided traffic, one slow collective rank, fragmented memory, a foreign allocation, and scattered one-GPU jobs that block an eight-GPU gang. **Explain back:** write a one-page report naming the bound, evidence, rejected alternatives, and next measurement. Completion requires all tests, reproducible output, and no optimization justified solely by peak utilization.

## Check yourself

1. Which simulator result is a lower bound rather than a prediction?
2. What real counter would falsify the assumed DRAM byte count?
3. Why preserve the failed allocation request size?

## Sources

### REQUIRED

- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)

### RECOMMENDED

- [Nsight Compute documentation](https://docs.nvidia.com/nsight-compute/)

### DEEP DIVE

- [NCCL tests](https://github.com/NVIDIA/nccl-tests)

## Next

Continue to [AI Infrastructure](../30-ai-infrastructure/README.md).
