# Reliability, scaling, and verification

Control-plane reliability is the ability to accept valid intent, preserve it, and converge within stated freshness objectives despite crashes, retries, skew, overload, and dependency failure. Verification must exercise state transitions and recovery, not only happy-path API calls.

## Why it matters

An API may return 200 while controllers are hours behind. Faster workers can amplify provider outages. Backups can restore bytes but lose external identity or encryption access. Unit tests rarely expose crash windows and queue unfairness.

## How it works

Define separate objectives for API availability and latency, accepted-write durability, observation freshness, convergence latency, deletion completion, and data-plane continuity. Measure distributions and oldest age by resource kind, tenant, and dependency. A resource-level condition explains local state; aggregate telemetry reveals systemic failure.

Scale from demand: event rate, resync volume, reconcile cost, provider quotas, cache size, and status-write amplification. Bound concurrency and rate at each dependency, shard by stable key when needed, and design leases or fencing so only the current worker performs side effects. Shed noncritical work before critical cleanup and safety actions.

Test the reconciler as a state machine. Use table and property tests for desired and observed combinations, idempotency under repeated calls, and invariants such as “never mutate an unowned external object.” Integration tests inject crashes around side effects, stale caches, conflicts, duplicate events, throttling, and version skew.

Back up durable intent, status when needed, audit evidence, keys, and schema metadata. Restore into an isolated environment, verify stable IDs and external correlation, then prove reconciliation does not duplicate, delete, or adopt the wrong resources. Run capacity and disaster exercises with explicit stop conditions.

## Vocabulary

- **convergence latency:** time from accepted intent to contract-satisfying observed state
- **fencing:** preventing stale workers or leaders from performing valid-looking writes
- **write amplification:** multiple storage writes caused by one logical change
- **invariant:** property that must hold across every valid transition

## See it yourself

Model 100,000 resources with a 10-minute global resync and 20-millisecond observation call. Predict minimum call demand: about 167 observations per second before event-driven work or retries. Compare provider quota and add jitter, incremental watches, and bounded resync. Arithmetic bounds load but does not model burst or tail latency.

## Where it shows up

During provider throttling, a database controller lowers concurrency, backs off with jitter, preserves delete priority, and reports degraded freshness. Existing databases continue serving. Recovery is complete only when oldest queue age and observed generations return within objective.

## When it breaks

Leader election lacks fencing, status updates trigger self-reconciliation loops, resync creates a thundering herd, and high-cardinality metrics overload telemetry. Restore reissues create calls because external IDs were omitted. Detect with queue age, work and retry rates, provider saturation, reconcile reasons, status-write ratio, leader transitions, and invariant violations.

## Practice

**Observe:** derive a capacity model from resource count, event rate, reconcile cost, resync, concurrency, and provider quota. Identify the first saturation point.

**Build:** define a test matrix for create, update, drift, delete, provider denial, timeout, crash, stale cache, conflict, duplicate event, and version skew. Attach an invariant and expected condition to each.

**Break:** run a paper game day with API outage, provider throttling, lost worker, and stale restore. State detection, automated response, operator decision, user impact, and recovery evidence.

**Design review:** specify a production database control plane: declarative API, desired and observed state, conditions, queue and state machine, idempotency, external identity, field ownership, finalizers, version evolution, tenant isolation, SLOs, capacity, backup, and failure tests. Reject any design whose retries can create an unowned duplicate.

## Check yourself

1. Why must API availability and convergence freshness have separate objectives?
2. When does adding workers reduce reliability?
3. Which invariants should survive every injected crash point?
4. What proves a restore is safe against existing external resources?

## Sources

### REQUIRED

- [Google SRE: Handling overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [Kubernetes controller pattern](https://kubernetes.io/docs/concepts/architecture/controller/)

### DEEP DIVE

- [Jepsen: Testing distributed systems](https://jepsen.io/)

## Next

Continue to [AI Foundations](../24-ai-foundations/README.md).
