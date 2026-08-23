# 23 — Control Planes

A control plane accepts durable intent, records desired and observed state, and repeatedly coordinates external systems until reality converges or the API reports an actionable reason it cannot.

## What you will learn

- Design evolvable declarative APIs with precise desired and observed state.
- Build idempotent, level-based reconciliation around queues and external identity.
- Engineer ownership, deletion, multitenancy, scaling, and recovery as correctness concerns.

## Lessons

1. [Declarative APIs and desired state](01-declarative-apis.md)
2. [Reconciliation, queues, and convergence](02-reconciliation.md)
3. [Ownership, policy, and control-plane operations](03-ownership-and-operations.md)
4. [Idempotency and external identity](04-idempotency-and-external-identity.md)
5. [Ownership, deletion, and finalizers](05-ownership-deletion-and-finalizers.md)
6. [API evolution and compatibility](06-api-evolution-and-compatibility.md)
7. [Multitenancy and security boundaries](07-multitenancy-and-security.md)
8. [Reliability, scaling, and verification](08-reliability-scaling-and-verification.md)

## Practice

1. Complete the lessons in order, then build the [platform control-plane lab](../labs/14-platform-control-plane/README.md). Preserve the API contract, desired and observed state, status conditions, deterministic action log, idempotency proof, newest-generation convergence proof, tenant-isolation tests, and bounded dead-letter behavior.
2. Run the failure-oriented design review in lesson 8 against those artifacts. Cover queue policy, external identity, ownership and deletion, version migration, tenant boundaries, freshness, recovery objectives, and the conditions that require manual intervention.
3. Attempt the [retry storm](../incidents/08-retry-storm/README.md) and [queue overload](../incidents/12-queue-overload/README.md) incidents before reading their solutions. Revise retry ownership, admission, fairness, queue-age signals, and replay safety from the evidence.
4. Implement milestone 2 of the [Secure Developer Platform Control Plane project](../projects/09-developer-platform-control-plane/README.md), then carry the incident-derived controls into its partial-failure drills. Project evidence must show convergence or a precise actionable terminal condition under duplicate, delayed, stale, and interrupted work.

## Ready to continue

You can specify and evolve a declarative resource, prove retry and replay safety, diagnose non-convergence and overload from queue and status evidence, preserve ownership and deletion safety, isolate tenants, and verify stated freshness and recovery objectives under injected failure.

## Next

Continue to [AI Foundations](../24-ai-foundations/README.md).
