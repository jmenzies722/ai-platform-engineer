# 17 — Distributed Systems

Distributed systems engineering begins where local certainty ends: messages are delayed or duplicated, clocks disagree, processes pause, and only part of the system may fail.

## What you will learn

- Reason precisely about time, causality, partial failure, and consistency.
- Choose replication, consensus, and transaction mechanisms from required guarantees.
- Design duplicate-safe request and queue paths that remain bounded under overload.
- Operate distributed workflows by testing partitions, lag, retries, and recovery.

## Lessons

1. [Time, causality, and partial failure](01-time-and-partial-failure.md)
2. [Consistency models and client guarantees](02-consistency-models.md)
3. [Replication, quorums, and repair](03-replication-and-quorums.md)
4. [Consensus, leadership, and membership](04-consensus-and-membership.md)
5. [Transactions, sagas, and the outbox](05-distributed-transactions.md)
6. [Idempotency, retries, and uncertain outcomes](06-idempotency-and-retries.md)
7. [Queues, flow control, and backpressure](07-queues-and-backpressure.md)

## Practice

Complete [expose duplicate work and overload](lab-failure-harness.md). Keep the prediction, baseline, injected failure, diagnostic evidence, correction, and production decision as an operator's record.

## Ready to continue

You can explain the guarantees and limits in this module, calculate the small bounds that govern production behavior, design a controlled failure, diagnose it from evidence, and operate the mechanism with explicit ownership and recovery.

## Next

Continue to [Observability](../18-observability/README.md).
