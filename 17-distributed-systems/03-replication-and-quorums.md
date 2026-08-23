# Replication, quorums, and repair

Replication creates copies; it does not by itself create durability, freshness, or safe failover. Those properties come from acknowledgement rules, version semantics, membership, and repair.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Leader-based replication orders writes at one authority and streams a log to followers. Synchronous acknowledgement raises latency but can guarantee a write reaches a failure domain; asynchronous acknowledgement reduces latency while exposing an acknowledged-loss window. Leaderless systems write and read replica sets, reconcile versions, and repair divergence.

For fixed membership of `N` replicas, read size `R` and write size `W` overlap when `R + W > N`. That overlap only provides a chance to observe a newest version; it is not linearizability without correct versioning, conflict handling, and membership. Anti-entropy repairs cold divergence; read repair repairs keys clients touch.

## See it yourself

With `N=3`, `W=2`, and `R=2`, any read and write sets intersect because two subsets of size two cannot be disjoint in a three-element set. Now let the intersecting replica reply slowly and the coordinator accept the first response: the mathematical overlap exists, but the implementation can still return stale data.

## Where it shows up

Database followers, object stores, caches, and multi-region control planes use different replication policies. Place replicas across independent failure domains, measure replication lag in both bytes and time, and test recovery time rather than counting copies.

## When it breaks

Stale leaders can accept uncommitted writes, hinted handoff can hide long divergence, tombstones can expire before repair, and operators can remove quorum during maintenance. Diagnose with commit index, replica version, membership epoch, lag, and repair backlog.

## Practice

Model three replicas and compare acknowledgements after one, two, and three durable writes. Build a table of surviving failures and latency. Break one replica for longer than tombstone retention. Completion means you identify possible resurrection and specify repair and deletion-retention constraints.

## Check yourself

1. What exactly follows from `R + W > N`?
2. Why can asynchronous replication lose acknowledged data?
3. How do anti-entropy and read repair differ?
4. Which evidence shows a stale read came from lag rather than cache?

## Sources

### REQUIRED

- [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

### RECOMMENDED

- [PostgreSQL: Warm Standby](https://www.postgresql.org/docs/current/warm-standby.html)

### DEEP DIVE

- [Designing Data-Intensive Applications: Replication](https://dataintensive.net/)

## Next

[Consensus, leadership, and membership](04-consensus-and-membership.md)
