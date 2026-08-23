# Facilitator solution: Memory Exhaustion and OOM Kill

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Large images are decoded concurrently into unbounded native buffers. The cgroup reaches its 1 GiB limit and the kernel kills the process; node memory is not exhausted.

## Reasoning from evidence

1. Exit code 137 alone is ambiguous, but `lastState.reason=OOMKilled` and the kernel cgroup message identify the terminating mechanism.
2. The working set approaches the cgroup limit while request rate is flat, which contradicts a simple traffic-volume explanation.
3. Heap accounts for only part of RSS, so a heap-only diagnosis is incomplete. Payload correlation and native allocation profiling discriminate decoded buffers from cache growth.
4. The onset follows high-resolution uploads and small requests remain healthier, linking cost to request shape.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Inspect pod last state and cgroup events | OOMKilled and `oom_kill` increment | Container-limit breach |
| Compare node and container memory | Node healthy; container at limit | Not node-wide exhaustion |
| Replay one bounded large request with profiles | Native/RSS spike follows decode | Payload-driven native allocation |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Protect capacity first: cap expensive concurrency or request size, shed excess work, and drain affected pods one at a time. Raise limits only after validating node headroom and the service’s expected working set.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- No OOM kills or restart growth through two peak workload cycles
- Memory returns to a stable baseline after expensive requests
- Large and small request SLOs recover without node pressure

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Load-test representative payload sizes and concurrency
- Alert on working-set headroom and OOM events, not only node memory
- Continuously profile heap and native allocations
- Set request limits and admission controls from measured cost

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [Linux cgroup v2 memory controller](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory)
- [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Go diagnostics](https://go.dev/doc/diagnostics)
