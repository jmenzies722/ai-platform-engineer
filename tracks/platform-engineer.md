# Platform Engineer Track

## Outcome role

An engineer who turns recurring delivery and infrastructure work into a secure, reliable internal product. The outcome is not a portal: it is a measured capability with explicit contracts, self-service boundaries, reconciliation, support, governance, economics, and voluntary adoption.

## Prerequisites

- Cloud delivery and infrastructure-as-code competency.
- Kubernetes and reliability evidence, including incident participation.
- Experience operating a service and supporting developers who consume shared capabilities.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [03 Computer Systems](../03-computer-systems/README.md), [04 Linux](../04-linux/README.md), and [07 Networking](../07-networking/README.md) | Preserve mechanism-level diagnosis beneath abstractions. |
| 2 | [09 Backend Engineering](../09-backend-engineering/README.md) and [11 Software Architecture](../11-software-architecture/README.md) | Establish API, state, evolution, and ownership contracts. |
| 3 | [12 AWS](../12-aws/README.md) | Supplies a concrete cloud substrate; translate concepts when another provider is used. |
| 4 | [13 DevOps](../13-devops/README.md) and [14 Terraform](../14-terraform/README.md) | Establish safe delivery and declarative infrastructure change. |
| 5 | [15 Containers](../15-containers/README.md) and [16 Kubernetes](../16-kubernetes/README.md) | Provide workload packaging, isolation, reconciliation, and policy. |
| 6 | [17 Distributed Systems](../17-distributed-systems/README.md) | Makes control-loop and partial-failure assumptions explicit. |
| 7 | [18 Observability](../18-observability/README.md) and [19 SRE](../19-sre/README.md) | Add service objectives, incident operations, capacity, and learning. |
| 8 | [20 Security](../20-security/README.md) | Establishes identity, secrets, tenant, and supply-chain controls. |
| 9 | [21 Platform Engineering](../21-platform-engineering/README.md) | Frames platform work as product discovery, contracts, adoption, and economics. |
| 10 | [22 Developer Platforms](../22-developer-platforms/README.md) | Develops catalogs, templates, golden paths, portals, plugins, and scorecards coherently. |
| 11 | [23 Control Planes](../23-control-planes/README.md) | Makes self-service converge through declarative APIs, ownership, idempotency, and lifecycle safety. |
| 12 | [34 System Design](../34-system-design/README.md) | Integrates scale, data ownership, overload, and recovery into platform design. |

## Required practice

**Labs:** [Terraform safety](../labs/08-terraform-safety/README.md), [container isolation](../labs/09-container-isolation/README.md), [Kubernetes operations](../labs/10-kubernetes-operations/README.md), [OpenTelemetry traces](../labs/11-opentelemetry-traces/README.md), [security threat model](../labs/13-security-threat-model/README.md), and [reconciliation control plane](../labs/14-platform-control-plane/README.md).

**Incidents:** [bad rollout](../incidents/06-bad-rollout/README.md), [Kubernetes CrashLoopBackOff](../incidents/07-kubernetes-crashloopbackoff/README.md), [retry storm](../incidents/08-retry-storm/README.md), and [queue overload](../incidents/12-queue-overload/README.md). For each, state what the platform contract should prevent, expose, and leave to the workload owner.

**Projects:** [Multi-Tenant Kubernetes Application Platform](../projects/06-kubernetes-platform/README.md) and [Secure Developer Platform Control Plane](../projects/09-developer-platform-control-plane/README.md) are required. [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md) is required when observability is a platform capability.

## Competency gates

**[Cloud delivery gate](../assessments/gates/cloud-delivery.md):** demonstrate recoverable infrastructure state, policy-bound artifact promotion, rollback, and least privilege.

**[Kubernetes reliability gate](../assessments/gates/kubernetes-reliability.md):** operate tenant workloads through reconciliation, resource pressure, upgrades, and failures.

**[Platform gate](../assessments/gates/platform.md):** show researched user needs; a versioned capability contract with responsibilities and escape hatches; a convergent control plane with tenant isolation and audit; a support and deprecation model; and measured adoption, reliability, lead time, cognitive load, and unit cost. Include evidence of what was deliberately not centralized.

## Certification overlays

[DOP-C02](../certs/aws-dop-c02.md) is optional for AWS-centered platform teams. It can reinforce the cloud operations and delivery substrate represented by the [AWS module](../12-aws/README.md), but it does not assess product discovery, interface coherence, control-plane convergence, adoption, or platform economics. Prioritize platform project evidence when the role is provider-neutral.
