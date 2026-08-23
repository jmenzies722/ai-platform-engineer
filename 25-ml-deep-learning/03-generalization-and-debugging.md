# Generalization and debugging

A useful model performs well beyond its training sample. Learning curves and controlled experiments turn that broad goal into observable diagnoses.

## Why it matters

Adding layers, data, or compute without identifying the limiting factor wastes resources and can deepen hidden failure modes.

## How it works

Underfitting produces high training and validation error. Classic overfitting produces low training error and a larger validation gap. Regularization, augmentation, early stopping, and more representative data can reduce that gap. Start debugging with a tiny batch the model should memorize, verify labels and losses, then increase complexity one variable at a time.

Bias and variance are diagnoses, not moral judgments about model size. More capacity can reduce training bias but increase sensitivity to sampling noise. More representative data often improves both coverage and estimation; duplicated data does not. Early stopping selects a point on the optimization path using validation evidence, so repeated tuning can itself overfit the validation set.

An ablation changes one mechanism while holding the evaluation fixed. Removing augmentation, a feature group, or a regularizer can establish whether it caused a measured difference, subject to run variance. Multiple seeds and confidence intervals matter when the claimed gain is similar to stochastic variation.

## See it yourself

Train the same network on 50 and 5,000 examples from two noisy classes. With 50 examples, expect training loss to approach zero while validation error remains noisy; with 5,000, expect a smaller gap. Randomize labels for the 50-example run. A sufficiently large model can still memorize training labels while validation stays near chance, directly disproving “low training loss means the pattern is real.”

## Where it shows up

For an image classifier, a training pipeline records learning curves and slice metrics by capture device. If one camera dominates training, aggregate validation can hide failure on another. Before buying more GPUs, an ablation of augmentation and a device-balanced split can reveal whether the bottleneck is capacity, data coverage, or preprocessing.

## When it breaks

Validation leakage disguises overfitting. Distribution shift invalidates curves. Aggregate metrics can improve while a critical slice regresses. The first move for an unexplained regression is to reproduce one known run and compare manifests, data counts, label distributions, and learning curves. If loss is non-finite, inspect the first bad batch; if only validation moved, inspect split and preprocessing parity before optimizer settings.

## Practice

**Build:** train a small model and save curves, seed, configuration, and slice metrics. Completion requires a second run within a stated tolerance.

**Break:** introduce one wrong label mapping and one train-only normalization. Diagnose each using a ladder where every step names the hypotheses distinguished.

**Explain back:** compare underfitting, overfitting, optimization failure, and distribution shift using curve shapes and the first evidence you would collect for each.

## Check yourself

1. What does a train-validation gap suggest?
2. Why test whether a model can memorize a tiny batch?
3. What can an ablation establish?

## Sources

### REQUIRED

- [PyTorch reproducibility notes](https://docs.pytorch.org/docs/stable/notes/randomness.html)

### RECOMMENDED

- [scikit-learn learning curves](https://scikit-learn.org/stable/modules/learning_curve.html)

### DEEP DIVE

- [Understanding deep learning requires rethinking generalization](https://arxiv.org/abs/1611.03530)

## Next

Continue to [Data and feature pipelines](04-data-and-feature-pipelines.md).
