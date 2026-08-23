# APIs, contracts, and boundaries

An API is a promise about meaning, authority, failure, and change, not merely a transport schema.

## Why it matters

Poor contracts export internal accidents, make retries unsafe, and force every consumer to rediscover ordering, authorization, and compatibility rules.

## How it works

Design from resource identity and state transitions. Define who may request each transition, which preconditions apply, where the decision is serialized, and what response establishes success. Choose synchronous calls when the caller needs an immediate bounded result; choose asynchronous jobs when work is long, variable, or independently retryable.

Specify failure semantics as carefully as success. Distinguish invalid input, failed authorization, conflict, quota exhaustion, transient unavailability, and accepted work still in progress. Timeouts create uncertainty because the server may have committed after the caller stopped waiting. An idempotency key needs a scope, retention period, request fingerprint, and atomic relationship to the effect.

Compatibility means old and new participants can coexist during a declared window. Add fields with safe defaults, preserve unknown values where forwarding occurs, and avoid reusing identifiers or enum meanings. Pagination requires a stable ordering contract. Rate limits should expose a predictable budget and protect fairness, not function as a mysterious production switch.

## See it yourself

Suppose `POST /jobs` commits job `j7` but its response is lost. A blind retry can create `j8`. With a tenant-scoped idempotency key and durable request hash, the retry returns `j7`; reuse with different input is rejected. The contract handles an ambiguous network outcome without pretending the network provides exactly-once delivery.

## Where it shows up

An inference endpoint may accept a request synchronously but return a job handle for large inputs. The contract must define cancellation as best effort, token and concurrency quotas, model-version selection, output provenance, and whether a disconnected client changes billing or execution.

## When it breaks

APIs fail when status codes carry no actionable distinction, list endpoints lack stable pagination, authorization is delegated to callers, or schemas change without coexistence. Reconstruct one failed request using principal, request identity, idempotency record, state transition, response, and audit event before changing retry behavior.

## Practice

**Build:** specify an inference-job API with state machine, authorization matrix, idempotent creation, pagination, quotas, cancellation, and version compatibility. **Break:** lose the creation response, repeat a key with altered input, and deploy an older consumer. **Explain back:** state what each response proves and what remains uncertain.

## Check yourself

1. Why is a timeout not evidence that no work happened?
2. What makes an idempotency key safe?
3. Which compatibility promises constrain enum evolution?

## Sources

### REQUIRED

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)

### RECOMMENDED

- [Google Cloud API Design Guide](https://cloud.google.com/apis/design)

### DEEP DIVE

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)

## Next

Continue to [Data models and ownership](04-data-models-and-ownership.md).
