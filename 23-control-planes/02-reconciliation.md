# Reconciliation, queues, and convergence

A reconciler repeatedly observes one resource and moves external reality closer to declared intent.

## Why it matters

Networks fail, processes restart, events duplicate, and dependencies complete later. Correct controllers derive the next safe action from current state rather than trusting a one-time event sequence.

## How it works

A watch enqueues a resource key. Workers collapse duplicate keys, read the latest resource, observe external state, compute one bounded action, update status, and requeue when needed. The operation must be idempotent.

Use exponential backoff and jitter for transient errors, terminal conditions for invalid intent, and periodic resynchronization as a safety net. Level-based reconciliation uses current desired state; it need not process every intermediate event. Limit concurrency and API calls to protect dependencies.

## See it yourself

If events say size changed from 10 to 20 and then 30, a level-based controller reads current size 30 and converges there even if the first event was lost.

## Where it shows up

Kubernetes controllers, infrastructure operators, certificate managers, autoscalers, and account provisioning.

## When it breaks

Retries create duplicates, errors hot-loop, stale caches overwrite new intent, two controllers own the same field, or global scans overload an API.

## Practice

Write pseudocode for an idempotent bucket reconciler. Include already-exists, permission-denied, timeout, drift, and deletion cases.

## Check yourself

1. Why queue keys instead of complete event payloads?
2. What is eventual convergence?

## Sources

### REQUIRED
- [Kubernetes controller pattern](https://kubernetes.io/docs/concepts/architecture/controller/)

### RECOMMENDED
- [client-go workqueue documentation](https://pkg.go.dev/k8s.io/client-go/util/workqueue)

### DEEP DIVE
- [Kubernetes controller-runtime FAQ](https://github.com/kubernetes-sigs/controller-runtime/blob/main/FAQ.md)

## Next

[Ownership, policy, and control-plane operations](03-ownership-and-operations.md)
