# Data and feature pipelines

Models learn from the examples a pipeline actually produces, so data boundaries and feature semantics are part of the model.

## Why it matters

[Generalization and debugging](03-generalization-and-debugging.md) shows how held-out behavior fails. Many apparent model failures begin earlier: labels arrive late, train and serving transformations differ, or a feature leaks future information.

## How it works

Define the prediction timestamp, available inputs, label event, label-maturation window, and example unit before extracting rows. A point-in-time join permits only feature values known at prediction time. Split by the deployment boundary, often time, user, account, or geography, before fitting transforms. A random row split leaks identity when one entity contributes many rows.

Numeric features need explicit missing-value and scaling policies. Categories can use one-hot, hashing, target encoding, or learned embeddings; target statistics must be fitted inside each training fold. Text and image transforms likewise have fitted state. Store transform code and learned state with the model so online inference applies the same contract.

Features encode assumptions. Ratios can expose scale-free structure; logarithms compress heavy tails; interaction terms let linear models express conditional effects. More features also increase leakage, instability, privacy exposure, and serving cost.

## Vocabulary

- **point-in-time correct:** uses only information available at the prediction timestamp
- **feature skew:** mismatch between training and serving feature computation
- **label maturation:** delay before an outcome can be considered complete
- **imputation:** explicit replacement of missing values

## See it yourself

For a loan decision at noon, let `days_late` be recomputed nightly and let default be known 90 days later. Joining today's final `days_late` value onto historical rows leaks outcomes backward. Reconstruct the value as of each decision timestamp.

Train a mean imputer on values `[1, 3]`; it stores 2. If validation values `[100, missing]` are included before the split, the stored mean becomes 34.67. The validation set changed training state, which is leakage even though labels were untouched.

## Where it shows up

A churn pipeline builds one row per account per scoring date. Offline and online jobs share a versioned transform definition. Freshness, null rate, range, and source timestamp travel with each feature vector so a prediction can be diagnosed later.

## When it breaks

Future joins create implausibly strong validation. New categories crash one-hot encoders. Training uses batch-complete values while serving sees partial values. Duplicate entities cross folds.

Start with ten examples and trace raw source timestamps through transformed tensors. Compare offline and online feature vectors by entity and feature version. If quality collapses only in production, inspect skew and freshness before retraining.

## Practice

**Observe:** mark every field available at a prediction timestamp. **Build:** create a point-in-time join and fit transforms on training only; completion requires a test with a late-arriving record. **Break:** fit an imputer before splitting and show the changed validation estimate.

## Check yourself

1. Why is a random row split unsafe for repeated users?
2. Which state must accompany a fitted transform?
3. How can an unlabeled feature leak the future?
4. What evidence distinguishes skew from concept drift?

## Sources

### REQUIRED

- [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

### RECOMMENDED

- [TensorFlow Transform](https://www.tensorflow.org/tfx/transform/get_started)

### DEEP DIVE

- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

## Next

Continue to [Classical models and baselines](05-classical-models-and-baselines.md).
