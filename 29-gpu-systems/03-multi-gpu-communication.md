# Multi-GPU communication

Multiple GPUs accelerate work only when computation outweighs communication and synchronization.

## Why it matters

Adding devices can reduce efficiency or increase completion time when topology and collective traffic are ignored.

## How it works

Data parallelism replicates parameters and all-reduces gradients. Tensor parallelism splits operations; pipeline parallelism splits layers and introduces bubbles. Collectives such as all-reduce, all-gather, and reduce-scatter have topology-dependent cost. Overlapping communication with computation hides only work that is truly independent.

Data parallelism increases aggregate batch unless local batch shrinks; that can change optimization. Tensor parallelism communicates within layers and benefits from fast links. Pipeline parallelism reduces per-device model memory but schedules microbatches to fill stages. Ring collectives use bandwidth efficiently for large messages, while latency matters for many small collectives. The slowest rank sets synchronized step time.

## See it yourself

With 90% parallel work, ideal speedup is \(1/(0.1+0.9/N)\): 1.82 on 2 devices, 4.71 on 8, and only 8.77 on 64. Efficiency at 64 is under 14% even before communication. Add a 20 ms all-reduce to a 100 ms single-device step and recompute. The ceiling proves scale needs decomposition and measurement, not device count.

## Where it shows up

For transformer training, tensor parallel groups are commonly kept within a node's fast fabric while data parallel traffic crosses nodes. Placement mistakes can send frequent layer collectives over slower links. Rank-level traces and topology-aware bandwidth tests connect an unexpectedly long step to the actual path.

## When it breaks

Slow links, stragglers, imbalanced partitions, small batches, and collective mismatches stall every participant. First align per-rank timelines around the blocked collective and inspect message sizes, rank arrival times, and topology. One late rank suggests upstream compute or input skew; all ranks spending long inside the collective suggests network or algorithm choice.

## Practice

**Build:** map data, tensor, and pipeline groups onto a two-node topology and calculate expected communication volume. **Break:** place a chatty group across slow links and delay one rank; capture both signatures. **Explain back:** use Amdahl's law and traces to explain why another GPU can reduce efficiency.

## Check yourself

1. What does all-reduce accomplish?
2. Why do pipeline bubbles occur?
3. When can communication overlap?

## Sources

### REQUIRED

- [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)

### RECOMMENDED

- [PyTorch distributed overview](https://pytorch.org/tutorials/beginner/dist_overview.html)

### DEEP DIVE

- [Megatron-LM](https://arxiv.org/abs/1909.08053)

## Next

Continue to [AI Infrastructure](../30-ai-infrastructure/README.md).
