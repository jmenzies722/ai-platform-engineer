# Pretraining and generation

Language models learn a conditional distribution over the next token, then generate by repeatedly sampling from that distribution.

## Why it matters

The objective explains why models can compress broad patterns yet produce confident falsehoods: likely continuation is not truth verification.

## How it works

Pretraining minimizes cross-entropy between predicted and observed next tokens across large corpora. Inference converts logits to probabilities. Greedy decoding selects the maximum; temperature rescales logits; top-k and top-p restrict candidates. The key-value cache avoids recomputing prior attention states. Instruction tuning and preference optimization alter behavior but do not replace the base objective with a factual database.

Teacher forcing supplies the real preceding tokens during training; generation conditions on the model's own sampled history. One low-probability choice can therefore move later prediction into a different region. Cross-entropy rewards probability assigned to the observed token, even when several continuations are reasonable. Dataset mixture and filtering determine which regularities are available to learn.

During decoding, temperature below one sharpens relative logit differences and temperature above one flattens them. Top-p keeps the smallest candidate set whose cumulative probability reaches \(p\), so its size adapts to uncertainty. Greedy output is repeatable but not necessarily globally best. KV caching saves repeated projection of prior positions at the cost of memory that grows with layers, sequence, and concurrency.

## See it yourself

For logits \([2,1,0]\), ordinary softmax is approximately \([0.665,0.245,0.090]\). At temperature 0.5, divide logits by 0.5 to get probabilities near \([0.867,0.117,0.016]\). At temperature 2, probabilities flatten to about \([0.506,0.307,0.186]\). The ranking is unchanged, but sampling diversity rises. This proves temperature transforms an existing distribution; it cannot add evidence or correct a false premise encoded in the logits.

## Where it shows up

In structured extraction, a team may use low temperature and schema-constrained decoding because variation is undesirable. A writing assistant can tolerate broader sampling. Both still need model-version and decoding metadata in traces: a behavior change may come from sampling configuration rather than weights. In high-concurrency chat, KV-cache pressure determines admission capacity.

## When it breaks

Sampling can amplify weak probabilities, repetitive loops can emerge, and long prompts consume cache memory and dilute relevant context. For a changed output, first replay the exact prompt with model revision, seed where supported, and decoding parameters fixed. For repetition, inspect token probabilities and stop conditions. For latency or out-of-memory events, record prompt and generated token counts plus cache utilization before changing model code.

## Practice

**Build:** write a small sampler for fixed logits supporting greedy, temperature, top-k, and top-p. Over 10,000 draws, observed frequencies should approximate the transformed probabilities.

**Break:** use high temperature for an enum extraction and omit length limits. Record invalid or runaway outputs, then add schema and budget controls.

**Explain back:** contrast training-time teacher forcing with generation and explain why “set temperature to zero” cannot make unsupported answers factual.

## Check yourself

1. What exactly does next-token loss reward?
2. Why does a KV cache speed decoding?
3. Can temperature correct false knowledge?

## Sources

### REQUIRED

- [Hugging Face text generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

### RECOMMENDED

- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)

### DEEP DIVE

- [Training language models to follow instructions](https://arxiv.org/abs/2203.02155)

## Next

Continue to [Capabilities, limits, and evaluation](03-capabilities-limits-and-evaluation.md).
