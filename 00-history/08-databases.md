# Databases

A database keeps shared information organized and recoverable while many users read and change it.

## Why it matters

**Prerequisite:** [Networking and the Internet](./07-networking-and-the-internet.md).

Applications that managed raw files duplicated parsing, indexing, locking, and recovery logic. Concurrent updates could leave those files internally valid but logically wrong.

Databases centralized those responsibilities behind schemas, queries, indexes, and transactions. Distributed SQL, object stores, and vector indexes specialize the model, but all still decide how to represent state, perform physical work, and recover after interruption.

## How it works

A database is a state machine plus durable log, concurrency policy, access paths, and recovery machinery—not merely files with an API.

Queries are parsed and planned; indexes narrow access; transactions coordinate visible versions; WAL records changes before data pages; checkpoints bound recovery; constraints reject invalid states.

Isolation levels trade concurrency for anomalies. MVCC lets readers observe snapshots while writers create versions, but vacuuming and long transactions become operational concerns. An index accelerates reads by adding write and storage cost.

## Vocabulary

- **Relation:** A set of tuples sharing named attributes in the relational model.
- **Schema:** The defined structure, types, and constraints of stored data.
- **Index:** An auxiliary data structure that speeds selected lookups at write and storage cost.
- **Transaction:** A logical unit of database work with defined completion guarantees.
- **ACID:** Atomicity, consistency, isolation, and durability properties associated with transactions.
- **Isolation:** Rules governing how concurrent transactions observe one another.
- **MVCC:** Multi-version concurrency control using multiple row versions to coordinate readers and writers.
- **WAL:** A write-ahead log recorded before related data pages for durability and recovery.
- **Checkpoint:** A recovery point that limits how much logged history must be replayed.
- **Replication:** Maintaining copies of data on multiple nodes.
- **Query plan:** The physical operations selected to execute a query.

## See it yourself

```sql
BEGIN;
SELECT status FROM model_versions WHERE id = 42 FOR UPDATE;
UPDATE model_versions SET status = 'deployed' WHERE id = 42;
COMMIT;
EXPLAIN ANALYZE SELECT * FROM model_versions WHERE id = 42;
```

Predict what happens when two sessions try to lock the same row. The second transaction should wait until the first commits or rolls back, and the plan should reveal whether the lookup uses an index. This supports the claim that the database coordinates concurrency and chooses physical access paths. It does not prove crash durability until recovery is tested, nor does one plan represent every data distribution.

## Where it shows up

A deployment controller may require exactly one active model version per environment. Two reconcilers can read the same old state and both attempt promotion. A transaction plus a uniqueness constraint lets the database serialize or reject that conflict, preserving the invariant even when application timing changes. The schema carries correctness that would otherwise depend on every caller behaving perfectly.

## When it breaks

A request that was fast last month may now spend seconds waiting. Data growth can invalidate cardinality estimates, remove an index advantage, or increase lock contention; replica lag and connection exhaustion can look similar at the application. First capture the exact query and transaction context, then inspect its actual plan, wait event, locks, and row estimates.

## Practice

### Observe

Create a PostgreSQL table with constraints and an index; compare plans before and after indexing and observe concurrent transaction behavior.

### Build

Design a model registry schema with immutable versions, one active deployment per environment, lineage, and idempotent updates.

### Break

Cause a uniqueness violation, deadlock, slow scan, and stale replica read. Capture evidence and define recovery.

### Say it out loud

Explain how a database preserves one business invariant under concurrency.

**Success:** Include the transaction boundary, physical access path, recovery record, and one observable contention symptom.

## Check yourself

1. Why does WAL precede page updates?
2. What does an index cost?
3. How can isolation permit anomalies?

### Interview stretch

- Debug a query that became slow after data growth.
- Choose consistency for feature serving.
- Explain MVCC and vacuum operationally.

## Sources

### REQUIRED

- “A Relational Model of Data for Large Shared Data Banks” — E. F. Codd. [ACM DOI](https://doi.org/10.1145/362384.362685). Introduces data independence through the relational model.

### RECOMMENDED

- “PostgreSQL: Concurrency Control” — PostgreSQL Global Development Group. [Official docs](https://www.postgresql.org/docs/current/mvcc.html). Canonical practical treatment of MVCC and isolation.

### DEEP DIVE

- “ARIES” — C. Mohan et al. [IBM Research](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging). Foundational recovery design using WAL.

## Next

Continue with [./09-distributed-systems.md](./09-distributed-systems.md).
