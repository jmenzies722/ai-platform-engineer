# Lab: Reproduce a Small Machine-Learning Experiment

Build a deterministic standard-library training pipeline, capture data and environment lineage, repeat it, and identify which changes invalidate a comparison.

## Prerequisites

- Python 3.10 or newer and Bash
- No GPU, package installation, or network access
- Basic understanding of train/test splits and mean squared error

## Safety

Use only generated non-personal data. The dataset has 1,000 rows, training is capped at 20 epochs, and outputs remain under `.work`. Do not claim that deterministic code proves scientific validity or production performance.

## Setup and baseline

```bash
mkdir -p .work
python3 - <<'PY' >.work/data.csv
import csv, random, sys
r=random.Random(42); w=csv.writer(sys.stdout); w.writerow(["id","x","y"])
for i in range(1000):
    x=r.uniform(-2,2); y=3*x+2+r.gauss(0,.1); w.writerow([i,x,y])
PY
python3 --version | tee .work/python-version.txt
sha256sum .work/data.csv | tee .work/data.sha256
```

Predict which artifacts must match for two metric values to be meaningfully comparable.

## Tasks

1. Write `.work/train.py` using only `csv`, `random`, `json`, `hashlib`, and `platform`.
2. Accept explicit seed, epoch count, and learning rate. Sort by immutable row ID, create a seeded 80/20 split, and ensure no ID appears in both sets.
3. Train `y = wx + b` with seeded shuffled stochastic gradient descent for exactly 20 epochs. Evaluate test mean squared error without updating parameters.
4. Write `.work/run.json` containing schema version, UTC timestamp, code hash, data hash, Python/platform details, parameters, seed, split-ID hashes, learned coefficients, and train/test metrics.
5. Run twice with the same inputs into separate directories. Compare all deterministic fields and explain any intentionally variable fields.
6. Add assertions for row count, columns, finite numeric values, unique IDs, split disjointness, and expected data hash.

## Evidence to keep

Keep immutable dataset hash, training-code hash, environment record, parameters, split hashes, metrics, model coefficients, validation results, and an exact rerun command. Record limitations such as synthetic data and single-platform testing.

## Failure injection

Run once with a different split seed while leaving the output filename unchanged in a copy of the workflow. Your comparison must reject the run because split hashes differ, even if test error is numerically close. Then alter one data row and prove the expected-hash check fails before training.

## Cleanup

```bash
rm -rf .work
```

## Rubric

- 2 points: validates and hashes data before training
- 3 points: reproduces deterministic split, order, coefficients, and metrics
- 2 points: captures code, parameters, environment, and lineage
- 2 points: rejects changed seed or data rather than comparing blindly
- 1 point: states limits on reproducibility and removes artifacts

## Sources

- [Python reproducibility notes for `random`](https://docs.python.org/3/library/random.html#notes-on-reproducibility)
- [ML experiment tracking, MLflow documentation](https://mlflow.org/docs/latest/ml/tracking/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
