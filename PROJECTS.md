# Portfolio Projects

Projects are where lesson models meet constraints. These fifteen briefs define future **independent repositories** with their own history, decisions, verification, operational evidence, and release process. This curriculum repository contains briefs only; implementations, generated scaffolds, cloud state, datasets, binaries, model artifacts, packet captures, and secrets belong elsewhere.

The canonical linked inventory is also available at [projects/README.md](projects/README.md). Status is intentionally not tracked here: a project earns a claim from inspectable evidence in its own repository.

## What a project must prove

Begin only when you can state the user problem without naming the technology. A working happy path is the midpoint, not the finish. A strong project measures normal behavior, survives a controlled failure, supports diagnosis and recovery, and records the decisions behind the design.

| # | Portfolio brief | Primary proof |
|---:|---|---|
| 01 | [**Systems Inspector and Capacity Probe**](projects/01-systems-inspector/README.md) | Kernel evidence, safe inspection, and mechanism-level diagnosis. |
| 02 | [**Production Change-Request API**](projects/02-production-api/README.md) | Durable API correctness, concurrency, migrations, asynchronous work, and recovery. |
| 03 | [**Network Failure Laboratory**](projects/03-network-failure-lab/README.md) | Reproducible DNS, TCP, TLS, proxy, timeout, and packet-loss diagnosis. |
| 04 | [**Recoverable AWS Foundation with Terraform**](projects/04-aws-terraform-foundation/README.md) | Least-privilege infrastructure, policy checks, state lifecycle, cost controls, and recovery. |
| 05 | [**Verifiable Software Delivery Pipeline**](projects/05-secure-delivery-pipeline/README.md) | Provenance from source through signed artifact, policy, promotion, and rollback. |
| 06 | [**Multi-Tenant Kubernetes Application Platform**](projects/06-kubernetes-platform/README.md) | Workload contracts, identity, policy, observability, upgrades, isolation, and recovery. |
| 07 | [**Operable Telemetry Stack**](projects/07-telemetry-stack/README.md) | Correlated metrics, logs, and traces with backpressure, governance, and unit costs. |
| 08 | [**Reliability Review and Incident Exercise**](projects/08-reliability-exercise/README.md) | SLOs, risk analysis, capacity, failure drills, incident command, and measured improvement. |
| 09 | [**Secure Developer Platform Control Plane**](projects/09-developer-platform-control-plane/README.md) | User-researched self-service backed by policy, reconciliation, tenancy, and actionable status. |
| 10 | [**Reproducible ML Training and Promotion Pipeline**](projects/10-reproducible-ml-pipeline/README.md) | Versioned data, evaluation, lineage, governed promotion, monitoring, and retirement. |
| 11 | [**Distributed GPU Capacity Planner and Simulator**](projects/11-distributed-gpu-planner/README.md) | Topology-aware scheduling, contention, checkpoint/failure simulation, and accelerator economics. |
| 12 | [**Multi-Tenant Model Serving System**](projects/12-model-serving-system/README.md) | Admission, batching, fairness, quotas, rollout, fallback, and inference cost attribution. |
| 13 | [**Governed Self-Service AI Platform**](projects/13-ai-platform/README.md) | Evaluation and deployment through policy, lineage, tenancy, reconciliation, and operational status. |
| 14 | [**Governed Agent Runtime**](projects/14-governed-agent-runtime/README.md) | Durable tool workflows with scoped identity, approvals, budgets, audit, evaluation, and replay. |
| 15 | [**Staff AI Platform Strategy and Design Package**](projects/15-staff-ai-platform-design/README.md) | Organization-wide architecture, economics, migration, governance, influence, and durable ownership. |

## Graduation Criteria

A project is portfolio-grade only when another engineer can evaluate both the system and your engineering judgment.

Explain the user problem plainly, then describe the components, state, critical path, and invariants. Finish with the production constraints: failure, operations, security, cost, and the tradeoffs you accepted.

### Problem and Users

- Defines a real user, workload, constraint set, and non-goals.
- Explains why the system should exist and why a simpler alternative is insufficient.
- Includes success measures beyond “it runs.”

### Architecture and Decisions

- Documents context, quality attributes, boundaries, data/control flows, trust boundaries, and failure domains.
- Records consequential decisions and rejected alternatives.
- Includes capacity assumptions and cost drivers.

### Implementation Quality

- Has reproducible setup, pinned or controlled dependencies, automated tests, linting, and meaningful commit history.
- Uses secure defaults, least privilege, explicit configuration, and no committed secrets.
- Exposes stable contracts and handles invalid, duplicate, delayed, and partial inputs.

### Reliability and Operations

- Defines service-level indicators and, where appropriate, objectives.
- Emits useful metrics, logs, traces, events, and status—not telemetry theater.
- Includes dashboards or queries, actionable alerts, runbooks, backup/recovery, upgrade, and rollback paths.
- Demonstrates load, failure injection, and recovery with captured evidence.

### Security and Governance

- Contains a threat model, dependency/supply-chain controls, secret strategy, and audit boundaries.
- Documents tenant isolation, data handling, retention, and residual risk where relevant.

### Communication

- README gives a truthful quick start, architecture map, tradeoffs, and current limitations.
- A concise demo starts with user value, shows normal behavior, introduces a failure, diagnoses it, and proves recovery.
- You can explain internals and defend tradeoffs without relying on generated prose.

### Independence

- The repository can be cloned and evaluated from documented prerequisites.
- It is not a verbatim tutorial implementation.
- Its design reflects measured behavior and lessons from at least one intentionally induced failure.

Use the selected directory brief as the initial project contract, then adapt it from real discovery and measurements. Track curriculum competencies in [PROGRESS.md](PROGRESS.md), not with inflated project completion percentages.

Before calling a project portfolio-grade, give its core explanation at all three levels in [TEACH-BACK.md](TEACH-BACK.md).
