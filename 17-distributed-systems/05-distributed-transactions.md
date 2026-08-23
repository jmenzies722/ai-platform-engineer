# Transactions, sagas, and the outbox

A distributed business operation must state which invariants are atomic and how incomplete work is repaired. A transaction protocol can coordinate storage commits; it cannot make remote side effects reversible.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Two-phase commit asks participants to prepare durable intent, then commit or abort. It preserves atomicity under its assumptions but can block when the coordinator’s decision is unavailable. A saga decomposes work into local transactions with compensations; compensation is a new business action, not time travel, and may itself fail.

The transactional outbox writes domain state and an event in one local transaction. A relay publishes pending events at least once, so consumers deduplicate. Inbox records provide consumer-side identity. Reconciliation compares desired and observed state after ambiguous failures.

## See it yourself

Suppose order state and outbox insertion commit in one database transaction. There is no history where the order exists but its outbox row does not. Publishing can still happen twice if the relay crashes after publish and before marking sent; atomic storage removes message loss, while idempotency handles duplication.

## Where it shows up

Order fulfillment, money movement, provisioning, and email delivery mix reversible and irreversible effects. Define a state machine, durable operation identifier, terminal states, compensation owner, and reconciliation query before choosing orchestration or choreography.

## When it breaks

A prepared participant can hold locks, compensations can violate newer decisions, event ordering can differ by aggregate, and a relay backlog can make committed state invisible downstream. Inspect transaction IDs, state transitions, outbox age, publish attempts, and consumer inbox records.

## Practice

Build an order state machine with inventory reservation and an outbox. Crash after local commit but before publish, then restart the relay. Completion means the event is eventually delivered, duplicate delivery changes no domain state, and every nonterminal operation is queryable.

## Check yourself

1. Why can two-phase commit block?
2. What guarantee does a transactional outbox add?
3. Why must outbox consumers remain idempotent?
4. When is compensation unsafe without a version check?

## Sources

### REQUIRED

- [Transaction Processing: Concepts and Techniques](https://www.microsoft.com/en-us/research/publication/transaction-processing-concepts-techniques/)

### RECOMMENDED

- [AWS Prescriptive Guidance: Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

### DEEP DIVE

- [Sagas](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)

## Next

[Idempotency, retries, and uncertain outcomes](06-idempotency-and-retries.md)
