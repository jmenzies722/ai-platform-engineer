# Cloud Delivery Gate

This gate tests whether the learner can preserve identity, intent, policy, and recovery evidence from infrastructure design through artifact delivery. It covers [AWS](../../12-aws/README.md), [DevOps](../../13-devops/README.md), [Terraform](../../14-terraform/README.md), and [containers](../../15-containers/README.md).

## Prerequisites

- Pass the [Systems, Linux, and Networking Gate](systems-linux-networking.md).
- Complete [Review Terraform Plans and Protect State](../../labs/08-terraform-safety/README.md) and [Inspect Container Isolation](../../labs/09-container-isolation/README.md).
- Provide either approved, redacted evidence from [the read-only AWS review](../../labs/07-aws-architecture-review/README.md) or complete its paper mode without credentials.
- Bring a baseline modeled on [Recoverable AWS Foundation with Terraform](../../projects/04-aws-terraform-foundation/README.md) and [Verifiable Software Delivery Pipeline](../../projects/05-secure-delivery-pipeline/README.md). A local provider-free Terraform root and local OCI registry or equivalent simulated evidence store are acceptable.

## Challenge

Design a two-availability-zone sandbox foundation for one containerized service. Define account, identity, VPC, subnet, route, DNS, ingress, egress, data, logging, encryption, state, failure-domain, and cost boundaries. Implement the smallest safe proof using Terraform and a reproducibly built container. The proof must:

- pin providers, modules, base image, and artifact identity;
- produce a reviewable saved plan and machine-readable action summary;
- keep state sensitive, locked when shared, backed up, and recoverable;
- build, test, inspect, and identify the image by digest;
- promote the same immutable digest through two simulated lifecycle environments;
- verify policy and provenance before promotion; and
- provide rollback and teardown paths with retained audit evidence.

The evaluator introduces one fresh change or fault:

- configuration changes after a saved plan;
- manual drift or an interrupted apply in a disposable target;
- missing or stale state copy;
- denied identity or encryption permission in a paper or simulated review;
- modified artifact, unsigned digest, or untrusted build provenance;
- container endpoint mismatch or resource-limit failure; or
- a cost or availability assumption that invalidates the design.

The candidate must stop unsafe application, identify the affected identity or contract, reconcile through supported workflows, verify artifact continuity, and update the design decision. No real cloud mutation is required. If an AWS account is used, access must be owner-approved, sandboxed, budgeted, and limited to the declared role and region.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- redacted account and region or explicit paper-mode statement, command allowlist, resource inventory, topology, trust boundaries, and uncertainty register;
- Terraform configuration, dependency graph, version lock, validation and test output, saved-plan hash, action summary, state addresses, drift or recovery transcript, and backup disposal proof;
- container build inputs, image ID and digest, SBOM or local inventory, test result, runtime limits, namespace/cgroup/mount evidence, and endpoint proof;
- source-to-artifact-to-environment identity chain, policy decisions, promotion record, rollback record, and exception ownership;
- monthly cost model with fixed and variable drivers, budget and quota guardrails, sensitivity to egress or availability choice, and teardown verification; and
- runbooks for apply approval, state recovery, credential compromise, failed promotion, rollback, and cleanup.

## Dimension requirements

- **Explain:** Trace an authorized API call and network path through account, identity, region, availability zone, and VPC boundaries. Explain Terraform's configuration, prior state, and provider-reported reality, plus image, container, registry, and host-kernel distinctions.
- **Build:** Produce a tested infrastructure proof and immutable artifact flow with pinned inputs, least privilege, explicit state ownership, and digest continuity.
- **Debug:** Diagnose the hidden plan, state, identity, artifact, or runtime fault without hand-editing state, bypassing verification, or replacing evidence.
- **Operate:** Verify account, principal, region, plan, digest, and target; use approval and rollback triggers; recover or tear down safely; prove no billable or local runtime resources remain.
- **Design:** Defend failure domains, identity and network boundaries, state bootstrap, delivery authority, supply-chain policy, recovery objectives, and cost model under the evaluator's changed assumption.

## Evaluator instructions

Prefer provider-free or fully sandboxed fixtures. Review commands before cloud execution and stop on unexpected account, region, principal, resource count, sensitive output, or cost. For a paper AWS review, score reasoning and evidence handling rather than access.

Inject the fault only after the baseline identities and hashes are recorded. Require the candidate to identify stale evidence before application. Ask for one live policy or Terraform test change and rerun promotion or recovery from a clean state.

Critical requirements:

- the applied or promoted identity must match reviewed evidence;
- state is never hand-edited, publicly retained, or used without verified ownership and locking assumptions;
- untrusted code cannot obtain release authority;
- container execution has explicit process, resource, filesystem, network, and privilege limits; and
- recovery and teardown retain required evidence while removing active resources.

## Review prompts

1. Which identity authorizes each build, plan, apply, promotion, and runtime action?
2. What does a Terraform plan prove, and how can it become stale?
3. What happens when state is unavailable but infrastructure still exists?
4. How does the reviewer prove that tested bytes are the promoted bytes?
5. Which isolation evidence comes from namespaces, cgroups, mounts, capabilities, and the host kernel?
6. What fails during one availability-zone loss, and which claim requires a real recovery test?
7. Which cost driver dominates at baseline and under the changed assumption?
8. What evidence would trigger rollback, state recovery, credential containment, or teardown?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and a complete identity chain from reviewed source and plan to artifact and target. Any unapproved cloud mutation, unbounded spend, exposed secret, state edit, or verification bypass is a Stop.

Rework uses a fresh plan or artifact identity. A stale-plan miss requires a new changed-configuration variant. State recovery gaps require a fresh disposable state copy. Supply-chain gaps require a new tampered artifact. Design gaps require recalculation under a changed failure-domain or cost constraint.

## Remediation

Return to [AWS identity and API](../../12-aws/01-identity-and-api.md), [artifacts and promotion](../../13-devops/04-artifacts-and-promotion.md), [Terraform state, plans, and drift](../../14-terraform/02-state-plans-drift.md), [Terraform recovery](../../14-terraform/06-drift-and-recovery.md), or [container debugging](../../15-containers/06-debugging.md). Repeat the bounded lab evidence before a fresh integrated assessment.
