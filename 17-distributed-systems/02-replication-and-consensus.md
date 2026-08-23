# Replication, consistency, and consensus

Replication improves availability and read scale only after the system defines which copies are authoritative and how conflicting progress is resolved.

## Why it matters

Multiple copies introduce lag, concurrent writes, failover ambiguity, and the possibility that acknowledged data is unavailable or lost.

## How it works

Leader-based replication orders writes through one node and ships a log to followers. Synchronous acknowledgement improves durability but adds latency; asynchronous acknowledgement risks losing recent writes during failover.

Quorum systems choose read and write sets so they overlap, but guarantees also depend on versioning, repair, and membership. Consensus protocols let a changing set of nodes agree on an ordered log despite some failures; a majority is required for progress, so consensus favors safety during a partition rather than allowing two leaders to commit conflicting histories.

## See it yourself

For three replicas, compare acknowledging after one, two, or three durable writes. State what survives each single-node failure and what latency cost changes.

## Where it shows up

Database replication, Kubernetes etcd, configuration stores, and elected schedulers all encode these tradeoffs.

## When it breaks

An old leader continues accepting uncommitted work, replication lag serves stale reads, or operators lose quorum by replacing too many nodes together.

## Practice

Choose guarantees for a product catalog and for bank transfers. Explain why their read freshness and write availability choices differ.

## Check yourself

1. Why does adding replicas not automatically improve write availability?
2. What does majority quorum prevent during a partition?

## Sources

### REQUIRED
- [Raft paper](https://raft.github.io/raft.pdf)

### RECOMMENDED
- [etcd consistency guarantees](https://etcd.io/docs/v3.5/learning/api_guarantees/)

### DEEP DIVE
- [CAP twelve years later](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)

## Next

[Retries, idempotency, and backpressure](03-retries-and-backpressure.md)
