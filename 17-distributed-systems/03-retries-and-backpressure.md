# Retries, idempotency, and backpressure

Reliable distributed work assumes attempts can be lost or repeated and ensures overload does not grow without bound.

## Why it matters

Retries improve success for transient faults but multiply load and side effects. Queues absorb bursts only until their finite capacity or latency budget is exhausted.

## How it works

A client supplies an idempotency key for one logical operation. The server atomically records the key, operation state, and result, then returns the same result for duplicates. This is stronger than merely making an HTTP method nominally idempotent.

Retries need deadlines, capped exponential backoff, jitter, and one clear retry layer. Backpressure limits admission through bounded queues, concurrency controls, rate limits, or explicit rejection. Consumers should acknowledge only after durable handling and send poison messages to a bounded dead-letter path.

## See it yourself

If three layers each retry three times, one request can cause 27 downstream attempts. Remove retries from inner layers and preserve one budget at the edge.

## Where it shows up

Payment APIs, queue consumers, webhook receivers, database clients, and controller work queues all need duplicate-safe behavior.

## When it breaks

Idempotency records expire too early, keys cover different payloads, retries exceed the caller deadline, or an unbounded queue converts overload into memory exhaustion and stale work.

## Practice

Design a `POST /payments` idempotency table including key scope, request hash, state, result, concurrency behavior, retention, and recovery after a worker crash.

## Check yourself

1. Why is backoff without jitter insufficient?
2. Where should an acknowledgement occur?

## Sources

### REQUIRED
- [AWS Builders' Library: retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### RECOMMENDED
- [Google SRE: Addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)

### DEEP DIVE
- [Reactive Streams specification](https://www.reactive-streams.org/)

## Next

[Observability](../18-observability/README.md)
