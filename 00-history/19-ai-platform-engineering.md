# AI Platform Engineering

AI platform engineering turns model infrastructure and governance into safe, reusable capabilities for many teams.

## Why it matters

**Prerequisite:** [AI Infrastructure](./18-ai-infrastructure.md).

Hand-assembled notebooks, clusters, data jobs, registries, and endpoints make model delivery difficult to reproduce or govern. AI platforms turn recurring lifecycle decisions into maintained workflows and contracts.

Self-service does not remove judgment. Evaluation gaps, changing model behavior, accelerator economics, tenancy, and platform coupling still require explicit ownership, so the platform must expose evidence and evolve without trapping its users.

## How it works

An AI platform is a control plane for lineage and policy plus data planes for training and inference, connected by immutable artifacts and evaluation evidence.

Users submit versioned specifications; workflows resolve data/code/environment; schedulers allocate compute; artifacts and lineage are registered; evaluation gates promotion; serving controllers deploy; telemetry and feedback inform governance and retraining.

Model identity must include weights, architecture, tokenizer, runtime, prompt policy, and dependencies. Evaluation is a release primitive, not a dashboard afterthought. Multi-tenancy combines fairness, security, topology, quota, and economic policy.

## Vocabulary

- **MLOps:** Engineering practices and systems for repeatable model development and operation.
- **Lineage:** Traceable relationships among data, code, configuration, model, and deployment artifacts.
- **Model registry:** A managed catalog of model versions, metadata, and lifecycle state.
- **Evaluation gate:** A required quality or safety check before promotion.
- **Inference gateway:** A policy and routing boundary in front of model-serving backends.
- **Accelerator tenancy:** Rules for sharing and isolating accelerator resources among users.
- **Quota:** An enforced resource or usage limit.
- **Control plane:** APIs and controllers that manage desired platform state.
- **Data plane:** Runtime components that perform training or inference work.
- **Promotion:** Advancing a verified artifact into a later lifecycle stage or environment.

## See it yourself

```yaml
kind: ModelRelease
spec:
  artifactDigest: sha256:...
  tokenizerDigest: sha256:...
  evaluationSuite: safety-quality-v4
  servingProfile: gpu-latency
  rollout: { canaryPercent: 5 }
```

Predict which fields must stay identical to reproduce this release and what state an evaluator should add. The declaration should identify immutable artifacts and policy, while status records evaluation and rollout outcomes. This supports evidence-gated model promotion. It does not prove that the named evaluation is adequate, that serving is healthy, or that lineage is complete.

## Where it shows up

A self-service fine-tuning request should resolve immutable code, data, base model, tokenizer, environment, and evaluation policy before allocating expensive compute. The workflow records lineage, gates promotion on evidence, canaries the serving artifact, and attributes cost to the caller. This makes a model release reviewable and repeatable while preserving explicit ownership for data approval and model quality.

## When it breaks

A model release may be irreproducible even though a registry contains its weights. The tokenizer, prompt policy, data snapshot, runtime, evaluation, or serving configuration may be unversioned. First resolve the release identity and lineage from request through endpoint, then locate the first artifact or decision that lacks an immutable reference.

## Practice

### Observe

Map a model release with inputs, outputs, owners, evidence, failure states, rollback, and retention requirements.

### Build

Specify an AI platform API for training-to-serving promotion with lineage, policy, evaluation, SLOs, cost, and status conditions.

### Break

Change tokenizer without weights, exhaust quota, fail evaluation, and lose lineage. Ensure promotion fails safely and diagnostically.

### Say it out loud

Explain the contract for promoting a model into production.

**Success:** Include immutable identity, lineage, evaluation, policy, serving status, rollback, and clear ownership.

## Check yourself

1. Why separate control and data planes?
2. What must promotion evidence contain?
3. Why is evaluation a platform primitive?

### Interview stretch

- Design a multi-tenant AI platform.
- Allocate scarce GPUs fairly.
- Make a model release reproducible and reversible.

## Sources

### REQUIRED

- “Hidden Technical Debt in Machine Learning Systems” — Sculley et al., Google. [Google Research](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/). Defines the systems pressures an AI platform must absorb.

### RECOMMENDED

- “The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction” — Breck et al., Google. [Google Research](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/). Turns production-readiness concerns into concrete tests and release evidence.

### DEEP DIVE

- “vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention” — Kwon et al. [arXiv](https://arxiv.org/abs/2309.06180). Shows how serving internals shape platform capability.

## Next

Continue with [./20-agentic-engineering.md](./20-agentic-engineering.md).
