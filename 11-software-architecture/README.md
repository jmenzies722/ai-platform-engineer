# 11 — Software Architecture

Design systems as explicit boundaries, runtime interactions, data ownership, and reversible decisions. Read the lessons in order: no architecture style is allowed to hide its coupling, consistency, deployment, or operational bill.

## What you will learn

By the end, you can:

- identify cohesion, coupling, information hiding, and dependency direction in a real change;
- turn quality attributes into measurable scenarios and decision records;
- compare layered, ports-and-adapters, modular-monolith, service, event-driven, and pipe styles;
- assign data ownership and consistency without shared-write ambiguity;
- evolve APIs, schemas, events, and deployments through compatible intermediate states; and
- use fitness functions and operational evidence to revisit decisions responsibly.

## Lessons

1. [Boundaries, Coupling, and Cohesion](./01-boundaries-coupling-and-cohesion.md)
2. [Quality Attributes and Decisions](./02-quality-attributes-and-decisions.md)
3. [Data Ownership and Evolution](./03-data-ownership-and-evolution.md)
4. [Architecture Styles and Deployment Boundaries](./04-architecture-styles-and-deployment-boundaries.md)
5. [Integration, Consistency, and Data Flow](./05-integration-consistency-and-data-flow.md)
6. [Evolutionary Architecture and Decision Practice](./06-evolutionary-architecture-and-decision-practice.md)

## Practice

[Architecture a Checkout Change](./lab-architecture-evolution.md) follows one feature through boundaries, quality scenarios, data ownership, failure modes, an ADR, and a compatible rollout.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can show why a boundary exists, compare two styles against quality scenarios, name every data owner, narrate partial failure, design expand-and-contract evolution, and state the evidence that would reverse an ADR.

## Next

Start with [Boundaries, Coupling, and Cohesion](./01-boundaries-coupling-and-cohesion.md).
