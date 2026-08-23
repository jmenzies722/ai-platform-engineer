# Facilitator solution: GPU Out of Memory

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

The context limit increase allows eight 28k-token sequences on one GPU; key-value cache and prefill workspace exceed device memory. The evidence does not require a leak.

## Reasoning from evidence

1. The allocator reports only 1.14 GiB free before a 2 GiB request, directly establishing immediate capacity failure.
2. Failures correlate with long prompts and eight active sequences after the context-limit change.
3. A clean worker baseline returning to 61 GiB and repeated bounded tests staying stable argues against monotonic leakage.
4. Hardware faults generally surface through device health or Xid events; none are provided, so they remain a checked but unsupported hypothesis.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Measure memory by tokens and active sequences | Peak crosses capacity near observed cohort | Workload capacity |
| Restart and repeat bounded cycles | Baseline returns; no monotonic growth | Leak less likely |
| Inspect device health events | No Xid or retired-page change | Hardware fault unsupported |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Stop admitting work to the affected worker, reconcile in-flight request IDs, then restart it cleanly. Temporarily cap long-context concurrency based on measured peak memory.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Worker rejoins with expected baseline memory
- No duplicate or lost request outcomes
- Bounded long-context load completes without allocation failure
- Memory remains stable across repeated cycles

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Admission-control by estimated token memory
- Load-test context and concurrency combinations
- Track allocated, reserved, and non-framework GPU memory
- Use workload-aware scheduling and explicit limits

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [NVIDIA CUDA memory management](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html)
- [PyTorch CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html#cuda-memory-management)
- [NVIDIA GPU memory errors](https://docs.nvidia.com/deploy/xid-errors/index.html)
