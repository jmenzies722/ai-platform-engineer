# Safe changes and recovery

Delivery safety comes from limiting blast radius, detecting harm quickly, and having a tested recovery path.

## Why it matters

No review or test suite proves a production change harmless. Systems differ in traffic, data, dependencies, and emergent behavior. Recovery speed therefore matters alongside change failure rate.

## How it works

Make changes small and backward-compatible. Use health checks before traffic, canaries or staged cohorts during exposure, and explicit success criteria. Observe user outcomes, not only process uptime. Stop automatically when guardrails fail.

Rollback is appropriate when old code can safely read current state. Database migrations and external side effects often make roll-forward safer: expand the schema, deploy compatible readers and writers, migrate data, then contract later. A kill switch can disable risky behavior while preserving the rest of the release.

## See it yourself

For a column rename, compare an in-place rename with adding a new column, dual-writing temporarily, backfilling, switching reads, and removing the old column later. The longer sequence supports mixed versions.

## Where it shows up

Feature flags, canary deployments, migration jobs, automated rollback, incident runbooks, and game days all make recovery concrete.

## When it breaks

Rollback procedures are untested, flags become permanent, canaries receive unrepresentative traffic, or teams watch averages that hide a harmed cohort. Automation can amplify failure when it lacks rate limits and stop conditions.

## Practice

Write a release plan for a behavior plus schema change. Include compatibility, exposure steps, guardrails, decision owner, and rollback or roll-forward triggers.

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

[Terraform](../14-terraform/README.md)
