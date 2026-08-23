# Platform contracts and paved roads

A platform contract defines what users request, what the platform guarantees, and where responsibility changes hands.

## Why it matters

Without a stable contract, every team learns infrastructure internals and every platform change becomes a migration crisis.

## How it works

A paved road packages common workflows behind versioned APIs, templates, and policy. Contracts cover inputs, ownership, SLOs, compatibility, observability, and support. Escape hatches are explicit and costly enough to preserve incentives without blocking legitimate exceptions.

The contract separates intent from implementation: users request a deployment with resource and risk properties; the platform chooses controllers and infrastructure. Defaults encode the common safe choice, while validation rejects states the platform cannot support. Versioning and deprecation preserve existing consumers. An escape hatch transfers named responsibilities rather than granting an undocumented bypass.

## See it yourself

Submit `image:latest` with no owner or limits to a minimal container API; it can start, but cannot be attributed, capacity-planned, or reproduced. A stronger contract requires immutable digest, owner, readiness, resource bounds, model identity, and rollback. Validation should reject the first and accept a complete request. This proves the interface creates operational evidence before deployment.

## Where it shows up

For model deployment, a team supplies artifact digest, traffic class, SLO, and owner. The platform generates probes, policy checks, telemetry, and rollout stages. Teams do not need scheduler internals, but remain responsible for prediction semantics. The responsibility matrix prevents both platform overreach and application abandonment.

## When it breaks

Abstractions leak, defaults become unsafe, mandatory roads cannot meet real needs, and breaking changes are hidden. When users bypass a road, first inspect failed journey steps, support evidence, and contract rejections by reason. Repeated exceptions reveal a missing capability; isolated unsupported risk may justify a maintained exception. Do not infer laziness from adoption alone.

## Practice

**Build:** write and validate a minimal versioned deployment API with a responsibility matrix. **Break:** submit mutable identity, absent ownership, and a legitimate unsupported workload; record rejection and exception behavior. **Explain back:** show how the contract hides implementation without hiding responsibility or failure.

## Check yourself

1. What makes a contract stable?
2. Why provide escape hatches?
3. Which defaults should be policy?

## Sources

### REQUIRED

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### RECOMMENDED

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

### DEEP DIVE

- [Team Topologies](https://teamtopologies.com/key-concepts)

## Next

Continue to [Tenancy, governance, and cost](02-tenancy-governance-and-cost.md).
