# Project: Title

## Status

Planned / Discovery / Building / Operating / Graduated

## Problem

Define the user, job, current pain, constraints, and evidence that the problem is worth solving.

## Goals and Non-Goals

### Goals

- Measurable outcome

### Non-Goals

- Explicitly excluded scope

## Users and Workloads

Describe actors, scale, access patterns, critical journeys, and misuse cases.

## Requirements

### Functional

- Required behavior

### Quality Attributes

| Attribute | Measure / target | Rationale |
|---|---|---|
| Reliability |  |  |
| Performance |  |  |
| Security |  |  |
| Operability |  |  |
| Cost |  |  |

## Constraints and Assumptions

List fixed boundaries; identify assumptions that require measurement.

## Architecture

```mermaid
flowchart LR
    User --> API
    API --> ControlPlane[Control plane]
    ControlPlane --> DataPlane[Data plane]
    DataPlane --> Evidence[Operational evidence]
```

Describe components, contracts, ownership, data/control flows, trust boundaries, and failure domains.

## Data and State

Define schemas, ownership, lifecycle, consistency, migration, backup, retention, and deletion.

## APIs and Contracts

Specify interfaces, identity, validation, idempotency, versioning, quotas, status, and error semantics.

## Failure Model

| Failure | User symptom | Detection | Containment | Recovery |
|---|---|---|---|---|
|  |  |  |  |  |

## Security and Threat Model

Identify assets, actors, entry points, trust boundaries, abuse cases, mitigations, and residual risk.

## Observability and SLOs

Define user-centered SLIs, objectives, telemetry, debugging paths, and alert ownership.

## Capacity and Cost Model

Estimate demand, bottlenecks, headroom, scaling thresholds, and dominant unit costs. Record measurements.

## Delivery and Rollback

Describe build provenance, tests, environments, promotion, migrations, canaries, rollback, and recovery.

## Build Plan

Sequence thin vertical slices that produce testable evidence.

## Break and Recovery Plan

List controlled failure experiments, safeguards, expected signals, and recovery proof.

## Decision Log

| Decision | Alternatives | Rationale | Revisit trigger |
|---|---|---|---|
|  |  |  |  |

## Graduation Evidence

Map evidence to the criteria in [PROJECTS.md](../PROJECTS.md): user value, implementation, reliability, security, operations, communication, and independent evaluation.

## References

Use official documentation, standards, primary papers, and linked architecture decisions.
