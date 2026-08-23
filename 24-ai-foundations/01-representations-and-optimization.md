# Representations and optimization

Learning begins by turning observations into numbers and choosing parameters that reduce a measurable error. The mathematics is compact; the modeling choices hidden inside it are not.

## Why it matters

A model can only use distinctions encoded in its representation. Optimization then finds parameters that fit the stated objective, not the unstated intent. Understanding both explains why a training run can succeed numerically while failing the product.

## How it works

A feature vector \(x\) represents one example. A linear model computes \(z=w^Tx+b\); a nonlinear activation or deeper stack can transform that score. Training defines a loss \(L(w)\), computes derivatives, and updates parameters with gradient descent: \(w_{t+1}=w_t-\eta\nabla L(w_t)\). The learning rate \(\eta\) controls step size.

Gradients report local sensitivity. They do not prove a global optimum, causal structure, or useful generalization. Feature scaling changes the geometry of the loss surface and can make the same optimizer converge smoothly or oscillate.

Representation decides which examples the model considers similar. A one-hot category preserves identity but no notion of distance; a learned embedding places categories in a geometry shaped by the training objective. That geometry is useful only for distinctions rewarded by the data and loss. Optimization cannot recover information discarded during measurement, nor can it decide that an available feature is ethically inappropriate.

For a batch, the optimizer usually follows an average gradient rather than every example's exact gradient. Larger batches reduce sampling noise and use parallel hardware efficiently, but consume more memory and can require learning-rate changes. Momentum smooths updates by accumulating recent directions; adaptive optimizers rescale coordinates using gradient history. These methods change the path and speed of training, not the meaning of the objective.

## Vocabulary

- **feature:** measured input supplied to a model
- **parameter:** value learned during training
- **loss:** differentiable training error
- **gradient:** direction and rate of local change

## See it yourself

For points \((1,2)\) and \((2,4)\), start \(\hat y=wx\) at \(w=0\). The mean squared error is \((2^2+4^2)/2=10\), and \(dL/dw=-10\). With \(\eta=0.1\), the new weight is \(1\); predictions become 1 and 2, and loss falls to \(2.5\). One more update reaches \(w=1.5\).

Now multiply every input by 100 while preserving the same targets. At \(w=0\), the gradient is \(-1000\), so the old learning rate jumps to \(w=100\), producing enormous predictions and loss. This proves that gradient descent is sensitive to coordinate scale: the objective did not change conceptually, but its numerical geometry did.

## Where it shows up

In a recommender, user and item IDs become learned vectors. A dot product scores compatibility, and clicked or purchased examples shape the space. If the loss treats every unobserved item as a negative, it confuses “not shown” with “disliked.” Production quality therefore depends on exposure logging and negative sampling as much as optimizer choice. The same representation-objective split appears in simple regression and billion-parameter models.

## When it breaks

Missing signals cannot be recovered by optimization. Bad scaling can destabilize updates. A proxy loss can reward shortcuts, and a highly expressive model can memorize examples rather than learn reusable structure.

If loss becomes `NaN` or explodes, first inspect input, activation, gradient, and parameter ranges on the first failing step; non-finite values and a sudden norm jump distinguish numerical instability from ordinary overfitting. If training loss falls but validation behavior is poor, first compare train and validation distributions and slice errors. If both losses stay flat, verify one batch and its labels, then check that gradients are nonzero and parameters actually change.

## Practice

**Build:** implement scalar linear regression without an ML library. Log parameter, gradient, and loss each step; completion means the loss decreases and the fitted slope is within 0.05 of the known slope.

**Break:** add one extreme outlier, then multiply inputs by 100 without changing the learning rate. Capture the divergent trace and repair each failure separately using a robust loss or scaling and a justified step size.

**Explain back:** in two minutes, explain to a peer why “the optimizer learned it” is not evidence that the representation or objective was appropriate. Use the logged runs as evidence and name one decision optimization could not make.

## Check yourself

1. Why does lower training loss not guarantee better predictions?
2. What does a gradient say, and what does it not say?
3. How can representation choice introduce unfairness before training starts?

## Sources

### REQUIRED

- [PyTorch autograd tutorial](https://docs.pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html)

### RECOMMENDED

- [Stanford CS231n: optimization](https://cs231n.github.io/optimization-1/)

### DEEP DIVE

- [Deep Learning, chapter 8: optimization](https://www.deeplearningbook.org/contents/optimization.html)

## Next

Continue to [Probability and uncertainty](02-probability-and-uncertainty.md).
