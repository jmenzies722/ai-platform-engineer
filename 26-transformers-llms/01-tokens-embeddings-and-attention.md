# Tokens, embeddings, and attention

Transformers process token IDs as vectors and let each position gather information from other positions through attention.

## Why it matters

Token boundaries affect cost and behavior. Attention explains both long-range capability and the steep memory cost of long contexts.

## How it works

A tokenizer maps text to subword IDs. An embedding table maps IDs to vectors and position information distinguishes order. For matrices \(Q,K,V\), attention computes \(\text{softmax}(QK^T/\sqrt{d})V\). Multiple heads learn different projections; residual paths, normalization, and feed-forward layers form a transformer block. Causal masking prevents a decoder from reading future tokens.

Queries express what each position seeks, keys what each position offers, and values the content to mix. Dot products measure compatibility, scaling prevents their variance from making softmax nearly one-hot as dimension grows, and softmax makes each row a weighted average. Different query positions can therefore gather different context from the same sequence.

Attention itself is permutation-equivariant, so position encodings carry order. Residual connections preserve an information path around each transformation, while normalization controls scale. Standard self-attention materializes interactions between every pair of positions, giving quadratic score-memory growth with sequence length. Efficient variants trade exact global interaction for sparsity, kernels, or recurrence.

## See it yourself

Let one query be \(q=[1,0]\), with keys \(k_1=[1,0]\), \(k_2=[0,1]\) and values \(v_1=[10,0]\), \(v_2=[0,4]\). Ignoring scale, scores are \([1,0]\); softmax is approximately \([0.731,0.269]\), producing \([7.31,1.08]\). Swap the query to \([0,1]\) and the mixture reverses. This proves attention routes value content according to query-key compatibility; it does not copy keys themselves.

Also tokenize `unbelievable`, ` unbelievable`, and a misspelling with a real tokenizer. Record IDs and lengths. The expected differences explain why visually similar prompts can consume different context and follow different embedding paths.

## Where it shows up

In a decoder-only serving system, each new token attends to cached keys and values from prior tokens. Longer conversations therefore increase per-request cache memory and per-token attention work. Tokenization also drives billing and truncation: a multilingual request may use more tokens than an English request with similar characters, creating a production fairness and capacity concern.

## When it breaks

Rare text fragments poorly, sequence length raises memory use, and attention weights are not reliable causal explanations. For an unexpected context failure, first inspect actual token IDs, total length, truncation boundary, mask, and tensor shapes. For memory growth, measure allocated memory against sequence length and batch size. If attention output is wrong in an implementation, verify score rows and masks before interpreting learned behavior.

## Practice

**Build:** implement single-head attention for three two-dimensional tokens and compare every intermediate matrix with a library calculation.

**Break:** remove scaling, then apply the causal mask in the wrong direction. Capture saturated probabilities and forbidden future attention; repair both.

**Explain back:** draw all tensor shapes and explain to a peer why token count affects both semantics and memory. Completion means they can recompute one output row.

## Check yourself

1. Why divide attention scores by \(\sqrt d\)?
2. What does causal masking enforce?
3. Why are tokens not words?

## Sources

### REQUIRED

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

### RECOMMENDED

- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary)

### DEEP DIVE

- [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)

## Next

Continue to [Pretraining and generation](02-pretraining-and-generation.md).
