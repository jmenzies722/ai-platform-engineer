# Classical models and baselines

Classical models make strong, inspectable baselines and often win on structured data where deep representation learning adds little.

## Why it matters

[Data and feature pipelines](04-data-and-feature-pipelines.md) produces defensible examples. Without a simple baseline, an expensive neural model has no credible reference for quality, latency, or operational complexity.

## How it works

Linear regression minimizes residual error; logistic regression models log odds as a weighted sum. Regularization penalizes complexity: \(L_2\) shrinks correlated weights smoothly, while \(L_1\) can produce zeros. Coefficients describe associations conditional on the supplied features, not causal effects.

Decision trees recursively partition feature space. Depth controls interactions and capacity. Random forests average decorrelated trees to reduce variance. Gradient boosting adds weak trees that fit current residual structure, often excelling on tabular data but overfitting noisy identifiers without constraints.

Nearest-neighbor methods store examples and make locality assumptions; support vector machines choose a margin and kernel-defined geometry. Every model embeds inductive bias. Baselines include majority, recency, and rules, not just simpler learned models.

## See it yourself

Consider XOR: labels are positive for `(0,1)` and `(1,0)`. No line separates positives from negatives, so raw logistic regression cannot fit it. Add interaction \(x_1x_2\) and suitable terms, or use a depth-two tree.

This four-row proof shows that failure can come from representation-model mismatch, not optimizer weakness. It does not establish that a deeper tree will generalize from noisy data.

## Where it shows up

A fraud team compares a rule, regularized logistic regression, boosted trees, and a neural network on the same time split. The logistic model offers calibrated, cheap serving; boosting captures nonlinear interactions. Selection includes recall at review capacity, p99 latency, explanation needs, and retraining burden.

## When it breaks

Unscaled features distort distance and regularization. High-cardinality IDs invite memorization. Deep trees fit noise. Class weights alter the fitted objective but do not automatically calibrate outputs.

Plot train and validation curves versus capacity. Verify the simple baseline first. For suspicious feature importance, retrain without the feature and inspect permutation behavior on held-out data; impurity importance alone is biased toward many-valued features.

## Practice

**Observe:** solve a tiny logistic prediction by hand. **Build:** compare constant, logistic, and tree baselines on one fixed split; completion includes quality, latency, and model size. **Break:** add a unique row ID and show a tree's train-test gap.

## Check yourself

1. Why can a linear model be the correct production choice?
2. What bias-variance change does bagging seek?
3. Why is a coefficient not a causal effect?
4. How does a high-cardinality identifier fool a tree?

## Sources

### REQUIRED

- [scikit-learn supervised learning guide](https://scikit-learn.org/stable/supervised_learning.html)

### RECOMMENDED

- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/)

### DEEP DIVE

- [Greedy Function Approximation: A Gradient Boosting Machine](https://doi.org/10.1214/aos/1013203451)

## Next

Continue to [Deep network training](06-deep-network-training.md).
