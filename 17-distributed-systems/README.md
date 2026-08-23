# 17 — Distributed Systems

Once work crosses a network, delay, loss, duplication, reordering, and partial failure become normal conditions rather than edge cases.

## What you will learn

- Reason from uncertainty instead of assuming a global clock or instant failure detection.
- Use replication, quorums, and consensus with explicit guarantees.
- Build retry-safe, overload-aware request and message flows.

## Lessons

1. [Time, ordering, and partial failure](01-time-and-partial-failure.md)
2. [Replication, consistency, and consensus](02-replication-and-consensus.md)
3. [Retries, idempotency, and backpressure](03-retries-and-backpressure.md)

## Practice

For a payment request, write every outcome after the client times out. Design an idempotency record and state which component may retry, for how long, and under what load limit.

## Ready to continue

You can explain why a timeout is not proof of failure, compare quorum guarantees, and design bounded retries without creating duplicate work or a retry storm.

## Next

Continue to [Observability](../18-observability/README.md).
