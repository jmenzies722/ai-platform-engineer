# Queues, streams, and asynchronous work

Asynchronous systems exchange immediate certainty for buffering, independent scaling, and replay; the design must account for every uncertainty introduced.

## Why it matters

Queues can isolate bursts and failures, yet an unbounded backlog is delayed failure, and redelivery turns careless side effects into duplicates.

## How it works

Choose a work queue when one of several workers should process a task. Choose a log or stream when multiple consumers need an ordered, replayable history. Define message identity, schema, partition key, ordering scope, retention, visibility or acknowledgment rule, retry budget, and terminal disposition.

Delivery is normally at least once. A worker acknowledges only after its durable effect is complete, and it makes repetition harmless with an idempotency record or naturally idempotent write. Use exponential backoff with jitter for transient failures. Permanent validation failures should not consume the transient retry budget. A dead-letter destination is a quarantine with ownership, alerts, inspection, replay controls, and retention, not a graveyard.

Backpressure must reach producers. Track backlog in units of time as well as count because user harm depends on age. Bound per-tenant concurrency and message size. Prefer load shedding or delayed admission when recovery time would exceed the job’s deadline. Schema evolution and replay require consumers that tolerate historical forms.

## See it yourself

A worker completes an external write, crashes before acknowledgment, and receives the same message again. Without durable identity, the side effect repeats. With an atomic processed-message record beside the local effect, the worker returns the recorded result. If the effect is remote, its API also needs idempotency; a local ledger cannot control another system’s commit.

## Where it shows up

Document ingestion separates upload, parsing, chunking, embedding, and indexing. Each stage records source version and attempt identity. Per-tenant limits preserve fairness, while activation occurs only after required outputs pass validation. Replay builds a new projection without pretending old events have new semantics.

## When it breaks

Poison messages loop forever, retries synchronize, partitions become hot, acknowledgment precedes effects, and operators cannot estimate drain time. During an incident, inspect oldest age, arrival and completion rates, failure class, retry volume, partition skew, and downstream saturation before increasing consumers.

## Practice

**Build:** design an ingestion pipeline with message contracts, partitioning, idempotency, retry classification, dead-letter operations, fairness, and replay. **Break:** poison one document, throttle the embedding provider, duplicate delivery, and create a hot tenant. **Explain back:** show where pressure is bounded and how an operator decides whether to retry, quarantine, or shed.

## Check yourself

1. Why is backlog age often more useful than backlog count?
2. What must be true before acknowledgment?
3. When does adding consumers worsen the incident?

## Sources

### REQUIRED

- [Apache Kafka documentation: Design](https://kafka.apache.org/documentation/#design)

### RECOMMENDED

- [Amazon Builders’ Library: Avoiding insurmountable queue backlogs](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/)

### DEEP DIVE

- [Google Cloud Architecture: Pub/Sub reliability guide](https://cloud.google.com/pubsub/docs/reliability-intro)

## Next

Continue to [Reliability, overload, and recovery](08-reliability-overload-and-recovery.md).
