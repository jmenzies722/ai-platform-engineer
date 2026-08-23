# Idempotency, retries, and uncertain outcomes

Retries are repeated attempts at one logical operation. Safe retry behavior requires a shared operation identity, atomic result recording, bounded policy, and a way to resolve uncertain outcomes.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

An idempotency key is scoped to caller and operation. The server stores key, request hash, state, result, and retention atomically with the side effect or its durable intent. A duplicate with the same hash receives the stored result; a duplicate key with a different payload is rejected. Concurrent first attempts serialize on the key.

Retry only transient failures, within an end-to-end deadline, with capped exponential backoff and jitter. Keep one retry owner where possible. Hedged requests can reduce tail latency for safe reads but increase load and need cancellation.

## See it yourself

If three layers each make one initial attempt plus two retries, one user request can produce `3 × 3 × 3 = 27` database attempts. Moving retry ownership to one layer reduces the worst case to three. This arithmetic is why local retry defaults are a system-wide capacity decision.

## Where it shows up

Payment APIs, webhook receivers, controllers, and job workers all see reply loss after commit. Return operation status endpoints and stable results. Retain keys at least through the maximum retry and replay horizon, subject to privacy and storage policy.

## When it breaks

Keys can be reused across payloads, records can expire while clients still retry, retries can exceed deadlines, and “retry all errors” can amplify deterministic failure. Correlate logical operation ID, attempt number, deadline remaining, response class, and downstream attempts.

## Practice

Implement an in-memory idempotency table around a counter. Drop the first response after commit and retry concurrently. Completion means the counter changes once, all matching callers receive one stable result, and a changed payload is rejected.

## Check yourself

1. Why is an idempotent HTTP verb not enough for payment safety?
2. How does jitter change synchronized clients?
3. Where should retry budgets be enforced?
4. What retention fact bounds idempotency-record lifetime?

## Sources

### REQUIRED

- [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [Google Cloud: Retry strategy](https://cloud.google.com/storage/docs/retry-strategy)

### DEEP DIVE

- [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

## Next

[Queues, flow control, and backpressure](07-queues-and-backpressure.md)
