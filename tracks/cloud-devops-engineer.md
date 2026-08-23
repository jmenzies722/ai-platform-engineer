# Cloud and DevOps Engineer Track

## Outcome role

An engineer who turns application changes into secure, repeatable, observable production changes on cloud infrastructure. The role owns delivery feedback, infrastructure as code, identity and network boundaries, container and Kubernetes operations, rollback, recovery, and supply-chain evidence.

## Prerequisites

- Foundations competency in programming and Git.
- Systems, Linux, and networking diagnosis from direct evidence.
- A production-shaped service whose build, deployment, and recovery can be exercised.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [01 Software Foundations](../01-software-foundations/README.md) | Frames execution, resources, interfaces, and operational evidence. |
| 2 | [02 Python](../02-python/README.md) | Enables automation without treating scripts as unreviewed glue. |
| 3 | [05 Git](../05-git/README.md) | Establishes recoverable collaborative change. |
| 4 | [03 Computer Systems](../03-computer-systems/README.md) | Grounds compute, memory, storage, and isolation mechanisms. |
| 5 | [04 Linux](../04-linux/README.md) | Enables host diagnosis and safe automation. |
| 6 | [07 Networking](../07-networking/README.md) | Supplies routing, DNS, TLS, and failure-domain reasoning. |
| 7 | [09 Backend Engineering](../09-backend-engineering/README.md) | Provides a real workload and its deployment contracts. |
| 8 | [12 AWS](../12-aws/README.md) | Covers cloud identity, VPCs, compute, storage, resilience, operations, cost, and governance. |
| 9 | [13 DevOps](../13-devops/README.md) | Establishes feedback, continuous delivery, safe change, artifacts, and learning. |
| 10 | [14 Terraform](../14-terraform/README.md) | Makes infrastructure plans, state, drift, modules, and recovery explicit. |
| 11 | [15 Containers](../15-containers/README.md) | Connects images and runtimes to kernel isolation and supply-chain trust. |
| 12 | [16 Kubernetes](../16-kubernetes/README.md) | Adds declarative workloads, reconciliation, policy, scaling, and upgrades. |
| 13 | [18 Observability](../18-observability/README.md) | Makes delivery and infrastructure outcomes measurable. |
| 14 | [20 Security](../20-security/README.md) | Integrates threat modeling, least privilege, secrets, and software supply-chain controls. |
| 15 | [17 Distributed Systems](../17-distributed-systems/README.md) | Deepens retry, coordination, queue, and partial-failure reasoning. |

## Required practice

**Labs:** [Linux diagnosis](../labs/02-linux-diagnosis/README.md), [Git recovery](../labs/03-git-recovery/README.md), [network diagnosis](../labs/04-network-dns-tls/README.md), [AWS architecture review](../labs/07-aws-architecture-review/README.md), [Terraform safety](../labs/08-terraform-safety/README.md), [container isolation](../labs/09-container-isolation/README.md), [Kubernetes operations](../labs/10-kubernetes-operations/README.md), [OpenTelemetry traces](../labs/11-opentelemetry-traces/README.md), and [security threat modeling](../labs/13-security-threat-model/README.md).

**Incidents:** [OOM kill](../incidents/02-oom/README.md), [disk exhaustion](../incidents/03-disk-exhaustion/README.md), [TLS expiry](../incidents/04-tls-expiry/README.md), [bad rollout](../incidents/06-bad-rollout/README.md), and [Kubernetes CrashLoopBackOff](../incidents/07-kubernetes-crashloopbackoff/README.md).

**Projects:** complete [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md) and [Verifiable Software Delivery Pipeline](../projects/05-secure-delivery-pipeline/README.md). Add [Multi-Tenant Kubernetes Application Platform](../projects/06-kubernetes-platform/README.md) for Kubernetes-heavy roles.

## Competency gates

**[Foundations gate](../assessments/gates/foundations.md):** write and test bounded automation, trace it through runtime and machine state, repair an evidence defect, and explain how the workload consumes host resources.

**[Systems, Linux, and networking gate](../assessments/gates/systems-linux-networking.md):** use Git recovery deliberately and diagnose a process, disk, DNS, TLS, or connection failure from mechanism-level evidence.

**[Cloud delivery gate](../assessments/gates/cloud-delivery.md):** provision a least-privilege networked cloud foundation from reviewed plans; protect and recover state; produce a provenance-bearing artifact; promote it through explicit policy; exercise rollback; and connect every claim to logs, configuration, or cloud inventory.

**[Kubernetes reliability gate](../assessments/gates/kubernetes-reliability.md):** explain container isolation, debug workload intent through scheduler and runtime evidence, enforce resource and tenancy boundaries, and complete an upgrade or failure drill with rollback criteria.

## Certification overlays

[AWS Certified DevOps Engineer - Professional (DOP-C02)](../certs/aws-dop-c02.md) is directly relevant for AWS-centered roles because its delivery, resilience, monitoring, incident response, security, and governance domains overlap this path. Use it with the [AWS module](../12-aws/README.md). It is optional: multi-cloud, private-cloud, or platform-specific roles may gain little from exam-focused AWS breadth, and certification never replaces infrastructure plans, rollback, restore, or incident evidence.
