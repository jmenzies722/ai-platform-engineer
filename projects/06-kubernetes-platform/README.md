# 06 — Multi-Tenant Kubernetes Application Platform

Create the implementation in an independent repository. The platform should host representative services safely; it is not a YAML showcase.

## Problem and users

Application teams need a supported path from an image to a reachable, observable workload without becoming cluster administrators. Platform operators need enforceable tenancy, upgrades, capacity controls, and recovery. Security engineers need workload identity and policy evidence.

## Constraints and service contract

- Support one Kubernetes minor-version range, three synthetic teams, and stateless plus stateful sample workloads.
- Prefer managed primitives and documented add-ons; every cluster-wide component needs an owner and upgrade path.
- No privileged application pods, long-lived service-account tokens, public unauthenticated endpoints, or production claims from a single-node cluster.
- Define what the platform guarantees and what remains the workload team's responsibility.

## Architecture expectations

Design cluster and node failure domains, namespaces/tenants, ingress, DNS, workload identity, network policy, secrets, storage, quotas, autoscaling, disruption controls, telemetry, and Git-based reconciliation. Separate platform and workload APIs. Explain admission order, controller convergence, certificate rotation, scheduling, eviction, and add-on dependency failure.

## Milestone plan

1. Publish workload contract, tenancy/threat model, capacity model, and cluster lifecycle plan.
2. Establish declarative cluster add-ons, identity, ingress, policy, secrets, and baseline telemetry.
3. Onboard sample services with quotas, autoscaling, disruption budgets, persistent data, and golden dashboards.
4. Test upgrades, node/AZ loss, control-plane/add-on faults, restore, rollback, and noisy-neighbor controls.

## Required artifacts

- Platform API/workload contract, topology and trust diagrams, add-on inventory, compatibility matrix, and ADRs.
- Conformance/policy test suite, upgrade and restore evidence, capacity report, and tenant onboarding guide.
- SLO dashboard, actionable alerts, runbooks, post-incident review, and ownership matrix.
- Cost allocation model by cluster, node pool, namespace, and workload.

## Tests and failure drills

Use schema, policy, reconciliation, security, and workload conformance tests. Drill node drain, zone loss, DNS failure, expired certificate, webhook outage, image-pull failure, secret rotation, quota exhaustion, storage detach delay, API throttling, and an incompatible add-on upgrade. Confirm tenant isolation during every fault.

## Observability, security, and cost

Measure API and controller health, scheduling latency, pending pods, DNS/ingress errors, resource saturation, restart causes, and tenant SLOs. Enforce workload identity, restricted pod security, default-deny networking, signed-image policy, secret encryption/rotation, and audited break-glass access. Reconcile requested, reserved, and used resources; report idle capacity, shared add-on cost, and scaling thresholds.

## Explicit success rubric

| Dimension | Graduation threshold |
|---|---|
| Self-service | A new team deploys the sample contract without cluster-admin help. |
| Isolation | Cross-tenant network, identity, secret, and quota attacks fail under test. |
| Resilience | Platform and sample SLOs recover within declared bounds for node, zone, and add-on drills. |
| Lifecycle | Minor upgrade and rollback preserve workload and policy contracts with captured evidence. |
| Efficiency | Capacity and allocation data explain headroom and the dominant cost drivers. |

## Stretch work

Add virtual clusters, progressive delivery, or heterogeneous GPU node pools with explicit scheduling and cost policy.

## Authoritative sources

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [CNCF Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/tree/main/security-whitepaper)

## Mapped modules

[15 Containers](../../15-containers/README.md), [16 Kubernetes](../../16-kubernetes/README.md), [17 Distributed Systems](../../17-distributed-systems/README.md), [18 Observability](../../18-observability/README.md), [19 Site Reliability Engineering](../../19-sre/README.md), and [20 Security](../../20-security/README.md).
