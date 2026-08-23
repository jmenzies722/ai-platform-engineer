# Data models and ownership

A data model is an executable statement about identity, relationships, lifecycle, and which system may declare a fact true.

## Why it matters

Storage engines can be replaced; ambiguous identity and competing authority become correctness failures that spread through every interface and migration.

## How it works

Begin with access patterns and invariants, then model entities. Define stable identity, uniqueness scope, cardinality, lifecycle, retention, and deletion. Separate authoritative facts from derived projections. One component should own each decision even when replicas and indexes distribute its representation.

Choose storage by required operations and failure properties. Relational systems are strong when transactions and constraints protect related facts. Key-value models favor known-key access and horizontal partitioning. Document and wide-column models trade joins for aggregate-oriented access. Search indexes and vector indexes are derived retrieval structures, not automatically systems of record.

Partition keys determine locality, parallelism, and hot-spot risk. Indexes accelerate reads but amplify writes, storage, and migration work. Schema design includes provenance, tenancy, time, and versioning. Deletion must cover replicas, caches, indexes, backups, and derived datasets under explicit policy; a row-level delete is not a lifecycle design.

## See it yourself

Model a document as a source record with immutable tenant and document identity. Chunks, embeddings, and search entries reference the source version that produced them. When the source changes, a new version is indexed and the projection’s active pointer changes only after validation. Retrieval can now explain which source version supported an answer.

## Where it shows up

Feature platforms distinguish raw events, point-in-time-correct feature definitions, computed values, and training snapshots. Without provenance and event time, an apparently convenient table can leak future information into training or produce serving values that cannot be reproduced.

## When it breaks

Data designs break through natural keys that change, hot partitions, unbounded collections, orphaned projections, and dual ownership. Trace one entity across authoritative record, change event, index, cache, retention policy, and backup. If two stores disagree, the design must already say which one wins and how repair is observed.

## Practice

**Build:** model tenants, source documents, versions, chunks, embeddings, and deletion requests. Include keys, constraints, indexes, partition strategy, provenance, and lifecycle. **Break:** create one hot tenant and fail indexing halfway through a version. **Explain back:** identify authoritative facts and prove that every projection can be rebuilt or retired.

## Check yourself

1. Why is a search index usually a projection?
2. Which partition-key property prevents parallel scaling?
3. What information makes derived data reproducible?

## Sources

### REQUIRED

- [PostgreSQL documentation: Data Definition](https://www.postgresql.org/docs/current/ddl.html)

### RECOMMENDED

- [AWS DynamoDB: Designing partition keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)

### DEEP DIVE

- [Martin Kleppmann: Designing Data-Intensive Applications resources](https://dataintensive.net/)

## Next

Continue to [Consistency and distributed invariants](05-consistency-and-distributed-invariants.md).
