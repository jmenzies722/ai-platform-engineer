# 10 — Reproducible ML Training and Promotion Pipeline

Build one useful model lifecycle end to end in a separate repository. The portfolio claim is reproducibility and governed release, not benchmark novelty.

## Problem and users

Data scientists need fast experiments; reviewers need comparable evaluation; operators need deployable artifacts with lineage; affected users need known limitations and rollback. Ad hoc notebooks cannot reliably answer which data, code, configuration, environment, and approval produced a model.

## Constraints and model contract

- Choose a bounded public or synthetic dataset with documented license and a decision-relevant task.
- Version immutable raw data references, transformations, splits, code, configuration, environment, metrics, and artifacts.
- Train on CPU or a small accelerator budget; make a deterministic baseline before optimization.
- Exclude sensitive personal data, unreviewed online learning, and promotion based on one aggregate metric.

## Architecture expectations

Define ingestion/validation, feature transformation, training, evaluation, artifact store, metadata/lineage, registry, promotion, batch or online serving handoff, monitoring, and retirement. Prevent train/serve skew and leakage. State reproducibility limits, random seed policy, schema contracts, comparison protocol, and how a released model maps to immutable evidence.

## Milestone plan

1. Write model card draft, data contract, baseline, evaluation slices, and acceptance policy.
2. Make ingestion through training reproducible with lineage and hermetic environment capture.
3. Add registry, policy-based promotion, deployment contract, monitoring, and rollback.
4. Test drift/schema faults, reproduce an old candidate, challenge evaluation, and retire a version.

## Required artifacts

- Dataset datasheet, model card, experiment protocol, lineage graph, and artifact manifest.
- Reproduction transcript from clean checkout; evaluation report with slices, uncertainty, and error analysis.
- Registry/promotion policy, deployment contract, monitor design, rollback and retirement runbooks.
- Compute, storage, carbon-proxy or energy, and human-review cost report.

## Tests and failure drills

Test schemas, transformations, split integrity, leakage guards, deterministic components, metric calculations, lineage completeness, and promotion rules. Inject corrupt input, schema evolution, missing artifact, stale feature logic, failed training worker, metric regression in one slice, registry outage, drift alert, and bad model release. Verify rollback restores both model and compatible preprocessing.

## Observability, security, and cost

Track pipeline duration/status, data freshness/quality, resource use, model/evaluation identifiers, promotion decisions, serving quality proxies, drift, and feedback delay. Authenticate artifact access, scan serialized models, record licenses, protect provenance, minimize data, and audit approvals/deletions. Report cost per experiment and promoted model, cache savings, retention growth, and the quality gained per compute unit.

## Explicit success rubric

| Claim | Required proof |
|---|---|
| Reproducibility | A reviewer rebuilds a selected candidate within declared numeric tolerance from immutable references. |
| Evaluation | Metrics, slices, uncertainty, leakage checks, and limitations support the stated use and reject a flawed candidate. |
| Governance | Every promoted artifact has lineage, approval, compatibility, and retirement metadata. |
| Operations | Drift and bad-release drills trigger actionable evidence and restore a known-good model. |
| Efficiency | Baseline-to-final quality improvement is justified against measured compute and storage cost. |

## Stretch work

Add distributed training only if profiling justifies it, automated data-deletion propagation, or champion/challenger shadow evaluation.

## Authoritative sources

- [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
- [Model Cards for Model Reporting](https://doi.org/10.1145/3287560.3287596)
- [Datasheets for Datasets](https://doi.org/10.1145/3458723)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Mapped modules

[24 AI Foundations](../../24-ai-foundations/README.md), [25 Machine Learning and Deep Learning](../../25-ml-deep-learning/README.md), [28 MLOps](../../28-mlops/README.md), [18 Observability](../../18-observability/README.md), and [20 Security](../../20-security/README.md).
