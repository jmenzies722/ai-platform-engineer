# Data and feature platform contracts

An AI data platform makes datasets and features discoverable, reproducible, policy-aware, and safe to consume through versioned contracts.

## Why it matters

Training from mutable paths or undocumented joins makes results irreproducible and can leak restricted data into artifacts that are hard to recall.

## How it works

A dataset version binds schema, snapshot or manifest, producer, purpose, lineage, quality checks, retention, and access policy. Immutable manifests reference checksummed shards. Feature contracts define entity key, event time, freshness, null behavior, and offline-online consistency. Identity and purpose flow into authorization and audit.

The platform separates control metadata from bulk data, validates compatibility before publication, and records every training consumption. Data minimization and deletion obligations propagate through derived datasets, checkpoints, and deployed models according to governance policy.

## See it yourself

Train twice from `data/latest`; a producer appends records between runs, so identical code and seed consume different examples. Pinning a manifest digest makes the byte set stable. It does not prove deterministic training, but removes one source of ambiguity.

## Where it shows up

A training request resolves approved dataset versions, checks schema and policy, issues scoped workload credentials, and records the resolved manifests in run lineage. Online features include freshness and fallback telemetry.

## When it breaks

Backfills violate event time, labels leak future information, schema changes silently coerce values, caches outlive revocation, and sensitive columns enter logs. Compare manifest, schema decision, event timestamps, principal, policy, and derived lineage. Quarantine rather than overwrite bad versions.

## Practice

**Observe:** trace one field from source to model. **Build:** define dataset and feature contracts with compatibility tests. **Break:** introduce a future-derived label and revoke one source. Completion requires leakage detection and a list of affected artifacts.

## Check yourself

1. What does a manifest digest prove?
2. Why does feature freshness belong in the contract?
3. How can deletion propagate to trained artifacts?

## Sources

### REQUIRED

- [NIST AI RMF data guidance](https://airc.nist.gov/AI_RMF_Knowledge_Base/AI_RMF/)

### RECOMMENDED

- [Apache Iceberg specification](https://iceberg.apache.org/spec/)

### DEEP DIVE

- [Feast architecture](https://docs.feast.dev/getting-started/architecture-and-components)

## Next

Continue to [Training platform architecture](05-training-platform-architecture.md).
