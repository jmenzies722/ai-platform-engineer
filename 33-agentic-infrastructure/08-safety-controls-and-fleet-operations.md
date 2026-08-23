# Fleet reliability and recovery

Operating an agent fleet requires capacity isolation, versioned rollout, dependency-aware service objectives, and recovery that reconciles durable runs rather than merely restarting workers.

## Why it matters

At fleet scale, ordinary bursts, stuck runs, model or tool regressions, and shared dependency failures can exhaust queues or hide tenant impact. A healthy worker count says little about completed tasks or unresolved effects.

## How it works

Partition capacity by tenant, authority class, model, and tool dependency so low-consequence background work cannot consume reserves for interactive or reconciliation work. Admission charges expected model, tool, sandbox, and effect work against run and fleet budgets. Queue age and deadline feasibility matter more than depth alone. Retry ownership belongs to one layer under an end-to-end deadline.

Release identity binds model, prompt, tool schema, policy, evaluator, runtime, and sandbox image. Shadow runs cannot commit effects. Canaries use bounded authority and advance only after minimum samples and hard safety gates. Rollback restores a compatible complete release; durable runs either finish on their pinned version or pass an explicit migration with replay tests.

Fleet SLOs cover valid task completion, time to terminal state, stuck-run age, policy and tool availability, approval wait by service class, effect reconciliation age, cancellation acknowledgement, and cost per attempted and completed task. Dashboards preserve denominators for succeeded, failed, safely aborted, denied, cancelled, and needs-reconciliation outcomes. Alerts join user impact to saturation or dependency evidence.

Recovery is state repair. Replace failed workers, replay verified events under fenced ownership, query effect receipts, reissue only safe idempotent calls, and preserve runs whose outcome remains unknown. Resume traffic gradually while checking queue age, terminal-state mix, effect inventory, tenant fairness, and cost velocity. Human containment and kill-switch protocols are defined in the preceding lesson; fleet recovery consumes their audit evidence.

## See it yourself

Suppose arrival is 40 runs/s and healthy completion is 50 runs/s. A tool outage lowers completion to 20 runs/s for ten minutes, creating \((40-20)\times600=12{,}000\) queued runs. After recovery, spare drain capacity is only \(50-40=10\) runs/s, so draining takes at least 1,200 seconds while normal load continues. Restarting workers at minute ten does not restore latency; bounded admission and priority policy are required before the outage.

If one tenant contributes 75% of arrivals but has only 40% of reserved service, a global FIFO queue can let its backlog dominate everyone. Per-class scheduling and admission make the isolation claim testable: during overload, other tenants retain their declared minimum completion rate and bounded oldest age.

## Where it shows up

Operations dashboards segment tenant, authority, release, state, and dependency. Runbooks cover stuck runs, model regression, tool outage, policy outage, receipt backlog, cost surge, and tenant overload. The [queue-overload drill](../incidents/12-queue-overload/README.md) exercises backlog and recovery arithmetic; the [bad-rollout drill](../incidents/06-bad-rollout/README.md) exercises guarded rollback. Project evidence belongs in the [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md).

## When it breaks

A global queue hides class starvation, retries multiply a tool outage, rollout mixes incompatible event schemas, rollback strands pinned runs, and scale-down steals leases without fencing. Aggregate success can hide one tenant or authority class, while trace sampling can omit rare unresolved effects.

Diagnose from state age and flow: arrivals, admissions, transitions, terminals, retries, lease transfers, tool calls, approvals, receipts, and costs on one timeline. Check cohort and release digests before blaming the model. Recovery requires declining oldest age under continued demand, no growth in ambiguous effects, restored reserved service by class, and reconciled accounting.

## Practice

**Build:** create a bounded fleet simulation with two tenants, three priority classes, a finite queue, pinned release versions, worker leases, and one tool dependency. **Break:** halve tool capacity for ten simulated minutes, introduce a bad runtime canary, and retire a worker with active runs. **Prove:** queue memory stays bounded, protected classes retain reserved service, rollback does not mix incompatible state, stale workers cannot advance runs, and oldest age declines after recovery.

Complete [Lab 19](../labs/19-agent-runtime-safety/README.md) first, then expose its terminal states and audit outcomes as fleet counters. Keep simulation time, event count, and memory explicitly capped so the result is reproducible.

## Check yourself

1. Why does worker recovery not imply queue recovery?
2. Which dimensions require capacity isolation?
3. What proves a rollout rollback preserved durable-run compatibility?

## Sources

### REQUIRED

- [Google SRE: service level objectives](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### DEEP DIVE

- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

## Next

Continue to [Practical lab: simulate a durable agent runtime](09-practical-agent-runtime-lab.md).
