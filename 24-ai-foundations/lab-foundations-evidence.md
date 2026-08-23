# Foundations evidence lab

This lab makes optimization stability, uncertainty, and threshold costs visible in one dependency-light Python experiment.

## Goal

Produce a reproducible evidence bundle for a one-parameter classifier and test the claim that lower loss, calibrated probabilities, and useful decisions are distinct properties.

## Before you start

- Related lesson: [Decision-centered evaluation](08-decision-centered-evaluation.md)
- Tools: Python 3.10 or newer and the standard library
- Environment: local CPU; expected cost is zero
- Privileges: no network, elevated rights, or private data
- Destructive actions: one disposable `foundations-lab` directory

Stop if the input contains real user data. Before running anything, predict which learning rate will diverge and whether a 0.5 threshold minimizes a false-negative cost ten times larger than a false-positive cost.

## Establish a baseline

Run:

```bash
python3 - <<'PY'
import math
x = [-2, -1, 1, 2]
y = [0, 0, 1, 1]
w = 0.0
p = [1 / (1 + math.exp(-w * a)) for a in x]
print(len(x), sum(p) / len(p), sum(y))
PY
```

Expect `4 0.5 2`. This establishes deterministic inputs and a valid initial probability, not model quality.

## Make it work

Create a script that performs 40 full-batch logistic-loss updates for rates `0.1` and `1.0`. On each step record weight, loss, and gradient. Then emit each example's probability, calculate Brier score, and enumerate thresholds at every unique score. For each threshold calculate confusion counts and `10 * FN + FP`.

Use stable log-loss by clipping probabilities to `[1e-12, 1-1e-12]`. Completion requires a JSON or CSV record containing inputs, rates, every update, final probabilities, metric formulas, and the minimum-cost threshold. Rerunning must produce byte-identical output.

## Break it

Use rate `100.0` and remove probability clipping. Predict the first symptom. Depending on implementation, expect overflow, a logarithm domain error, or an apparently perfect zero loss caused by numerical saturation. Change no other variable.

## Diagnose it

Start from the non-finite or impossible loss. Inspect the first failing step's logit, probability, gradient, and weight. This separates an excessive update from bad labels. Restore stable loss and reduce the rate; prove correction by finite values and monotonically decreasing full-batch loss. Do not use clipping to claim the unsafe optimizer is repaired.

## Clean up

Remove only the disposable directory:

```bash
rm -rf foundations-lab
test ! -e foundations-lab
```

The silent `test` success proves the lab artifact is gone.

## What to keep

Keep the predicted failure, stable trace, failed hypothesis, corrected rate, threshold-cost table, and one paragraph explaining why optimization loss did not choose an operating threshold. Finish by deriving the first gradient without notes.

## Sources

- [Python math module](https://docs.python.org/3/library/math.html)
- [scikit-learn Brier score loss definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
