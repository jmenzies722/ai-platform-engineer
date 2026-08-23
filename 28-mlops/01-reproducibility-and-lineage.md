# Reproducibility and lineage

Reproducibility means a model result can be traced to immutable code, data, configuration, environment, and randomness.

## Why it matters

A model binary without lineage cannot be audited, repaired, or confidently rolled back.

## How it works

Each run records source revision, dataset snapshot, feature definitions, parameters, dependencies, seeds, hardware, metrics, and artifact digest. Deterministic execution is not always available, so define acceptable numerical variance and preserve enough evidence to explain it.

Lineage is a directed graph: source artifacts and transformations lead to a candidate, evaluation, and release. Content-addressed identifiers prevent a familiar name from silently changing underneath a run. Reproducibility has levels: repeatability on the same machine, reproducibility in a reconstructed environment, and statistical reproducibility within a tolerance. Exact bits may be impossible across kernels, but missing inputs are avoidable.

## See it yourself

Train a tiny model twice with fixed seed and environment. Expect matching manifests and metrics within a declared tolerance. Then omit the seed and change thread count; record whether artifact hashes diverge even when accuracy rounds to the same value. This proves that similar headline metrics do not establish identical provenance.

## Where it shows up

During an incident, a prediction ID should resolve to model digest, feature version, training run, dataset snapshot, and evaluation. That path lets responders identify which users saw the candidate and reproduce its inputs. A registry alias such as “production” is useful routing state, but the immutable digest is the evidence.

## When it breaks

Mutable data paths, unpinned environments, hidden notebook state, and nondeterministic kernels sever lineage. For an unreproducible result, first diff run manifests and input digests, then locate the earliest divergent stage. Matching inputs with divergent outputs points toward randomness or hardware; differing snapshots point to lineage, not model math.

## Practice

**Build:** design a run manifest and reproduce one candidate within a stated tolerance. **Break:** mutate a dataset behind a stable path and show the digest catches it; then omit a dependency pin and capture divergence. **Explain back:** walk another engineer from prediction to immutable inputs. Completion means they can rerun it without asking you questions.

## Check yourself

1. Is a random seed sufficient?
2. Why hash artifacts?
3. What should remain immutable?

## Sources

### REQUIRED

- [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/)

### RECOMMENDED

- [PyTorch reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)

### DEEP DIVE

- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

## Next

Continue to [Training pipelines and registries](02-training-pipelines-and-registries.md).
