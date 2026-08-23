# Calculus and gradient reasoning

Derivatives describe local sensitivity. Training uses them to choose a direction, while engineering uses them to explain which inputs and parameters can change an output.

## Why it matters

[Linear algebra for models](04-linear-algebra-for-models.md) established transformations; calculus explains how their outputs respond to small changes. A computed gradient can be numerically wrong, saturated, or irrelevant to the product objective.

## How it works

For scalar \(f(x)\), the derivative is the limit \(\lim_{h\to0}(f(x+h)-f(x))/h\). For many inputs, the gradient collects partial derivatives. The chain rule composes local sensitivities: if \(z=f(y)\) and \(y=g(x)\), then \(dz/dx=(dz/dy)(dy/dx)\). A Jacobian handles vector outputs; a Hessian records how gradients themselves change.

The first-order approximation \(f(x+\Delta)\approx f(x)+\nabla f(x)^T\Delta\) explains gradient descent. Among equal-length small steps, the negative gradient produces the steepest local decrease under Euclidean geometry. “Local” matters: curvature can invalidate a large step, saddle points have zero gradient without being minima, and nondifferentiable points require a chosen subgradient.

Finite differences approximate a derivative but subtract nearly equal floating-point numbers when \(h\) is too small. Central difference, \((f(x+h)-f(x-h))/(2h)\), usually has lower truncation error. Gradient checking compares this independent approximation with automatic differentiation on a tiny deterministic problem.

## Vocabulary

- **Jacobian:** matrix of all first derivatives of a vector function
- **Hessian:** matrix of second derivatives of a scalar function
- **saddle point:** stationary point with rising and falling directions
- **gradient check:** comparison of analytic or automatic gradients with finite differences

## See it yourself

For \(L(w)=(wx-y)^2\), derive \(dL/dw=2x(wx-y)\). At \(w=1,x=2,y=5\), the gradient is \(-12\). With \(h=10^{-4}\), central difference gives approximately \(-12\).

Now try \(h=10^{-20}\) in ordinary double precision. The numerical derivative may become zero because \(w+h\) rounds to \(w\). This tiny counterexample proves that disagreement with a finite difference is evidence to investigate, not automatic proof that autodiff is wrong.

## Where it shows up

In a binary classifier, a saturated sigmoid can make upstream gradients tiny even though predictions are wrong. A stable implementation combines sigmoid and cross-entropy algebraically, avoiding extreme intermediate probabilities. Gradient and activation histograms reveal this mechanism earlier than final accuracy.

## When it breaks

Exploding gradients follow products of large local derivatives; vanishing gradients follow products below one. In-place mutation can invalidate saved values. A custom operation can return a backward formula with the right shape but wrong value.

First overfit one fixed mini-batch. Compare loss, parameter deltas, activation ranges, and per-layer gradient norms. If a custom operation is implicated, run a double-precision central-difference check away from kinks. If gradients are finite but loss rises, test a smaller step before blaming differentiation.

## Practice

**Observe:** derive and numerically check a scalar quadratic. **Build:** implement central-difference checking for a two-parameter linear model; completion requires relative error below \(10^{-5}\). **Break:** introduce a wrong factor in one derivative, then use an excessively small \(h\); record how the two faults differ.

## Check yourself

1. Why is the negative gradient only a local recommendation?
2. How can a zero gradient occur away from a minimum?
3. What evidence isolates a backward-formula bug?
4. Why can making the finite-difference step smaller make the estimate worse?

## Sources

### REQUIRED

- [PyTorch numerical accuracy notes](https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html)

### RECOMMENDED

- [CS231n gradient checks](https://cs231n.github.io/neural-networks-3/#gradcheck)

### DEEP DIVE

- [Automatic Differentiation in Machine Learning: a Survey](https://jmlr.org/papers/v18/17-468.html)

## Next

Continue to [Optimization dynamics](06-optimization-dynamics.md).
