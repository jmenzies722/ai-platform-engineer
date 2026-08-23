# Systematic ML debugging

ML debugging isolates whether failure comes from data, implementation, optimization, generalization, or the evaluation contract.

## Why it matters

[Architectures and inductive bias](07-architectures-and-inductive-bias.md) adds structural choices. Changing architecture before locating the failing boundary makes experiments slower and explanations weaker.

## How it works

Begin with invariants: schema, units, labels, split membership, tensor shapes, finite values, and deterministic fixture outputs. Establish simple references: a constant predictor, a rule, and a classical baseline. Then use the smallest reproducibility ladder: one example, one batch, small subset, full train, validation, shadow production.

The bias-variance pattern narrows hypotheses. High train and validation error suggests underfitting, weak features, bad optimization, or bad labels. Low train and high validation error suggests leakage, mismatch, or excess variance. Good offline and bad online behavior suggests skew, shift, feedback, or serving defects.

Ablations remove one component; perturbation tests change one known factor; metamorphic tests assert expected behavior under valid transformations. Seeded replay controls randomness but multiple seeds quantify sensitivity. Debugging ends with a regression test tied to the observed failure.

## See it yourself

Replace all labels with one constant. A model reaching perfect accuracy proves only that it can learn the constant. Now randomly permute labels. A high-capacity network may memorize training but validation remains chance.

These controls separate pipeline capacity from meaningful signal. If validation stays high under permuted labels, investigate leakage or duplicate examples before celebrating.

## Where it shows up

A ranking model loses online conversion. Engineers first verify deployed digest and feature parity, replay production requests, then compare candidate distributions and delayed labels. Only after serving and data contracts pass do they test retraining hypotheses.

## When it breaks

Non-deterministic kernels frustrate replay, logging omits sample identities, and dashboards average away a failed slice. Hyperparameter sweeps can accidentally select test noise. Logging raw private examples creates a second incident.

Capture privacy-safe IDs, digests, ranges, losses, and transitions. Change one variable per test. If a fix cannot be explained by evidence and protected by a regression test, treat it as an unconfirmed correlation.

## Practice

**Observe:** classify learning-curve patterns into candidate failure classes. **Build:** implement one-example and shuffled-label controls around a toy trainer. **Break:** introduce a train-serving normalization mismatch and locate it from paired feature traces.

**Say it out loud:** narrate the first failed rung and the single experiment that separates your top two hypotheses.

## Check yourself

1. What does shuffled-label validation reveal?
2. Why is “try a larger model” not a diagnosis?
3. Which evidence separates serving skew from overfitting?
4. When does deterministic replay remain insufficient?

## Sources

### REQUIRED

- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)

### RECOMMENDED

- [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)

### DEEP DIVE

- [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## Next

Continue to [Model debugging lab](lab-model-debugging.md).
