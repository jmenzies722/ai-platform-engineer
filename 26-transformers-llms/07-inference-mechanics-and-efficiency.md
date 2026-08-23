# Inference mechanics and efficiency

LLM inference has two different phases: parallel prompt processing and sequential token generation, each with different bottlenecks.

## Why it matters

[Post-training and alignment](06-post-training-and-alignment.md) shapes behavior. Serving that behavior requires understanding latency, memory, batching, quantization, and output reproducibility.

## How it works

Prefill processes prompt tokens in parallel and creates key-value cache entries for each layer. Decode consumes the cache and emits one token per sequence per step. Time to first token is dominated by queueing and prefill; inter-token latency is dominated by repeated decode. Cache memory grows with layers, cached sequence, heads or KV heads, head dimension, bytes per value, and concurrent sequences.

Continuous batching admits and removes sequences between decode steps. Prefix caching reuses identical trusted prefixes. Quantization reduces weight or cache bytes but introduces approximation and hardware-specific kernels. Tensor parallelism splits operations across devices and pays communication; speculative decoding uses a smaller proposer plus target verification without changing the target distribution when implemented exactly.

Sampling reproducibility requires model, tokenizer, prompt bytes, decoding parameters, implementation, and often hardware details. A seed alone is insufficient across changed kernels.

## See it yourself

A cache storing keys and values for 32 layers, 32 heads, head dimension 128, 2,048 tokens, and two bytes per element needs `2 * 32 * 32 * 128 * 2048 * 2`, about 1 GiB per sequence. Grouped-query attention reduces KV heads and therefore cache size.

This arithmetic is a capacity lower bound for cache tensors, not total service memory.

## Where it shows up

A chat service separates prompt-token and generated-token histograms, queue delay, prefill time, decode time, cache occupancy, cancellation, and output finish reason. Admission control considers token budgets, not request count alone.

## When it breaks

Long prompts exhaust cache, one long generation delays a batch, tokenizer mismatch changes boundaries, and aggressive quantization harms rare slices. Prefix caches can cross tenant boundaries if identity and policy are absent from keys.

Replay a request with exact artifacts. For latency, decompose queue, prefill, and per-token decode before tuning. For quality changes, compare logits on fixed short fixtures layer by layer or checkpoint by checkpoint.

## Practice

**Observe:** calculate cache memory for two architectures. **Build:** simulate continuous batching with prompt and decode lengths; completion reports time to first token and completion time. **Break:** key a prefix cache only by text and demonstrate tenant-policy collision.

## Check yourself

1. Why are prefill and decode bottlenecks different?
2. Which dimension makes cache grow during conversation?
3. How does grouped-query attention reduce memory?
4. Why is a random seed not a complete replay identity?

## Sources

### REQUIRED

- [Orca: A Distributed Serving System for Transformer-Based Generative Models](https://www.usenix.org/conference/osdi22/presentation/yu)

### RECOMMENDED

- [Hugging Face KV cache strategies](https://huggingface.co/docs/transformers/kv_cache)

### DEEP DIVE

- [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)

## Next

Continue to [Evaluating language models](08-evaluating-language-models.md).
