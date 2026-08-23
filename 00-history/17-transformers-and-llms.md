# Transformers and LLMs

Transformers learn relationships among tokens at scale, enabling models that predict and generate language.

## Why it matters

**Prerequisite:** [Machine Learning](./16-machine-learning.md).

Recurrent sequence models processed tokens serially and struggled to preserve useful information across long distances. Attention let each position compute relationships with other positions and made training far more parallel.

Transformers scaled into general language interfaces, not truth engines. Their useful behavior comes with large compute and memory demands, context limits, unstable factuality, and safety risks that serving and evaluation systems must manage.

## How it works

An LLM repeatedly maps token context to a probability distribution for the next token; generation samples or selects, appends, and repeats.

Tokens become vectors; attention scores relate queries to keys and combine values; stacked blocks transform representations; a final projection yields token logits. Training processes sequences in parallel; autoregressive inference is sequential and caches prior keys/values.

Attention training cost grows roughly quadratically with sequence length in standard form. KV cache grows with concurrent tokens and layers. Temperature reshapes probabilities but does not add knowledge. Alignment changes behavior, not factual guarantees.

## Vocabulary

- **Token:** A discrete unit used to encode model input and output text.
- **Embedding:** A learned numeric vector representation.
- **Attention:** A mechanism that mixes representations using learned relevance weights.
- **Query:** The vector used to score which other positions are relevant.
- **Key:** The vector compared with a query to produce attention scores.
- **Value:** The vector mixed according to attention weights.
- **Logit:** An unnormalized score before conversion to probabilities.
- **Prefill:** Processing prompt tokens to initialize inference state.
- **Decode:** Generating subsequent tokens, usually one step at a time.
- **KV cache:** Stored attention keys and values reused during autoregressive decoding.
- **Context window:** The bounded token sequence available to the model for one computation.
- **Temperature:** A parameter that rescales logits before sampling.

## See it yourself

```python
while len(tokens) < limit:
    logits, kv_cache = model(tokens[-1:], kv_cache=kv_cache)
    next_token = sample(logits / temperature)
    tokens.append(next_token)
```

Predict how many model calls produce five new tokens and how the cache changes. The loop requires five sequential decode steps and retains prior attention state between them. This supports autoregressive generation and the purpose of a KV cache. It omits prefill cost, batching, stopping rules, numerical kernels, and any guarantee that generated text is true.

## Where it shows up

Increasing an LLM context window can reduce serving concurrency even when weights and hardware do not change. Prefill performs attention work over the prompt, and each active sequence retains a KV cache across layers. Longer prompts therefore consume more compute and memory, leaving fewer requests in a batch. Token counts and cache allocation are operational inputs, not merely application text.

## When it breaks

An LLM service may slow sharply as prompts grow or return confident unsupported claims. Cache exhaustion, context truncation, tokenizer mismatch, retrieval failure, decoding changes, or model behavior can overlap. First freeze model, tokenizer, prompt, and decoding settings, then inspect tokenized context, retrieved evidence, finish reason, cache memory, and evaluation slice.

## Practice

### Observe

Tokenize several inputs, compare token counts, vary temperature and context, and measure first-token versus per-token latency.

### Build

Implement a miniature single-head attention calculation and verify tensor shapes and probability normalization.

### Break

Overflow context, mismatch tokenizer, exhaust KV cache, and inject conflicting instructions. Add explicit handling and evaluation.

### Say it out loud

Explain one generated token and its serving cost.

**Success:** Cover tokenization, attention state, logits, decoding, KV cache, and why none of these mechanisms guarantees truth.

## Check yourself

1. Why is training more parallel than generation?
2. What does KV cache trade?
3. Why does temperature not ensure truth?

### Interview stretch

- Explain prefill versus decode.
- Diagnose falling throughput at long context.
- Design evaluation for a model upgrade.

## Sources

### REQUIRED

- “Attention Is All You Need” — Vaswani et al. [arXiv](https://arxiv.org/abs/1706.03762). Introduces the Transformer architecture.

### RECOMMENDED

- “Language Models are Few-Shot Learners” — Brown et al. [arXiv](https://arxiv.org/abs/2005.14165). Documents scale-driven in-context behavior.

### DEEP DIVE

- “FlashAttention” — Dao et al. [arXiv](https://arxiv.org/abs/2205.14135). Shows how I/O-aware algorithms change attention performance.

## Next

Continue with [./18-ai-infrastructure.md](./18-ai-infrastructure.md).
