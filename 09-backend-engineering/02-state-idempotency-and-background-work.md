# State, Idempotency, and Background Work

Reliable backends make state transitions and retry behavior explicit, especially when work crosses process boundaries.

## Why it matters

A client that receives a timeout after submitting a charge cannot know whether the server committed it and lost the response. Blind retry may charge twice; refusing retry may leave the user uncertain. Idempotency keys and explicit job state turn that ambiguity into a recoverable protocol rather than a hope that failures happen at convenient boundaries.

## How it works

An idempotent operation can be repeated without changing the intended result after the first success. Servers can attach an idempotency key to a stored outcome. Background queues decouple acceptance from completion; workers claim jobs, record outcomes, and retry transient failures with limits.

An idempotency key names one logical operation within a documented caller and endpoint scope. The server must atomically claim a new key with request identity or detect an existing claim, then return the stored outcome or a compatible in-progress result. Comparing a hash of relevant input prevents accidental key reuse for different work. A queue separates acceptance from execution: producers persist jobs, workers claim them, perform bounded work, and record outcome before acknowledgment according to queue semantics. Because a worker can fail between side effect and acknowledgment, at-least-once delivery requires idempotent effects or deduplication. States such as pending, running, succeeded, retryable failure, and terminal failure need legal transitions and timestamps. Backoff, jitter, attempt limits, and a dead-letter path bound repeated failure.

## See it yourself

Predict that both calls with `request-7` return the same logical charge ID and leave one entry in `seen`. Changing the amount under the same key should prompt you to define rejection rather than silently returning unrelated prior work.

```bash
python3 - <<'PY2'
seen={}
def charge(key, amount):
    if key not in seen: seen[key]={'id':len(seen)+1,'amount':amount}
    return seen[key]
print(charge('request-7', 50)); print(charge('request-7', 50))
PY2
```

Expected observation: The same key returns the original outcome rather than creating a second logical charge. Real implementations need atomic storage.

Limits of the state, idempotency, and background work observation: The dictionary is not atomic across threads or processes, does not persist through restart, and does not coordinate a real payment provider. It illustrates identity reuse only.

## Where it shows up

Webhook ingestion commonly returns quickly after storing provider event ID and payload, then processes in the background. Providers retry on timeout, so a unique event ID prevents duplicate logical application even when delivery repeats. Operators can inspect pending age, attempts, and terminal reason instead of guessing from an HTTP acknowledgment. The downstream business transition still needs its own atomic or idempotent guard.

## When it breaks

Duplicate effects indicate missing scope, non-atomic claim, or an unguarded downstream side effect; jobs stuck running suggest a lost worker and absent lease expiry; a growing retry queue suggests permanent errors classified as transient. First query one logical key or job ID across state history, attempts, worker ownership, and side-effect records. Pause or quarantine only the affected class before replaying; replay without understanding the commit point reproduces damage.

## Practice

**Build:** persist an idempotency record and bounded job state machine in SQLite, including input hash and attempt count. **Break:** terminate a worker after the side effect but before acknowledgment, then retry the same key without duplicating the logical result. **Explain back:** mark every possible crash point and what the next worker observes. Success is one durable outcome per key, legal state transitions, bounded retries, and a queryable terminal reason.

## Check yourself

1. Why is a timeout not proof of failure?
2. What storage property does an idempotency-key check need?

## Sources

### REQUIRED

- [HTTP idempotent methods](https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2)

### RECOMMENDED

- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/)

### DEEP DIVE

- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)

## Next

Continue to [Reliability and Observability](./03-reliability-and-observability.md).
