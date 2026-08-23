# Deep network training

Training a deep network is an experiment with interacting data, initialization, normalization, optimizer, precision, and schedule state.

## Why it matters

[Classical models and baselines](05-classical-models-and-baselines.md) supplies a reference. A neural network should earn its complexity, and its training run must be diagnosable beyond final loss.

## How it works

Mini-batch training alternates forward computation, loss reduction, reverse-mode differentiation, and parameter update. Initialization keeps activation and gradient variance in useful ranges. Residual connections provide short gradient paths. Batch normalization uses batch statistics during training and running statistics during evaluation; layer normalization normalizes within each example.

Dropout randomly masks activations during training and is disabled at evaluation. Weight decay constrains parameter scale. Data augmentation encodes invariances, but an invalid augmentation trains the wrong task. Mixed precision accelerates supported hardware; accumulation and numerically sensitive operations often remain higher precision, and dynamic loss scaling avoids underflow.

A checkpoint sufficient for exact continuation includes model, optimizer moments, scheduler, scaler, random states, sampler position, data and code identities, and step counters.

## See it yourself

For \(y=w_2(w_1x)\), \(dL/dw_1\) contains \(w_2\). Stacking scalar multipliers of 0.5 makes a gradient shrink as \(0.5^L\); at 20 layers it is below one millionth. Multipliers of 2 grow as \(2^L\).

This tiny chain demonstrates vanishing and exploding products. Real networks have matrices, nonlinearities, residual paths, and correlated activations, so measure actual norms rather than extrapolating blindly.

## Where it shows up

An image classifier starts by overfitting 32 examples, then scales data and capacity. Run records include per-layer activation and gradient distributions, throughput, memory, validation slices, and data order. A baseline checkpoint is replayed before a costly sweep.

## When it breaks

Training mode during evaluation makes dropout stochastic and updates normalization state. Forgotten gradient clearing accumulates updates. Loss reduction changes with batch size. Mixed precision overflows silently if finite checks are absent.

Use a ladder: validate one example, overfit one batch, train a small subset, then full data. At the first failing rung inspect shapes, labels, loss units, gradients, parameter deltas, and mode flags. This localizes mechanism before hyperparameter search.

## Practice

**Observe:** hand-trace a two-layer forward and backward pass. **Build:** train a small network that overfits 32 examples; completion includes a resumable checkpoint. **Break:** leave evaluation in training mode and omit gradient clearing separately; record distinct signatures.

## Check yourself

1. Why can batch normalization change behavior at evaluation?
2. What does residual connectivity change about gradient paths?
3. Which state is needed for faithful resume?
4. Why is one-batch overfitting a useful gate?

## Sources

### REQUIRED

- [PyTorch recipe: saving and loading a general checkpoint](https://docs.pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)

### RECOMMENDED

- [Deep Learning, practical methodology](https://www.deeplearningbook.org/contents/guidelines.html)

### DEEP DIVE

- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

## Next

Continue to [Architectures and inductive bias](07-architectures-and-inductive-bias.md).
