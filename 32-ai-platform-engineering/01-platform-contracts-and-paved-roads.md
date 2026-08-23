# Platform contracts and paved roads

A platform contract defines what users request, what the platform guarantees, and where responsibility changes hands.

## Why it matters

Without a stable contract, every team learns infrastructure internals and every platform change becomes a migration crisis. A useful platform does not merely automate tickets. It turns repeated organizational decisions about identity, risk, ownership, reliability, and lifecycle into an interface that can be tested. That interface must be narrower and more durable than the implementation behind it.

## How it works

A paved road packages a common workflow behind a versioned API, templates, policy, and support. Its contract covers accepted intent, immutable identities, ownership, lifecycle states, service levels, compatibility, observability, and deletion. The API should expose properties users can reason about, such as latency class or rollback target, rather than scheduler flags that bind them to today's implementation.

Admission validates syntax, authorization, policy, and feasibility before recording desired state. A reconciler then drives observed state toward that intent and publishes conditions such as `Accepted`, `Ready`, or `Degraded`; an HTTP success only proves the request was recorded. Defaults encode safe, common choices, but the resolved configuration is recorded so a later default change cannot rewrite history. Idempotency keys prevent duplicate effects, optimistic concurrency prevents lost updates, and immutable artifact digests make rollback targets meaningful.

Compatibility is a claim bounded by tests. Additive optional fields can often remain backward compatible; changing default semantics, enum meaning, authorization, or status interpretation may not be. Maintain representative old clients, publish a support window, measure remaining consumers, provide conversion tooling, and delete the old path only after evidence shows migration. An escape hatch is a separate, registered contract: scope, owner, compensating controls, telemetry, expiry, and the responsibilities no longer carried by the platform. It is not an undocumented bypass.

## See it yourself

Compare two requests. The first supplies `image: latest`, no owner, and no limits. It may start, but cannot be reproduced, attributed, capacity-planned, or safely rolled back. The second supplies an image digest, model digest, owner, resource envelope, readiness rule, SLO class, and previous compatible digest. Assert that admission rejects the first with field-level reasons and records the second's resolved values. This demonstrates only that the control plane creates auditable preconditions; it does not prove the workload is semantically correct or will meet its SLO under representative load.

## Where it shows up

For model deployment, a team supplies artifact and runtime digests, traffic class, interface schema, owner, evaluation evidence, and rollback target. The platform generates workload identity, probes, policy checks, dashboards, capacity settings, and rollout stages. The platform owns execution reliability and policy enforcement; the model team owns intended prediction behavior and domain acceptance criteria; release approval is shared. This responsibility matrix prevents both platform overreach and application abandonment during incidents.

## When it breaks

Abstractions fail when status hides the first actionable cause, defaults become unsafe, synchronous APIs mask partial completion, mandatory roads cannot represent real workloads, or breaking semantic changes are labeled additive. Debug from the boundary inward: preserve request ID, authenticated principal, API version, desired generation, policy decision, controller attempts, dependency effects, and conditions. Distinguish rejection from stalled reconciliation and terminal failure. When users bypass the road, inspect journey traces, rejection reasons, and support cases. Repeated governed exceptions suggest a missing platform capability; one high-risk workload may remain intentionally unsupported. Adoption alone cannot distinguish either case.

## Practice

**Build:** write a minimal versioned deployment schema, state machine, compatibility test, and responsibility matrix. **Break:** submit mutable identity, absent ownership, a duplicate idempotency key, a stale update, and one legitimate unsupported workload. Record exact rejection, status, and exception evidence. **Explain back:** show how the contract hides replaceable implementation while preserving ownership, failure visibility, and migration obligations.

## Check yourself

1. What makes a contract stable?
2. Why provide escape hatches?
3. Which defaults should be policy?

## Sources

### REQUIRED

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [Kubernetes API deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

### RECOMMENDED

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

### DEEP DIVE

- [Team Topologies](https://teamtopologies.com/key-concepts)
- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

Continue to [Tenancy, governance, and cost](02-tenancy-governance-and-cost.md).
