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

1. Complete the module [GPU performance investigation](09-practical-gpu-systems-lab.md). Produce a roofline argument, memory ledger, topology map, profiler interpretation, numerical check, and evidence-based bottleneck claim before proposing an optimization.
2. Complete the [standalone GPU scheduling and OOM lab](../labs/16-gpu-scheduling-oom/README.md). Preserve deterministic fixtures, policy outputs, invariants, queue-wait distributions, memory and OOM timelines, bounded retry behavior, and the boundary between simulated and hardware evidence.
3. Attempt the [GPU out-of-memory incident](../incidents/11-gpu-oom/README.md) before reading its solution. Distinguish capacity exhaustion, fragmentation, leak, and hardware fault; then state measured admission limits and prove that recovery neither loses nor duplicates work.
4. Feed the roofline, topology, memory, scheduling, and incident evidence into the workload and resource models for the [Distributed GPU Capacity Planner and Simulator project](../projects/11-distributed-gpu-planner/README.md). Document every fidelity limit instead of presenting simulation output as a device measurement.

## Ready to continue

You can derive execution and memory limits, validate them with profiles and numerical tests, choose safe precision, map collectives to topology, distinguish fragmentation from a real capacity shortfall, and translate hardware evidence into explicit scheduler assumptions.

## Next

Begin [AI Infrastructure](../30-ai-infrastructure/README.md).
