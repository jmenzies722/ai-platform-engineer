# Facilitator solution: Database Pool Exhaustion

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

The new streaming export holds a database connection until the client consumes the entire response and fails to release promptly on disconnect, exhausting the application pool.

## Reasoning from evidence

1. Fast queries and moderate database CPU contradict general database saturation.
2. The application pool is exactly at max with a large pending queue, identifying acquisition as the immediate bottleneck.
3. Timing and route attribution connect the change to exports; cancellation logs suggest the cleanup path deserves testing.
4. More connections could briefly reduce waiting but would increase database concurrency and preserve the ownership bug.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Measure hold time by route | Exports hold connections for minutes | Long ownership |
| Disconnect a canary export | Connection remains checked out | Cancellation leak |
| Inspect server activity | Mostly idle or streaming sessions; low query latency | Not query saturation |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Stop or limit new streaming exports, rollback the faulty release if safe, and allow healthy requests to regain pool access. Cancel only identified export sessions using the normal cancellation path.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Pool pending returns to zero with healthy idle reserve
- Normal routes meet latency SLO
- Database connections and lock waits remain below limits
- Cancelled requests release connections promptly

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Scope connection and transaction lifetimes explicitly
- Test client cancellation and streaming backpressure
- Use per-workload concurrency limits
- Alert on pool wait and connection hold time by route

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [PostgreSQL monitoring statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL client connection defaults](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- [Google SRE overload handling](https://sre.google/sre-book/handling-overload/)
