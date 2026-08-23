# Reliability, Errors, and Observability

Reliable software does not avoid every failure. It bounds damage, communicates what happened, and leaves enough evidence to make the next decision safely.

## Why it matters

A request that times out at the caller may still commit at the server. Blindly retrying can duplicate work; declaring failure can lie about durable state. Production systems need explicit deadlines, error categories, recovery rules, and observations tied to one operation. Logs alone are not observability when they cannot connect symptoms to state.

## How it works

A fault is an underlying defect or adverse condition, an error is an incorrect internal state, and a failure is externally visible behavior outside the contract. Defensive design validates inputs, maintains invariants, limits resource use, and contains faults so one failure does not cascade. Timeouts bound waiting; deadlines communicate the remaining budget across calls; cancellation asks obsolete work to stop. Retries help transient failures only when operations are safe to repeat, delays are bounded, and a shared dependency is not already overloaded. Exponential backoff and jitter reduce synchronized retry bursts.

Observability derives system state from outputs. Logs describe discrete events, metrics aggregate numeric behavior, and traces relate work across boundaries. Each has cost and blind spots. A useful event includes time, operation or correlation identity, outcome, and relevant dimensions without credentials or personal data. Health checks answer narrow questions: process liveness is different from readiness to accept work. Service objectives connect user-visible success and latency to an acceptable error budget; they prevent “up” from meaning only that a PID exists.

## See it yourself

**Tiny Proof:** predict that the `finally` record appears for both success and failure, giving each operation one terminal observation without swallowing the exception.

```bash
python3 - <<'PY2'
def run(value):
    outcome = "failed"
    try:
        result = 10 // value
        outcome = "ok"
        return result
    finally:
        print("operation_finished", {"value": value, "outcome": outcome})
for value in (2, 0):
    try:
        print("result", run(value))
    except ZeroDivisionError:
        print("caller_handled", value)
PY2
```

Expected observation: each call emits one completion event; the failed call still propagates a typed error to its caller.

Limits of this proof: printing synchronously is not a durable telemetry pipeline, and a process crash can interrupt `finally`. The example does not establish safe logging fields, distributed correlation, or service reliability.

## Where it shows up

An order service calling inventory and payment needs one end-to-end deadline. If each dependency receives a fresh timeout, nested work can outlive the caller and consume capacity after the result is useless. Propagating the remaining budget, recording stage durations, and using an idempotency key allows operators to distinguish queueing, dependency latency, and uncertain completion. A circuit breaker may contain repeated dependency failure, but only if its open, probing, and recovery behavior are observable.

## When it breaks

Timeout clusters may indicate downstream latency, exhausted worker pools, DNS, or an unrealistically low budget. Repeated identical log events suggest retry amplification. A flat success metric with user complaints suggests the metric observes the wrong boundary. First select one affected operation and preserve its timestamps, identifiers, status, dependency outcomes, resource saturation, and deployment version. Do not raise log volume indiscriminately; high-cardinality labels and sensitive payloads can create a second incident.

## Practice

**Build:** complete [Trace a Failure Across Boundaries](./lab-trace-a-failure.md), then add a deadline and structured completion record to a three-stage program. **Break:** inject delay and one transient error, with at most two safe retries. **Explain back:** identify fault, error, failure, retry decision, and evidence. Success means every path terminates within a bound, emits exactly one final outcome, preserves the original exception cause, and leaves no secret in telemetry.

## Check yourself

1. Why is a timeout not proof that the remote operation failed?
2. What different questions do logs, metrics, and traces answer?

## Sources

### REQUIRED

- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

### RECOMMENDED

- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)

### DEEP DIVE

- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)

## Next

Continue to [Software Lifecycle and Engineering Tradeoffs](./06-software-lifecycle-and-tradeoffs.md).
