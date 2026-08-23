# 09 — Backend Engineering

Turn untrusted requests into authorized, durable work with explicit API contracts, queue semantics, concurrency limits, and measured performance. Read the lessons in order: each boundary makes the failure model more concrete.

## What you will learn

By the end, you can:

- design versioned APIs with validation, pagination, idempotency, and stable error contracts;
- separate authentication, session handling, and resource-level authorization;
- make database and message-broker boundaries honest about duplicate delivery;
- propagate deadlines and cancellation while bounding queues and concurrency;
- diagnose latency using saturation, profiles, traces, and load tests; and
- deploy and shut down services without dropping accepted work or hiding overload.

## Lessons

1. [Request Handling and API Contracts](./01-request-handling-and-api-contracts.md)
2. [State, Idempotency, and Background Work](./02-state-idempotency-and-background-work.md)
3. [Reliability and Observability](./03-reliability-and-observability.md)
4. [Authentication, Authorization, and API Evolution](./04-authentication-authorization-and-api-evolution.md)
5. [Queues, Delivery, and Workflow State](./05-queues-delivery-and-workflow-state.md)
6. [Concurrency, Backpressure, and Performance](./06-concurrency-backpressure-and-performance.md)

## Practice

[Build and Overload a Bounded Worker Service](./lab-bounded-worker-service.md) asks you to implement a small standard-library service, preserve request and idempotency contracts, queue bounded work, induce overload, and explain every observed outcome.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can map each response to a contract boundary, prove an authorization decision at the object level, explain duplicate delivery without promising exactly-once magic, derive a concurrency bound, and use a profile or trace to change the correct bottleneck.

## Next

Start with [Request Handling and API Contracts](./01-request-handling-and-api-contracts.md).
