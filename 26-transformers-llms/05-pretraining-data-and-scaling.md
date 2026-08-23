# Pretraining data and scaling

Pretraining quality emerges from the interaction of corpus construction, token budget, model capacity, objective, and stable distributed optimization.

## Why it matters

[Transformer block internals](04-transformer-block-internals.md) defines the computation. Scale magnifies duplicate data, contamination, unsafe content, and training instability rather than making those problems disappear.

## How it works

A corpus pipeline discovers sources, applies licensing and policy rules, parses content, detects language, filters quality, removes sensitive data, deduplicates, mixes domains, tokenizes, and packs sequences. Each stage changes the learned distribution. Exact and near-duplicate removal reduce memorization and prevent repeated sources from dominating.

Causal language modeling minimizes token cross-entropy under teacher forcing. Perplexity is `exp(mean loss)` when tokenization and evaluation units match; it cannot be fairly compared across arbitrary tokenizers. Scaling laws describe empirical average trends among loss, parameters, data, and compute, not guarantees for downstream usefulness.

Large training shards data and model state across workers. Global batch, sequence length, optimizer state, precision, communication, and checkpoint cadence jointly determine the run. A loss curve without consumed-token and data-mixture context is incomplete.

## See it yourself

Suppose a four-token example has assigned probabilities `[0.5, 0.25, 0.5, 0.25]`. Mean negative log likelihood is about `1.04`, and perplexity is about `2.83`. Duplicate the easiest token many times and aggregate perplexity improves although hard behavior is unchanged.

This counterexample proves token-weighted averages can move through mixture changes. Report domains and slices alongside the aggregate.

## Where it shows up

A training run records immutable shard manifests and example-selection policies. Checkpoints include data cursor and RNG state so resume does not silently repeat or skip shards. Held-out benchmark documents are matched against training fingerprints before evaluation.

## When it breaks

Benchmark contamination creates false capability. Poor packing wastes compute or crosses boundaries incorrectly. Worker restart changes sample order. Repeated toxic sources dominate gradients. Loss falls while important domain loss rises.

Inspect per-domain loss, duplicate rates, token counts, sample hashes, gradient norms, and worker progress. Replay a small shard through the complete pipeline. Never diagnose corpus problems from global loss alone.

## Practice

**Observe:** calculate cross-entropy and perplexity by hand. **Build:** create a manifest-driven tokenizer and packer over tiny documents; completion includes provenance for every token span. **Break:** duplicate one document 100 times and show aggregate versus deduplicated metrics.

## Check yourself

1. Why can lower perplexity reflect a mixture change?
2. What state prevents repeated shards after resume?
3. Why are cross-tokenizer perplexity comparisons unsafe?
4. How does deduplication affect evaluation validity?

## Sources

### REQUIRED

- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)

### RECOMMENDED

- [Hugging Face causal language modeling](https://huggingface.co/docs/transformers/tasks/language_modeling)

### DEEP DIVE

- [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499)

## Next

Continue to [Post-training and alignment](06-post-training-and-alignment.md).
