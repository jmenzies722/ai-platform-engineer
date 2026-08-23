# Architecture Fieldbook

This fieldbook is a set of reusable design-review notes. Each note names the
system's purpose, invariants, major components, failure boundaries, questions,
tradeoffs, and primary references. The diagrams are intentionally small:
boundaries and contracts matter more than vendor inventories.

## Index

| Note | Viewpoint | Central review concern |
|---|---|---|
| [Request path](request-path.md) | Edge-to-handler data path | Budgets, retries, overload, and identity |
| [Cloud network](cloud-network.md) | Regional network and trust zones | Routing, isolation, egress, and failure domains |
| [Kubernetes control loop](kubernetes-control-loop.md) | Declarative orchestration | Convergence, ownership, and safe reconciliation |
| [Telemetry pipeline](telemetry-pipeline.md) | Signals from source to use | Loss, cardinality, cost, and data governance |
| [Distributed data and consistency](distributed-data-consistency.md) | Replicated state | Guarantees, conflicts, and recovery |
| [ML training platform](ml-training-platform.md) | Data-to-model lifecycle | Reproducibility, scheduling, and lineage |
| [Model serving](model-serving.md) | Online inference | Latency, rollout safety, and capacity |
| [AI platform control plane](ai-platform-control-plane.md) | Policy and lifecycle management | Tenant-safe orchestration and auditability |
| [Agent runtime](agent-runtime.md) | Stateful tool-using execution | Authority, isolation, durability, and limits |
| [Multi-tenant security boundaries](multi-tenant-security-boundaries.md) | Cross-cutting isolation | Identity, policy, data separation, and containment |

## How to use the fieldbook

1. State measurable requirements and non-goals before selecting components.
2. Mark data, control, trust, and failure boundaries separately.
3. Assign an owner, timeout, retry policy, and observability contract to every
   remote interaction.
4. Record assumptions and the evidence that would invalidate them.
5. Test at least one overload, dependency failure, rollback, and recovery path.

Diagrams supplement contracts and reasoning. Validate designs with measurements,
fault experiments, and recovery exercises rather than treating a diagram as
proof.
