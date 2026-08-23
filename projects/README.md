# Project Briefs

This directory contains exactly fifteen curriculum briefs. Implement each selected project in an independent repository with its own history, release process, operational evidence, and security boundary. Keep generated scaffolding, application code, infrastructure state, datasets, model artifacts, captures, and credentials out of this curriculum repository.

The sequence moves from direct observation of one machine to multi-team AI platform strategy. Projects are not mandatory in lockstep: choose evidence that closes a real competency gap, but do not claim a later platform project without proving its foundations.

## Inventory

| # | Brief | Primary portfolio proof | Level |
|---:|---|---|---|
| 01 | [Systems Inspector and Capacity Probe](01-systems-inspector/README.md) | Kernel evidence, safe inspection, and mechanism-level diagnosis | Foundations |
| 02 | [Production Change-Request API](02-production-api/README.md) | Durable API correctness, concurrency, migrations, and recovery | Service engineering |
| 03 | [Network Failure Laboratory](03-network-failure-lab/README.md) | Protocol reasoning from packets and endpoint evidence | Service engineering |
| 04 | [Recoverable AWS Foundation with Terraform](04-aws-terraform-foundation/README.md) | Reproducible, least-privilege cloud infrastructure and state recovery | Cloud infrastructure |
| 05 | [Verifiable Software Delivery Pipeline](05-secure-delivery-pipeline/README.md) | Artifact provenance, policy, promotion, and rollback | Cloud infrastructure |
| 06 | [Multi-Tenant Kubernetes Application Platform](06-kubernetes-platform/README.md) | Workload contracts, tenancy, lifecycle, and cluster operations | Cloud platform |
| 07 | [Operable Telemetry Stack](07-telemetry-stack/README.md) | Useful signals, data governance, backpressure, and telemetry economics | Operations |
| 08 | [Reliability Review and Incident Exercise](08-reliability-exercise/README.md) | SLO-led risk reduction, incident command, and recovery | Operations |
| 09 | [Secure Developer Platform Control Plane](09-developer-platform-control-plane/README.md) | Product research plus convergent, policy-bound self-service | Platform engineering |
| 10 | [Reproducible ML Training and Promotion Pipeline](10-reproducible-ml-pipeline/README.md) | Lineage, evaluation, governed promotion, monitoring, and retirement | ML systems |
| 11 | [Distributed GPU Capacity Planner and Simulator](11-distributed-gpu-planner/README.md) | Topology-aware scheduling, failure simulation, and accelerator economics | AI infrastructure |
| 12 | [Multi-Tenant Model Serving System](12-model-serving-system/README.md) | Admission, batching, fairness, rollout, and inference unit cost | AI infrastructure |
| 13 | [Governed Self-Service AI Platform](13-ai-platform/README.md) | Evidence-bound model lifecycle through a reliable control plane | AI platform |
| 14 | [Governed Agent Runtime](14-governed-agent-runtime/README.md) | Durable tool use, scoped authority, approvals, replay, and safe failure | Agent infrastructure |
| 15 | [Staff AI Platform Strategy and Design Package](15-staff-ai-platform-design/README.md) | Cross-team architecture, economics, migration, governance, and durable ownership | Staff |

## How to use a brief

1. Copy the brief into a new repository and replace assumptions with measured requirements.
2. Record the initial baseline before choosing products or optimizations.
3. Build thin vertical milestones; retain plans, test output, profiles, drill timelines, and recovery evidence.
4. Ask another engineer to run the documented setup and at least one blind failure drill.
5. Grade against the brief's explicit rubric. “Deployed” and “demo works” are intermediate states.

The portfolio-wide evaluation rules and a second synchronized inventory live in [PROJECTS.md](../PROJECTS.md).
