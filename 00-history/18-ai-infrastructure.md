# AI Infrastructure

AI infrastructure supplies the compute, data movement, scheduling, and operations needed to train and serve models reliably.

## Why it matters

**Prerequisite:** [Transformers and LLMs](./17-transformers-and-llms.md).

Growing models and datasets exceeded the useful capacity of one general-purpose processor. GPUs, optimized kernels, collective communication, high-speed fabrics, and distributed training combined many devices into one workload.

That cluster behaves like a specialized supercomputer whose performance depends on topology and data movement. Scarce accelerators, fragmented capacity, poor utilization, and high cost make AI infrastructure a distinct part of the cloud stack.

## How it works

Useful throughput is the minimum rate allowed by compute, accelerator memory, interconnect, storage, software efficiency, and workload shape.

Frameworks launch kernels over tensors; device memory feeds compute units; collectives synchronize gradients or activations; checkpoints stream to storage; schedulers allocate topology-compatible devices; serving engines batch requests and manage KV cache.

Data parallelism replicates weights and synchronizes gradients; tensor/pipeline parallelism partitions work but adds communication and bubbles. High GPU utilization can still mean poor useful throughput if work is padding or stalled downstream.

## Vocabulary

- **GPU:** A processor optimized for high-throughput parallel operations.
- **HBM:** High-bandwidth memory located close to an accelerator.
- **Kernel:** A function executed in parallel on an accelerator; distinct from an OS kernel.
- **Collective:** A coordinated communication operation across multiple workers.
- **All-reduce:** A collective that combines values and returns the result to every participant.
- **Data parallelism:** Replicating a model while partitioning input data across workers.
- **Tensor parallelism:** Partitioning tensor operations across devices.
- **Topology:** The physical and logical arrangement of compute and communication links.
- **Occupancy:** The share of accelerator execution capacity available to active work.
- **Checkpoint:** Persisted model/training state used for recovery or continuation.
- **Quantization:** Representing values with lower precision or fewer bits.

## See it yourself

Use a capacity model to see why more accelerators do not guarantee a proportional speedup:

```python
single_device_compute_ms = 100
gradient_gib = 8
link_gib_per_second = 50

for devices in (1, 2, 4, 8):
    compute_ms = single_device_compute_ms / devices
    # Simplified ring all-reduce traffic per device.
    communication_ms = 0 if devices == 1 else (
        2 * (devices - 1) / devices * gradient_gib / link_gib_per_second * 1000
    )
    print(devices, round(compute_ms + communication_ms, 1))
```

Predict whether total time falls as the device count rises, then run the model. With the stated numbers, communication dominates and the estimate gets worse beyond one device. This supports the claim that scaling depends on data movement as well as arithmetic. It is not a hardware benchmark; overlap, topology, collective algorithms, and tensor sizes can change the result.

## Where it shows up

A distributed training job may run faster on four tightly connected GPUs than on eight split across a slower fabric boundary. Every synchronization step waits for collective communication and the slowest participant. Topology-aware placement, balanced input pipelines, and measured communication time can matter more than nominal device count. Scheduler policy therefore affects both completion time and cost.

## When it breaks

A multi-GPU job may show busy devices but make no training progress. One rank may have crashed, a collective may be waiting, input may be starved, memory may be fragmented, or topology may force slow transfers. First compare per-rank step timestamps, errors, memory, data wait, and collective duration; aggregate utilization hides stragglers.

## Practice

### Observe

Profile a matrix workload across batch sizes; record memory and throughput; identify the saturation and OOM boundaries.

### Build

Create a capacity model estimating memory, compute, network, and storage for a distributed training or serving workload.

### Break

Introduce one slow worker, undersized batches, and checkpoint contention. Detect each from correlated metrics.

### Say it out loud

Explain why eight accelerators can be slower than four.

**Success:** Use compute, communication, topology, synchronization, and one per-rank measurement to support the claim.

## Check yourself

1. What limits scaling efficiency?
2. Why does topology matter?
3. What can GPU utilization hide?

### Interview stretch

- Diagnose a hanging collective.
- Capacity-plan LLM serving.
- Compare training and inference bottlenecks.

## Sources

### REQUIRED

- “CUDA C++ Programming Guide” — NVIDIA. [Official documentation](https://docs.nvidia.com/cuda/cuda-c-programming-guide/). Canonical GPU execution and memory model.

### RECOMMENDED

- “PyTorch Distributed Overview” — PyTorch Foundation. [Official docs](https://pytorch.org/tutorials/beginner/dist_overview.html). Maps training patterns to distributed primitives.

### DEEP DIVE

- “Megatron-LM” — Shoeybi et al. [arXiv](https://arxiv.org/abs/1909.08053). Demonstrates large-model parallel training.

## Next

Continue with [./19-ai-platform-engineering.md](./19-ai-platform-engineering.md).
