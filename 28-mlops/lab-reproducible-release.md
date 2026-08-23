# Reproducible release lab

This lab builds an auditable miniature path from dataset manifest to registry promotion, canary observation, rollback, and retirement.

## Goal

Produce immutable artifacts and prove that a changed input invalidates descendants while a failed gate cannot reach deployment.

## Before you start

- Related lesson: [Governance and lifecycle controls](08-governance-and-lifecycle-controls.md)
- Tools: Python 3.10 or newer, `sha256sum`, and a POSIX shell
- Environment and cost: local filesystem, zero external cost
- Privileges and data: no elevated rights and synthetic rows only
- Destructive action: one disposable `mlops-release-lab` directory

Predict which artifact identities change when feature code changes and what rollback can reuse.

## Establish a baseline

Create five synthetic CSV rows and compute `sha256sum`. Record row count, schema, and event-time range in a manifest. Recompute and expect the same digest. This proves byte identity, not semantic validity.

## Make it work

Implement stages for validate, feature transform, mock train, evaluate, and register. Hash each stage from upstream digest, source digest, parameters, and environment identity. Write outputs to temporary paths and rename only after checks pass.

Create a registry record with candidate digest, lineage, metric, slice gate, owner, and status. Promote only if validation and evaluation pass. Simulate canary by routing deterministic request IDs, record deployed digest, then roll back to the previous digest. Completion requires a script that reproduces all identities and a report linking every stage.

## Break it

Remove feature-source identity from its cache key, change the transform, and rerun. Expect stale feature reuse. Change no other key.

## Diagnose it

Start from the unexpectedly cached stage. Print all key components and compare them with the declared lineage. The absent source digest separates cache invalidation from nondeterministic training. Restore it and prove the feature plus all descendants receive new identities while raw validation is reused.

## Clean up

```bash
rm -rf mlops-release-lab
test ! -e mlops-release-lab
```

Silent success confirms all local artifacts are removed. No cloud resources are created.

## What to keep

Keep the initial prediction, manifests, key explanation, stale-cache trace, corrected lineage, rejected promotion, rollback evidence, and retirement checklist. Explain why production never rebuilds the candidate.

## Sources

- [SLSA specification](https://slsa.dev/spec/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
