# Interfaces, State, and Data Flow

Useful software is a set of components exchanging values under contracts. Correctness depends as much on ownership, state transitions, and boundary rules as on the calculation inside a function.

## Why it matters

A producer can emit valid JSON and still break its consumer by changing a field from absent to `null`, changing units, or retrying a non-idempotent request. These failures cross team and process boundaries, where assumptions are harder to see and rollbacks may not restore old data. A precise interface states syntax, meaning, ownership, ordering, compatibility, and failure behavior.

## How it works

An interface exposes operations while hiding some implementation choices. Its contract includes accepted inputs, returned outputs, side effects, errors, timing constraints, and invariants that remain true. Data flows through representations: in-memory objects become bytes, cross a file, pipe, socket, or database boundary, and are parsed into new objects. Serialization preserves only what its schema defines; it does not preserve object identity or undocumented meaning.

State is information whose current value depends on prior events. A state machine names allowed states and transitions, making illegal transitions testable. Ownership answers who may mutate or release a resource. Immutable values simplify sharing; mutable state requires a clear writer and synchronization when access overlaps. At remote boundaries, delivery may be delayed, duplicated, reordered, or lost. An idempotent operation produces the same intended state when repeated with the same key, which makes retries safer, but does not make every side effect free. Backward compatibility requires new producers and old consumers to agree during rollout, often by adding optional fields before removing old ones.

## See it yourself

**Tiny Proof:** predict that two identical `set` commands leave one final state, while two identical `increment` commands change it twice. The distinction is operation semantics, not JSON syntax.

```bash
python3 - <<'PY2'
state = {"quota": 10}
def apply(message):
    if message["op"] == "set":
        state["quota"] = message["value"]
    elif message["op"] == "increment":
        state["quota"] += message["value"]
for command in ({"op":"set","value":20},) * 2:
    apply(command)
print(state)
for command in ({"op":"increment","value":5},) * 2:
    apply(command)
print(state)
PY2
```

Expected observation: repeating `set` stabilizes at 20; repeating `increment` reaches 30.

Limits of this proof: one dictionary has no network, concurrent writer, persistence failure, or deduplication window. It demonstrates why a retry policy depends on the operation contract, not that remote retries are automatically safe.

## Where it shows up

Payment and job APIs commonly accept an idempotency key. The server records the key and result so a client retry does not create a second logical operation. That design still needs a scope, retention period, request-equivalence rule, and transactional relationship between the recorded key and side effect. Similar reasoning applies to database migrations: deploy readers that understand both representations, then writers of the new representation, then remove the old form only after observation proves it unused.

## When it breaks

Duplicate records suggest retries crossed a non-idempotent boundary; impossible state suggests an unchecked transition or competing writer; decoding errors suggest representation drift; stale reads suggest cache or replication semantics. Preserve the original request bytes, schema or version, correlation identifier, timestamps, and observed state before replaying anything. Reproduction should use a disposable target because replay may repeat the harmful effect.

## Practice

**Build:** implement a six-state job model with explicit allowed transitions and an idempotent `complete(job_id, result)` operation. **Break:** deliver completion twice, attempt completion before start, and parse a message missing a required field. **Explain back:** separate representation validity, contract validity, transition validity, and delivery semantics. Success means tests prove every legal transition, reject every illegal transition, and show repeated completion returns the original result without a second side effect.

## Check yourself

1. Why can syntactically valid data violate an interface?
2. What must be specified before calling an operation idempotent?

## Sources

### REQUIRED

- [RFC 9110: HTTP Semantics, idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)

### RECOMMENDED

- [Protocol Buffers updating a message type](https://protobuf.dev/programming-guides/proto3/#updating)

### DEEP DIVE

- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)

## Next

Continue to [Reliability, Errors, and Observability](./05-reliability-errors-and-observability.md).
