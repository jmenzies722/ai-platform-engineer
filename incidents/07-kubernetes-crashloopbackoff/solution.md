# Facilitator solution: Kubernetes CrashLoopBackOff

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

A ConfigMap update sets `PAYMENT_TIMEOUT=0`; the application intentionally exits during validation. Existing pods retain the old environment value until recreated.

## Reasoning from evidence

1. Exit code 1 and the application validation log show a process-controlled exit, not a liveness kill or OOM.
2. Only recreated pods fail because environment variables from a ConfigMap are captured at container start.
3. The ConfigMap change precedes replacement failures and comparison with healthy pod specs reveals the differing value.
4. CrashLoopBackOff is the kubelet’s restart backoff state, not the root cause.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Read `lastState.terminated` and previous logs | Exit 1 after config error | Application exit |
| Compare healthy and failing effective env | Timeout differs | Configuration boundary |
| Create one canary with restored revision | Starts and becomes ready | Mitigation validation |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Pause voluntary capacity reduction, restore the last valid configuration or deployment revision, and let the controller replace failed pods. Do not weaken probes when the process exits itself.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Desired and available replicas converge
- Restart counters stop increasing
- New pods pass startup and readiness checks
- Payments SLO remains healthy during resumed maintenance

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Validate configuration in CI and admission workflows
- Version configuration with deployments
- Alert on available replicas and restart rate
- Exercise replacement pods before node maintenance

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [Kubernetes pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes debugging applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
