# Facilitator solution: Database Deadlock

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Each transfer locks its source account then destination. Simultaneous 42-to-17 and 17-to-42 transfers create a cycle.

## Reasoning from evidence

1. SQLSTATE 40P01 and PostgreSQL’s two-process cycle establish an actual deadlock, not merely contention.
2. The onset with opposite-direction parallel work narrows the statements to account updates.
3. Mapping process statements shows reversed lock order. Either transaction alone succeeds, but together each waits on the other.
4. The database aborts one transaction to restore progress; application handling must treat that transaction as fully failed unless commit outcome is uncertain.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Capture deadlock graph and statements | Two sessions lock accounts in reverse order | Cycle mechanism |
| Reproduce with controlled opposite transfers | 40P01 occurs under interleaving | Causal reproduction |
| Lock rows by sorted account ID | Concurrent test completes | Ordering fix |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Pause the triggering parallel batch, let PostgreSQL abort deadlock victims, and retry only idempotent whole transactions with bounded jitter after confirming request identity.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Deadlock counter stops increasing
- All transfer request IDs have exactly one committed outcome
- Latency returns to baseline
- Opposite-direction concurrency test completes

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Acquire account locks in stable account-ID order
- Keep transactions short
- Make retries idempotent and bounded
- Capture deadlock details with privacy controls

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [PostgreSQL explicit locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
- [PostgreSQL error codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
