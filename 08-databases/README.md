# 08 — Databases

Treat a database as an engine with contracts, storage structures, concurrency rules, replication lag, caches, and operational limits. Read the lessons in order: the relational model comes first, then the machinery that preserves and serves it.

## What you will learn

By the end, you can:

- encode invariants with types, keys, constraints, and normalized ownership;
- read query plans and choose indexes from workload shape instead of folklore;
- reason about PostgreSQL MVCC, WAL, checkpoints, vacuum, locks, and isolation;
- explain replication consistency, lag, failover, recovery point, and recovery time;
- design Redis and cache usage around freshness, eviction, stampedes, and durability; and
- operate backups, restores, migrations, capacity, and connection pools with measurable safety.

## Lessons

1. [Relational Models and Constraints](./01-relational-models-and-constraints.md)
2. [Queries and Indexes](./02-queries-and-indexes.md)
3. [Transactions and Concurrency](./03-transactions-and-concurrency.md)
4. [PostgreSQL Storage, WAL, and Vacuum](./04-postgresql-storage-wal-and-vacuum.md)
5. [Replication, Failover, and Recovery](./05-replication-failover-and-recovery.md)
6. [Redis, Caching, and Database Operations](./06-redis-caching-and-database-operations.md)

## Practice

[Measure a Database, Then Break It Safely](./lab-database-behavior.md) builds a disposable SQLite workload that exposes constraints, plans, transaction rollback, lock contention, and cache invalidation. PostgreSQL and Redis extension prompts are explicitly optional and require disposable instances.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can defend a schema and index from invariants and plans, predict an isolation anomaly, explain why vacuum and WAL are both necessary, choose a read-consistency contract, restore a tested backup, and state exactly what a cache may return during failure.

## Next

Start with [Relational Models and Constraints](./01-relational-models-and-constraints.md).
