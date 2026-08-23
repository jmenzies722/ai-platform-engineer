# Evolution and design review

A design is complete only when it explains how the system enters production, coexists with what is already there, proves itself, and can be removed.

## Why it matters

Most architectural risk lives in migration and operation, while many reviews spend their attention on the clean target-state diagram.

## How it works

Plan compatibility before rollout. Expand readers to accept old and new forms, introduce versioned writers, backfill with checkpoints, compare results, switch authority with explicit evidence, and contract only after the compatibility window closes. Every phase needs owner, entry and exit criteria, observability, rollback semantics, and stop conditions.

Dual writes across independent systems are not atomic. Declare the source of truth, capture repairable intent, reconcile continuously, and know what rollback will do with data written in the new form. Shadow traffic tests behavior without user authority; canaries limit exposure; feature controls separate deployment from release. Neither replaces data compatibility.

A serious design review begins with requirements, invariants, assumptions, and decision request. Review alternatives, capacity, failure modes, security, privacy, operability, cost, migration, ownership, and deletion. Classify comments as correctness blockers, risk acceptance, evidence requests, or preferences. Record the decision, dissent, owner, and revisit trigger.

## See it yourself

To replace an embedding model, write new vectors into a versioned index while old retrieval remains authoritative. Compare quality, latency, coverage, and cost on shadow queries. Canary routing by tenant only after coverage is complete. Rollback changes the active index pointer; cleanup waits until replay and audit windows close.

## Where it shows up

Database field changes, API deprecations, queue repartitioning, identity migration, and model upgrades all require coexistence. A review packet makes the dangerous middle states visible and prevents “we can roll back” from surviving without a tested mechanism.

## When it breaks

Migrations break when old readers see new data, backfills race with writes, comparison excludes failures, rollback cannot interpret new state, or temporary adapters have no removal owner. Freeze destructive cleanup, identify authority, quantify divergence, and repair forward or back from preserved evidence.

## Practice

**Build:** write an expand-and-contract plan for an embedding-model migration with compatibility matrix, phases, reconciliation, quality gates, rollback, and deletion. **Break:** fail five percent of dual writes and roll back after new-only data exists. **Explain back:** lead a review that distinguishes blockers, accepted risks, and preferences.

## Check yourself

1. Why does deployment rollback not guarantee data rollback?
2. What evidence permits authority to switch?
3. Which design-review comments require an accountable risk owner?

## Sources

### REQUIRED

- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)

### RECOMMENDED

- [Kubernetes API deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

### DEEP DIVE

- [Architecture Decision Records](https://adr.github.io/)

## Next

Continue to the [design packet lab](90-design-packet-lab.md).
