# Distributed training systems

Distributed training couples an optimization algorithm to process groups, communication, input state, and checkpoints; changing the system can change the mathematics.

## Why it matters

A job can scale throughput while silently changing effective batch, sample order, optimizer state, or convergence. Operational success is not merely keeping ranks alive.

## How it works

Data parallel workers compute local gradients and reduce them. Tensor parallelism partitions operators; pipeline parallelism partitions layers and schedules microbatches; sharded data parallelism partitions parameters, gradients, and optimizer state. The decomposition determines memory, communication frequency, and numerical order.

Global batch is local batch times data-parallel degree times accumulation steps. Learning-rate and schedule choices must follow the intended optimization, not cluster size. Deterministic resume captures model, optimizer, scheduler, random generators, scaler, sampler position, and parallelism metadata. Rendezvous establishes membership; elasticity is valid only when the algorithm handles changed world size.

## See it yourself

With local batch 8, 32 data ranks, and four accumulation steps, global batch is 1,024. Doubling data ranks without reducing another factor makes it 2,048. If the run retains a step-based schedule, it consumes twice as many samples per scheduled step. This proof identifies changed semantics even if loss initially looks plausible.

## Where it shows up

A launcher creates topology-aware groups, distributes immutable code and data manifests, records run identity, and streams rank progress. Training telemetry joins samples, tokens, loss, step time, collective time, and hardware errors.

## When it breaks

Collective mismatch deadlocks; one input shard creates a straggler; non-finite gradients propagate; resumed samplers duplicate data; changed world size invalidates shards. Align rank traces at the first divergence and compare group sequence, sample identity, optimizer step, and checkpoint manifest. Retry only classified transient faults.

## Practice

**Observe:** derive memory and communication for three decompositions. **Build:** specify a resumable 64-GPU run manifest. **Break:** change world size and omit sampler state. Completion requires detecting duplicated samples and proving whether optimization semantics remained constant.

## Check yourself

1. Which factors determine global batch?
2. Why is a model-only checkpoint insufficient?
3. When is elastic membership mathematically unsafe?

## Sources

### REQUIRED

- [PyTorch distributed overview](https://pytorch.org/tutorials/beginner/dist_overview.html)

### RECOMMENDED

- [PyTorch Fully Sharded Data Parallel](https://docs.pytorch.org/docs/stable/fsdp.html)

### DEEP DIVE

- [Megatron-LM](https://arxiv.org/abs/1909.08053)

## Next

Continue to [Capacity planning and queueing](06-capacity-planning-and-queueing.md).
