# Optimization dynamics

Optimization is a controlled dynamical process: gradients, step size, noise, curvature, and numerical precision jointly determine whether training converges.

## Why it matters

[Calculus and gradient reasoning](05-calculus-and-gradient-reasoning.md) explains a single derivative. Real training takes millions of coupled, noisy updates, so “use Adam” is not a diagnosis when loss diverges or stalls.

## How it works

Stochastic gradient descent estimates the full-data gradient from a mini-batch. Its noise can help leave narrow regions but also makes loss fluctuate. Momentum maintains \(v_t=\beta v_{t-1}+g_t\) and updates against \(v_t\), averaging directions across steps. Adam also tracks squared gradients to rescale coordinates; its epsilon, bias correction, and weight-decay implementation are part of the algorithm.

For \(L(w)=aw^2/2\), gradient descent gives \(w_{t+1}=(1-\eta a)w_t\). It converges only when \(|1-\eta a|<1\), equivalently \(0<\eta<2/a\). Different curvature across coordinates means one safe global learning rate can be slow in flat directions. Scaling, normalization, preconditioning, and adaptive methods alter this geometry.

Schedules use larger early steps and smaller late steps; warmup prevents unstable early updates when activation and optimizer statistics are immature. Gradient clipping bounds an update signal but can hide a persistently broken model. Regularization changes the objective; early stopping changes how far optimization follows it.

## See it yourself

Set \(L(w)=5w^2/2\), \(w_0=1\). Predict five updates for \(\eta=0.1\): each multiplies \(w\) by 0.5. For \(\eta=0.4\), each multiplies it by -1, so loss never decreases. For \(\eta=0.5\), magnitude grows by 1.5.

This is a complete proof for the quadratic, not for arbitrary neural networks. It establishes why a finite gradient and correct code can still diverge under an unsafe step size.

## Where it shows up

A large training job often scales batch size and learning rate together. If the global batch changes after a worker failure but the scheduler still assumes the old number of optimizer steps, the effective training trajectory changes. Logs must therefore include samples, tokens, optimizer steps, batch composition, and schedule state.

## When it breaks

Loss spikes can come from a toxic batch, precision overflow, scheduler discontinuity, or excessive rate. Plateaus can mean weak signal, dead activations, or a rate too small. Compare the first bad step with its predecessor: batch IDs, loss scale, gradient norm before and after clipping, update-to-weight ratio, and optimizer state.

Replay the exact batch from a checkpoint. If failure follows the batch, inspect data and per-example loss. If it follows optimizer state, inspect schedule and moments. If it disappears in higher precision, isolate the overflowing operation.

## Practice

**Observe:** plot scalar quadratic trajectories on both sides of the stability limit. **Build:** implement SGD and momentum without a library; completion means both match a hand-calculated three-step trace. **Break:** inject one outlier batch and separately jump the learning rate; diagnose each from logs.

## Check yourself

1. Why does curvature constrain learning rate?
2. Which state must be restored to resume Adam faithfully?
3. When does clipping conceal rather than solve a problem?
4. Why is optimizer-step count different from example count?

## Sources

### REQUIRED

- [Deep Learning, chapter 8: Optimization](https://www.deeplearningbook.org/contents/optimization.html)

### RECOMMENDED

- [PyTorch optimizer documentation](https://docs.pytorch.org/docs/stable/optim.html)

### DEEP DIVE

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)

## Next

Continue to [Statistical estimation and uncertainty](07-statistical-estimation.md).
