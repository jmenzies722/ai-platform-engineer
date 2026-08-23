# Systems, Linux, and Networking Gate

This gate tests a local service across operating-system, version-control, algorithm, network, database, backend, language, and architecture boundaries. It covers [Linux](../../04-linux/README.md), [Git](../../05-git/README.md), [data structures and algorithms](../../06-data-structures-algorithms/README.md), [networking](../../07-networking/README.md), [databases](../../08-databases/README.md), [backend engineering](../../09-backend-engineering/README.md), [Go](../../10-go/README.md), and [software architecture](../../11-software-architecture/README.md).

## Prerequisites

- Pass the [Foundations Gate](foundations.md).
- Provide prior evidence from [Diagnose a Slow Linux Workload](../../labs/02-linux-diagnosis/README.md), [Recover Git Work](../../labs/03-git-recovery/README.md), [Debug DNS, TCP, TLS, and HTTP](../../labs/04-network-dns-tls/README.md), [Observe PostgreSQL and Redis](../../labs/05-postgres-redis/README.md), and [Add Timeouts, Retries, and Idempotency](../../labs/06-backend-reliability/README.md), or equivalent evidence covering each mechanism.
- Show a tested service baseline based on [Production Change-Request API](../../projects/02-production-api/README.md) or a smaller implementation with the same contract concerns.
- Use only a disposable local environment. Any packet capture, process signal, database, or network namespace must be explicitly authorized and scoped.

## Challenge

Build a small HTTP change-request service in Python or Go with:

- a versioned JSON contract and deterministic error format;
- a relational source of truth with legal state-transition and uniqueness constraints;
- object-level authorization using synthetic identities;
- idempotent create behavior;
- bounded concurrency, queueing, request deadline, and graceful shutdown;
- structured correlation across request, database work, and any background action; and
- tests for malformed input, duplicate requests, concurrent transitions, timeout, and shutdown.

Run a measured healthy baseline. Preserve query plans, socket identity, process state, request timing, and stored invariants. The evaluator then injects one blind primary fault and one misleading symptom selected from:

- DNS resolution failure from [the DNS drill](../../incidents/01-dns-failure/README.md);
- process stop, descriptor pressure, or disk exhaustion from [the Linux lab](../../labs/02-linux-diagnosis/README.md) or [disk drill](../../incidents/03-disk-exhaustion/README.md);
- database lock, deadlock, or pool exhaustion from [the deadlock drill](../../incidents/09-deadlock/README.md) or [pool drill](../../incidents/05-database-pool-exhaustion/README.md);
- deadline and retry amplification from [the retry-storm drill](../../incidents/08-retry-storm/README.md); or
- a service that is listening but violates its HTTP or application contract.

The candidate must lead from user impact, distinguish resolver, route, TCP, TLS when present, HTTP, process, queue, and database layers, apply a reversible correction, and prove stored invariants plus user-visible recovery. Then recover one evaluator-created Git commit or conflict without rewriting shared history and produce an ADR for the service boundary most affected by the incident.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- source history, tests, API schema, database schema and constraints, state-transition model, and exact clean setup;
- healthy and failed request timelines correlated to socket, process, queue, and database observations;
- query plan and measured operation costs under two documented workloads;
- timeout, retry, idempotency, and concurrency budgets with units;
- ranked hypotheses, rejected hypothesis, mitigation and rollback trigger, stored-invariant checks, and sustained recovery;
- before/after Git graphs, recovered object IDs or conflict rationale, and proof that no shared reference was rewritten;
- ADR with quality-attribute scenario, alternatives, coupling and ownership consequences, migration concern, and revisit evidence; and
- bounded cleanup proof for local processes, ports, databases, temporary repositories, and captures.

## Dimension requirements

- **Explain:** Narrate one request without collapsing process, DNS, transport, protocol, application, and transaction layers. Explain ownership, duplicate delivery, isolation, timeout, and graceful shutdown limits.
- **Build:** Deliver the tested service and database contracts with bounded concurrency and deterministic recovery behavior.
- **Debug:** Isolate the blind fault using discriminating evidence, preserve misleading evidence, and verify the causal mechanism rather than merely restoring a green response.
- **Operate:** Check process and socket identity, control load and retries, preserve accepted work, mitigate reversibly, verify recovery at user and dependency layers, and drain cleanly.
- **Design:** Defend data structures, database invariants, API evolution, boundary placement, and the ADR against measured quality attributes and failure behavior.

## Evaluator instructions

Use synthetic data and prepare the hidden fault without altering the candidate's source history. Keep [incident solutions](../../incidents/README.md) closed until hypotheses, falsifying evidence, and mitigation are recorded. If the candidate knows a solution, use another listed incident or vary the causal layer.

Observe a clean build, one concurrent test, the full incident response, and Git recovery. Ask for a live contract change such as adding optimistic concurrency or changing the deadline. Do not accept a broad restart as diagnosis; it may be a temporary mitigation only with preserved evidence and a rollback plan.

Critical requirements:

- duplicate or concurrent requests cannot create an illegal stored transition;
- retry behavior remains bounded and uses a stable idempotency identity where retry is permitted;
- the diagnosis distinguishes at least three relevant system layers;
- accepted work is accounted for through shutdown and recovery; and
- Git recovery preserves intent and does not rewrite others' work.

## Review prompts

1. Which tuple identifies the connection, and what does a listening socket prove?
2. What is the last completed layer and first failed layer in the incident?
3. Which database constraint protects the invariant when application instances race?
4. When is retry safe, and who owns deduplication after an ambiguous outcome?
5. How were concurrency and queue bounds derived from the workload?
6. Which evidence rejects the misleading symptom as the primary cause?
7. Why was this service boundary chosen, and what evidence would reverse the ADR?
8. What state lived only in the working tree, index, local references, and shared history during recovery?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and successful diagnosis of a fresh blind variant. Debug and Operate must be independently demonstrated; a correct post hoc explanation is insufficient.

Rework must use a new fault when diagnosis was hinted. Contract or invariant gaps require a negative or concurrent test plus a clean rerun. Operational gaps require a fresh bounded incident. Git gaps require a new disposable history. Design gaps require an ADR revision after a changed quality attribute.

## Remediation

Use the narrowest relevant asset: [Linux diagnosis](../../04-linux/06-observability-logs-and-resource-diagnosis.md), [Git recovery](../../05-git/03-inspecting-and-recovering-history.md), [network debugging](../../07-networking/06-network-debugging-from-symptom-to-packet.md), [transactions and concurrency](../../08-databases/03-transactions-and-concurrency.md), [backend concurrency and backpressure](../../09-backend-engineering/06-concurrency-backpressure-and-performance.md), or [architecture decisions](../../11-software-architecture/02-quality-attributes-and-decisions.md). Reproduce the mechanism in isolation before attempting a fresh integrated variant.
