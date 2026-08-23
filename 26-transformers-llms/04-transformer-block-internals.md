# Transformer block internals

A transformer block alternates communication across token positions with independent transformation at each position, while residual paths preserve a shared state stream.

## Why it matters

[Capabilities, limits, and evaluation](03-capabilities-limits-and-evaluation.md) describes behavior. Engineers diagnosing context, memory, or numerical failures need to trace the exact tensors producing it.

## How it works

For hidden states \(X\), learned projections produce \(Q=XW_Q\), \(K=XW_K\), and \(V=XW_V\). One attention head computes `softmax(QK^T / sqrt(d_k))V`. The scale prevents dot products from growing with dimension and saturating softmax. A causal mask excludes future keys before normalization. Multiple heads use separate projections, concatenate outputs, and project them back to model width.

The position-wise feed-forward network expands each token state, applies a nonlinearity, and contracts it. Residual addition lets each sublayer propose a state update. Layer normalization stabilizes scale; pre-norm and post-norm place it on different sides of the update and produce different gradient paths.

Position information may be added, learned, or applied as rotations to queries and keys. Without it, self-attention is permutation-equivariant and cannot distinguish reordered tokens from content alone.

## See it yourself

Use one query with scores `[0, log(3)]` and values `[2, 6]`. Softmax weights are `[0.25, 0.75]`, so output is `5`. Mask the second key; output becomes `2`. Change the masked score to one million and output remains `2` if masking occurs before softmax.

This proves a proper mask removes a path. It does not prove no information leaked earlier through preprocessing or labels.

## Where it shows up

In decoder inference, prompt tokens attend to earlier prompt tokens; each generated token attends to prompt plus prior generated states. Attention matrices grow quadratically during full-sequence training, while cached single-token decoding trades computation for persistent key-value memory.

## When it breaks

Mask polarity errors expose future tokens. Missing position information loses order. Residual or normalization mistakes destabilize depth. Shape-correct head transposes silently mix batch, head, and sequence axes.

Test a two-token fixture with hand-computed scores and assert masked probabilities are exactly zero within tolerance. Log shapes, row sums, finite values, and residual norms at every sublayer before scaling up.

## Practice

**Observe:** compute the two-value attention example. **Build:** implement one causal attention head with NumPy and compare every intermediate. **Break:** apply the mask after softmax and show future leakage.

## Check yourself

1. Why divide scores by the square root of head dimension?
2. What does the residual stream preserve?
3. Why is position information necessary?
4. Which fixture catches a causal-mask bug?

## Sources

### REQUIRED

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

### RECOMMENDED

- [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)

### DEEP DIVE

- [PyTorch multi-head attention reference](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

## Next

Continue to [Pretraining data and scaling](05-pretraining-data-and-scaling.md).
