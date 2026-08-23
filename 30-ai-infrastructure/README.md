# 30 — AI Infrastructure

AI infrastructure supplies scarce accelerators, fast data paths, reliable jobs, and observability for training and inference workloads.

## What you will learn

- Design accelerator clusters from failure domains, network, and storage.
- Schedule heterogeneous distributed workloads and reason about training decomposition.
- Plan fault tolerance, capacity, utilization, and workload economics.

## Lessons

1. [Accelerator scheduling](01-accelerator-scheduling.md)
2. [Storage and networking](02-storage-and-networking.md)
3. [Reliable distributed jobs](03-reliable-distributed-jobs.md)
4. [Cluster architecture and failure domains](04-cluster-architecture-and-failure-domains.md)
5. [Distributed training systems](05-distributed-training-systems.md)
6. [Capacity planning and queueing](06-capacity-planning-and-queueing.md)
7. [Infrastructure economics and efficiency](07-infrastructure-economics-and-efficiency.md)
8. [Control planes and operational observability](08-control-planes-and-operations.md)
9. [Practical lab: simulate an accelerator cluster](09-practical-ai-infrastructure-lab.md)

## Practice

1. Bring forward the measured limits and scheduler assumptions from [GPU Systems](../29-gpu-systems/README.md), including the module performance investigation, standalone scheduling simulation, and GPU OOM diagnosis. Label each input as measured, published, estimated, or synthetic.
2. Complete the [accelerator cluster simulator lab](09-practical-ai-infrastructure-lab.md). Preserve its workload and fleet definitions, deterministic event log, invariants, placement comparisons, contention evidence, checkpoint and recovery timelines, queue distributions, and cost calculation.
3. Attempt the [queue overload incident](../incidents/12-queue-overload/README.md) before reading its solution. Use arrival, service, retry, age, fairness, and downstream-limit evidence to revise admission, queue policy, capacity triggers, and recovery projections.
4. Build the [Distributed GPU Capacity Planner and Simulator project](../projects/11-distributed-gpu-planner/README.md). Compare at least three policies under baseline and adverse workloads, validate reduced cases analytically, quantify uncertainty, and make every recommendation reproducible from manifests and raw event logs.

## Ready to continue

You can connect measured accelerator limits, queueing, topology, data delivery, training decomposition, checkpoints, failure domains, and economics to useful work and job completion time, and defend a capacity decision under uncertainty and injected failure.

## Next

Begin [Model Serving](../31-model-serving/README.md).
