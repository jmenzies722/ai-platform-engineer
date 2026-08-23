# Durable execution and effect reconciliation

Durable execution survives process failure by recording intent and reconciling uncertain external effects instead of blindly replaying them.

## Why it matters

A crash can occur after a payment, message, or deployment commits but before acknowledgement. Retrying may duplicate harm; assuming success may lose work.

## How it works

Append sequence-numbered events for state transitions, tool intent, authorization, approval, attempt, result, and budget. Each effect receives an idempotency key stable across retries. The external service stores that key or offers status lookup. On timeout, the run enters an ambiguous state and queries the effect ledger before retry.

Checkpoints accelerate replay but are verified projections, not the source of truth. Leases with fencing tokens prevent stale workers from committing. Timers and callbacks are durable events. Compensation is a new authorized effect, not deletion of history, and cannot guarantee reversal of every consequence.

## See it yourself

Record intent `k7`, execute a mock charge, then crash before result storage. On resume, lookup `k7` returns the committed result, so no second charge occurs. If lookup is unavailable, transition to `NEEDS_RECONCILIATION`; do not guess.

## Where it shows up

Long-running research, deployment, and support agents wait across approvals and callbacks. Operators can reconstruct exactly which effect is pending and why.

## When it breaks

Keys change on retry, external systems ignore deduplication, stale workers write after lease loss, events arrive out of order, and compensation is mistaken for rollback. Validate monotonic sequence, fencing token, effect status, and current policy before advancing.

## Practice

**Observe:** enumerate every crash window around an effect. **Build:** implement event replay, leases, idempotency, timers, and reconciliation. **Break:** crash before intent, after intent, after effect, and after acknowledgement. Completion requires exactly one effect or an explicit ambiguous terminal state.

## Check yourself

1. Why is exactly-once execution generally not a local guarantee?
2. What does a fencing token prevent?
3. When is compensation impossible?

## Sources

### REQUIRED

- [AWS Builders' Library: idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [Temporal durable execution](https://docs.temporal.io/workflows)

### DEEP DIVE

- [Life beyond distributed transactions](https://queue.acm.org/detail.cfm?id=3025012)

## Next

Continue to [Evaluation and trajectory observability](07-evaluation-and-trajectory-observability.md).
