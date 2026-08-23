# Neural networks and backpropagation

Neural networks compose parameterized transformations. Backpropagation makes their many parameters trainable by efficiently applying the chain rule.

## Why it matters

Without a mechanical understanding of forward and backward passes, exploding loss, dead activations, and silent gradient errors look like infrastructure problems.

## How it works

A layer computes \(h=\phi(Wx+b)\). Stacking layers creates representations useful to later layers. The forward pass records intermediate values; the backward pass propagates each output derivative through the computation graph. Automatic differentiation performs this bookkeeping, while an optimizer applies updates. Mini-batches trade noisy gradient estimates for efficient matrix operations.

For a composition \(L(f(g(x)))\), the chain rule multiplies local derivatives. Reverse mode starts with \(dL/dL=1\) and accumulates contributions when one value feeds multiple paths. Saved activations make this efficient but consume memory; checkpointing trades extra forward computation for fewer saved values. `zero_grad` matters because many frameworks accumulate gradients by default.

Nonlinearity lets stacked layers express more than one linear transformation. ReLU preserves positive gradients but can leave units inactive; sigmoid bounds outputs but saturates. Initialization controls the scale carried through many layers. Normalization and residual connections make deep signal propagation easier, but do not compensate for incorrect targets.

## Vocabulary

- **activation:** nonlinear layer output
- **backpropagation:** reverse-mode derivative computation
- **epoch:** one pass over training examples

## See it yourself

For \(y=(wx)^2\), choose \(w=2,x=3\). The forward values are \(u=wx=6\) and \(y=u^2=36\). Backward gives \(dy/du=12\), \(du/dw=3\), and \(dy/dw=36\). PyTorch should return `w.grad == 36`. Reuse \(w\) in \(y=(wx)^2+w\); the expected gradient becomes 37, demonstrating that reverse mode sums contributions from both graph paths.

## Where it shows up

In transformer training, the loss at every token sends gradients through output projection, residual streams, attention, and embeddings. Activation memory often limits batch size before parameters do. Mixed precision changes storage and arithmetic, while gradient scaling protects small values. The same graph mechanics therefore influence distributed strategy and hardware capacity.

## When it breaks

Poor initialization, saturated activations, numerical overflow, bad normalization, or detached tensors can block useful gradients. For flat loss, first prove that one tiny batch can overfit while logging per-layer activation and gradient norms. All-zero gradients near a detach identify a graph break; rapidly growing norms suggest instability; healthy gradients with unchanged parameters point to optimizer setup. Check inputs and labels before architectural changes.

## Practice

**Build:** train a two-layer network on XOR until all four predictions are correct. Print tensor shapes, activation ranges, gradient norms, and parameter deltas.

**Break:** detach the hidden activation, then separately use an excessive learning rate. Record the distinct signatures and repair each from evidence.

**Explain back:** trace one scalar path through forward and backward calculations and explain why automatic differentiation saves bookkeeping rather than choosing a good model.

## Check yourself

1. Why are nonlinear activations necessary?
2. What does reverse-mode differentiation reuse?
3. Why can a valid gradient still produce bad learning?

## Sources

### REQUIRED

- [PyTorch autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)

### RECOMMENDED

- [Deep Learning, chapter 6](https://www.deeplearningbook.org/contents/mlp.html)

### DEEP DIVE

- [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0)

## Next

Continue to [Generalization and debugging](03-generalization-and-debugging.md).
