# Incident Drill Academy

This academy contains evidence-first incident simulations and facilitator
solutions. Every drill forces diagnosis from incomplete symptoms. Do not open a
scenario's `solution.md` until you have written hypotheses, named falsifying
evidence, and chosen a safe mitigation.

All names, addresses, identifiers, logs, and metric values are synthetic. Never
put credentials, customer data, or production logs in an exercise.

## Scenario inventory

| Incident | Difficulty | Focus |
|---|---:|---|
| [DNS resolution failure](01-dns-failure/README.md) | Starter | Resolver path, caching, boundary isolation |
| [Memory exhaustion and OOM kill](02-oom/README.md) | Intermediate | Linux memory pressure, cgroups, heap growth |
| [Disk exhaustion](03-disk-exhaustion/README.md) | Intermediate | Capacity, inodes, deleted-open files |
| [TLS certificate expiry](04-tls-expiry/README.md) | Intermediate | Certificate paths, time, renewal |
| [Database pool exhaustion](05-database-pool-exhaustion/README.md) | Advanced | Connection ownership, transactions, backpressure |
| [Bad rollout](06-bad-rollout/README.md) | Intermediate | Canaries, version correlation, rollback |
| [Kubernetes CrashLoopBackOff](07-kubernetes-crashloopbackoff/README.md) | Intermediate | Pod lifecycle, probes, configuration |
| [Retry storm](08-retry-storm/README.md) | Advanced | Backoff, retry budgets, load amplification |
| [Database deadlock](09-deadlock/README.md) | Advanced | Lock graphs, transaction ordering, retries |
| [Inference latency regression](10-inference-latency/README.md) | Advanced | Model serving, batching, queueing |
| [GPU out of memory](11-gpu-oom/README.md) | Advanced | Accelerator memory, fragmentation, workload shape |
| [Queue overload](12-queue-overload/README.md) | Advanced | Backlog, consumer capacity, age-based SLOs |

## Academy method

1. Assign an incident commander, investigator, operations lead, and scribe.
2. Start from user-visible impact and build a timestamped timeline.
3. Separate observations from interpretations.
4. Rank at least three hypotheses by explanatory power, likelihood, and test
   cost.
5. Test across system boundaries and preserve contradicting evidence.
6. Reduce impact with the smallest reversible action.
7. Prove recovery from the user's perspective and through subsystem signals.
8. Compare with `solution.md`; score the reasoning, not whether the final cause
   matched.

## Facilitation

- Reveal evidence in timeline order for a live drill, or provide the whole
  scenario for self-study.
- Require a rollback trigger before every mitigation.
- Inject a decision point whenever the team proposes a broad restart, capacity
  increase, disabled validation, or destructive cleanup.
- End with owned prevention actions and measurable acceptance criteria.

## Completion rubric

| Dimension | Complete when |
|---|---|
| Impact | Scope, severity, and affected user journey are explicit |
| Evidence | Claims cite observations and account for contradictions |
| Diagnosis | Tests discriminate among plausible causes |
| Mitigation | Blast radius, reversibility, owner, and rollback trigger are stated |
| Recovery | User, service, and dependency signals remain healthy for a relevant cycle |
| Learning | Prevention addresses the causal mechanism and is objectively testable |

Use [the repository incident template](../templates/INCIDENT.md) for additional
scenarios.
