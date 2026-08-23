# Facilitator solution: Retry Storm

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Three caller layers each retry immediately within similar 500 ms timeouts, multiplying requests and keeping the recovered catalog saturated.

## Reasoning from evidence

1. User traffic is flat while catalog traffic is about four times higher, proving internally generated load.
2. Logs show zero-delay retries and aligned timeout windows, explaining synchronized waves.
3. Catalog remained overloaded after its cache recovered; persistent queueing is therefore a consequence of amplified demand, not ongoing cache failure.
4. Retry ownership must be checked across layers because per-library attempt counts can understate total multiplication.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Tag requests with attempt and parent IDs | Most catalog calls are retries | Amplification source |
| Disable retries for a canary cohort | Success improves as offered load falls | Overload feedback |
| Inspect all calling layers | Gateway and client both retry | Multiplicative policy |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Disable or sharply cap retries for optional reads, enforce end-to-end deadlines, shed low-priority work, and restore traffic gradually with exponential backoff and jitter.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Downstream-to-original request ratio returns near one
- Queues drain and remain bounded
- Latency and success SLO recover without oscillation
- No caller layer independently re-amplifies requests

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Use capped exponential backoff with jitter
- Define one retry-owning layer and a retry budget
- Honor end-to-end deadlines
- Load-test dependency failure and recovery

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [AWS Builders Library: timeouts and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Google SRE overload handling](https://sre.google/sre-book/handling-overload/)
- [RFC 9110 Retry-After](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after)
