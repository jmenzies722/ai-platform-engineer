# Consensus, leadership, and membership

Consensus lets a group agree on one growing history despite delay and crash failures. It does not make an unavailable majority available, execute commands exactly once, or remove the need to define state-machine semantics.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Raft separates leader election, log replication, and safety. Terms identify election epochs. A leader appends entries, replicates them, and commits an entry after a majority stores it under the protocol’s commit rule. Followers apply only committed entries in order. Randomized election timeouts reduce repeated split votes.

Safety requires overlapping majorities. Membership changes therefore use a joint configuration or an equivalent staged protocol; replacing nodes informally can create disjoint groups that each believe they can decide. Snapshots compact applied history but must preserve included index, term, and state.

## See it yourself

In five nodes, any two majorities contain at least one common node: two sets of three cannot be disjoint because that would require six nodes. This intersection carries knowledge across decisions. It does not guarantee progress if three nodes cannot communicate.

## Where it shows up

Configuration stores, schedulers, locks, and metadata services often replicate a deterministic state machine. Keep slow external side effects outside the consensus apply loop; record intent in the log, then reconcile side effects idempotently.

## When it breaks

Disk stalls can cause election churn, stale leaders can serve unsafe reads, snapshots can omit state, and simultaneous replacement can destroy quorum. Inspect term, role changes, commit index, applied index, fsync latency, and active membership before restarting nodes.

## Practice

Run or simulate a five-node log. Elect a leader, commit entries, partition it with one follower, and predict both sides. Completion means the minority cannot commit, the majority elects once, and the healed cluster converges without two committed values at one index.

## Check yourself

1. Why does consensus require quorum intersection?
2. What can a minority leader safely do during a partition?
3. Why is membership change part of the protocol?
4. How can apply lag differ from replication lag?

## Sources

### REQUIRED

- [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)

### RECOMMENDED

- [etcd: Raft](https://etcd.io/docs/v3.5/learning/why/)

### DEEP DIVE

- [Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)

## Next

[Transactions, sagas, and the outbox](05-distributed-transactions.md)
