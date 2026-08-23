# Lab: Design a production document intelligence service

You are responsible for a multi-tenant service that ingests private documents and offers cited search, interactive answers, and asynchronous evaluation. The exercise is complete when another engineer can challenge the design, reproduce its arithmetic, and operate its failure paths without private explanation.

## Scenario

- 200 enterprise tenants; the largest may produce 30 percent of peak traffic.
- 20 million source documents at launch, growing 4 percent monthly.
- Interactive traffic averages 250 requests per second, peaks at 1,500, and has a 3,000-request-per-second launch burst.
- Interactive p95 must remain below 2.5 seconds for admitted requests. Batch work has a four-hour completion objective.
- Tenant isolation and cited provenance are invariants. Confirmed deletion must disappear from interactive retrieval within 30 minutes.
- One model provider and one region may fail. Product accepts cited search without generation as a degraded mode.
- The initial monthly infrastructure and provider budget is $180,000.

## Deliverables

Produce a reviewable packet containing:

1. A requirements table with actors, journeys, conditions, SLOs, invariants, non-goals, assumptions, and owners.
2. Capacity math with units for arrival, concurrency, tokens, storage, indexing, queue drain, provider quota, failover, and sensitivity to tenant skew.
3. A context diagram and component diagram. Mark authority, trust, failure, and team boundaries.
4. API contracts for ingestion, job status, retrieval, deletion, pagination, idempotency, quota errors, and compatibility.
5. A data model naming identity, system of record, indexes, projections, versions, partitioning, retention, and deletion propagation.
6. A consistency table. For each invariant, name the serialization point, stale behavior, idempotency mechanism, and repair path.
7. Cache and queue policies, including keys, unsafe staleness, coalescing, ordering scope, retries, dead-letter ownership, fairness, and backpressure.
8. A reliability model with dependency budgets, overload priorities, degraded modes, RPO, RTO, failover capacity, and a restore drill.
9. A threat model covering tenant isolation, operator access, prompt injection, tool authority, exports, secrets, audit, abuse, and spend.
10. An observability plan with journey SLIs, trace decomposition, bounded labels, privacy controls, actionable alerts, and runbooks.
11. Monthly and marginal cost models with quality and reliability guardrails.
12. An AI evaluation plan with baseline, representative slices, retrieval and answer measures, human adjudication, rollout, and lineage.
13. A compatible migration plan from one embedding model to another, with reconciliation, rollback, and deletion.
14. A decision log and a list of the five assumptions most likely to overturn the design.

## Required evidence

Your arithmetic must be reproducible. Every important diagram element must trace to a requirement, invariant, or measured constraint. Every retry must have a budget. Every durable copy must have an owner and deletion story. Every dashboard must answer an operational question. Every accepted risk must name who may accept it.

## Failure injection

Revise the packet after all of these occur together:

- The primary model provider throttles half of calls for 25 minutes.
- A parser release causes one percent of documents to produce empty chunks.
- One tenant sends 45 percent of interactive traffic.
- The queue delivers duplicates and one partition stops advancing.
- An access revocation arrives while answer-cache entries remain warm.
- The healthy region has only 60 percent of global peak capacity.

Show admission, degradation, detection, response, reconciliation, and recovery. State which objectives are missed and why. Do not silently change an invariant.

## Review rubric

A strong submission is bounded, numerate, falsifiable, and operable. It distinguishes authoritative and derived state; separates latency, correctness, quality, security, and cost; treats migration as a series of observable states; and names uncomfortable unknowns. A weak submission uses vendor names as reasoning, relies on unbounded queues or retries, calls all data eventually consistent, or claims rollback without addressing new data.

## Completion

Proceed to the [adversarial design review lab](91-adversarial-design-review-lab.md) with a packet that contains no unresolved placeholder hidden as a fact.
