# 13 — Governed Self-Service AI Platform

Build a thin but complete platform slice in a separate repository: teams register an evaluated model or prompt application and request a governed deployment.

## Problem and users

Model teams face fragmented training metadata, evaluation, serving, policy, and operations. Risk reviewers receive incomplete evidence, while platform teams manually coordinate releases. The platform must shorten a validated idea-to-service journey without making weak quality, privacy, or cost decisions easier.

## Constraints and product contract

- Support one batch model and one LLM service profile, two tenants, and development/staging lifecycles.
- Integrate an artifact/registry source, evaluation runner, serving target, policy engine, and telemetry through replaceable adapters.
- Use declarative resources with status; every promotion cites immutable evidence and an accountable owner.
- Exclude foundation-model training, a universal feature store, opaque “responsible AI” scores, and automatic production approval.

## Architecture expectations

Define catalog/API, identity and tenancy, desired-state store, reconcilers, evaluation jobs, policy decisions, lineage graph, deployment adapter, endpoint status, usage ledger, and audit/event paths. Separate control-plane availability from serving availability. Specify evidence freshness, policy versioning, reproducibility, deletion propagation, adapter idempotency, condition semantics, and escape hatches.

## Milestone plan

1. Research model-team and reviewer journeys; define resources, policies, evidence, SLOs, and unit economics.
2. Reconcile registration and evaluation with lineage and clear terminal status.
3. Add policy-bound promotion, deployment, monitoring, rollback, tenancy, and usage attribution.
4. Pilot both profiles; test policy migration, adapter failures, lineage gaps, model recall, and platform upgrade.

## Required artifacts

- Product brief/research, platform and trust diagrams, API schemas, evidence model, policy catalog, and ADRs.
- Evaluation protocol and reports, lineage views, deployment contract, model/service cards, and audit samples.
- SLOs, dashboards, alerts, support/ownership model, runbooks, migration and disaster-recovery plans.
- Adoption, journey lead-time, policy rejection quality, reliability, and unit-cost scorecard.

## Tests and failure drills

Test schemas, reconciliation, tenancy, evidence freshness, policy versions, lineage, adapter contracts, deletion, and rollback. Inject evaluation timeout, conflicting results, missing lineage, corrupt artifact, stale approval, revoked data consent, serving-target outage, quota exhaustion, duplicate reconcile, and control-plane database loss. Prove serving remains safe when control plane is unavailable.

## Observability, security, and cost

Track journey lead time, reconcile age/result, evaluation queue, policy outcomes, deployment health, serving SLO, drift/quality signals, evidence age, and spend by team/model/environment. Apply least-privilege workload identity, purpose-bound data access, signed artifacts, tenant-scoped metadata, audited approvals, retention/deletion, and emergency recall. Report platform shared cost, evaluation compute, serving cost, telemetry, storage, support toil, and cost per active model or validated promotion.

## Explicit success rubric

| Platform claim | Evidence required |
|---|---|
| Self-service | Both pilot teams complete registration-to-staging through documented APIs without operator mutation. |
| Governance | Every endpoint maps to current policy, evaluation, lineage, owner, artifact, and rollback target. |
| Safety | Stale/missing evidence, tenant crossover, revoked data, and unsigned artifact drills are contained. |
| Control-plane design | Retries converge, status is actionable, and serving continues through control-plane outage. |
| Product outcome | Lead time and toil improve while quality, reliability, and cost remain within explicit guardrails. |

## Stretch work

Add policy simulation before rollout, federated metadata, evaluation-as-a-service for red teams, or multi-region control-plane recovery.

## Authoritative sources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [Model Cards for Model Reporting](https://doi.org/10.1145/3287560.3287596)
- [Google Cloud Architecture Framework: MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

## Mapped modules

[23 Control Planes](../../23-control-planes/README.md), [28 MLOps](../../28-mlops/README.md), [31 Model Serving](../../31-model-serving/README.md), [32 AI Platform Engineering](../../32-ai-platform-engineering/README.md), [20 Security](../../20-security/README.md), and [34 System Design](../../34-system-design/README.md).
