# Platform Gate

This gate tests whether the learner can turn a researched user need into a safe, operable, evolvable self-service capability. It covers [platform engineering](../../21-platform-engineering/README.md), [developer platforms](../../22-developer-platforms/README.md), and [control planes](../../23-control-planes/README.md).

## Prerequisites

- Pass the [Kubernetes Reliability Gate](kubernetes-reliability.md).
- Complete [Design and Test a Reconciliation Control Plane](../../labs/14-platform-control-plane/README.md).
- Provide research, baseline journey evidence, and a narrow capability contract modeled on [Secure Developer Platform Control Plane](../../projects/09-developer-platform-control-plane/README.md).
- Be prepared to use only fictional tenants and fake adapters. No control-plane action may call a real source, cloud, CI, identity, or catalog system during the gate.

## Challenge

Choose one high-friction developer journey supported by interview or recorded usability evidence. Design and implement a local self-service control-plane slice in Python and SQLite that accepts a versioned declarative resource and reconciles it through fake repository, delivery, and environment adapters.

The implementation must include:

- authenticated, immutable tenant identity and object-level authorization;
- validation, idempotency, optimistic concurrency, desired and observed state, generation, and actionable conditions;
- a bounded work queue, level-based reconciliation, deterministic backoff, and explicit terminal status;
- external identity, ownership, deletion and finalizer behavior;
- append-only audit evidence, policy decisions, quotas, and an approved escape hatch;
- compatibility for one API evolution; and
- service SLOs, support ownership, adoption and task measures, and unit-cost assumptions.

The evaluator injects two faults, one correctness fault and one product or operating change:

- duplicate event, stale desired state, lost wake-up, adapter timeout, partial provisioning, revoked adapter identity, poison resource, or crash after side effect;
- tenant-crossing request, orphan deletion, incompatible API client, policy change, offboarding request, declining adoption, or support cost above the stated budget.

The candidate must prove convergence or precise terminal state, avoid duplicate external effects, protect tenant and deletion invariants, and revise the product or technical design in response to the changed evidence.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- user research synthesis, current and target journey, problem statement, non-goals, baseline measures, and selected outcome hypothesis;
- versioned API and status schemas, state and sequence diagrams, tenant and trust boundaries, policy matrix, adapter contracts, and deletion protocol;
- simulator source, database schema, deterministic fixtures, action and audit logs, idempotency receipt, newest-generation convergence proof, bounded retry proof, and tenant-isolation tests;
- compatibility and migration test, escape-hatch and offboarding procedure, SLO and runbook, support and ownership model;
- task completion, lead time, adoption or abandonment, support burden, and satisfaction evidence or a clearly marked synthetic evaluation plan; and
- unit-cost model, dominant cost driver, capacity bound, and stop-investing or deprecation trigger.

## Dimension requirements

- **Explain:** Explain platform as product, paved road versus mandate, desired versus observed state, level-based reconciliation, external identity, condition semantics, tenant ownership, and why API acceptance does not mean readiness.
- **Build:** Deliver a bounded deterministic controller with versioned contracts, fake adapters, policy and authorization, auditability, deletion safety, and compatibility tests.
- **Debug:** Diagnose non-convergence or duplicate-effect risk using queue, generation, condition age, retry, adapter, and audit evidence; handle the evaluator's fault without manual database repair.
- **Operate:** Use SLOs and actionable status, bound retries and poison work, execute safe override or offboarding, recover restart, and preserve audit and tenant boundaries.
- **Design:** Connect the capability to researched user value; defend contracts, tenancy, support, governance, evolution, economics, escape hatches, and deprecation under changed evidence.

## Evaluator instructions

Verify that the journey precedes the proposed interface. If no real interviews are available, provide synthetic transcripts and require the candidate to label that limitation; do not let invented research count as user validation.

Inject faults through fake adapter behavior or deterministic database fixtures. Require two reconciliations for idempotency and a restart between effect and status for duplicate protection. Ask for one live schema evolution or policy change. Inspect both user-facing status and operator evidence.

Critical requirements:

- tenant identity is server-derived and present in admission, storage, queue, adapter, status, and audit paths;
- repeated or interrupted reconciliation cannot duplicate a protected external effect;
- deletion cannot orphan an owned external resource or remove another tenant's resource;
- exhausted work becomes actionable and bounded rather than retrying forever; and
- product success is measured by user outcomes and operating cost, not resource count or portal use.

## Review prompts

1. Which researched friction justifies this capability, and what result would show that no platform investment is needed?
2. What is durable intent, what is observed state, and who owns each transition?
3. How does the system avoid duplicate effects after a crash between adapter success and status update?
4. How do generation and conditions prevent stale or falsely ready status?
5. What happens during deletion when an adapter is unavailable?
6. Where can tenant identity be lost, forged, or confused?
7. How is an exception approved, expired, audited, and removed?
8. What adoption, support, reliability, or cost evidence would change, deprecate, or stop the capability?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and a fresh interruption test that proves convergence or explicit terminal status. Design must score at least 2 from both product and control-plane evidence.

Rework for Build or Debug requires a new fault and event log. Tenancy or deletion gaps require adversarial tests before any rerun. Product gaps require new journey evidence or a narrower hypothesis. Evolution gaps require a working compatibility and migration test. Unsafe cross-tenant behavior is a Stop.

## Remediation

Return to [platform product practice](../../21-platform-engineering/01-platform-as-product.md), [self-service and tenancy](../../21-platform-engineering/04-self-service-and-tenancy.md), [developer workflows](../../22-developer-platforms/02-templates-and-workflows.md), [control-plane reconciliation](../../23-control-planes/02-reconciliation.md), or [ownership and deletion](../../23-control-planes/05-ownership-deletion-and-finalizers.md). Repeat the local control-plane lab with a new tenant and fault before reassessment.
