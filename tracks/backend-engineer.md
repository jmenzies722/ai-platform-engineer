# Backend Engineer Track

## Outcome role

An engineer who owns APIs and asynchronous services from contract design through data integrity, deployment, diagnosis, and recovery. The outcome includes authorization, concurrency, queues, database behavior, overload control, telemetry, and failure-aware architecture.

## Prerequisites

- Foundations evidence: a tested program, deliberate Git history, and working complexity analysis.
- Ability to explain a process, memory, files, and one network request at a basic level.
- Learners without that evidence should begin with the [Software Engineer track](software-engineer.md) through its systems gate.

## Ordered module path

| Order | Module | Rationale |
|---:|---|---|
| 1 | [01 Software Foundations](../01-software-foundations/README.md) | Establishes runtime, state, concurrency, interface, and failure vocabulary. |
| 2 | [02 Python](../02-python/README.md) | Provides the implementation language used in core practice. |
| 3 | [05 Git](../05-git/README.md) | Makes collaboration, review, and recovery observable. |
| 4 | [06 Data Structures and Algorithms](../06-data-structures-algorithms/README.md) | Supports complexity, queue, cache, and indexing decisions. |
| 5 | [03 Computer Systems](../03-computer-systems/README.md) | Grounds performance and durability in machine behavior. |
| 6 | [04 Linux](../04-linux/README.md) | Enables host and process diagnosis. |
| 7 | [07 Networking](../07-networking/README.md) | Makes service boundaries and transport failures concrete. |
| 8 | [08 Databases](../08-databases/README.md) | Establishes transactional, indexing, replication, recovery, and cache semantics. |
| 9 | [09 Backend Engineering](../09-backend-engineering/README.md) | Integrates API, auth, queues, deadlines, backpressure, and deployment behavior. |
| 10 | [10 Go](../10-go/README.md) | Adds explicit concurrency, cancellation, races, and production service practice. |
| 11 | [11 Software Architecture](../11-software-architecture/README.md) | Develops evolvable boundaries and recorded tradeoffs. |
| 12 | [17 Distributed Systems](../17-distributed-systems/README.md) | Corrects assumptions about time, partial failure, retries, consistency, and coordination. |
| 13 | [18 Observability](../18-observability/README.md) | Connects service claims to traces, metrics, logs, and telemetry cost. |
| 14 | [34 System Design](../34-system-design/README.md) | Integrates requirements, capacity, data ownership, overload, and recovery. |

Python and Go are not interchangeable checkboxes: build the initial service in Python, then use Go to expose different concurrency and runtime tradeoffs.

## Required practice

**Labs:** [software execution](../labs/01-software-execution/README.md), [network diagnosis](../labs/04-network-dns-tls/README.md), [PostgreSQL and Redis](../labs/05-postgres-redis/README.md), [backend reliability](../labs/06-backend-reliability/README.md), and [OpenTelemetry traces](../labs/11-opentelemetry-traces/README.md).

**Incidents:** [DNS failure](../incidents/01-dns-failure/README.md), [database pool exhaustion](../incidents/05-database-pool-exhaustion/README.md), [retry storm](../incidents/08-retry-storm/README.md), [database deadlock](../incidents/09-deadlock/README.md), and [queue overload](../incidents/12-queue-overload/README.md).

**Projects:** [Production Change-Request API](../projects/02-production-api/README.md) is required. Complete [Network Failure Laboratory](../projects/03-network-failure-lab/README.md) to prove boundary diagnosis. For senior backend scope, add [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md) or [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md).

## Competency gates

**[Foundations gate](../assessments/gates/foundations.md):** implement and test a bounded program, trace it through runtime and machine state, repair an evidence defect, and explain the mechanism without borrowed wording.

**[Systems, Linux, and networking gate](../assessments/gates/systems-linux-networking.md):** recover Git state, defend representation and complexity choices, trace a request through DNS, TCP/TLS, service, and database, and diagnose a controlled process or network fault.

**Backend outcome evidence:** independently deliver an authenticated API with migrations, constraints, stable errors, pagination, object-level authorization, idempotency, bounded queues, deadline propagation, graceful shutdown, telemetry, and a restore or recovery drill. Load evidence must show saturation behavior and a justified concurrency limit. Incident evidence must include a timeline, competing hypotheses, reversible mitigation, and user-visible recovery.

## Certification overlays

No certification is required. [DOP-C02](../certs/aws-dop-c02.md) is optional only for backend roles that also own AWS delivery pipelines and production operations. In that case, complete the [AWS module](../12-aws/README.md) and use the overlay as a review index. Exam preparation does not substitute for database correctness, overload, or incident evidence.
