# Idempotency and external identity

Idempotency means repeating an operation under the same intent has the same externally visible effect. A control plane achieves it by coupling stable resource identity, request identity, external lookup, and state-aware retry rather than assuming calls execute exactly once.

## Why it matters

A timeout means the caller does not know whether a side effect occurred. Blind retries can create duplicate accounts, databases, charges, or messages. Avoiding retries instead leaves intent permanently unconverged.

## How it works

Give every control-plane resource an immutable internal identifier. Derive or store a stable external correlation identifier that survives worker restart, rename, and status-write failure. Pass provider idempotency keys where supported, but also observe by external ID or unique ownership tags before creating.

Separate operation identity from resource identity. A create request may reuse the resource key across retries, while a later resize needs a distinct operation key tied to desired generation. Persist operation intent before the side effect when possible and record provider operation IDs in status.

Design each state transition for retry. Create handles already-present with matching ownership as success, but treats a conflicting object as an ownership error. Update compares desired and observed values. Delete treats confirmed absence as success. Never convert an ambiguous provider timeout into absent without observation.

Exactly-once execution across an API and external provider generally requires a shared transaction they do not have. Use at-least-once attempts with idempotent effects, reconciliation, deduplication, and explicit unknown state.

## Vocabulary

- **idempotency key:** stable token identifying one logical operation
- **external identity:** durable correlation to the provider-side object
- **ambiguous outcome:** side effect whose success is unknown to the caller
- **deduplication:** recognizing repeated delivery of one logical operation

## See it yourself

Trace create with four crash points: before provider call, after provider success, after external ID persistence, and after status update. Predict each retry. A stable key plus external lookup prevents duplicate creation after every point. A random name generated on each attempt defeats the guarantee.

## Where it shows up

An account controller tags the provider account with immutable control-plane UID and tenant. After a timeout, it searches by UID, validates ownership and requested parent, records the account ID, and continues. Display-name collision is never accepted as proof of identity.

## When it breaks

Idempotency keys expire before retries, keys are reused for different intent, provider search is eventually consistent, and ownership tags are mutable. Status loss disconnects resources from billable objects. Monitor duplicate-key conflicts, ambiguous-operation age, unassociated external inventory, adoption of external IDs, and manual import events.

## Practice

**Observe:** enumerate every side effect in one controller and document idempotency key, lookup, conflict semantics, and crash recovery.

**Build:** write a create/update/delete state table for a bucket resource across desired state, observed external state, prior operation, and next action.

**Break:** timeout after provider success, delay provider search, and reuse a key with changed intent. Demonstrate no duplicate creation and actionable unknown or conflict status.

**Say it out loud:** explain why HTTP method idempotency does not prove provider-side retry safety.

## Check yourself

1. Why are display names weak external identity?
2. When should “already exists” be success versus conflict?
3. What must happen when external observation is temporarily inconclusive?
4. Why is exactly-once execution usually the wrong control-plane model?

## Sources

### REQUIRED

- [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [RFC 9110: Idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)

### DEEP DIVE

- [Kubernetes API conventions: idempotency](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency)

## Next

Continue to [Ownership, deletion, and finalizers](05-ownership-deletion-and-finalizers.md).
