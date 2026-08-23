# 12 — Multi-Tenant Model Serving System

Implement this system in an independent repository using small open models or deterministic stand-ins. The focus is serving behavior under contention and failure.

## Problem and users

Application teams need predictable inference APIs across model versions; platform operators need utilization and safe rollout; model owners need quality evidence; finance and security need tenant attribution and boundaries. Direct access to model servers makes overload, rollout, and spend inconsistent.

## Constraints and SLO envelope

- Support streaming and non-streaming requests, two model classes, three tenants, and one GPU or simulated accelerator pool.
- Define latency SLOs by request class plus throughput, availability, and quality guardrails.
- Enforce bounded input/output, admission, deadlines, quotas, and cancellation.
- Exclude training, a general API marketplace, and claims of scale beyond measured tests.

## Architecture expectations

Specify edge authentication, validation, token estimation, admission, queueing, routing, dynamic batching, model workers, cache policy, registry metadata, rollout/fallback, usage ledger, and telemetry. Preserve tenant context without leaking prompts. Analyze queue discipline, head-of-line blocking, memory residency, cold start, streaming backpressure, retries, idempotency limits, and model/version compatibility.

## Milestone plan

1. Define API, workload distributions, SLOs, threat model, quality checks, and capacity hypotheses.
2. Establish one model path with admission, deadlines, cancellation, token accounting, and load tests.
3. Add batching, multi-model routing, quotas, tenant isolation, rollout, fallback, and cost attribution.
4. Tune from profiles; run saturation, worker/GPU loss, bad-model, dependency, and recovery drills.

## Required artifacts

- OpenAPI or protocol contract, sequence/state diagrams, queueing and memory model, and ADRs.
- Reproducible load generator, workload traces, latency-throughput curves, profiles, and quality report.
- Tenant dashboards, alerts, runbooks, rollout/rollback evidence, and usage reconciliation.
- Threat model, abuse tests, data retention policy, and cost-per-request/token analysis.

## Tests and failure drills

Test contracts, token bounds, scheduler fairness, batch correctness, cancellation, streaming, authorization, accounting, and rollout policy. Inject burst overload, long-request monopolization, GPU OOM, worker death, model-load failure, corrupt artifact, registry outage, slow client, cache poisoning attempt, tenant quota abuse, and quality regression. Verify fallback does not silently violate quality or data policy.

## Observability, security, and cost

Measure queue wait, time to first token, inter-token latency, end-to-end latency, tokens/second, batch size, cache hit, rejection reason, GPU memory/utilization, model-load time, quality gate, and usage by tenant/version. Use workload identity, encrypted transport, signed models, strict parser limits, prompt redaction, scoped caches, and audited admin routes. Calculate accelerator-seconds per token/request, idle residency, cache/storage/egress, and marginal versus allocated tenant cost.

## Explicit success rubric

| Outcome | Passing threshold |
|---|---|
| Predictability | Declared SLO is met at stated workload and admission rejects cleanly beyond capacity. |
| Fairness | One abusive or long-request tenant cannot violate another tenant's reserved service class. |
| Safety | Cross-tenant, malformed-input, artifact, and admin-route attacks fail with useful audit evidence. |
| Release | Quality and operational canaries detect a bad model and restore the prior version. |
| Economics | Measurements explain batching/caching tradeoffs and reconcile usage to infrastructure cost. |

## Stretch work

Add speculative decoding, prefix-cache isolation, disaggregated prefill/decode simulation, or topology-aware multi-GPU routing.

## Authoritative sources

- [vLLM paper](https://doi.org/10.1145/3600006.3613165)
- [Triton Inference Server documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/)
- [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [OWASP Machine Learning Security Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)

## Mapped modules

[26 Transformers and LLMs](../../26-transformers-llms/README.md), [27 LLM Engineering](../../27-llm-engineering/README.md), [29 GPU Systems](../../29-gpu-systems/README.md), [30 AI Infrastructure](../../30-ai-infrastructure/README.md), [31 Model Serving](../../31-model-serving/README.md), and [20 Security](../../20-security/README.md).
