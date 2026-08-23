# AI Platform Engineer Track

## Outcome role

An engineer who provides governed, observable, multi-tenant capabilities for data, training, evaluation, model release, inference, and bounded agents. The role joins platform product practice with model lifecycle, accelerator, serving, reliability, security, lineage, and cost engineering.

## Prerequisites

- Software, systems, Linux, networking, database, and distributed-systems competency.
- Cloud delivery, containers, Kubernetes, observability, SRE, security, and platform gates.
- Quantitative comfort with probability, optimization, measurement, and uncertainty.
- Evidence of operating both a service and a shared platform capability.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [17 Distributed Systems](../17-distributed-systems/README.md), [18 Observability](../18-observability/README.md), and [19 SRE](../19-sre/README.md) | Establish partial failure, useful signals, objectives, overload, and incident practice. |
| 2 | [20 Security](../20-security/README.md) | Establishes identity, data, artifact, tenant, and supply-chain boundaries. |
| 3 | [21 Platform Engineering](../21-platform-engineering/README.md), [22 Developer Platforms](../22-developer-platforms/README.md), and [23 Control Planes](../23-control-planes/README.md) | Builds product, self-service, contract, and reconciliation capability. |
| 4 | [24 AI Foundations](../24-ai-foundations/README.md) | Supplies probability, linear algebra, optimization, and evaluation reasoning. |
| 5 | [25 ML and Deep Learning](../25-ml-deep-learning/README.md) | Explains training, generalization, data, and model behavior. |
| 6 | [26 Transformers and LLMs](../26-transformers-llms/README.md) | Makes transformer training, inference, evaluation, and limits concrete. |
| 7 | [27 LLM Engineering](../27-llm-engineering/README.md) | Connects models to retrieval, tools, evaluations, safety, cost, and operations. |
| 8 | [28 MLOps](../28-mlops/README.md) | Establishes reproducibility, lineage, registries, release gates, monitoring, and retirement. |
| 9 | [29 GPU Systems](../29-gpu-systems/README.md) | Grounds accelerator execution, memory, topology, profiling, scheduling, and OOM behavior. |
| 10 | [30 AI Infrastructure](../30-ai-infrastructure/README.md) | Integrates compute fleets, schedulers, data paths, operations, and economics. |
| 11 | [31 Model Serving](../31-model-serving/README.md) | Develops batching, cache, routing, admission, rollout, quality, and unit-cost tradeoffs. |
| 12 | [32 AI Platform Engineering](../32-ai-platform-engineering/README.md) | Productizes lifecycle and serving capabilities with governance and tenant contracts. |
| 13 | [33 Agentic Infrastructure](../33-agentic-infrastructure/README.md) | Adds durable state, scoped tools, approvals, replay, trajectory evidence, and fleet controls. |
| 14 | [34 System Design](../34-system-design/README.md) | Integrates requirements, capacity, ownership, overload, and recovery. |

Stages 1 through 3 are prerequisites, not a reading recap. Modules 24 through 27 may begin in parallel with platform study once systems competency is sound; modules 28 through 33 should remain ordered because each consumes the previous contracts.

## Required practice

**Labs:** [SLO incident](../labs/12-sre-slo-incident/README.md), [platform control plane](../labs/14-platform-control-plane/README.md), [ML reproducibility](../labs/15-ml-reproducibility/README.md), [GPU scheduling and OOM](../labs/16-gpu-scheduling-oom/README.md), [model-serving overload](../labs/17-model-serving-overload/README.md), [AI platform tenancy](../labs/18-ai-platform-tenancy/README.md), and [agent runtime safety](../labs/19-agent-runtime-safety/README.md).

**Incidents:** [retry storm](../incidents/08-retry-storm/README.md), [inference latency regression](../incidents/10-inference-latency/README.md), [GPU out of memory](../incidents/11-gpu-oom/README.md), and [queue overload](../incidents/12-queue-overload/README.md).

**Projects:** complete [Reproducible ML Training and Promotion Pipeline](../projects/10-reproducible-ml-pipeline/README.md), [Distributed GPU Capacity Planner](../projects/11-distributed-gpu-planner/README.md), [Multi-Tenant Model Serving System](../projects/12-model-serving-system/README.md), [Governed Self-Service AI Platform](../projects/13-ai-platform/README.md), and [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md). Agent evidence is required because the track includes module 33 and the AI platform gate; a role that excludes agent capabilities should stop at the model-serving and AI-platform evidence rather than claim the full track.

## Competency gates

**[Platform gate](../assessments/gates/platform.md):** prove a user-informed capability contract, safe reconciliation, tenant boundaries, support, adoption, reliability, and economics.

**[AI platform gate](../assessments/gates/ai-platform.md):** trace model identity and governed data through reproducible training, evaluation, promotion, serving, rollback, monitoring, and retirement; characterize GPU and serving capacity under failure and load; enforce tenant identity, quotas, isolation, metering, and audit; show quality, latency, reliability, cost, and adoption evidence; and demonstrate bounded agent authority, approvals, durable execution, replay, and safety denials.

## Certification overlays

[DOP-C02](../certs/aws-dop-c02.md) is optional and secondary. It may help an AI platform engineer who directly owns AWS delivery and operations review the [AWS module](../12-aws/README.md), but it does not cover model evaluation, GPU systems, inference economics, lineage, or AI tenancy. Prioritize AI platform project evidence.
