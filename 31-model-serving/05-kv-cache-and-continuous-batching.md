# KV cache and continuous batching

LLM serving schedules tokens, not merely requests, while the KV cache preserves attention state whose size grows with every active sequence.

## Why it matters

Static batches waste decode slots when sequences finish at different times. Unaccounted cache growth causes late OOMs, head-of-line blocking, and unfairness.

## How it works

Prefill computes keys and values for the prompt; each decode step appends one position per layer. Approximate cache bytes are \(2LTHD b\): keys and values, layers \(L\), cached tokens \(T\), KV heads \(H\), head dimension \(D\), and bytes \(b\). Grouped-query attention changes \(H\).

Continuous batching removes finished sequences and admits new ones between decode iterations. Paged allocation maps logical cache blocks to noncontiguous physical blocks, reducing external fragmentation. Admission reserves a bounded future token budget. Scheduling can weight age, remaining budget, tenant share, and prefill cost.

## See it yourself

For 32 layers, 4 KV heads, dimension 128, FP16, cache costs \(2\times32\times4\times128\times2=65{,}536\) bytes per token. An 8,000-token sequence needs about 500 MiB. Forty such sequences need roughly 19.5 GiB before weights and workspace. This is a capacity estimate, not allocator overhead.

## Where it shows up

Serving dashboards expose prompt tokens, generated tokens, blocks allocated, prefix-cache hits, decode batch width, time to first token, inter-token latency, and evictions. Prefix reuse is keyed by model and exact token sequence, with tenant and privacy boundaries.

## When it breaks

One huge prefill stalls decode, optimistic reservations overcommit memory, cancelled requests leak blocks, and affinity creates hot replicas. Reconcile logical tokens to physical blocks and lifecycle events. Track free blocks, largest admission, cancellations, prefill queue, and per-tenant service.

## Practice

**Observe:** calculate cache size for three models. **Build:** simulate paged allocation and continuous batching. **Break:** cancel mid-generation and inject one long prompt. Completion requires zero leaked blocks, bounded decode delay, and a fairness explanation.

## Check yourself

1. Why does request concurrency poorly predict KV use?
2. What fragmentation does paging reduce?
3. Which metric distinguishes first-token from decode distress?

## Sources

### REQUIRED

- [vLLM PagedAttention paper](https://arxiv.org/abs/2309.06180)

### RECOMMENDED

- [vLLM scheduling documentation](https://docs.vllm.ai/en/latest/)

### DEEP DIVE

- [Orca serving system](https://www.usenix.org/conference/osdi22/presentation/yu)

## Next

Continue to [Quantization and quality control](06-quantization-and-quality-control.md).
