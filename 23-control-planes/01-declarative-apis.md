# Declarative APIs and desired state

A declarative API records what a user wants and lets a control plane determine repeatable steps toward that outcome.

## Why it matters

Imperative provisioning scripts lose progress and intent when interrupted. A durable resource model supports retries, observation, policy, and many independent clients.

## How it works

Design a resource with stable identity, desired `spec`, controller-owned `status`, and conditions containing type, state, reason, message, and observed generation. Default and validate inputs at admission. Make updates explicit about mutability; replacing an immutable field may require a new external object.

Use optimistic concurrency to prevent lost updates. APIs should support idempotent create and delete, pagination, and clear error semantics. Version contracts and provide conversion or migration rather than silently changing meaning.

## See it yourself

Model `Database.spec.size` and `Database.status.endpoint`. Users choose capacity; the provider-derived endpoint belongs in status. A `Ready=False` condition can report provisioning without changing intent.

## Where it shows up

Kubernetes resources, cloud APIs, GitOps systems, deployment platforms, and managed database services.

## When it breaks

Status becomes an input, fields mix desired and observed data, names are reused before deletion completes, or clients must know provider-specific workflow order.

## Practice

Design create, resize, and delete semantics for a database resource, including immutable fields and condition reasons.

## Check yourself

1. Why should endpoint data usually live in status?
2. What does observed generation protect against?

## Sources

### REQUIRED
- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### RECOMMENDED
- [Kubernetes API concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/)

### DEEP DIVE
- [CNCF Operator whitepaper](https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## Next

[Reconciliation, queues, and convergence](02-reconciliation.md)
