# Telemetry as an evidence model

Telemetry is a lossy model of running software. A useful design begins with decisions and hypotheses, then chooses signals whose semantics, blind spots, delay, and cost are explicit.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Metrics aggregate measurements over dimensions and time; logs preserve selected events; traces preserve sampled causal paths; profiles sample resource use. Resource attributes describe the producer, instrumentation scope names the library, and signal records describe observations.

Separate user outcome, service behavior, dependency behavior, and resource saturation. Every observation has a measurement point: a load balancer’s success may disagree with a worker’s durable completion. Treat telemetry pipelines as distributed systems with buffering, loss, retries, and backpressure.

## See it yourself

For 99 requests at 10 ms and one at 10 s, the mean is about 110 ms, a value experienced by no request. A histogram can bound percentiles; one trace can explain a path but cannot estimate population frequency. Different questions require different evidence.

## Where it shows up

A checkout SLO uses edge events for user outcome, spans for path localization, structured logs for exceptional state, and profiles for CPU. A telemetry contract records name, unit, temporality, attributes, owner, and retention.

## When it breaks

Collection can silently drop under overload, clocks can distort span timing, schema drift can split a metric, and instrumentation can report success before durable commit. Compare emitted, accepted, dropped, exported, and queried counts along the full path.

## Practice

Choose one user journey. Write five operational questions and the minimum signal for each. Build a telemetry contract for one counter and one event; break it by changing a unit. Completion means a query detects the incompatibility and the contract names ownership.

## Check yourself

1. Why is telemetry evidence rather than ground truth?
2. Which measurement point best represents durable success?
3. Why can a trace explain but not estimate incidence?
4. How would you detect collector loss?

## Sources

### REQUIRED

- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

### RECOMMENDED

- [Google SRE: Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

### DEEP DIVE

- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)

## Next

[OpenTelemetry context and pipeline internals](02-opentelemetry-internals.md)
