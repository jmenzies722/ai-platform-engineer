# Leases, fencing, and effect reconciliation

Durable execution survives worker races and process failure by fencing ownership, recording effect intent, and reconciling uncertain external state instead of blindly replaying it.

## Why it matters

A lease alone does not stop a paused worker from resuming after its lease expires. A crash can also occur after a payment, message, or deployment commits but before acknowledgement. Retrying may duplicate harm; assuming success may lose work.

## How it works

Append sequence-numbered events for state transition, ownership, tool intent, authorization, approval, attempt, receipt, result, budget, and compensation. A worker acquires a time-bounded lease and a monotonically increasing fencing token. Every state write, effect dispatch, callback, and timer carries that token. The durable store and effect broker reject a token lower than the latest token observed for the run. Renewal extends time but does not change identity; transfer issues a higher token.

Each external effect receives an idempotency key stable across retries and derived from durable intent, never from attempt number. The external service stores the key or offers status lookup. On timeout, the run enters `RECONCILING`, queries by key, and records one of committed, not-found, failed, or unknown. Only a definitive not-found under the service contract permits retry. Unknown remains an explicit operator-visible state.

For multi-step work without a distributed transaction, a saga records forward effects and compensations. Compensation runs in reverse dependency order where required, with fresh authorization, idempotency keys, and receipts. It is a new business effect, not history deletion: a refund does not erase a charge, and a sent message may be impossible to retract. The workflow can end `COMPENSATED`, `PARTIALLY_COMPENSATED`, or `NEEDS_RECONCILIATION`, never falsely `ROLLED_BACK`.

Checkpoints accelerate replay but are verified projections, not the source of truth. Timers and callbacks are durable events. Resume reconstructs state, verifies sequence and ownership, reconciles pending effects, re-evaluates current policy, and only then asks a planner for another proposal.

## See it yourself

Worker A holds fencing token 41 and pauses. Its lease expires, so worker B acquires token 42 and advances the run. When A resumes, a conditional append with 41 is rejected because \(41<42\). Without enforcement by the state store and effect boundary, the token is merely a log field and proves nothing.

Enumerate one effect's crash windows. Before durable intent, replay has no effect to run. After intent but before dispatch, lookup returns not-found and dispatch is allowed. After the remote commit but before local receipt, lookup by stable key returns the committed receipt and dispatch is forbidden. After receipt, replay returns the stored result. If lookup is unavailable in the third window, the only safe automatic result is unknown. These cases prove that local persistence cannot create exactly-once external execution; the guarantee requires remote idempotency or authoritative reconciliation.

For a two-step saga, reserve inventory then create shipment. If shipment fails, releasing the reservation can compensate the first effect. If shipment succeeds but customer notification fails, cancelling shipment may already be impossible. A correct state records the committed shipment and failed notification rather than claiming atomic rollback.

## Where it shows up

Long-running research, deployment, and support agents wait across approvals, callbacks, outages, and worker replacement. Operators reconstruct which worker owns the run, which effect is pending, what the external ledger knows, and which compensations remain authorized. The [queue-overload drill](../incidents/12-queue-overload/README.md) exercises duplicate side-effect risk during replay.

## When it breaks

Lease expiry based on a worker's local clock, unenforced fencing, keys that change on retry, a deduplication window shorter than workflow lifetime, and non-authoritative status lookup all reopen duplication. Callbacks can arrive after cancellation, and compensation can fail or require new approval.

On ambiguity, freeze planner advancement and inspect the durable intent, latest fencing token, broker dispatch record, external receipt, callback identity, and compensation ledger. Do not repair by deleting an event or changing the key. Recovery means every intent has a known terminal effect state or remains explicitly assigned for reconciliation.

## Practice

**Build:** implement a local event store whose compare-and-append checks sequence and fencing token, plus a mock effect ledger keyed by durable intent. Add a two-effect saga with idempotent compensation. **Break:** pause a worker through lease transfer; crash before intent, after intent, after remote commit, and after receipt; fail the second forward effect and one compensation. **Prove:** stale token writes are rejected, each stable key has at most one committed remote effect, replay is deterministic, and every run ends in an accurate terminal or reconciliation state.

Extend [Lab 19](../labs/19-agent-runtime-safety/README.md) with these failure points, then carry the event, receipt, and compensation evidence into the [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md).

## Check yourself

1. Where must a fencing token be enforced to have meaning?
2. Why does an ambiguous remote result forbid blind retry?
3. Why is saga compensation not atomic rollback?

## Sources

### REQUIRED

- [AWS Builders' Library: idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [Temporal durable execution](https://docs.temporal.io/workflows)

### DEEP DIVE

- [Life beyond distributed transactions](https://queue.acm.org/detail.cfm?id=3025012)

## Next

Continue to [Human approval, escalation, and kill-switch operation](07-evaluation-and-trajectory-observability.md).
