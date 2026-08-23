# Queues, flow control, and backpressure

A queue moves work across time, but finite capacity still governs the system. Backpressure keeps admitted work within the rate at which downstream components can complete it before its value or deadline expires.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Producers enqueue durable messages; consumers claim, process, and acknowledge them. At-least-once delivery requires idempotent handling. Visibility timeouts must exceed normal processing or be extended by a live worker. Ordering is usually guaranteed only within a partition or key.

Little’s Law gives average items `L = λW`: at 1,000 arrivals per second and 30 seconds in system, expect 30,000 items. Bounded queues, concurrency limits, rate limits, load shedding, and admission control make overload explicit. Dead-letter queues isolate bounded poison work but require ownership and replay policy.

## See it yourself

If arrival rate is 120 jobs/s and sustainable service is 100 jobs/s, backlog grows by 20 jobs/s. A 12,000-item queue buys ten minutes, not resilience. The proof is conservation of work: no retry policy changes the long-run rate mismatch.

## Where it shows up

Queue age is often more useful than depth because it maps backlog to user delay. Operate per-class capacity, fairness, retry limits, and expiration. Scale consumers from service time and downstream headroom, not queue depth alone.

## When it breaks

Unbounded buffers cause memory failure; redelivery storms duplicate expensive work; poison messages cycle forever; and scaling consumers can overload the database. Inspect oldest age, arrival and completion rates, attempts, lease extensions, saturation, and downstream rejection.

## Practice

Build a bounded worker queue with a slower consumer. Measure depth and oldest age, then double arrival rate. Completion means producers receive explicit backpressure, memory remains bounded, expired work is discarded, and recovery drains without retry spikes.

## Check yourself

1. How does Little’s Law connect latency and queue depth?
2. When should a consumer acknowledge?
3. Why can autoscaling consumers worsen an incident?
4. What policy makes a dead-letter queue operationally complete?

## Sources

### REQUIRED

- [Reactive Streams Specification](https://www.reactive-streams.org/)

### RECOMMENDED

- [Google SRE: Handling overload](https://sre.google/sre-book/handling-overload/)

### DEEP DIVE

- [Queueing Systems, Volume 1](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316870)

## Next

[Observability](../18-observability/README.md)
