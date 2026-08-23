# 23 — Control Planes

A control plane accepts intent, records state, and repeatedly coordinates external systems until observed reality converges or reports why it cannot.

## What you will learn

- Design declarative APIs with status, conditions, and stable contracts.
- Build idempotent reconciliation around queues and state machines.
- Handle ownership, deletion, policy, tenancy, and operational failure.

## Lessons

1. [Declarative APIs and desired state](01-declarative-apis.md)
2. [Reconciliation, queues, and convergence](02-reconciliation.md)
3. [Ownership, policy, and control-plane operations](03-ownership-and-operations.md)

## Practice

Model a `Database` resource on paper. Define desired fields, observed status, conditions, ownership, retry behavior, deletion semantics, and what happens when the provider is unavailable.

## Ready to continue

You can separate spec from status, write an idempotent reconcile loop, explain eventual convergence, and design cleanup that survives retries and partial failure.

## Next

Continue to [AI Foundations](../24-ai-foundations/README.md).
