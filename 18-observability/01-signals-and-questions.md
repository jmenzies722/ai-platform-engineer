# Signals and useful telemetry

Telemetry is useful when it helps answer a concrete operational question with known cost and limitations.

## Why it matters

Collecting everything creates expense and noise without guaranteeing diagnosis. A dashboard of host averages can remain green while a user journey fails.

## How it works

Metrics aggregate numeric measurements across time and dimensions; they are efficient for rates, ratios, distributions, and alerts. Logs record discrete events with context. Traces connect spans along one request path. Profiles sample where code spends CPU or memory.

Start from questions: Are users succeeding? Which cohort is slow? Where is time spent? What changed? Instrument service boundaries with request count, error classification, and latency distributions, then add domain outcomes. Use structured logs and preserve stable identifiers for correlation.

## See it yourself

Compare mean latency with a histogram where 99 requests take 10 ms and one takes 10 seconds. The mean hides the harmed request; percentiles and a trace reveal different facts.

## Where it shows up

Alerts use aggregated metrics, incident exploration pivots to logs, traces localize cross-service latency, and profiles explain expensive code paths.

## When it breaks

Logs omit request context, metric labels contain user IDs, traces do not propagate across queues, or telemetry reports success before durable work completes.

## Practice

For checkout, write three questions and the minimum metric, log event, or trace attributes needed to answer each.

## Check yourself

1. Which signal best alerts on an error-rate ratio?
2. Why are averages dangerous for skewed latency?

## Sources

### REQUIRED
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

### RECOMMENDED
- [Google SRE: Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

### DEEP DIVE
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)

## Next

[Context propagation and OpenTelemetry](02-context-and-opentelemetry.md)
