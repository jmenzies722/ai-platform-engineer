# Queues, Delivery, and Workflow State

Queues decouple when work is accepted from when it completes, but delivery and processing remain separate facts.

## Why it matters

A worker can charge a card and crash before acknowledging its message. Redelivery is then correct broker behavior, but repeating the charge is a business failure. Reliable asynchronous systems treat duplicates, poison messages, ordering, backlogs, and partial effects as normal states with explicit evidence.

## How it works

A producer publishes a message, a broker stores or routes it under its durability contract, and a consumer receives it under a lease or visibility timeout. Acknowledgment usually tells the broker that this delivery is complete. If the lease expires or the connection fails first, another delivery may occur. “At least once” means the handler must tolerate duplicates. “At most once” permits loss. Claims of exactly-once processing apply only inside defined transactional boundaries and cannot erase an arbitrary external effect.

An idempotency key names a logical operation. A consumer can atomically record that key and its result with local state, returning the saved outcome on redelivery. The transactional outbox writes domain state and an event in one database transaction; a publisher later sends unsent rows and may send duplicates. An inbox or processed-message table deduplicates at the consumer. These patterns trade storage and cleanup for a truthful local atomic boundary.

Ordering is scoped. A partition may preserve broker order while retries, concurrent consumers, and downstream calls reorder effects. Partitioning by aggregate ID can serialize one entity at the cost of hot partitions. Workflows model durable state transitions and compensation rather than holding a thread or database transaction across services. Compensation is a new business action, not time travel.

Backlog age often matters more than message count because arrival and service rates vary. Retry delays need exponential backoff, jitter, attempt limits, and an error classification. A dead-letter queue is quarantine requiring ownership, alarms, inspection, replay tooling, and retention; it is not successful processing.

## See it yourself

Predict that the duplicate delivery returns the first result and increments the effect counter only once.

```bash
python3 - <<'PY'
done, effects = {}, 0
def handle(message_id):
    global effects
    if message_id in done:
        return done[message_id]
    effects += 1
    done[message_id] = f"receipt-{effects}"
    return done[message_id]
print(handle("order-7"), handle("order-7"), "effects", effects)
PY
```

Expected observation: a stable key collapses sequential duplicate attempts to one modeled effect.

Limits of the observation: the dictionary check and effect are not durably atomic, concurrent workers can race, and no crash is injected. Real deduplication requires a transaction or an idempotent downstream contract.

## Where it shows up

Order placement writes the order and `OrderAccepted` outbox row together. A publisher emits it. Fulfillment records the event ID before reserving stock in the same local transaction. Email delivery uses the order ID as provider idempotency metadata when supported. A workflow records each durable step and compensation, letting operators answer where an order stopped without reconstructing truth from log lines.

## When it breaks

Oldest-message age rising means service rate is below arrival rate or consumers are stalled. Rapid redelivery suggests a visibility timeout shorter than processing or lost acknowledgments. One partition lagging suggests a hot key. DLQ growth identifies terminally classified attempts, not root cause. Capture message ID, logical operation key, enqueue time, receive count, lease deadline, handler version, state transition, acknowledgment, and downstream request ID. Pause replay before flooding a damaged dependency.

## Practice

**Build:** implement a bounded worker with a durable operation table, explicit states, retry classification, jitter, and a quarantine path. **Break:** crash after the side effect but before acknowledgment, exceed the lease, submit a poison payload, and create a hot partition. **Explain back:** identify which boundary can duplicate or lose each effect. Success includes safe replay, backlog-age alerting, deduplication under concurrent delivery, and a documented retention policy.

## Check yourself

1. Why does acknowledging after a side effect create a duplicate window?
2. What operational work is required for a dead-letter queue to be useful?

## Sources

### REQUIRED

- [Amazon Builders’ Library: Avoiding Insurmountable Queue Backlogs](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/)
- [CloudEvents Specification](https://github.com/cloudevents/spec)

### RECOMMENDED

- [Enterprise Integration Patterns: Idempotent Receiver](https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html)
- [Microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html)

### DEEP DIVE

- [Life Beyond Distributed Transactions](https://queue.acm.org/detail.cfm?id=3025012)

## Next

Continue to [Concurrency, Backpressure, and Performance](./06-concurrency-backpressure-and-performance.md).
