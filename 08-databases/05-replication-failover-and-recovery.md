# Replication, Failover, and Recovery

Replication copies change, but only an explicit consistency and recovery contract says what clients may safely observe.

## Why it matters

A successful write followed by an empty read from a replica can be expected lag, not data loss. A failover can restore availability yet lose acknowledged transactions if the promoted replica was behind. “Highly available” is incomplete without commit semantics, read routing, fencing, recovery point objective, and a restore procedure that has actually run.

## How it works

Physical PostgreSQL streaming replication sends WAL records from a primary to standby servers, which write and replay them. The primary’s current WAL location, a standby’s received location, flushed location, and replayed location describe distinct stages. Replication lag can be measured in bytes or time, but a quiet system makes time-since-last-replay misleading. Logical replication decodes changes into a higher-level stream and can select tables, but schema changes, sequences, and conflict behavior require separate handling.

Asynchronous replication lets the primary acknowledge without waiting for a standby, giving lower coordination latency but allowing acknowledged work to be absent after primary loss. Synchronous replication can wait for selected standbys at a configured stage, reducing that gap while coupling write availability and latency to them. Even synchronous replication does not replace backups: operator error and bad writes replicate faithfully.

Failover chooses a sufficiently current standby, prevents the former primary from accepting writes, promotes the candidate, and redirects clients. Fencing is essential because two writable primaries create divergent histories. Promotion changes topology, not every client connection; pools need bounded reconnect and discovery behavior.

Backups define recovery capability. A base backup plus archived WAL can support point-in-time recovery before an accidental change. RPO bounds acceptable data loss; RTO bounds acceptable restoration time. Both must include detection, transfer, replay, validation, and application reconnection, not just a vendor control-plane duration.

## See it yourself

On a disposable PostgreSQL topology, predict nonnegative byte differences and identify which stage each location represents.

```sql
SELECT application_name, state, sync_state,
       sent_lsn, write_lsn, flush_lsn, replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_bytes_behind
FROM pg_stat_replication;

SELECT pg_is_in_recovery(),
       pg_last_wal_receive_lsn(),
       pg_last_wal_replay_lsn(),
       pg_last_xact_replay_timestamp();
```

Expected observation: the primary reports sender-side progress per standby, while a standby reports receive and replay progress. An empty result can simply mean no standby is connected.

Limits of the observation: locations are samples that can change immediately. Zero replay-byte lag does not prove the replica is allowed to serve a particular read, and status views do not prove a backup can restore.

## Where it shows up

After creating an account, an API may redirect the user to a page read from a replica. The contract can route that user’s read to primary for a bounded interval, carry a required commit position and wait for replay, or accept temporary staleness in the UI. Randomly retrying replicas hides neither lag nor monotonic-read violations.

## When it breaks

Growing receive lag suggests network or sender pressure; growing replay lag suggests standby I/O, conflicts, or expensive WAL application; retained WAL can fill primary storage when a slot’s consumer stalls. Timeline divergence and a reachable former primary signal split-brain risk. First capture commit policy, WAL positions, slot retention, archive status, topology, leader lease or fencing state, and client endpoints. Freeze automated churn before improvising promotion. Never delete a replication slot solely to free space without understanding whether its consumer can be rebuilt.

## Practice

**Build:** write a recovery runbook with trigger, authority, candidate selection, fencing, promotion, client redirection, validation, and rollback. **Break:** in disposable infrastructure, pause replay or a logical subscriber and watch lag plus retained storage. **Explain back:** state which acknowledged writes each failure can lose. Success requires a timed restore test to a separate destination and validation by application-level invariants.

## Check yourself

1. Why does replication not protect against an accidental `DELETE`?
2. What must happen besides promoting a standby to prevent split brain?

## Sources

### REQUIRED

- [PostgreSQL Warm Standby and Streaming Replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL Continuous Archiving and Point-in-Time Recovery](https://www.postgresql.org/docs/current/continuous-archiving.html)

### RECOMMENDED

- [PostgreSQL Synchronous Replication](https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION)
- [PostgreSQL Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html)

### DEEP DIVE

- [Designing Data-Intensive Applications](https://dataintensive.net/)

## Next

Continue to [Redis, Caching, and Database Operations](./06-redis-caching-and-database-operations.md).
