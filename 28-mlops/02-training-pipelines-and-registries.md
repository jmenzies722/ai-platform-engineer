# Training pipelines and registries

A training pipeline makes dependencies and validation explicit; a registry records which evaluated artifact may enter each environment.

## Why it matters

Automating an invalid process only produces bad models faster.

## How it works

Pipeline stages validate inputs, transform data, train, evaluate, and publish immutable outputs. Caching keys include every relevant input. Promotion is a state transition backed by policy and evidence, not a copy to a vaguely named folder. A registry tracks artifact digest, lineage, evaluation, status, owner, and compatibility.

Each stage should be idempotent and publish output only after validation succeeds. Data and model contracts make schema assumptions executable. A cache key combines stage code, parameters, environment, and upstream digests; omitting one creates stale reuse. Promotion moves an already evaluated digest through an audited state machine, preserving the exact candidate tested.

## See it yourself

Draw `snapshot -> validate -> features -> train -> evaluate -> register`. Hash each node from its inputs. Change one feature definition: features and every descendant should get new keys, while snapshot and raw validation remain reusable. If training is reused, the cache key is incomplete. This exercise proves invalidation follows dependency edges, not file timestamps.

## Where it shows up

In scheduled retraining, a new snapshot triggers validation and training, but promotion waits for slice gates and an owner decision. The registry records a rejected candidate as evidence rather than deleting it. Deployment consumes the approved digest, so rebuilding in production cannot introduce an untested dependency.

## When it breaks

Partial cache keys reuse stale data, concurrent runs race, and registry labels move without audit. When a stage looks unexpectedly cached, first print its full cache-key components and upstream digests. When the wrong model serves, compare deployed digest, registry transition log, and evaluation digest before rerunning training.

## Practice

**Build:** define an idempotent DAG and promotion policy covering schema, slices, reproducibility, ownership, and rollback compatibility. **Break:** omit feature code from a cache key and run concurrent promotions; capture stale reuse and race evidence. **Explain back:** show why promotion references an immutable artifact rather than rebuilding it.

## Check yourself

1. What makes a pipeline stage cacheable?
2. Why promote metadata rather than rebuild?
3. What evidence should a registry retain?

## Sources

### REQUIRED

- [Kubeflow Pipelines concepts](https://www.kubeflow.org/docs/components/pipelines/concepts/)

### RECOMMENDED

- [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)

### DEEP DIVE

- [TFX paper](https://dl.acm.org/doi/10.1145/3097983.3098021)

## Next

Continue to [Release and monitoring](03-release-and-monitoring.md).
