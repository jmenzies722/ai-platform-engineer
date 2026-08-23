# Consistency and distributed invariants

Consistency is the application’s promise about what observations and decisions are allowed while copies, messages, and participants disagree.

## Why it matters

Replication and retries improve availability only when the design states which stale, duplicated, missing, or reordered effects are safe.

## How it works

Write the invariant first, then choose its serialization point. A local transaction can atomically check a precondition and record an effect. Optimistic concurrency uses a version to reject stale updates. Stronger coordination is justified when conflicting decisions would violate an important invariant; many displays and analytical views can tolerate bounded staleness.

Cross-system workflows cannot rely on an imaginary distributed transaction. Use a transactional outbox to atomically record local state and an event for later publication. Consumers record durable event identity with their effect so redelivery is harmless. Sagas coordinate compensatable steps, but compensation is a new business action, not a rewind of history.

Name guarantees precisely: read-your-writes, monotonic reads, bounded staleness, causal ordering, or linearizable decisions. CAP is about behavior during a network partition, not a menu where any two letters solve data design. “Exactly once” is usually an end-to-end property built from identity, atomicity, and deduplication.

## See it yourself

A quota starts at one. Two workers read one and both approve. Strongly consistent reads alone did not preserve the invariant because the check and decrement were separate. A conditional update from version 8 to 9 lets one commit and forces the other to reconsider. The protected unit is the decision, not the read.

## Where it shows up

An indexing workflow commits a source version and outbox record together. Repeated delivery may recompute an embedding, but activation uses a conditional source-version check. An obsolete worker cannot make an older projection current after a newer version has won.

## When it breaks

Dual writes diverge, timestamps are treated as global truth, consumers assume order across partitions, and retries duplicate irreversible effects. Reconstruct a single entity’s version history from transaction, outbox, broker offsets, consumer ledger, and projection. Repair only after identifying the invariant’s intended authority.

## Practice

**Build:** design document publication across a database, event broker, and search index. State invariants, transaction boundaries, event identity, ordering scope, deduplication, and repair. **Break:** lose a response, duplicate and reorder messages, and run two publishers concurrently. **Explain back:** name the serialization point for every protected decision.

## Check yourself

1. Why can a strongly consistent read still lead to a race?
2. What atomic boundary does an outbox create?
3. When is compensation unsafe or impossible?

## Sources

### REQUIRED

- [Google Cloud: Transactional outbox pattern](https://cloud.google.com/architecture/modern-transactional-stack)

### RECOMMENDED

- [AWS Prescriptive Guidance: Saga pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga.html)

### DEEP DIVE

- [Martin Kleppmann: Please stop calling databases CP or AP](https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html)

## Next

Continue to [Caching and derived state](06-caching-and-derived-state.md).
