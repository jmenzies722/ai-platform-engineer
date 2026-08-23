# Portfolio Projects

These fifteen targets are future **independent repositories**. Each should have its own history, architecture decisions, automated verification, operational evidence, and release process. This repository supplies the curriculum and project briefs; it should not become a monorepo containing all implementations.

All projects are **Planned**.

| # | Portfolio target | Primary proof |
|---:|---|---|
| 01 | **Systems Inspector CLI** | Inspect Linux processes, memory, file descriptors, sockets, and cgroups; correlate observations with `/proc` and system calls. |
| 02 | **Production Backend Service** | Authenticated API with durable storage, migrations, idempotency, asynchronous work, tests, telemetry, and capacity evidence. |
| 03 | **Network Failure Lab** | Reproducible DNS, TCP, TLS, proxy, timeout, retry, and packet-loss experiments with evidence-led runbooks. |
| 04 | **Cloud Foundation** | Least-privilege AWS account/VPC baseline expressed in Terraform with policy checks, state strategy, cost controls, and recovery. |
| 05 | **Secure Delivery Pipeline** | Build, test, scan, sign, promote, verify, roll back, and audit a service artifact across environments. |
| 06 | **Container Runtime Explorer** | A teaching implementation that creates isolated processes from Linux namespaces, cgroups, mounts, and capabilities. |
| 07 | **Kubernetes Production Platform** | Cluster add-ons and workload contracts for ingress, identity, policy, secrets, observability, autoscaling, upgrades, and recovery. |
| 08 | **Reconciliation Control Plane** | Declarative API plus idempotent controllers, work queues, status conditions, finalizers, retries, and convergence tests. |
| 09 | **Service Reliability System** | SLIs/SLOs, error-budget policy, telemetry, alerts, load tests, capacity model, incident exercises, and reliability backlog. |
| 10 | **Internal Developer Platform** | User-researched paved road offering secure self-service creation and operation of a service; adoption and cognitive-load measures included. |
| 11 | **Reproducible ML Platform Slice** | Versioned data, training, evaluation, registry, lineage, promotion, deployment, monitoring, and rollback for one model. |
| 12 | **GPU Workload Observatory** | Collect and correlate scheduler, node, GPU, framework, and workload signals; diagnose utilization and memory bottlenecks. |
| 13 | **Multi-Tenant Model Serving Gateway** | Admission, routing, batching, quotas, auth, observability, rollout, fallback, and cost attribution across model servers. |
| 14 | **AI Platform Control Plane** | Self-service model deployment and evaluation with policy, lineage, tenancy, reconciliation, and operational status. |
| 15 | **Governed Agent Runtime** | Durable tool-using workflows with scoped identity, sandboxing, approvals, budgets, audit logs, evaluation, replay, and recovery. |

## Graduation Criteria

A project is portfolio-grade only when another engineer can evaluate both the system and your engineering judgment.

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
- A concise demo follows user value → system behavior → failure → diagnosis → recovery.
- You can explain internals and defend tradeoffs without relying on generated prose.

### Independence

- The repository can be cloned and evaluated from documented prerequisites.
- It is not a verbatim tutorial implementation.
- Its design reflects measured behavior and lessons from at least one intentionally induced failure.

Use [templates/PROJECT.md](templates/PROJECT.md) to shape an initial brief. Track curriculum competencies in [PROGRESS.md](PROGRESS.md), not with inflated project completion percentages.
