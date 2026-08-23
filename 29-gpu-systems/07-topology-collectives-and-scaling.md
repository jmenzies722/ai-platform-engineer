# Topology, collectives, and scaling

A collective is a communication algorithm embedded in a physical topology; its name alone does not determine cost.

## Why it matters

Tensor, pipeline, and data parallel groups communicate at different frequencies and volumes. A placement that crosses a slow or oversubscribed link can erase the compute saved by adding GPUs.

## How it works

All-reduce combines and returns values; reduce-scatter returns partitions; all-gather assembles partitions; all-to-all exchanges distinct partitions. A ring all-reduce moves approximately \(2(N-1)M/N\) bytes per rank for message size \(M\), favoring bandwidth. Trees reduce latency rounds for smaller messages. Implementations choose channels, routes, and protocols from topology.

NVLink, PCIe switches, CPU sockets, network interfaces, top-of-rack switches, and zones form nested failure and bandwidth domains. Keep frequent tensor-parallel traffic on the fastest fabric, then map lower-frequency data-parallel traffic outward. Overlap is valid only when communication has independent compute and does not contend for the same engines or memory bandwidth.

## See it yourself

For eight ranks and a 1 GiB gradient, the ring volume per rank is \(2(7/8)\), or 1.75 GiB. At an ideal 25 GiB/s link this alone needs at least 70 ms, before startup, contention, and slow ranks. If backward computation after the first ready bucket lasts 100 ms, at most 100 ms can hide communication. This is a lower bound, not a performance promise.

## Where it shows up

Large-model training forms topology-aware process groups and buckets gradients so reduction begins during backward execution. Mixture-of-experts all-to-all is sensitive to token imbalance as well as links. Rank traces must include group identity, message size, arrival time, chosen algorithm, and physical path.

## When it breaks

One rank arriving late makes peers appear stuck inside the collective. Mismatched collective order deadlocks. Tiny buckets pay startup repeatedly; huge buckets remove overlap. Link degradation and cross-NUMA placement reduce bandwidth. Compare rank arrival skew, collective sequence numbers, message sizes, topology inventory, link counters, and isolated bandwidth tests before blaming the collective library.

## Practice

**Observe:** draw an eight-GPU, two-node topology with measured edge bandwidth. **Build:** estimate ring lower bounds and place tensor and data groups. **Break:** move one chatty edge across nodes and delay one rank. Completion requires distinguishing transport saturation from an upstream straggler using synchronized traces.

## Check yourself

1. Why can reduce-scatter plus all-gather replace all-reduce?
2. Which group should receive the fastest links?
3. What observation disproves the claim that peers are network-bound?

## Sources

### REQUIRED

- [NCCL collective operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html)

### RECOMMENDED

- [PyTorch distributed overview](https://pytorch.org/tutorials/beginner/dist_overview.html)

### DEEP DIVE

- [Efficient large-scale language model training on GPU clusters](https://arxiv.org/abs/2104.04473)

## Next

Continue to [Scheduling, sharing, and OOM recovery](08-scheduling-sharing-and-oom.md).
