# Facilitator solution: Inference Latency Regression

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Scheduler revision 19 increases maximum batching wait from 20 ms to 200 ms and allows deeper queues, optimizing throughput at the expense of interactive first-token latency.

## Reasoning from evidence

1. Stable inter-token latency and unchanged model digest argue against decode or weight regression.
2. Trace decomposition places the increase in queue time; prefill remains small.
3. The scheduler revision and batch-wait change precede the SLO breach while GPU utilization barely changes.
4. A controlled canary with the prior wait setting tests causality without assuming correlation.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Compare trace stages by revision | Queue delta explains most regression | Scheduler boundary |
| Canary prior batch-wait setting | First-token latency recovers | Configuration causality |
| Compare model digest and decode rate | Unchanged | Model and GPU less likely |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Restore the prior batch-wait configuration for interactive traffic, canary it on one server, and preserve a separate throughput-optimized class for offline requests.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- First-token latency returns within SLO by prompt cohort
- Queue wait is bounded
- Inter-token latency and error rate remain healthy
- Required throughput and cost guardrails hold

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Track stage-level inference latency
- Canary scheduler configuration with interactive traffic
- Separate latency and throughput classes
- Replay representative prompt-length distributions

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [NVIDIA Triton dynamic batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)
- [Google SRE latency](https://sre.google/sre-book/monitoring-distributed-systems/)
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)
