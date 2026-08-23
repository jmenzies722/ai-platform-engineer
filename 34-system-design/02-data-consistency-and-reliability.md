# Data, consistency, and reliability

Data design chooses durable facts, ownership, and consistency guarantees; reliability design preserves the critical invariants when components fail.

## Why it matters

Replication and retries improve availability only when their effects on ordering, duplication, and stale reads are understood.

## How it works

Choose a data model from access patterns and invariants. Assign one authoritative owner per fact. Transactions preserve local invariants; asynchronous events propagate changes with lag. Idempotency, deduplication, timeouts, backoff, and circuit breaking bound distributed failure. Recovery objectives define acceptable data loss and restoration time.

Consistency is an application promise, not a database brand. Some reads may tolerate staleness; uniqueness or balance invariants may require serialized decisions. Events carry immutable identity and version so consumers can deduplicate and detect reordering. Timeout creates uncertainty, not cancellation: the remote effect may have committed even when the caller received no response.

## See it yourself

Send payment key `order-7`. If the server commits a charge then the response is lost, a retry without the key can charge twice. With a durable unique key, the server returns the first result. Crash before commit and retry safely creates one charge; crash after commit returns one existing charge. The exercise shows “exactly once” comes from durable identity and atomic effect recording.

## Where it shows up

An order service owns payment intent and publishes versioned events after transaction commit. Fulfillment consumes idempotently and records the processed event ID. A cache may serve stale display status, but authorization checks read an authoritative source. Different consistency choices follow different consequences.

## When it breaks

Dual writes diverge, retries amplify load, caches serve unsafe stale data, and backups have never been restored. First reconstruct one entity's timeline from request ID, idempotency key, transaction record, event offsets, and consumer state. Determine whether the invariant broke at commit, publication, delivery, or projection before replaying messages.

## Practice

**Build:** model a multi-step workflow with invariants, transaction boundaries, event identity, RPO, and RTO. **Break:** lose a response, duplicate and reorder an event, and restore a backup in a test environment. **Explain back:** show why timeout is ambiguous and where each invariant is enforced.

## Check yourself

1. Why is exactly-once usually an application property?
2. What does a transaction boundary protect?
3. How do RPO and RTO differ?

## Sources

### REQUIRED

- [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)

### RECOMMENDED

- [Amazon Builders' Library: timeouts and retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### DEEP DIVE

- [Designing Data-Intensive Applications resources](https://dataintensive.net/)

## Next

Continue to [Evolution and design review](03-evolution-and-design-review.md).
