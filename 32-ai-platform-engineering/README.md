# 32 — AI Platform Engineering

An AI platform turns recurring infrastructure work into safe, supported interfaces that product teams can use without surrendering control.

## What you will learn

- Define versioned contracts and paved roads with explicit responsibilities.
- Govern tenant identity, data, training, serving, retrieval, evaluation, and cost.
- Operate the platform as a reliable product with measurable user outcomes.

## Lessons

1. [Platform contracts and paved roads](01-platform-contracts-and-paved-roads.md)
2. [Tenancy, governance, and cost](02-tenancy-governance-and-cost.md)
3. [Operating the platform as a product](03-operating-the-platform-as-a-product.md)
4. [Data and feature platform contracts](04-data-and-feature-platform-contracts.md)
5. [Training platform architecture](05-training-platform-architecture.md)
6. [Serving platform architecture](06-serving-platform-architecture.md)
7. [Retrieval and index platform contracts](07-retrieval-and-index-platform-contracts.md)
8. [Evaluation, lineage, and release governance](08-evaluation-lineage-and-release-governance.md)
9. [Cost, reliability, and platform operations](09-cost-reliability-and-operations.md)
10. [Practical lab: verify an AI platform control plane](10-practical-ai-platform-lab.md)

## Practice

Run the [module control-plane lab](10-practical-ai-platform-lab.md), then complete standalone [Lab 18: Verify AI Platform Tenant Isolation](../labs/18-ai-platform-tenancy/README.md). Together they exercise digest-bound lineage, retrieval namespaces, index publication, promotion, rollback, cache boundaries, quotas, and idempotent usage.

Use these incident drills to practice evidence-led operation:

- [Bad rollout](../incidents/06-bad-rollout/README.md) for version correlation and rollback.
- [Retry storm](../incidents/08-retry-storm/README.md) for retry budgets and load amplification.
- [Inference latency regression](../incidents/10-inference-latency/README.md) for queue and batching diagnosis.
- [GPU out of memory](../incidents/11-gpu-oom/README.md) for workload-aware admission.
- [Queue overload](../incidents/12-queue-overload/README.md) for backlog age and recovery proof.

Extend the work through [Reproducible ML Training and Promotion](../projects/10-reproducible-ml-pipeline/README.md), [Distributed GPU Capacity Planner](../projects/11-distributed-gpu-planner/README.md), [Multi-Tenant Model Serving](../projects/12-model-serving-system/README.md), [Governed Self-Service AI Platform](../projects/13-ai-platform/README.md), or the [Staff AI Platform Strategy and Design Package](../projects/15-staff-ai-platform-design/README.md).

## Ready to continue

You can separate policy from implementation, preserve identity and lineage across workflows, define tenant-scoped retrieval and rollback, and use quality, cost, reliability, and adoption evidence.

## Next

Begin [Agentic Infrastructure](../33-agentic-infrastructure/README.md).
