# Model debugging lab

This lab turns leakage, overfitting, and feature skew into distinct observable failures.

## Goal

Build a tiny binary classifier pipeline and an evidence ladder that identifies which boundary failed.

## Before you start

- Related lesson: [Systematic ML debugging](08-systematic-ml-debugging.md)
- Tools: Python 3.10 or newer; optionally scikit-learn
- Environment and cost: local CPU, zero external cost
- Privileges and data: no elevated rights and synthetic data only
- Destructive action: one disposable `ml-debug-lab` directory

Predict the train and validation behavior for valid labels, shuffled labels, and an identifier feature before running.

## Establish a baseline

Generate 400 seeded rows with two numeric features and label `x1 + x2 > 0`. Split the first 300 for training and last 100 for validation. Confirm row counts, class counts, no shared IDs, and a majority baseline near one half. These checks establish the fixture, not the learner.

## Make it work

Fit a standardized logistic regression with scaler state learned from training only. Record seed, split IDs, transform parameters, coefficients, confusion counts, and per-row predictions. Completion requires validation accuracy above 0.9 and byte-identical metrics on replay.

Add two controls: overfit four examples with a sufficiently expressive learner, and train on shuffled labels. The first must reach perfect train fit; the second must remain near chance on validation.

## Break it

At serving simulation time, replace training standardization with raw values multiplied by 100. Change nothing else. Expect shifted logits and degraded predictions despite the same model digest.

## Diagnose it

Start from differing predictions for the same row ID. Compare raw feature, transformed feature, transform version, logit, and threshold. Matching raw values with mismatched transformed values isolates feature skew from model drift. Restore the fitted scaler and prove exact prediction parity.

## Clean up

```bash
rm -rf ml-debug-lab
test ! -e ml-debug-lab
```

No output from `test` confirms cleanup.

## What to keep

Keep your prediction table, baseline, learning controls, paired skew trace, rejected hypothesis, correction, and regression assertion. Explain without notes why shuffled-label validation is a leakage alarm.

## Sources

- [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)
