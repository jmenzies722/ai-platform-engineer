# Consistency models and client guarantees

Consistency is a contract about which histories clients may observe. Calling a system “strong” or “eventual” without naming operations, scope, and session guarantees leaves the correctness argument unfinished.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Linearizability makes each operation appear atomic between invocation and response and respects real-time order. Sequential consistency preserves one legal global order but not necessarily real time. Causal consistency preserves happened-before relationships while allowing concurrent writes to appear in different orders. Eventual convergence says replicas agree after writes stop, not what users see meanwhile.

Clients often need narrower guarantees: read-your-writes, monotonic reads, monotonic writes, or writes-follow-reads. Tokens carrying a version or log position can route a session to a sufficiently caught-up replica. Invariants, not labels, decide the required model.

## See it yourself

Consider `put(x,1)` completing before `get(x)` begins. A return of `0` disproves linearizability because no atomic point for the read can fit between invocation and response while respecting real time. It may still satisfy eventual consistency. Add a session token and state the minimum replica position required for read-your-writes.

## Where it shows up

A social feed may tolerate convergent ordering while password revocation cannot tolerate a stale authorization read. Product catalogs often need read-your-writes for editors but permit stale public reads. Document consistency per API, including failover behavior.

## When it breaks

A failover may lose sticky-session state, lag can violate read-your-writes, and caches can provide weaker guarantees than the database beneath them. Capture versions at write acknowledgement and read response; a timestamp alone is weak evidence when clocks differ.

## Practice

Write histories for a profile editor and a uniqueness constraint. Build a checker that flags a read older than the caller’s last observed version. Inject a stale replica response. Completion means the checker catches the violation and your design names whether it waits, reroutes, or fails.

## Check yourself

1. Which history distinguishes sequential consistency from linearizability?
2. Why does eventual convergence not imply read-your-writes?
3. When is a session token preferable to sticky routing?
4. What invariant would force stronger consistency for account balances?

## Sources

### REQUIRED

- [Viotti and Vukolić: Consistency in Non-Transactional Distributed Storage Systems](https://arxiv.org/abs/1512.00168)

### RECOMMENDED

- [Jepsen: Consistency Models](https://jepsen.io/consistency)

### DEEP DIVE

- [Linearizability: A Correctness Condition for Concurrent Objects](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf)

## Next

[Replication, quorums, and repair](03-replication-and-quorums.md)
