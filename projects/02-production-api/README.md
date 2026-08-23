# 02 — Production Change-Request API

Design and build the implementation in a separate repository: an API that safely accepts, approves, schedules, and audits operational change requests.

## Problem and users

Service owners need a dependable way to submit changes while approvers need clear risk, ownership, and immutable history. Web clients, automation, approvers, and auditors are distinct users with different permissions. The system must remain correct when clients retry, workers crash, and database transactions contend.

## Constraints and boundaries

- Use a relational database as the source of truth and an asynchronous worker for notifications or execution simulation.
- Provide HTTP/JSON contracts, schema migrations, authentication, authorization, pagination, and deterministic error semantics.
- Assume 100 requests per second, 10 million retained records, bursty reads, and two availability zones.
- Do not execute real infrastructure changes, build a frontend, or invent a custom identity provider.

## Architecture expectations

Define lifecycle states and legal transitions before endpoints. Keep request acceptance transactional; use idempotency keys and an outbox so durable state and work publication cannot diverge. Specify ownership of approval policy, audit records, and derived views. Include API versioning, concurrency control, timeout budgets, data retention, backup, and zero-downtime migration strategy.

## Milestone plan

1. Publish OpenAPI, state-machine invariants, threat model, and capacity assumptions.
2. Deliver create/read/list and approval transitions with migrations and authorization tests.
3. Add outbox processing, retry limits, dead-letter handling, idempotency, and audit export.
4. Validate load, multi-instance behavior, backup restore, canary release, and rollback.

## Required artifacts

- OpenAPI document, entity/state diagrams, ADRs, migration playbook, and data dictionary.
- Load model and measured latency/throughput report with query plans.
- Dashboard, alerts, runbooks, restore evidence, and incident timeline.
- Signed release manifest or equivalent provenance plus API compatibility report.

## Tests and failure drills

Use contract, unit, integration, migration, authorization, and property tests for state transitions. Exercise duplicate submissions, concurrent approvals, stale versions, malformed filters, worker death after commit, poison messages, database failover, connection exhaustion, slow dependencies, and restore from backup. Verify invariants directly in stored data after every drill.

## Observability, security, and cost

Measure successful request rate, p50/p95/p99 latency, saturation, queue age, transition failures, and outbox lag; trace API-to-worker flow with request and idempotency IDs. Hash secrets, validate all inputs, apply object-level authorization, encrypt transport/storage, minimize audit PII, and log privileged actions. Price steady and peak traffic, storage growth, backups, telemetry, and cross-zone transfer; state a monthly budget and cost per 1,000 accepted changes.

## Explicit success rubric

| Dimension | Graduation threshold |
|---|---|
| Contract | Compatibility checks pass and all error, retry, and pagination behavior is documented. |
| Correctness | No duplicate logical change or illegal transition occurs under concurrency and retries. |
| Reliability | Stated SLO survives the load test; restore meets declared RPO/RTO; alerts identify the injected fault. |
| Security | Independent tests cannot cross tenant or role boundaries; audit evidence is complete. |
| Judgment | ADRs explain rejected designs, measured bottlenecks, and residual risks. |

## Stretch work

Add policy-as-code approval checks, read replicas with explicit consistency semantics, or change-calendar conflict detection.

## Authoritative sources

- [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)

## Mapped modules

[02 Python](../../02-python/README.md) or [10 Go](../../10-go/README.md), [07 Networking](../../07-networking/README.md), [08 Databases](../../08-databases/README.md), [09 Backend Engineering](../../09-backend-engineering/README.md), [11 Software Architecture](../../11-software-architecture/README.md), and [20 Security](../../20-security/README.md).
