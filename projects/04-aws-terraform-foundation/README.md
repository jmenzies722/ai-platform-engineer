# 04 — Recoverable AWS Foundation with Terraform

Specify and prove a small AWS environment that a product team can safely consume. Build it only in a dedicated project repository and sandbox account.

## Problem and users

Platform operators need repeatable account and network foundations; service teams need clear interfaces without broad cloud permissions; security and finance need evidence. Hand-built environments drift, conceal ownership, and are hard to recover. The result should enable one sample workload while making blast radius, cost, and recovery explicit.

## Constraints and non-goals

- Target a sandbox AWS Organization or isolated account, two availability zones, and one documented region.
- Terraform owns declared resources; remote state, locking, provider constraints, and bootstrap boundaries must be explicit.
- Use short-lived federation and least privilege. No static AWS keys, production data, multi-region failover, or custom Terraform provider.
- Set a hard monthly budget and a one-command destroy path that preserves required audit/state evidence.

## Architecture expectations

Separate account bootstrap, network, identity, shared services, and workload interfaces into versioned root modules. Include VPC/subnets/routes/endpoints, centralized logs, KMS ownership, state recovery, and a minimal workload contract. Explain public egress, DNS, availability-zone dependencies, policy evaluation, module upgrade compatibility, drift, and what happens if state is unavailable.

## Milestone plan

1. Write requirements, threat model, cost estimate, resource inventory, and bootstrap procedure.
2. Create versioned networking and identity modules with tests and policy checks.
3. Add workload interface, logs, budgets, backup/state recovery, and drift detection.
4. Exercise clean apply, interrupted apply, import, module upgrade, rollback, disaster recovery, and destroy.

## Required artifacts

- Architecture diagrams, module contracts, ADRs, and ownership matrix.
- Plans captured in CI, policy test results, bill-of-materials inventory, and drift report.
- Cost forecast versus measured sandbox bill; quota and capacity worksheet.
- Bootstrap, break-glass, state recovery, credential compromise, upgrade, and teardown runbooks.

## Tests and failure drills

Run formatting, validation, static analysis, module tests, policy tests, and ephemeral integration applies. Inject an interrupted apply, manual resource drift, missing state lock, denied KMS permission, exhausted NAT path, module incompatibility, and loss of the primary state copy. Recover without broadening permissions or editing state blindly.

## Observability, security, and cost

Route CloudTrail and configuration changes to protected storage; alert on root use, policy changes, budget thresholds, failed applies, and drift. Analyze IAM access, encryption, log immutability, endpoint policies, egress, and supply-chain provenance. Report monthly fixed cost, data-processing/egress sensitivity, idle waste, and cost per hosted sample workload.

## Explicit success rubric

| Review area | Pass condition |
|---|---|
| Reproducibility | An empty sandbox reaches the expected inventory from documented bootstrap and pinned inputs. |
| Isolation | Policy tests and adversarial checks show workload roles cannot administer foundation resources. |
| Recovery | State loss and interrupted apply are recovered within stated RPO/RTO using the runbook. |
| Economics | Estimate is reconciled to measured spend and automated limits prevent unbounded cost. |
| Lifecycle | Upgrade, drift reconciliation, and clean teardown retain required evidence. |

## Stretch work

Add a second account with delegated administration, VPC IPAM, or a verified multi-region recovery design without deploying permanent duplicate capacity.

## Authoritative sources

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
- [Terraform module development](https://developer.hashicorp.com/terraform/language/modules/develop)

## Mapped modules

[12 AWS](../../12-aws/README.md), [13 DevOps](../../13-devops/README.md), [14 Terraform](../../14-terraform/README.md), [17 Distributed Systems](../../17-distributed-systems/README.md), and [20 Security](../../20-security/README.md).
