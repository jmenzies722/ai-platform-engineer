# 26 — Transformers and LLMs

Transformers model sequences with attention and large-scale pretraining. This module explains the mechanism, the training objective, and the limits behind fluent generation.

## What you will learn

- Trace tokenization, embeddings, attention, and transformer blocks.
- Explain corpus construction, next-token training, post-training, and generation.
- Reason about context, alignment limits, inference capacity, hallucination, and evaluation.

## Lessons

1. [Tokens, embeddings, and attention](01-tokens-embeddings-and-attention.md)
2. [Pretraining and generation](02-pretraining-and-generation.md)
3. [Capabilities, limits, and evaluation](03-capabilities-limits-and-evaluation.md)
4. [Transformer block internals](04-transformer-block-internals.md)
5. [Pretraining data and scaling](05-pretraining-data-and-scaling.md)
6. [Post-training and alignment](06-post-training-and-alignment.md)
7. [Inference mechanics and efficiency](07-inference-mechanics-and-efficiency.md)
8. [Evaluating language models](08-evaluating-language-models.md)

## Practice

- [Transformer internals lab](lab-transformer-internals.md): implement causal attention and sampling, introduce a mask fault, and calculate cache growth.

## Ready to continue

You can trace transformer tensors, explain training and alignment objectives, calculate inference memory, debug masking and decoding, and build evaluation evidence that does not confuse plausible text with verified knowledge.

## Next

Begin [LLM Engineering](../27-llm-engineering/README.md).
