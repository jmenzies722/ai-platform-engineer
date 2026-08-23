# Site Reliability Engineer Track

## Outcome role

An engineer who translates user expectations into reliability policy, engineers systems within error and capacity budgets, and leads evidence-based diagnosis and recovery. The role combines software, systems, distributed-systems, observability, incident, and organizational judgment.

## Prerequisites

- Programming and Git competency sufficient to build automation and review production changes.
- Systems, Linux, networking, and database diagnosis.
- Experience deploying and operating at least one production-shaped service.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [01 Software Foundations](../01-software-foundations/README.md) | Establishes execution and failure boundaries. |
| 2 | [02 Python](../02-python/README.md) and [10 Go](../10-go/README.md) | Support automation, services, concurrency, cancellation, and tooling. |
| 3 | [03 Computer Systems](../03-computer-systems/README.md) | Grounds resource and I/O behavior. |
| 4 | [04 Linux](../04-linux/README.md) | Enables process, host, and storage diagnosis. |
| 5 | [07 Networking](../07-networking/README.md) | Enables protocol and path diagnosis. |
| 6 | [08 Databases](../08-databases/README.md) | Covers transaction, lock, replication, and recovery failure modes. |
| 7 | [09 Backend Engineering](../09-backend-engineering/README.md) | Supplies request, queue, overload, and deployment semantics. |
| 8 | [13 DevOps](../13-devops/README.md) | Connects reliability to safe change and ownership. |
| 9 | [15 Containers](../15-containers/README.md) and [16 Kubernetes](../16-kubernetes/README.md) | Add workload isolation and declarative operations. |
| 10 | [17 Distributed Systems](../17-distributed-systems/README.md) | Builds partial-failure, coordination, retry, and backpressure reasoning. |
| 11 | [18 Observability](../18-observability/README.md) | Develops useful, governed signals and investigation methods. |
| 12 | [19 SRE](../19-sre/README.md) | Integrates SLIs, SLOs, budgets, incidents, toil, capacity, and release resilience. |
| 13 | [20 Security](../20-security/README.md) | Prevents operational convenience from weakening trust boundaries. |
| 14 | [34 System Design](../34-system-design/README.md) | Integrates capacity, failure domains, overload, and recovery at design time. |

## Required practice

**Labs:** [Linux diagnosis](../labs/02-linux-diagnosis/README.md), [network diagnosis](../labs/04-network-dns-tls/README.md), [database behavior](../labs/05-postgres-redis/README.md), [backend reliability](../labs/06-backend-reliability/README.md), [Kubernetes operations](../labs/10-kubernetes-operations/README.md), [OpenTelemetry traces](../labs/11-opentelemetry-traces/README.md), and [SLO incident](../labs/12-sre-slo-incident/README.md).

**Incidents:** complete all drills in the [Incident Drill Academy](../incidents/README.md). At minimum, run [OOM](../incidents/02-oom/README.md), [disk exhaustion](../incidents/03-disk-exhaustion/README.md), [database pool exhaustion](../incidents/05-database-pool-exhaustion/README.md), [bad rollout](../incidents/06-bad-rollout/README.md), [retry storm](../incidents/08-retry-storm/README.md), and [queue overload](../incidents/12-queue-overload/README.md) with rotating incident roles.

**Projects:** [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md) and [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) are required. Add [Multi-Tenant Kubernetes Application Platform](../projects/06-kubernetes-platform/README.md) when cluster reliability is part of the role.

## Competency gates

**[Systems, Linux, and networking gate](../assessments/gates/systems-linux-networking.md):** localize controlled resource and protocol faults from direct evidence and state uncertainty honestly.

**[Cloud delivery gate](../assessments/gates/cloud-delivery.md):** demonstrate safe promotion, rollback, immutable artifact identity, least privilege, and recoverable infrastructure state.

**[Kubernetes reliability gate](../assessments/gates/kubernetes-reliability.md):** debug reconciliation and runtime failures, model capacity and failure domains, and preserve service during a controlled disruption.

**SRE outcome evidence:** define user-centered SLIs and justified SLOs; calculate burn and make an error-budget decision; produce a capacity and overload model; lead an incident with hypotheses, reversible mitigations, and recovery proof; and turn learning into owned, testable prevention without hiding toil.

## Certification overlays

[DOP-C02](../certs/aws-dop-c02.md) is optional for SREs operating primarily on AWS. Its operations, resilience, monitoring, and incident-response coverage can provide a useful review structure alongside the [AWS module](../12-aws/README.md). It is less relevant for provider-neutral reliability roles and cannot establish SLI quality, incident leadership, or novel failure diagnosis.
