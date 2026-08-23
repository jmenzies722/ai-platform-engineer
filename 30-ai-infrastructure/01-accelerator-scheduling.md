# Accelerator scheduling

Accelerator scheduling matches constrained workloads to heterogeneous, expensive resources while preserving fairness and useful utilization.

## Why it matters

A cluster can report high allocation while GPUs sit idle behind data loading, fragmented capacity, or unschedulable gangs.

## How it works

Requests declare accelerator type, count, memory, locality, and duration. Gang scheduling starts distributed workers together. Quotas and queues separate entitlement from instantaneous availability. Bin packing improves utilization but may fragment large shapes; preemption recovers capacity but requires checkpoint-aware workloads.

Scheduling is constrained matching over time. Device labels describe compatibility; topology constraints describe communication quality; priorities decide whose delay matters. Backfilling can run short jobs while preserving a reservation for a large gang. Fair-share accounting often considers historical consumption so one tenant cannot continuously occupy returned capacity.

## See it yourself

Place four 1-GPU jobs across both 8-GPU nodes, two per node, then request one 8-GPU gang. Twelve GPUs are free but no node has eight, so the gang cannot run. Packing the four small jobs on one node leaves the other available. The observation proves aggregate free capacity is insufficient; shape and placement determine schedulability.

## Where it shows up

In a training cluster, a queue admits an eight-GPU job only when all workers can be placed near one another. Device plugins advertise inventory, while the batch scheduler owns gang and quota semantics. Useful-utilization telemetry must join scheduler allocation with device activity; allocation alone can reward idle reservations.

## When it breaks

Topology is ignored, device health is stale, jobs over-request, and preemption destroys uncheckpointed progress. For a pending job, first inspect its exact scheduling predicates, events, free-device shapes, and reservations. For allocated but idle GPUs, correlate device activity with process, input, and collective state before changing queue policy.

## Practice

**Build:** simulate queues, quotas, gang placement, and backfill for research and production. **Break:** fragment nodes and preempt an uncheckpointed job; measure wait and lost work. **Explain back:** distinguish allocation, schedulability, fairness, and useful utilization using the event trace.

## Check yourself

1. Why use gang scheduling?
2. What is fragmentation?
3. Which metric reveals useful utilization?

## Sources

### REQUIRED

- [Kubernetes device plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)

### RECOMMENDED

- [Kubernetes scheduling](https://kubernetes.io/docs/concepts/scheduling-eviction/)

### DEEP DIVE

- [Volcano scheduler](https://volcano.sh/en/docs/)

## Next

Continue to [Storage and networking](02-storage-and-networking.md).
