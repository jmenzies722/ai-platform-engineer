# Facilitator solution: Queue Overload

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Promotion ingress exceeds consumer capacity; downstream 429 retries consume 38 percent of attempts, reducing useful egress and accelerating backlog growth.

## Reasoning from evidence

1. Ingress is twice useful egress, so backlog must grow even with a healthy broker.
2. No offline or under-replicated partitions weakens a broker-failure hypothesis.
3. Consumer logs show downstream rate limiting and retries; scaling consumers without quota would increase rejected attempts rather than useful throughput.
4. Oldest age proves user delay more directly than depth and must fall continuously during recovery.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Compute successful service rate | About 9k/s versus 18k/s ingress | Capacity deficit |
| Segment lag and retries by partition/type | Broad lag; retry-heavy fulfillment calls | Not one poison partition |
| Canary higher consumer count within quota | 429 rises without useful egress gain | Downstream bottleneck |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Apply admission controls to nonessential producers, honor downstream rate limits, isolate priority classes where ordering permits, and raise consumer capacity only to a measured downstream-safe rate.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Ingress remains below sustainable successful egress
- Oldest-message age and depth decline predictably
- Retry and dead-letter rates normalize
- Sampled orders have exactly-once business outcomes

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Capacity-plan from arrival and service distributions
- Alert on oldest age and growth rate, not depth alone
- Use idempotent consumers and bounded retries
- Isolate workload classes and document shedding policy

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [Apache Kafka monitoring](https://kafka.apache.org/documentation/#monitoring)
- [RabbitMQ queue length](https://www.rabbitmq.com/docs/queues#queue-length)
- [Google SRE handling overload](https://sre.google/sre-book/handling-overload/)
