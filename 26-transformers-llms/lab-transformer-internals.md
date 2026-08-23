# Transformer internals lab

This lab makes token boundaries, causal attention, sampling, and cache growth observable without a model download.

## Goal

Implement a tiny attention and decoding simulator and prove that masking and cache accounting match hand calculations.

## Before you start

- Related lesson: [Transformer block internals](04-transformer-block-internals.md)
- Tools: Python 3.10 or newer; standard library is sufficient
- Environment and cost: local CPU, zero external cost
- Privileges and data: none; use supplied synthetic tokens
- Destructive action: one disposable `transformer-lab` directory

Predict the attention output for scores `[0, log(3)]` and how cache bytes change when sequence length doubles.

## Establish a baseline

Use tokens `["un", "help", "ful"]`, integer IDs `[0,1,2]`, and a printed round trip back to the same strings. Assert sequence length three. This establishes deterministic token identity, not linguistic correctness.

## Make it work

Implement numerically stable softmax by subtracting the maximum. Compute the lesson's two-value attention example and assert output `5` within `1e-9`. Add a causal mask and assert every future probability is zero. Implement temperature and top-k sampling over fixed logits with a seeded generator.

Add a cache calculator parameterized by layers, KV heads, head dimension, sequence length, bytes, and batch. Completion requires intermediate scores, probabilities summing to one, masked entries, sampled counts, and cache bytes in a reproducible report.

## Break it

Apply the causal mask after softmax without renormalizing. Expect row sums below one or future influence in the output. Change no other code.

## Diagnose it

Start from the failed row-sum or output assertion. Print pre-mask scores, mask, probabilities, and weighted values. This separates mask placement from shape transposition. Move exclusion before softmax, rerun the hand fixture, and prove exact zero future weight.

## Clean up

```bash
rm -rf transformer-lab
test ! -e transformer-lab
```

Silent success confirms cleanup.

## What to keep

Keep predictions, hand values, failing trace, corrected assertions, cache calculation, and one production implication for long-context admission control. Explain causal masking without notes.

## Sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)
- [Hugging Face generation documentation](https://huggingface.co/docs/transformers/main_classes/text_generation)
