# Serving platform architecture

A serving platform offers a stable deployment contract while owning placement, rollout, routing, capacity controls, and operational evidence.

## Why it matters

Without a platform boundary, every model team rebuilds risky gateways and autoscaling; with an overreaching boundary, the platform becomes responsible for prediction semantics it cannot judge.

## How it works

The deployment contract names immutable model and runtime artifacts, interface schema, owner, traffic class, SLO, resource envelope, data policy, evaluation evidence, and rollback target. The platform validates, provisions identity, loads replicas, runs readiness, configures routes, shifts traffic, meters usage, and emits standard telemetry.

Responsibility is explicit: the platform owns execution reliability and policy enforcement; model teams own intended behavior and domain acceptance criteria; both own release decisions. Versioned APIs and migrations preserve compatibility. Exceptions are registered, time bounded, observable, and supported by named owners.

## See it yourself

A request specifies `model: latest` and a 100 ms SLO but no tokenizer, hardware, or load profile. The platform cannot reproduce the artifact or prove capacity. Requiring digests plus representative workload turns vague intent into a testable contract.

## Where it shows up

A paved road generates canary stages, admission budgets, dashboards, alerts, and rollback from one declaration. Policy blocks unapproved data egress or missing evaluation before traffic.

## When it breaks

Abstractions hide critical tuning, default quotas starve real workloads, ownership is ambiguous during incidents, and rollback targets are incompatible. Diagnose contract rejection and journey telemetry before adding bypasses. Treat repeated exceptions as product evidence.

## Practice

**Observe:** create a responsibility matrix. **Build:** specify a versioned deployment API and validation rules. **Break:** submit mutable identity, impossible SLO, and legitimate unsupported hardware. Completion requires useful rejection messages and a governed exception.

## Check yourself

1. Which serving properties belong to user intent?
2. Who owns semantic correctness?
3. What makes an escape hatch governable?

## Sources

### REQUIRED

- [KServe concepts](https://kserve.github.io/website/latest/modelserving/)

### RECOMMENDED

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### DEEP DIVE

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

## Next

Continue to [Evaluation, lineage, and release governance](07-evaluation-lineage-and-release-governance.md).
