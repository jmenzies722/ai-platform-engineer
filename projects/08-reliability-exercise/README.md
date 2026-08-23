# 08 — Reliability Review and Incident Exercise

Take ownership of a deliberately fragile service in a standalone repository and improve its reliability using measured risk, not a rewrite.

## Problem and participants

Users experience intermittent latency and lost work, but the team lacks an SLO, capacity model, or tested recovery path. Service owners, incident commanders, support, and product stakeholders need a shared definition of reliability and evidence for investment choices. The exercise evaluates operational judgment as much as code.

## Constraints and scenario

- Begin from a documented flawed baseline with at least three interacting failure modes.
- Preserve the external contract and make changes incrementally through canaries.
- Use a fixed error-budget and infrastructure budget; reliability work must expose tradeoffs.
- Do not hide faults with unlimited retries, overprovisioning, or manually edited evidence.

## Architecture expectations

Map critical user journeys, dependencies, queues, storage, caches, timeouts, retries, overload boundaries, and recovery state. Define service and dependency SLIs from the user's perspective. Establish failure domains and invariants for accepted work. Every mitigation must state which risk it reduces, which new risk it creates, and how rollback works.

## Milestone plan

1. Baseline correctness, SLI history, load shape, capacity, dependency budgets, and top risks.
2. Define SLO/error-budget policy and make the first alerts and runbooks actionable.
3. Fix the highest expected-loss risks with tested overload, retry, and recovery behavior.
4. Facilitate a surprise incident, complete a blameless review, and prioritize the reliability backlog.

## Required artifacts

- Service map, risk register/FMEA, SLO and error-budget policy, capacity model, and decision log.
- Load-test dataset, dashboards, alert evaluations, runbooks, and recovery proof.
- Incident packet: inject plan, safeguards, timeline, communications, postmortem, and tracked actions.
- Before/after report comparing availability, latency, lost work, toil, and spend.

## Tests and failure drills

Cover invariants, retry/idempotency, timeout propagation, overload, migration, and recovery. Drill dependency latency, partial database outage, queue backlog, cache stampede, instance churn, stale configuration, bad deploy, telemetry loss, and backup corruption. Include one compound incident where a plausible first diagnosis is wrong.

## Observability, security, and cost

Alert on user-impacting symptoms and exhausted risk budgets, with diagnostic telemetry for saturation, queue age, dependency budgets, and data integrity. Keep incident access least-privileged, sanitize shared evidence, audit emergency actions, and time-limit break-glass credentials. Quantify mitigation cost, reserved headroom, observability spend, downtime exposure, and the opportunity cost of the reliability backlog.

## Explicit success rubric

| Capability | Graduation threshold |
|---|---|
| Reliability definition | SLIs are user-centered, SLO math is reproducible, and policy drives a real release decision. |
| Incident response | Team detects, coordinates, mitigates, and recovers the blind incident within declared objectives. |
| Learning | Postmortem distinguishes trigger, contributing conditions, and systemic actions without blame. |
| Improvement | Repeated baseline tests show meaningful risk reduction without contract breakage or hidden cost. |
| Sustainability | Alerts are actionable, runbooks work for a new responder, and backlog priorities follow evidence. |

## Stretch work

Run a game day with human role rotation, build a probabilistic availability model, or test graceful regional evacuation in simulation.

## Authoritative sources

- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)
- [NIST Computer Security Incident Handling Guide, SP 800-61](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [AWS Builders' Library](https://aws.amazon.com/builders-library/)

## Mapped modules

[11 Software Architecture](../../11-software-architecture/README.md), [17 Distributed Systems](../../17-distributed-systems/README.md), [18 Observability](../../18-observability/README.md), [19 Site Reliability Engineering](../../19-sre/README.md), [20 Security](../../20-security/README.md), and [35 Senior and Staff Engineering](../../35-senior-staff-engineering/README.md).
