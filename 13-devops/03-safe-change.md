# Safe changes and recovery

Delivery safety comes from limiting blast radius, detecting harm quickly, and having a tested recovery path.

## Why it matters

No review or test suite proves a production change harmless. Systems differ in traffic, data, dependencies, and emergent behavior. Recovery speed therefore matters alongside change failure rate.

## How it works

Make changes small and backward-compatible. Use health checks before traffic, canaries or staged cohorts during exposure, and explicit success criteria. Observe user outcomes, not only process uptime. Stop automatically when guardrails fail.

Rollback is appropriate when old code can safely read current state. Database migrations and external side effects often make roll-forward safer: expand the schema, deploy compatible readers and writers, migrate data, then contract later. A kill switch can disable risky behavior while preserving the rest of the release.

Define guardrails before exposure: user error ratio, latency, correctness, saturation, business invariant, and cohort-specific impact. A canary must exercise representative dependencies and enough traffic to detect the risk under review. Progressive delivery advances through bounded cohorts only after a minimum observation window; automation pauses or restores traffic when thresholds fail.

Separate four recovery mechanisms. Rollback changes code or configuration to a previous compatible version. Roll-forward deploys a corrective version. Traffic shifting stops exposure without changing deployment. Data recovery restores or compensates state. Each has different prerequisites, time, and potential loss.

## See it yourself

For a column rename, compare an in-place rename with adding a new column, deploying readers that tolerate both, dual-writing with reconciliation, bounded backfill, switching reads, stopping old writes, and contracting later. Predict behavior for every adjacent version pair and for rollback at each stage. The longer sequence supports mixed versions and measurable convergence.

## Where it shows up

Feature flags, canary deployments, shadow reads, migration jobs, automated rollback, incident runbooks, and game days make recovery concrete. A payment release might expose read-only UI behavior widely while constraining money-moving paths to an internal cohort, with ledger invariants overriding generic availability metrics.

## When it breaks

Rollback procedures are untested, old artifacts have been deleted, flags become permanent, canaries receive unrepresentative traffic, or teams watch averages that hide a harmed cohort. Schema contraction invalidates old code. Queued work continues after traffic rollback. Automation amplifies failure without rate limits and stop conditions. A nominal recovery restores uptime while data remains wrong.

Preserve artifact and configuration identities, cohort assignment, guardrail windows, migration checkpoints, queue state, and user examples. Verify recovery with both technical SLIs and domain invariants.

## Practice

**Observe:** reconstruct one release's exposure cohorts, guardrails, decisions, and recovery eligibility from evidence.

**Build:** write a release plan for behavior plus schema change. Include version compatibility, migration checkpoints, exposure, representative traffic, guardrails, owner, and rollback, roll-forward, traffic, and data-recovery triggers.

**Break safely:** tabletop an error spike after dual writes begin and inject a canary failure in a sandbox. Completion means exposure stops automatically, reconciliation identifies divergent records, mixed versions remain compatible, and user recovery is verified.

## Check yourself

1. When is rollback unsafe?
2. What makes a canary representative enough to trust?

## Sources

### REQUIRED
- [Google SRE: Reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

### RECOMMENDED
- [DORA: Working in small batches](https://dora.dev/capabilities/working-in-small-batches/)

### DEEP DIVE
- [Google SRE: Emergency response](https://sre.google/sre-book/emergency-response/)

## Next

[Artifacts, registries, and promotion](04-artifacts-and-promotion.md)
