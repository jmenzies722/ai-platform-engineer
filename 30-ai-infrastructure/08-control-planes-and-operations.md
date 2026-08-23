# Control planes and operational observability

An AI infrastructure control plane reconciles desired workloads and capacity while preserving enough identity and telemetry to explain every decision.

## Why it matters

Distributed failures span scheduler, node, device, network, storage, and job layers. Metrics without shared identity produce dashboards but not diagnosis.

## How it works

APIs accept immutable workload specifications with owner, artifacts, resources, topology, priority, and retry policy. Controllers use observed state and idempotent operations to converge. Admission rejects unsupported or unsafe intent before expensive allocation. Inventory controllers quarantine unhealthy resources; job controllers coordinate launch, progress, checkpoint, and termination.

Events carry workload, attempt, rank, node, device, dataset, checkpoint, and policy-decision identifiers. Golden signals include queue age, scheduling failures, useful utilization, step progress, collective tails, data stalls, checkpoint success, hardware errors, and repair backlog. SLOs cover both user journeys and control-plane convergence.

## See it yourself

If 64 ranks heartbeat but step number has not changed for 20 minutes, liveness is true and progress is false. If one rank's input wait precedes all peers entering a collective wait, the first causal anomaly is input, not network. An aligned event sequence supports that conclusion; aggregate averages do not.

## Where it shows up

An operator starts with a job ID, follows its admission and placement decisions, compares rank timelines, resolves node and fabric health, and verifies the last durable checkpoint. Runbooks encode this path and preserve evidence before retries.

## When it breaks

Controllers fight over ownership, retries duplicate workers, stale inventory admits bad devices, and unbounded cardinality overwhelms telemetry. Audit controller writes, use generations and finalizers, cap retries, and separate high-cardinality traces from aggregate metrics. A kill switch must stop new admission even when workload systems are degraded.

## Practice

**Observe:** reconstruct a stalled step from cross-layer events. **Build:** define a desired-state schema and reconciliation table. **Break:** deliver duplicate events, stale health, and partial controller failure. Completion requires convergence without duplicate work and an evidence-preserving incident timeline.

## Check yourself

1. Why are heartbeats insufficient for job health?
2. Which identity joins scheduler and collective evidence?
3. What prevents two controllers from repeatedly undoing each other?

## Sources

### REQUIRED

- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)

### RECOMMENDED

- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)

### DEEP DIVE

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

## Next

Continue to [Practical lab: simulate an accelerator cluster](09-practical-ai-infrastructure-lab.md).
