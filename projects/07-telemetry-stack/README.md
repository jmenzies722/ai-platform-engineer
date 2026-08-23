# 07 — Operable Telemetry Stack

Build a small but defensible metrics, logs, and traces service in a separate repository, then onboard two contrasting applications.

## Problem and users

On-call engineers need to move from a user symptom to relevant evidence quickly. Service owners need useful telemetry without accidental data leakage or unbounded cardinality. Platform operators need predictable ingestion, retention, and cost. A dashboard collection without data contracts and failure behavior does not solve this problem.

## Constraints and data contract

- Accept OpenTelemetry signals from two sample services and preserve cross-service correlation.
- Define per-tenant volume/cardinality budgets, retention tiers, and late/out-of-order behavior.
- Run on bounded infrastructure and degrade explicitly when downstream storage is unavailable.
- Exclude a custom storage engine, permanent raw payload retention, and “collect everything” defaults.

## Architecture expectations

Specify SDK/agent boundaries, collectors, queues, sampling, redaction, signal backends, query paths, and tenant isolation. Define resource attributes, service identity, trace propagation, log fields, histogram semantics, and schema evolution. Analyze at-least-once delivery, duplicates, clock skew, backpressure, tail versus head sampling, and observability of the telemetry system itself.

## Milestone plan

1. Establish telemetry conventions, user journeys, budgets, and a sensitive-data threat model.
2. Instrument golden signals and one critical trace across both services.
3. Add durable buffering, sampling, retention, dashboards, recording rules, and alerts.
4. Load-test ingestion/query paths and run loss, cardinality, corruption, and backend-outage drills.

## Required artifacts

- Telemetry schema and governance guide, architecture/trust diagrams, sampling ADR, and retention policy.
- Instrumentation examples, service dashboard, telemetry-stack dashboard, alerts, and runbooks.
- Cardinality/volume forecast compared with measurements; query performance and cost report.
- Fault-injection evidence showing what was lost, delayed, sampled, or recovered.

## Tests and failure drills

Contract-test required attributes and propagation; test redaction, sampling determinism, histogram boundaries, duplicate handling, and tenant access. Inject collector restart, full queue, dropped packets, slow storage, clock skew, trace fan-out, cardinality explosion, malformed payloads, query overload, and accidental secret fields. Verify alerts use independent enough signals to detect stack blindness.

## Observability, security, and cost

Track accepted/refused/dropped items, queue utilization, export latency, sampling reason, backend health, query latency, and bytes by tenant/signal. Authenticate producers and readers, encrypt traffic, redact before persistence, restrict debug endpoints, audit queries, and test deletion/retention. Publish cost per million spans, million metric points, and GiB of logs plus top cardinality and retention drivers.

## Explicit success rubric

| User claim | Passing evidence |
|---|---|
| Diagnosability | A blind reviewer isolates four injected application faults within ten minutes using documented queries. |
| Data quality | Required context survives service boundaries; loss, sampling, and staleness are visible. |
| Safety | Secret canaries never reach storage and tenants cannot query each other's signals. |
| Resilience | Backpressure bounds application impact and recovery behavior matches the stated delivery contract. |
| Economics | Enforced budgets keep peak scenario cost within the published envelope. |

## Stretch work

Add exemplars between metrics and traces, adaptive sampling, or a formal telemetry quality scorecard.

## Authoritative sources

- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)
- [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

## Mapped modules

[09 Backend Engineering](../../09-backend-engineering/README.md), [17 Distributed Systems](../../17-distributed-systems/README.md), [18 Observability](../../18-observability/README.md), [19 Site Reliability Engineering](../../19-sre/README.md), and [20 Security](../../20-security/README.md).
