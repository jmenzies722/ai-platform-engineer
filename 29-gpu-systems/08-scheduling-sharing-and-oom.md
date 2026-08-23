# Scheduling, sharing, and OOM recovery

GPU capacity is a set of devices, memory regions, links, and failure domains whose safe sharing requires explicit placement and memory accounting.

## Why it matters

An allocated GPU may do no useful work, and free bytes may still be unusable. Scheduling and OOM diagnosis must distinguish admission, placement, fragmentation, leaks, transient peaks, and external consumers.

## How it works

Exclusive devices give the clearest isolation. Hardware partitioning can divide compute and memory; time slicing shares execution but not necessarily performance isolation. A scheduler matches model, memory, device capability, topology, health, and gang size. Utilization means active engines; allocation means ownership; useful utilization means progress attributable to intended work.

A memory ledger includes weights, optimizer state, gradients, activations, communication buffers, allocator reservations, runtime workspaces, graphs, and peer contexts. Allocators reserve segments and suballocate blocks, so reserved bytes can exceed live tensors. OOM occurs when a requested contiguous block cannot be satisfied, even when the sum of small free blocks appears large. Peak lifetime, not steady state, governs admission.

## See it yourself

On a 40 GiB device, weights use 10, live activations 12, gradients 10, workspace peaks at 6, and another process holds 3. The 41 GiB peak cannot fit. Freeing an unrelated 2 GiB cache makes it fit; lowering batch enough to remove 2 GiB also works. This ledger proves capacity shortage for that overlap, but heap snapshots are needed to distinguish fragmentation or a leak.

## Where it shows up

Training platforms reserve whole topology-aligned gangs. Serving platforms reserve future KV-cache bytes before admission. Both join process ownership, allocator statistics, device inventory, and workload phase to explain why nominally free resources cannot serve a request.

## When it breaks

Retries after OOM can synchronize a fleet into repeated failure. Stale processes retain contexts. Dynamic shapes create rare peaks. Fragmentation grows although live bytes are flat. Memory leaks show monotonically increasing live allocations. Capture the failing allocation size, free and reserved bytes, per-process ownership, allocator snapshot, phase, shape, and recent peak. Do not begin with blind cache clearing because it destroys evidence.

## Practice

**Observe:** produce a phase-by-phase memory ledger. **Build:** implement first-fit and best-fit allocation in a small simulator. **Break:** create equal total free space as one large block and many small blocks, then request a large allocation. Completion requires a runbook that separately treats capacity, fragmentation, leak, and foreign-process failures.

## Check yourself

1. Why are free bytes insufficient to predict allocation success?
2. How does hardware partitioning differ from time slicing?
3. Which time series distinguishes a leak from a transient peak?

## Sources

### REQUIRED

- [CUDA C++ Programming Guide: device memory](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

### RECOMMENDED

- [PyTorch CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html#cuda-memory-management)

### DEEP DIVE

- [NVIDIA Multi-Instance GPU User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)

## Next

Continue to [Practical lab: simulate a GPU performance investigation](09-practical-gpu-systems-lab.md).
