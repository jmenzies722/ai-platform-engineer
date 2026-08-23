# Reconciliation, queues, and convergence

A reconciler is a level-based state machine: it repeatedly loads current intent, observes external reality, and performs a bounded idempotent action toward convergence. Queues schedule attention; events are hints, not the source of truth.

## Why it matters

Networks fail, workers restart, events duplicate or disappear, caches lag, and dependencies finish later. Correct controllers derive the next action from current state rather than trusting that every transition event arrives once and in order.

## How it works

A watch enqueues a stable resource key, not a complete event payload. Workers collapse duplicate keys, load the latest resource, verify authority, observe external state, compute a state-machine transition, perform at most a bounded side effect, update status, and requeue when more work or later observation is needed.

Partition errors into terminal intent errors, retryable dependency failures, conflicts requiring fresh state, and expected in-progress waits. Use exponential backoff with jitter for failures, explicit delayed requeue for polling, and periodic resynchronization as a repair net. Reset backoff after success.

Queue fairness and concurrency are correctness concerns in multitenant systems. Bound worker concurrency, per-provider calls, and per-tenant outstanding work. Apply backpressure before dependencies collapse. Dead-letter storage can preserve diagnosis, but a resource still needs actionable status and a defined replay policy.

Status writes and external side effects are not one transaction. Reconciliation must tolerate a crash between them by re-observing. Cache reads can improve scale, but mutation decisions that require fresh preconditions may need direct reads and optimistic concurrency.

## Vocabulary

- **level-based:** acting from current state rather than replaying every edge or transition
- **work queue:** scheduler holding resource keys needing reconciliation
- **backoff:** increasing delay after repeated failure
- **convergence:** desired and observed state becoming consistent within the contract

## See it yourself

Enqueue updates for size 20 and 30, then collapse both keys before a worker runs. Predict the result. The worker reads desired size 30 and converges there; processing the intermediate event is unnecessary. Now crash after provider resize but before status write. A safe retry observes size 30 rather than issuing a duplicate operation.

## Where it shows up

A certificate controller observes expiry and issuer status, requests renewal with stable identity, stores resulting reference, and requeues before the next deadline. Queue delay and issuer throttling appear as distinct conditions and metrics.

## When it breaks

Hot loops exhaust APIs, one noisy tenant starves others, stale cache data undoes new intent, and poison resources retry forever. A worker may appear healthy while oldest queue age grows. Distinguish throughput, depth, oldest age, reconcile duration, error class, retry count, and convergence lag.

## Practice

**Observe:** draw the state transitions and requeue source for one controller. Mark every side effect and crash window.

**Build:** write pseudocode for a bucket reconciler handling absent, creating, ready, drifted, deleting, denied, and provider-unavailable states.

**Break:** duplicate events, drop an event, crash after create, throttle the provider, and flood one tenant. Define expected queue and condition evidence for each.

**Say it out loud:** explain why queue delivery guarantees alone cannot make a controller correct.

## Check yourself

1. Why should queue items carry keys rather than complete resource snapshots?
2. When should a controller requeue without returning an error?
3. Which signals distinguish a poison item from broad provider failure?
4. How does level-based design tolerate lost events?

## Sources

### REQUIRED

- [Kubernetes controller pattern](https://kubernetes.io/docs/concepts/architecture/controller/)

### RECOMMENDED

- [client-go workqueue documentation](https://pkg.go.dev/k8s.io/client-go/util/workqueue)

### DEEP DIVE

- [Kubernetes controller-runtime FAQ](https://github.com/kubernetes-sigs/controller-runtime/blob/main/FAQ.md)

## Next

Continue to [Ownership, policy, and control-plane operations](03-ownership-and-operations.md).
