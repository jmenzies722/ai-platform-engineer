# 34 — System Design

System design is the disciplined conversion of an uncertain need into a system that can be explained, measured, operated, and changed. The work is not drawing boxes. It is making consequences visible before production makes them expensive.

## What you will learn

- Turn product language into requirements, invariants, budgets, and explicit non-goals.
- Estimate load and cost with units, ranges, sensitivity analysis, and measurement plans.
- Design APIs, data ownership, consistency, caching, queues, and overload behavior.
- Treat reliability, security, observability, and cost as architecture inputs.
- Reason about model-serving and retrieval systems without hiding uncertainty behind AI terminology.
- Evolve systems through compatible migrations and run design reviews that test claims.

## Lessons

1. [Requirements and system boundaries](01-requirements-load-and-boundaries.md)
2. [Estimation and capacity](02-estimation-and-capacity.md)
3. [APIs, contracts, and boundaries](03-apis-contracts-and-boundaries.md)
4. [Data models and ownership](04-data-models-and-ownership.md)
5. [Consistency and distributed invariants](05-consistency-and-distributed-invariants.md)
6. [Caching and derived state](06-caching-and-derived-state.md)
7. [Queues, streams, and asynchronous work](07-queues-streams-and-asynchronous-work.md)
8. [Reliability, overload, and recovery](08-reliability-overload-and-recovery.md)
9. [Security, privacy, and abuse resistance](09-security-privacy-and-abuse-resistance.md)
10. [Observability and operability](10-observability-and-operability.md)
11. [Cost and efficiency](11-cost-and-efficiency.md)
12. [Designing AI systems](12-designing-ai-systems.md)
13. [Evolution and design review](13-evolution-and-design-review.md)

## Practice

Complete the [design packet lab](90-design-packet-lab.md), then defend it in the [adversarial review lab](91-adversarial-design-review-lab.md). The packet must include requirements, capacity math, API and data contracts, failure policy, threat model, telemetry, cost model, migration, and unresolved questions.

## Ready to continue

You can trace every major component to a requirement or invariant, calculate the important limits, identify unsafe failure behavior, and state what production evidence would change the design.

## Next

Begin [Senior and Staff Engineering](../35-senior-staff-engineering/README.md).
