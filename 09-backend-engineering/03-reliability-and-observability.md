# Reliability and Observability

A service is operable when it bounds resource use, reports meaningful outcomes, and degrades deliberately.

## Why it matters

A service that retries three times with a fresh five-second timeout can violate a caller’s six-second deadline before it returns any error. During an outage those extra attempts multiply dependency load and hide overload in growing queues. Reliability policy must allocate one end-to-end budget and make attempts, waiting, and final outcomes observable.

## How it works

Timeouts bound waiting; deadlines propagate the caller’s remaining budget. Retries need backoff, jitter, and a retryable error class. Structured logs record events, metrics aggregate rates and distributions, and traces connect work across boundaries. Health checks should answer a defined operational question.

A timeout bounds one operation’s waiting, while a deadline names the latest acceptable completion time and can propagate remaining budget through calls. Retries are useful only for failures likely to be transient and operations safe to repeat; exponential backoff and jitter reduce synchronization, while attempt and deadline caps bound total work. Concurrency and queues must also be bounded so rejected or degraded responses occur before memory and latency grow without limit. Logs preserve discrete contextual events, metrics aggregate rates and distributions, and traces connect timed operations across boundaries. Stable request or job IDs join those signals. Health endpoints should answer a specific question such as process liveness or readiness for traffic; checking every dependency in liveness can create restart storms. Observability is designed around decisions, not volume of emitted data.

## See it yourself

Predict that remaining time decreases across attempts and reaches zero near the original deadline. No attempt should reset the budget to a new 0.2 seconds.

```bash
python3 - <<'PY2'
import time
deadline=time.monotonic()+0.2
for attempt in range(3):
    remaining=deadline-time.monotonic()
    print(attempt, round(max(remaining,0),3))
    if remaining <= 0: break
    time.sleep(min(0.09, remaining))
PY2
```

Expected observation: The available budget shrinks across attempts; resetting a full timeout each time would violate the original deadline.

Limits of the reliability and observability observation: This loop does not model network cancellation, backoff randomness, retry classification, or useful work. It only demonstrates monotonic budget consumption.

## Where it shows up

An API calling a recommendation service can degrade to a response without recommendations when the dependency exceeds its allocated 80 ms. Metrics separate degraded from full responses, a trace shows the dependency consuming its span budget, and logs carry the same request ID for sampled failures. A bounded circuit or concurrency limiter prevents one slow dependency from occupying every worker. The product chooses the fallback; the reliability mechanisms enforce its budget.

## When it breaks

Rising latency with flat CPU and growing in-flight work suggests waiting or queueing; repeated attempt spans suggest retries; memory growth with queue depth suggests unbounded admission; missing traces but present logs suggests context propagation failure. First compare request rate, outcome rate, latency distribution, saturation, and dependency timing over the same interval. Then inspect representative traces and logs; adding high-cardinality labels before defining the question raises cost without clarifying cause.

## Practice

**Build:** wrap a controlled flaky function with one total deadline, retry classification, capped exponential delay, and emitted attempt records. **Break:** test permanent failure, slow success beyond budget, and a burst exceeding a small concurrency limit. **Explain back:** justify which signal answers rate, latency, saturation, and one-request causality. Success means every run terminates inside tolerance, unsafe errors are not retried, overload is explicit, and emitted context reconstructs the decision.

## Check yourself

1. How does a deadline differ from a timeout?
2. When is a retry unsafe?

## Sources

### REQUIRED

- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)

### RECOMMENDED

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)

### DEEP DIVE

- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)

## Next

Continue to [Authentication, Authorization, and API Evolution](./04-authentication-authorization-and-api-evolution.md).
