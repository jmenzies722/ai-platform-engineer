# Concurrency, Backpressure, and Performance

Fast backends bound work, propagate budgets, and shed excess load before queues turn overload into an outage.

## Why it matters

Adding request workers can raise throughput until a database pool, CPU, memory allocator, or downstream service saturates. After that point, extra concurrency increases queueing and timeouts, retries add more work, and the service appears both busy and idle in the wrong places. Performance engineering begins with demand, capacity, and measured waiting.

## How it works

Concurrency is work in progress; parallelism is work executing simultaneously. For a stable system, average concurrency relates to throughput and time in system through Little’s Law. If a service completes 200 requests per second at 100 milliseconds average latency, roughly 20 requests are in the system on average. Tail distributions matter: a small slow fraction can hold most workers.

Bound each scarce resource with a semaphore, pool, queue, or admission policy derived from measured capacity. An unbounded in-memory queue accepts obligations the process may never fulfill and converts overload into memory growth and stale work. Backpressure slows producers when possible; load shedding rejects early with a useful signal when waiting cannot meet the deadline.

A request deadline is an end-to-end budget, not a fresh timeout for every hop. Reserve time for response and cleanup, propagate cancellation, and stop abandoned work. Retries need a budget, backoff, jitter, idempotency, and a limited set of transient errors. Hedged requests can reduce tails for suitable read operations but consume additional capacity.

Measure throughput, errors, latency distributions, saturation, queue depth and age, and resource profiles together. A CPU profile finds where sampled execution time accumulates; allocation and heap profiles explain memory churn and retention; lock and block profiles expose contention. Distributed traces show critical-path spans but sampling can miss rare faults. Load tests need realistic request mix, data, connection reuse, warm-up, and coordinated-omission awareness. Optimize only after a representative bottleneck is visible.

## See it yourself

Predict that only three tasks run at once and later tasks wait at the semaphore.

```bash
python3 - <<'PY'
import concurrent.futures, threading, time
gate = threading.Semaphore(3)
active = peak = 0
lock = threading.Lock()
def work(i):
    global active, peak
    with gate:
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.03)
        with lock:
            active -= 1
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    list(pool.map(work, range(12)))
print("peak", peak)
PY
```

Expected observation: executor size is twelve, but the protected resource sees peak concurrency three.

Limits of the observation: sleeping models waiting rather than CPU work, no request deadline expires, and fairness is unspecified. This does not prove three is an appropriate production limit.

## Where it shows up

An image service accepts uploads, decodes with a CPU semaphore, stores with a bounded client pool, and queues asynchronous derivatives. Admission checks body size and current capacity before expensive decoding. Shutdown marks the instance unready, rejects new work, drains within the deployment budget, cancels leftovers, and records unfinished durable jobs for redelivery.

## When it breaks

Rising latency with flat throughput and high saturation indicates a capacity ceiling; low CPU with pool wait points to a dependency or lock; memory growth with queue age suggests unbounded admission; client cancellations while server work continues reveal missing propagation. First preserve traffic rate, latency histogram, error class, in-flight count, queue age, pool waits, dependency timings, and profiles during the same interval. Do not increase every timeout or worker count simultaneously.

## Practice

**Build:** implement the module lab with bounded admission, per-operation deadlines, cancellation, idempotency, and graceful shutdown. **Break:** slow a dependency, exceed queue capacity, disconnect clients, and trigger shutdown with work in flight. **Explain back:** use Little’s Law to compare expected and measured concurrency. Success includes explicit overload responses, no unbounded queue, a profile-backed optimization, and a load-test report that states its representativeness limits.

## Check yourself

1. Why can increasing worker count reduce completed throughput?
2. What is wrong with giving every downstream call the full original timeout?

## Sources

### REQUIRED

- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)
- [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/)

### RECOMMENDED

- [Amazon Builders’ Library: Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

### DEEP DIVE

- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html)

## Next

Continue to [Go](../10-go/README.md).
