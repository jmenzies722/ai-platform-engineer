# PostgreSQL Storage, WAL, and Vacuum

PostgreSQL turns logical rows into page versions, records changes in a write-ahead log, and reclaims obsolete versions asynchronously.

## Why it matters

A table can contain few live rows yet occupy gigabytes, an update can slow because dirty pages trigger I/O, and a forgotten transaction can prevent cleanup across the cluster. These are not mysterious “database slowness.” They follow from MVCC version lifetime, WAL durability, checkpoint pressure, and vacuum’s ability to advance.

## How it works

PostgreSQL stores relations in fixed-size pages. A heap tuple contains visibility metadata including creating and deleting transaction identifiers. Under multiversion concurrency control, an update generally creates a new tuple version and marks the old one obsolete rather than overwriting it in place. Each statement or transaction uses a snapshot to decide which versions are visible. Index entries point to heap tuple locations, although an index-only scan may avoid heap access when the visibility map proves all tuples on a page are visible.

Before a changed data page must reach durable storage, the corresponding WAL record must be flushed according to the durability policy. This write-ahead rule enables crash recovery to replay logged changes after the last checkpoint. WAL also feeds physical replication and point-in-time recovery. A commit acknowledgment under normal synchronous-commit settings establishes WAL durability under PostgreSQL’s configured storage assumptions; it does not mean every heap page was immediately written.

Checkpoints bound recovery work by arranging writes of dirty pages and recording a recovery position. Too-frequent or bursty checkpoints create I/O pressure. Background writer behavior smooths some writes, while backends may still have to write buffers.

Vacuum identifies dead tuples no active snapshot can need, marks space reusable, maintains visibility information, and freezes old transaction IDs to prevent wraparound. Standard vacuum usually reuses space internally without returning the file to the operating system. Autovacuum must keep pace with update churn; long-running transactions, abandoned replication slots, and undersized maintenance settings can hold back reclamation.

## See it yourself

If a local PostgreSQL server is intentionally available, predict that `EXPLAIN (ANALYZE, BUFFERS)` reports actual execution and buffer activity, while the catalog query reveals dead-tuple estimates. Otherwise read the commands without inventing output.

```sql
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42;
```

Expected observation: statistics are estimates and plans report measured work for this execution. Buffer hits mean pages were found in PostgreSQL’s buffer cache, not that the query performed zero CPU or storage work everywhere.

Limits of the observation: one plan does not characterize parameter distributions, concurrent load, checkpoint behavior, or future cache state. Never run `ANALYZE` on an expensive write query merely for curiosity.

## Where it shows up

An event table receiving updates to indexed columns may lose HOT-update opportunities and generate heap versions, index entries, and WAL quickly. Replicas retain WAL while replay lags. Storage grows from both relation bloat and retained WAL. The correct response may combine shorter transactions, index review, autovacuum tuning, replica repair, and capacity relief; `VACUUM FULL` is not a harmless first move because it takes an exclusive lock and rewrites the table.

## When it breaks

Rising dead tuples with stale autovacuum timestamps suggest cleanup lag; checkpoint spikes correlate with write-latency sawteeth; WAL growth points to write volume, archiving failure, lagging slots, or large transactions; transaction-ID age approaching limits is urgent. First preserve `pg_stat_activity`, lock waits, table statistics, WAL and checkpoint metrics, slot lag, disk latency, and recent configuration changes. Terminate a blocking session only after identifying owner and impact.

## Practice

**Build:** on a disposable PostgreSQL instance, create a table, update the same rows repeatedly, and compare relation statistics before and after vacuum. **Break:** hold an old transaction open while updating from another session, then observe what vacuum cannot reclaim. **Explain back:** connect snapshot lifetime, tuple versions, WAL, checkpoint, and vacuum. Success includes cleanup, recorded version information, and no commands against shared production data.

## Check yourself

1. Why can PostgreSQL acknowledge commit before the changed heap page is written?
2. How can one idle transaction cause storage and performance trouble elsewhere?

## Sources

### REQUIRED

- [PostgreSQL MVCC](https://www.postgresql.org/docs/current/mvcc.html)
- [PostgreSQL Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html)

### RECOMMENDED

- [PostgreSQL WAL Configuration](https://www.postgresql.org/docs/current/wal-configuration.html)
- [PostgreSQL Database Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html)

### DEEP DIVE

- [PostgreSQL Internals](https://www.interdb.jp/pg/)

## Next

Continue to [Replication, Failover, and Recovery](./05-replication-failover-and-recovery.md).
