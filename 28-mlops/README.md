# 28 — MLOps

MLOps makes data, training, evaluation, and release processes reproducible and observable across a model's lifetime.

## What you will learn

- Version data, code, configuration, and model artifacts.
- Enforce data contracts and test reproducible training pipelines with lineage.
- Package, register, deploy, monitor, govern, and safely retire models.

## Lessons

1. [Reproducibility and lineage](01-reproducibility-and-lineage.md)
2. [Training pipelines and registries](02-training-pipelines-and-registries.md)
3. [Release and monitoring](03-release-and-monitoring.md)
4. [Data versioning and contracts](04-data-versioning-and-contracts.md)
5. [Pipeline testing and reproducibility](05-pipeline-testing-and-reproducibility.md)
6. [Model packaging and deployment](06-model-packaging-and-deployment.md)
7. [Model monitoring and response](07-model-monitoring-and-response.md)
8. [Governance and lifecycle controls](08-governance-and-lifecycle-controls.md)

## Practice

1. Complete the [standalone ML reproducibility lab](../labs/15-ml-reproducibility/README.md). Keep immutable data and code hashes, environment and parameter records, split identities, validation output, deterministic comparisons, and the exact rerun command.
2. Complete the [reproducible release lab](lab-reproducible-release.md). Extend the candidate evidence into content-addressed lineage, expose a stale cache, gate promotion, canary by immutable digest, roll back model and preprocessing together, and retire the release.
3. Attempt the [bad rollout incident](../incidents/06-bad-rollout/README.md) before reading its solution. Use its version and business-invariant evidence to revise promotion criteria, canary slices, rollback triggers, and reconciliation of affected outcomes.
4. Build the [Reproducible ML Training and Promotion Pipeline project](../projects/10-reproducible-ml-pipeline/README.md). A portfolio claim requires a clean-checkout reproduction, a rejected flawed candidate, complete promotion lineage, and drill evidence for rollback and retirement.

## Ready to continue

You can reproduce and trace a candidate from immutable inputs, reject incomparable or flawed evidence, prevent stale caches and invalid promotion, deploy and roll back an evaluated digest with compatible preprocessing, distinguish drift from harm, and retire safely.

## Next

Begin [GPU Systems](../29-gpu-systems/README.md).
