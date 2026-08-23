# Facilitator solution: Bad Rollout

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

The new release rounds percentage discounts before converting to integer minor units for zero-decimal currencies, producing incorrect JPY totals.

## Reasoning from evidence

1. The invariant failure is isolated to version `.4`; `.3` processes equivalent traffic correctly.
2. The example differs by one minor unit and is specific to JPY, matching a rounding-order defect rather than infrastructure failure.
3. Normal latency explains why rollout health analysis passed: it omitted correctness signals.
4. Replaying the captured input against both immutable versions provides a causal test before full rollback completes.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Replay redacted request against both versions | Only `.4` returns 1087 | Version causality |
| Compare currency cohorts | Zero-decimal currencies affected | Rounding scope |
| Inspect artifact diff and unit test | Rounding moved before minor-unit conversion | Mechanism |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Halt progression, route new traffic to the last known-good version, then roll back using the normal deployment mechanism. Preserve request IDs for transaction reconciliation.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- All serving instances report the known-good digest
- Invariant failures cease for the affected path
- Representative JPY transactions produce expected minor units
- Impacted orders are enumerated and reconciled

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Analyze business invariants in canaries
- Segment canary traffic across critical currencies and features
- Use immutable artifact digests and version labels
- Automate transaction reconciliation for pricing anomalies

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [Kubernetes deployment rollouts](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
- [Google SRE canarying releases](https://sre.google/workbook/canarying-releases/)
- [ISO 4217 currency codes](https://www.iso.org/iso-4217-currency-codes.html)
