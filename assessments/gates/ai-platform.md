# AI Platform Gate

This gate tests an AI workload as a governed, multi-tenant lifecycle rather than a model demo. It covers [AI foundations](../../24-ai-foundations/README.md), [machine learning and deep learning](../../25-ml-deep-learning/README.md), [transformers and LLMs](../../26-transformers-llms/README.md), [LLM engineering](../../27-llm-engineering/README.md), [MLOps](../../28-mlops/README.md), [GPU systems](../../29-gpu-systems/README.md), [AI infrastructure](../../30-ai-infrastructure/README.md), [model serving](../../31-model-serving/README.md), [AI platform engineering](../../32-ai-platform-engineering/README.md), and [agentic infrastructure](../../33-agentic-infrastructure/README.md).

## Prerequisites

- Pass the [Platform Gate](platform.md).
- Complete [Reproduce an ML Experiment](../../labs/15-ml-reproducibility/README.md), [Simulate GPU Scheduling and OOM](../../labs/16-gpu-scheduling-oom/README.md), [Control Model-Serving Overload](../../labs/17-model-serving-overload/README.md), [Verify AI Platform Tenancy](../../labs/18-ai-platform-tenancy/README.md), and [Bound an Agent Runtime](../../labs/19-agent-runtime-safety/README.md).
- Provide prior project evidence from at least two distinct lifecycle areas: [reproducible ML pipeline](../../projects/10-reproducible-ml-pipeline/README.md), [GPU planner](../../projects/11-distributed-gpu-planner/README.md), [model serving](../../projects/12-model-serving-system/README.md), [AI platform](../../projects/13-ai-platform/README.md), or [agent runtime](../../projects/14-governed-agent-runtime/README.md).
- Use synthetic or approved public data, deterministic model stand-ins, fake tools, and local simulation. No model API, external side effect, unrestricted shell or browser, credential, or production prompt is allowed.

## Challenge

Build a thin local platform slice for two fictional tenants. It registers one immutable model or prompt-application candidate, records data, code, configuration and environment lineage, runs a decision-relevant evaluation, applies a versioned promotion policy, deploys to a bounded synthetic serving target, attributes usage, and supports rollback and recall.

The slice must include:

- input and output contracts, data validation, split or evaluation-set identity, baseline, slices, uncertainty, limitations, and quality threshold;
- immutable artifact identity, lineage, evaluation freshness, policy version, accountable owner, and compatibility metadata;
- tenant-scoped storage, retrieval, cache, routing, quota, telemetry, and usage keys;
- bounded admission, queueing, deadlines, cancellation, fairness, memory ledger, and overload response;
- a control-plane status model separated from serving availability;
- typed agent-tool proposals treated as untrusted, exact approval binding, idempotent effects, budgets, audit chain, and safe halt; and
- quality, latency, reliability, safety, and unit-cost measures.

The evaluator injects one lifecycle fault and one operational fault:

- changed data row or split seed, stale feature or evaluation cache, missing lineage, conflicting evaluation, corrupt or unsigned artifact, or stale approval;
- [inference latency regression](../../incidents/10-inference-latency/README.md), [GPU OOM](../../incidents/11-gpu-oom/README.md), tenant cache collision, quota abuse, duplicate reconcile, serving-target outage, indirect prompt injection, mismatched approval, crash after side effect, or budget exhaustion.

The candidate must fail closed where evidence or authority is insufficient, diagnose from raw lineage and operating evidence, restore a known-good state without cross-tenant effect, and update the architecture under a changed workload, quality, or cost assumption.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- synthetic data or evaluation-set hash, code and environment identity, parameters, split identities, baseline, slice metrics, uncertainty, error analysis, and exact reproduction transcript;
- artifact manifest, lineage graph, evaluation and policy versions, promotion decision, owner, deployment identity, rollback target, recall and retirement records;
- tenant policy and schema, a coverage matrix with positive and negative tests for each critical lifecycle surface, cache-key construction, accounting replay, quota evidence, and redaction proof;
- workload distribution, queue and memory model, offered/admitted/completed rates, tail-latency method, rejection and retry counts, fairness evidence, and cost per request, token, or successful task;
- agent tool schemas, policy decisions, approval binding, idempotency receipts, budget counters, tamper-evident audit verification, safe-halt state, and residual risk;
- incident timeline, hypotheses, contradictory or missing evidence, mitigation and rollback triggers, user and subsystem recovery; and
- architecture revision with sensitivity analysis for the evaluator's changed assumption.

## Dimension requirements

- **Explain:** Connect objective, data, optimization, evaluation, artifact, accelerator memory, queueing, serving, tenancy, control plane, and agent authority. Distinguish probability from verified fact, reproducibility from validity, simulation from hardware evidence, and model intent from tool permission.
- **Build:** Deliver a reproducible, policy-gated, tenant-safe local lifecycle with bounded serving and agent effects, tests, lineage, rollback, and accounting.
- **Debug:** Isolate the lifecycle and operational faults without comparing invalid runs, hiding overload with unbounded queues or retries, or treating plausible model output as evidence.
- **Operate:** Enforce admission, quotas, quality and policy gates, least privilege, approval and budget limits; recall or roll back safely; preserve serving safety through control-plane failure; prove tenant-scoped recovery.
- **Design:** Defend evaluation, lineage, training or serving capacity, tenant contracts, failure domains, safety controls, cost allocation, ownership, and evolution under changed demand or risk.

## Evaluator instructions

Use fixed seeds and record fixture hashes privately before the attempt. Keep incident solutions closed until the candidate records hypotheses and safe mitigation. Inject faults through local fixtures or fake adapters. Require one reproduction from a clean checkout or clean work directory, one live policy or workload change, and one replay after interruption.

Do not award model-quality credit for a fluent demo. Validate metric calculations against a small hand-checkable case. Do not treat deterministic output as proof of validity, a simulator as hardware benchmarking, drift as harm, or a successful tool call as authorized success.

Critical requirements:

- an endpoint or effect maps to current artifact, lineage, evaluation, policy, owner, tenant, and rollback identity;
- stale or missing evidence, cross-tenant access, unsigned artifact, mismatched approval, and budget exhaustion fail closed;
- load, queue, retries, tokens, tool calls, memory, and simulated events remain bounded;
- duplicate or interrupted work cannot double-count usage or repeat protected effects; and
- recovery restores both artifact and compatible preprocessing, policy, cache, and tenant context.

## Review prompts

1. What decision does the evaluation support, and which slice or uncertainty could reverse it?
2. Why does a reproducible run not prove valid data, useful quality, or production performance?
3. Which identities bind data, split, code, environment, artifact, evaluation, policy, deployment, and owner?
4. How do queue discipline, batching, memory residency, and request shape affect tail latency and fairness?
5. Which evidence distinguishes fragmentation, capacity shortage, queueing, and a quality regression?
6. Where must tenant identity appear, and how does a missing cache or accounting key fail?
7. Why is model output an untrusted proposal, and how are authority, approval, idempotency, and safe halt enforced?
8. How does the architecture change when demand, quality threshold, accelerator supply, or risk tolerance changes?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and at least 2 in each of these cross-cutting claims: evaluation validity, lineage, tenancy, overload control, and bounded agent authority. Averages across those claims are not used.

Rework uses fresh fixture identities and faults. Reproducibility gaps require a clean rerun with immutable references. Evaluation gaps require a new flawed candidate or slice. Tenancy gaps require adversarial duplicate-name and cache-key tests. Serving gaps require a different overload shape. Agent gaps require a new injection or interruption. Any real unauthorized effect or sensitive-data exposure is a Stop.

## Remediation

Return to the smallest failed mechanism: [decision-centered evaluation](../../24-ai-foundations/08-decision-centered-evaluation.md), [systematic ML debugging](../../25-ml-deep-learning/08-systematic-ml-debugging.md), [LLM evaluations](../../27-llm-engineering/07-llm-application-evaluations.md), [MLOps reproducibility](../../28-mlops/05-pipeline-testing-and-reproducibility.md), [GPU OOM recovery](../../29-gpu-systems/08-scheduling-sharing-and-oom.md), [serving overload](../../31-model-serving/07-routing-autoscaling-and-overload.md), [AI platform governance](../../32-ai-platform-engineering/07-evaluation-lineage-and-release-governance.md), or [agent effect reconciliation](../../33-agentic-infrastructure/06-durable-execution-and-reconciliation.md). Repeat the matching local lab before a fresh integrated variant.
