# Machine Learning

Machine learning builds behavior from patterns in examples instead of requiring a programmer to write every rule.

## Why it matters

**Prerequisite:** [Platform Engineering](./15-platform-engineering.md).

Some tasks, such as perception and prediction, resist complete sets of hand-written rules. Machine learning fits a function from examples instead, using an objective that turns error into a quantity an optimizer can reduce.

The learned model becomes an executable artifact, but its behavior depends on data and measurement rather than source code alone. Bias, drift, weak evaluation, and irreproducible training are therefore system failures, not just research concerns.

## How it works

Training searches parameter space to minimize an objective on sampled data; evaluation estimates whether the learned function generalizes to the operating distribution.

Examples flow through a parameterized model; loss measures error; backpropagation computes gradients; an optimizer updates parameters over batches; held-out evaluation selects checkpoints; serving applies frozen parameters to new inputs.

The objective is a proxy for desired behavior, and the dataset is a sample of reality. Leakage creates unrealistically strong evaluation; distribution shift invalidates assumptions. Reproducibility requires versioning code, data, configuration, and environment.

## Vocabulary

- **Feature:** An input variable or representation supplied to a model.
- **Label:** A target value used for supervised learning or evaluation.
- **Parameter:** A learned numeric value controlling model behavior.
- **Loss:** A function measuring error for optimization.
- **Gradient:** The direction and rate of loss change with respect to parameters.
- **Optimizer:** An algorithm that updates parameters using gradients or related signals.
- **Epoch:** One pass through a training dataset.
- **Checkpoint:** Saved model and training state that supports reuse or recovery.
- **Generalization:** Performance on relevant data not used to fit the model.
- **Overfitting:** Fitting training details that do not transfer to new data.
- **Leakage:** Improper information that makes training or evaluation misleading.
- **Drift:** Change over time in data, behavior, or relationships relevant to a model.

## See it yourself

```python
for x, y in batches:
    prediction = model(x)
    loss = criterion(prediction, y)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

Predict what changes if `optimizer.zero_grad()` is omitted. Gradients should accumulate across batches, producing different updates from the intended loop. This supports the causal role of forward computation, loss, backpropagation, and optimizer state. A falling training loss does not prove generalization, fairness, calibration, or production value.

## Where it shows up

A fraud model can score well offline because a feature accidentally includes information recorded after the transaction. At decision time that feature is absent or delayed, so production quality collapses. Versioned feature definitions, time-aware splits, and training-serving parity checks keep the evaluation boundary honest. The failure belongs to the whole data and serving system, not only the fitted parameters.

## When it breaks

Offline metrics can improve while production outcomes fall. Leakage, distribution shift, stale features, label bias, objective mismatch, or different serving transforms are likely mechanisms. First reproduce the exact artifact and slice results by time and cohort, then compare feature computation and distributions at training and serving boundaries.

## Practice

### Observe

Train a small classifier, compare train/validation metrics, intentionally leak a label-derived feature, and document the misleading result.

### Build

Design a reproducible training manifest containing data, code, environment, hyperparameters, seed, metrics, and artifact identity.

### Break

Shift input distribution, corrupt labels, create imbalance, and introduce NaNs. Add detection at the earliest boundary.

### Say it out loud

Explain why a model is more than its weights.

**Success:** Include data, objective, optimization, held-out evidence, artifact identity, and one training-serving failure.

## Check yourself

1. What does loss optimize?
2. Why is held-out evaluation necessary?
3. What is training-serving skew?

### Interview stretch

- Design reproducible training.
- Diagnose good offline and poor online metrics.
- Separate model, data, and infrastructure failures.

## Sources

### REQUIRED

- “A Few Useful Things to Know about Machine Learning” — Pedro Domingos. [University of Washington PDF](https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf). Connects algorithmic learning to practical failure modes.

### RECOMMENDED

- “Learning representations by back-propagating errors” — Rumelhart, Hinton, and Williams. [Nature](https://doi.org/10.1038/323533a0). Seminal account of backpropagation for neural networks.

### DEEP DIVE

- “Hidden Technical Debt in Machine Learning Systems” — Sculley et al. [Google Research](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/). Explains production ML’s systems complexity.

## Next

Continue with [./17-transformers-and-llms.md](./17-transformers-and-llms.md).
