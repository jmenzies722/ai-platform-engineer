# 29 — GPU Systems

GPUs trade flexible control flow for massive parallel throughput. This module develops the hardware and performance model needed to use them efficiently.

## What you will learn

- Explain GPU architecture, SIMT execution, and the complete memory hierarchy.
- Design kernels and use profiler evidence, rooflines, and numerical tests.
- Reason about precision, collectives, topology, scheduling, and out-of-memory failures.

## Lessons

1. [GPU execution and memory](01-gpu-execution-and-memory.md)
2. [Kernels, precision, and performance](02-kernels-precision-and-performance.md)
3. [Multi-GPU communication](03-multi-gpu-communication.md)
4. [GPU architecture and instruction execution](04-architecture-and-instruction-execution.md)
5. [Memory systems and data movement](05-memory-systems-and-data-movement.md)
6. [Profiling and kernel engineering](06-profiling-and-kernel-engineering.md)
7. [Topology, collectives, and scaling](07-topology-collectives-and-scaling.md)
8. [Scheduling, sharing, and OOM recovery](08-scheduling-sharing-and-oom.md)
9. [Practical lab: simulate a GPU performance investigation](09-practical-gpu-systems-lab.md)

## Practice

Complete the simulator lab. Produce a roofline argument, a memory ledger, a topology map, and an evidence-based OOM diagnosis before proposing an optimization.

## Ready to continue

You can derive execution and memory limits, validate them with profiles, choose safe precision, map collectives to topology, and distinguish fragmentation from a real capacity shortfall.

## Next

Begin [AI Infrastructure](../30-ai-infrastructure/README.md).
