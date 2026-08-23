# Integration, Consistency, and Data Flow

System integration is the design of contracts across ownership, time, and partial failure.

## Why it matters

Two services writing the same table can preserve neither service’s invariants. A synchronous call can make a simple request depend on a distant outage. An event can decouple availability yet surprise readers with stale or reordered state. Integration decisions must say who owns truth, when another component may observe it, and how failures converge.

## How it works

Synchronous request-response provides an immediate outcome within a deadline and fits decisions that need a current answer. It couples caller availability and latency to the callee unless the caller has a fallback or can reject. Asynchronous messaging lets producers proceed after durable acceptance and lets consumers work later, but introduces lag, duplicate delivery, ordering scope, backlog operations, and reconciliation.

Data ownership means one component is authoritative for an invariant and controls writes through a contract. Other components may hold read models, caches, search indexes, or warehouses derived from published change. Those copies need provenance, freshness signals, rebuild procedures, and a policy for deletion or correction. Shared reads can still couple schemas and release timing; shared writes are more dangerous because they bypass policy.

Consistency is a user-visible contract, not a database adjective. Examples include read-your-writes for an actor, monotonic reads during a session, causal ordering between related actions, or eventual convergence within a stated bound. A workflow that crosses owners cannot rely on one local transaction. It records durable steps, uses idempotent messages, and applies compensating business actions when later steps fail. A saga is this coordination pattern, not automatic rollback.

Contract evolution includes syntax and semantics. APIs can add optional fields and tolerate unknown fields. Events should identify schema and event type, preserve old meaning, and avoid using a shared internal object as every consumer’s contract. Consumer-driven tests can reveal known expectations but do not find unknown consumers. A schema registry checks structural compatibility; it cannot prove semantic compatibility.

## See it yourself

Predict that duplicate and older events do not regress the read model.

```bash
python3 - <<'PY'
view = {}
def apply(event):
    current = view.get(event["id"])
    if current is None or event["version"] > current["version"]:
        view[event["id"]] = event
for e in [
    {"id":"order-1", "version":2, "state":"paid"},
    {"id":"order-1", "version":2, "state":"paid"},
    {"id":"order-1", "version":1, "state":"open"},
]:
    apply(e)
print(view["order-1"])
PY
```

Expected observation: a per-aggregate version makes these duplicate and out-of-order applications idempotent.

Limits of the observation: a dictionary is not durable, concurrent handlers can race, missing versions are not detected, and one aggregate version does not establish ordering across aggregates.

## Where it shows up

Checkout needs a current authorization from payment, then records an order and outbox event locally. Fulfillment consumes that event later. Customer support reads a composed view showing each source timestamp rather than implying one atomic snapshot. Refund is an explicit stateful workflow with idempotent provider calls and manual repair for ambiguous outcomes.

## When it breaks

Growing projection lag creates stale reads; schema parse errors reveal structural incompatibility; semantically valid but wrong values point to meaning drift; repeated workflow compensation suggests an unstable dependency or invalid boundary. First capture owner, contract version, operation or event ID, source commit position, publication and consumption times, retry count, projection version, and invariant violation. Stop destructive replay until handlers are idempotent and ordering assumptions are documented.

## Practice

**Build:** design one cross-boundary order flow using synchronous decisions, outbox events, a versioned read model, and compensation. **Break:** duplicate, delay, reorder, and omit events; make a synchronous dependency time out after committing. **Explain back:** state the consistency observed by customer, operator, and finance. Success includes replay from source, bounded staleness telemetry, an ownership table, and a manual repair path for ambiguous effects.

## Check yourself

1. Why is a schema-compatible event change still capable of breaking consumers?
2. Which consistency guarantee is needed when a user must see a change they just made?

## Sources

### REQUIRED

- [RFC 9413: Maintaining Robust Protocols](https://www.rfc-editor.org/rfc/rfc9413)
- [CloudEvents Specification](https://github.com/cloudevents/spec)

### RECOMMENDED

- [Martin Fowler: Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html)
- [Microservices.io Saga Pattern](https://microservices.io/patterns/data/saga.html)

### DEEP DIVE

- [Designing Data-Intensive Applications](https://dataintensive.net/)

## Next

Continue to [Evolutionary Architecture and Decision Practice](./06-evolutionary-architecture-and-decision-practice.md).
