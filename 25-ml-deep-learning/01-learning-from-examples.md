# Learning from examples

Supervised learning estimates a function from labeled examples. The central engineering question is whether patterns learned from one sample remain useful on unseen cases.

## Why it matters

Simple baselines often outperform complicated systems once latency, interpretability, and maintenance are counted. They also expose data problems before complexity hides them.

## How it works

Regression predicts quantities; classification predicts categories or probabilities. Training minimizes empirical loss, while regularization discourages brittle solutions. Features, labels, the hypothesis class, and the loss together define what can be learned. A linear or tree baseline establishes a measurable floor before neural-network work begins.

Empirical risk is an average over observed examples; expected risk concerns the unknown population. The gap depends on sample coverage, model capacity, and selection decisions. Regularization changes the optimization preference among solutions: an L2 penalty favors smaller weights, while tree depth limits conditional partitions. Neither repairs a label that measures the wrong outcome.

A baseline is also a diagnostic control. A constant predictor tests whether class imbalance explains apparent accuracy. A linear model tests whether simple additive structure is enough. Only a verified gap between baseline and requirement justifies added capacity and operational cost.

## See it yourself

Use 200 points with \(y=1\) when \(x_1+x_2>0\), then flip 10% of labels. A majority predictor should score near 50%, logistic regression near the attainable boundary, and an unrestricted tree can approach 100% training accuracy while held-out accuracy falls. Plot depth 1 through 20. The widening gap proves that fitting label noise is not reusable learning.

## Where it shows up

In churn prediction, the label “cancelled within 30 days” depends on an observation cutoff. Features computed after that cutoff leak the outcome. A simple baseline with timestamp-safe features establishes whether a more complex model creates enough lift to justify intervention cost. Production scoring must reproduce the same cutoff semantics, not merely the same column names.

## When it breaks

Labels may be noisy or reflect past decisions. Correlated examples inflate test results. Excess capacity memorizes; insufficient capacity misses structure. When validation underperforms, first plot training and validation loss against both epoch and training-set size. A persistent high pair suggests underfitting or broken features; a growing gap suggests variance or leakage. Before changing models, inspect misclassified rows and label provenance.

## Practice

**Build:** for one task, document the example unit, label provenance, constant and linear baselines, loss, split, and error costs. Produce a reproducible metric table.

**Break:** leak one post-outcome feature and permit duplicate entities across splits. Capture the implausible gain, then remove each defect and show the correction.

**Explain back:** justify to a reviewer why the chosen baseline is informative and which evidence would warrant a neural network. Completion means they can state the model's bounded claim and principal leakage risk.

## Check yourself

1. Why start with a baseline?
2. How does regularization differ from more data?
3. What makes a split representative?

## Sources

### REQUIRED

- [scikit-learn supervised learning](https://scikit-learn.org/stable/supervised_learning.html)

### RECOMMENDED

- [PyTorch basics: build the neural network](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)

### DEEP DIVE

- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/)

## Next

Continue to [Neural networks and backpropagation](02-neural-networks-and-backpropagation.md).
