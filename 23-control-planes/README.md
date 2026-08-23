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

Complete the lessons in order, then run the failure-oriented design review in lesson 8. The capstone covers an API schema, reconcile state machine, queue policy, idempotency key, ownership and deletion protocol, version migration, tenant boundary, and tested recovery objectives.

## Ready to continue

You can specify and evolve a declarative resource, prove retry safety, diagnose non-convergence from evidence, preserve ownership and deletion safety, isolate tenants, and test whether the control plane meets stated freshness and recovery objectives.

## Next

Continue to [AI Foundations](../24-ai-foundations/README.md).
