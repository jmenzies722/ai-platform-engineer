# Evolution and design review

A design is complete only when it can be introduced, observed, migrated, and retired safely.

## Why it matters

Most systems change while serving traffic. The migration path often carries more risk than the target architecture.

## How it works

Record assumptions and decisions, define compatibility windows, and split migration into observable reversible stages. Shadow reads, dual writes with reconciliation, backfills, and canaries each need explicit invariants. Reviews test requirements, alternatives, failure modes, security, operations, cost, and deletion plans rather than rewarding diagram complexity.

Expand-and-contract migrations first make readers tolerant, then write both forms, backfill and verify, switch authority, and finally remove old state. Each phase has entry criteria and rollback semantics. Dual writes are not atomic across independent stores, so reconciliation and a declared source of truth are mandatory. Review quality comes from falsifiable assumptions and operational detail.

## See it yourself

To rename `name` to `display_name`, first deploy readers that accept both. Next write both fields and compare them, backfill old rows with progress checkpoints, then make `display_name` authoritative. Stop writing `name` only after old-client traffic is zero; remove it later. The expected observation at every stage is compatible reads plus reconciliation counts trending to zero.

## Where it shows up

A model-output schema migration can shadow-parse the new format, record differences, and deploy tolerant consumers before switching producers. Rollback remains possible while old consumers and data remain compatible. Ownership includes deleting adapters and fields after the window, otherwise temporary complexity compounds.

## When it breaks

Dual writes lack repair, rollback cannot understand new data, temporary paths become permanent, and no owner removes old state. At divergence, first stop destructive cleanup and compare source-of-truth records, write logs, reconciliation counts, and rollout phase. Determine whether writers, backfill, or readers disagree before rerunning anything.

## Practice

**Build:** write and rehearse an expand-contract migration with entry evidence, rollback, and cleanup owner. **Break:** fail one dual write and roll back after new-format data exists; prove reconciliation and compatibility. **Explain back:** lead a review that tests assumptions and deletion, not diagram aesthetics.

## Check yourself

1. Why prefer reversible stages?
2. What makes dual writes dangerous?
3. What should a design review falsify?

## Sources

### REQUIRED

- [Google SRE: canarying releases](https://sre.google/workbook/canarying-releases/)

### RECOMMENDED

- [Kubernetes API deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

### DEEP DIVE

- [Architecture Decision Records](https://adr.github.io/)

## Next

Continue to [Senior and Staff Engineering](../35-senior-staff-engineering/README.md).
