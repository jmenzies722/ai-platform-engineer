# Lab: Architecture a Checkout Change

Design the addition of scheduled delivery to an existing checkout system without hiding the migration or failure model.

## Starting system

Assume a modular monolith with checkout, pricing, payment, and fulfillment modules in one process and one PostgreSQL cluster. Modules have separate schemas, but checkout currently writes a fulfillment table directly. A web client expects checkout to finish synchronously. Deployments replace instances gradually.

The new feature lets a customer select a delivery window. Fulfillment must reserve capacity, payment must not be captured for an impossible window, and support needs a coherent status. Peak checkout latency must remain under a stated budget. The team can operate PostgreSQL and one message broker but has no dedicated service platform.

## Map before choosing

Produce four views:

1. code dependencies between modules;
2. runtime calls with deadlines and failure responses;
3. authoritative data, derived copies, and write paths;
4. deployment units and accountable owners.

Trace one current checkout change through all four. Mark the direct fulfillment write as a policy bypass and list the invariant it can violate.

## Compare styles

Design at least these options:

- repair the modular monolith boundary;
- extract fulfillment into a service;
- coordinate reservations through events.

For each, evaluate a concrete latency scenario, broker outage, database outage, duplicate request, deployment rollback, capacity hot spot, and on-call diagnosis. Include translation and operational costs. A style name without runtime and data consequences earns no credit.

## Make the decision

Write an ADR with context, decision, two credible alternatives, consequences, owner, status, and review triggers. State why the chosen deployment boundary matches current operating capability. Define:

- who owns delivery-window capacity;
- the consistency promised between selection and confirmation;
- idempotency keys and transaction boundaries;
- compensation for ambiguous payment or reservation;
- observability needed to locate a stuck checkout.

## Evolve safely

Plan an expand-and-contract rollout across schema, code, API, and events. Include old and new instances running together, a resumable backfill if required, read switching, reconciliation, rollback, and deletion criteria. Every dual-write or feature flag needs an owner, metric, and expiry date.

Create fitness functions for forbidden writes, module dependencies, API or event compatibility, latency budget, and recovery behavior. Then inject:

1. an old client omitting the delivery window;
2. duplicate reservation delivery;
3. payment success followed by timeout;
4. broker lag;
5. partial backfill;
6. rollback to an old instance.

For each, write expected state, evidence, operator action, and what remains uncertain.

## Deliverable

Submit the four views, option matrix, ADR, rollout state machine, fitness checks, and failure notebook. Finish with the strongest evidence that would cause you to supersede the ADR.

Success means one owner controls each invariant, no step assumes distributed rollback, mixed-version operation is safe, every temporary mechanism has deletion criteria, and an operator can repair partial progress without editing several owners’ tables.
