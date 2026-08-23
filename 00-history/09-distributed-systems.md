# Distributed Systems

A distributed system coordinates work across computers that can be slow, disconnected, or wrong independently.

## Why it matters

**Prerequisite:** [Databases](./08-databases.md).

One machine places capacity, state, and failure in one box. Multiple machines can add capacity and survive component loss, but messages can be delayed, duplicated, reordered, or lost while clocks disagree.

Replication, logical clocks, consensus, and distributed transactions make selected guarantees explicit. They do not restore the certainty of a single process. Global cloud and AI platforms inherit the same partial failures and coordination costs.

## How it works

Each node has incomplete, delayed knowledge. Correctness comes from explicit assumptions about timing, failures, and consistency.

Nodes exchange messages; replicated logs establish ordered decisions; quorums ensure intersecting observations; timeouts trigger suspicions, not proof; retries and deduplication handle uncertain outcomes.

CAP concerns behavior during a partition, not a universal two-of-three menu. Consensus chooses one ordered history despite failures under stated assumptions. Linearizability is a real-time consistency property; it differs from transaction isolation.

## Vocabulary

- **Partition:** A communication failure that separates components that may otherwise remain alive.
- **Quorum:** A threshold of participants whose overlap supports a coordination guarantee.
- **Replication:** Keeping multiple copies of state for availability, locality, or durability.
- **Consensus:** Agreement on a sequence or value despite failure within stated assumptions.
- **Linearizability:** The appearance that operations occur atomically in one real-time-consistent order.
- **Logical clock:** A counter-based model of causal or event ordering without synchronized wall time.
- **Split brain:** Multiple components independently acting as the authoritative leader.
- **Idempotency:** Safe repetition without multiplying the intended effect.
- **Safety:** A property stating that something bad never happens.
- **Liveness:** A property stating that useful progress eventually happens.

## See it yourself

```text
handle(request):
  if dedupe_store.contains(request.id): return saved_result
  result = apply(request)
  atomically_save(request.id, result)
  return result
```

Trace two deliveries carrying the same request ID. The expected logical observation is one applied result and a repeated return of the saved result. This supports deduplication as a way to present one outcome over at-least-once delivery. It does not prove exactly-once execution: the effect and dedupe record still need an atomic boundary or reconciliation.

## Where it shows up

A client submits a deployment, the service commits it, and the response is lost. From the client’s view, failure and success are both possible. Retrying with a stable idempotency key lets the service return the committed result instead of creating another deployment. The user experience can be effectively once-only even though requests and responses may be repeated.

## When it breaks

A cluster may be healthy at the process level yet unable to commit writes. It may have lost quorum, split membership views, overloaded queues, or retries consuming the remaining capacity. First state the required invariant and build a per-node timeline from terms, membership, request IDs, and message delays; a timeout is evidence of uncertainty, not proof of node failure.

## Practice

### Observe

Simulate three replicas, delayed messages, and one failure. Compare read-one/write-one with majority quorum behavior.

### Build

Implement a replicated-log simulator with terms, leader election, commit index, and deterministic tests.

### Break

Partition the leader, duplicate messages, reorder delivery, and skew clocks. Verify safety separately from liveness.

### Say it out loud

Explain why a timeout cannot tell a client whether an operation happened.

**Success:** Succeed by describing an idempotent retry, its atomicity requirement, and the evidence needed after partial failure.

## Check yourself

1. Why are timeouts suspicions?
2. How do quorums intersect?
3. What does consensus guarantee?

### Interview stretch

- Design idempotent deployment submission.
- Explain CAP without the “pick two” myth.
- Diagnose a healthy cluster that cannot make progress.

## Sources

### REQUIRED

- “Time, Clocks, and the Ordering of Events in a Distributed System” — Leslie Lamport. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/). Establishes causal ordering without global time.

### RECOMMENDED

- “In Search of an Understandable Consensus Algorithm (Raft)” — Ongaro and Ousterhout. [Official Raft paper](https://raft.github.io/raft.pdf). Accessible consensus decomposition.

### DEEP DIVE

- “Brewer’s Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services” — Gilbert and Lynch. [MIT PDF](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf). Formalizes CAP’s actual scope.

## Next

Continue with [./10-virtualization-and-cloud.md](./10-virtualization-and-cloud.md).
