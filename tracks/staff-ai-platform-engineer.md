# Staff AI Platform Engineer Track

## Outcome role

A technical leader who shapes a multi-team AI platform through strategy, architecture, economics, governance, migration, and durable operating mechanisms. The outcome requires proven AI platform depth first. Staff scope is not achieved by reading leadership material or producing a diagram without implementation and operational evidence.

## Prerequisites

- All competencies in the [AI Platform Engineer track](ai-platform-engineer.md).
- Repeated independent evidence across design, implementation, production operation, incidents, security, and platform adoption.
- Experience resolving cross-team ownership and interface disputes without relying on reporting authority.
- Sufficient organizational access to validate needs, constraints, costs, and migration risks with real stakeholders.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [17 Distributed Systems](../17-distributed-systems/README.md), [19 SRE](../19-sre/README.md), and [20 Security](../20-security/README.md) | Refreshes non-negotiable failure, reliability, and trust mechanisms at platform scale. |
| 2 | [21 Platform Engineering](../21-platform-engineering/README.md), [22 Developer Platforms](../22-developer-platforms/README.md), and [23 Control Planes](../23-control-planes/README.md) | Anchors strategy in user outcomes, interfaces, convergence, governance, adoption, and economics. |
| 3 | [24 AI Foundations](../24-ai-foundations/README.md) through [27 LLM Engineering](../27-llm-engineering/README.md) | Establishes the model and application assumptions a leader must challenge. |
| 4 | [28 MLOps](../28-mlops/README.md) through [31 Model Serving](../31-model-serving/README.md) | Establishes lifecycle, GPU, infrastructure, and serving tradeoffs that drive cost and architecture. |
| 5 | [32 AI Platform Engineering](../32-ai-platform-engineering/README.md) and [33 Agentic Infrastructure](../33-agentic-infrastructure/README.md) | Integrates governed self-service model and agent capabilities. |
| 6 | [34 System Design](../34-system-design/README.md) | Provides a disciplined review structure for ownership, scale, failure, overload, and recovery. |
| 7 | [35 Senior and Staff Engineering](../35-senior-staff-engineering/README.md) | Converts technical depth into scope judgment, strategy, decisions, influence, execution, stewardship, and ethical leadership. |

Earlier modules are listed as an evidence review, not permission to skip weak foundations. Complete module 35 only after owning the project-scale technical work; otherwise its artifacts will be hypothetical.

## Required practice

**Labs:** retain current evidence from [platform control plane](../labs/14-platform-control-plane/README.md), [ML reproducibility](../labs/15-ml-reproducibility/README.md), [GPU scheduling and OOM](../labs/16-gpu-scheduling-oom/README.md), [model-serving overload](../labs/17-model-serving-overload/README.md), [AI platform tenancy](../labs/18-ai-platform-tenancy/README.md), and [agent runtime safety](../labs/19-agent-runtime-safety/README.md). Also complete the [staff operating packet](../35-senior-staff-engineering/90-staff-operating-packet-lab.md) and [organizational pressure simulation](../35-senior-staff-engineering/91-organizational-pressure-simulation-lab.md).

**Incidents:** lead [inference latency regression](../incidents/10-inference-latency/README.md), [GPU out of memory](../incidents/11-gpu-oom/README.md), and [queue overload](../incidents/12-queue-overload/README.md). Facilitate a second run in which another engineer commands the incident, then evaluate whether platform contracts and organizational interfaces improve the outcome.

**Projects:** [Governed Self-Service AI Platform](../projects/13-ai-platform/README.md) and [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md) provide prerequisite technical evidence. The capstone is [Staff AI Platform Strategy and Design Package](../projects/15-staff-ai-platform-design/README.md), grounded in measured constraints and stakeholder evidence rather than fictional certainty.

## Competency gates

**[AI platform gate](../assessments/gates/ai-platform.md):** independently demonstrate governed lifecycle, serving, tenant, reliability, cost, and agent controls at project depth.

**[Staff gate](../assessments/gates/staff.md):** produce a strategy linking user problems, technical architecture, economics, sequencing, migration, risks, governance, and measurable outcomes; lead a consequential cross-team decision while preserving dissent; define ownership and escalation boundaries; demonstrate delivery and incident mechanisms that work without personal heroics; and show mentoring, delegation, and deprecation choices that leave the organization more capable. Reviewers must be able to trace important claims to evidence and identify what would cause the strategy to change.

Passing the staff gate requires actual influence and durable outcomes. Document volume, meeting attendance, title, and sole-author implementation are not substitutes.

## Certification overlays

[DOP-C02](../certs/aws-dop-c02.md) is optional and usually low priority at this level. It can provide AWS operations breadth when the platform is strategically committed to AWS, using the [AWS module](../12-aws/README.md). It does not assess AI architecture judgment, economics, organizational interfaces, migration leadership, or durable cross-team outcomes.
