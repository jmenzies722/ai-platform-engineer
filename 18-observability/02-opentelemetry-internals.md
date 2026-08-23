# OpenTelemetry context and pipeline internals

OpenTelemetry standardizes telemetry APIs, SDK processing, semantic conventions, propagation, and export. It does not guarantee backend storage, complete delivery, or correct instrumentation.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Application code calls an API through an instrumentation library. An SDK provider applies resource identity, sampling, processors, aggregation, and exporters. OTLP transports telemetry to a Collector whose receivers, processors, exporters, and connectors form pipelines.

Context carries the active span and baggage across calls. W3C Trace Context serializes trace and parent identifiers; baggage carries application values and needs strict allowlists. Batch processors reduce overhead but can lose buffered data on abrupt exit. Collector memory limiters and sending queues protect the process but can drop or backpressure.

## See it yourself

A child span is connected only if its parent context crosses the boundary. Removing `traceparent` does not slow the request; it creates a new root, proving that correlation depends on explicit propagation rather than temporal proximity.

## Where it shows up

Use agents or auto-instrumentation for broad coverage, manual spans for domain boundaries, and Collector gateways for policy and routing. Pin semantic-convention changes and add resource attributes such as service name, version, and deployment environment.

## When it breaks

Double instrumentation duplicates spans; unsafe baggage leaks identifiers; unbounded exporter retries consume memory; and missing shutdown loses batches. Inspect SDK diagnostics, Collector accepted and dropped counters, queue fill, export errors, and trace-root rate.

## Practice

Draw an API-to-backend pipeline and annotate ownership and failure behavior. Build two local functions passing a trace context, then omit propagation. Completion means the second run creates a new root and you can name the exact boundary to instrument.

## Check yourself

1. What work belongs in the API versus SDK?
2. Why is baggage riskier than trace context?
3. How does a batch processor change failure behavior?
4. Which Collector metrics reveal pipeline saturation?

## Sources

### REQUIRED

- [OpenTelemetry specification overview](https://opentelemetry.io/docs/specs/otel/overview/)

### RECOMMENDED

- [W3C Trace Context](https://www.w3.org/TR/trace-context/)

### DEEP DIVE

- [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)

## Next

[Metrics, distributions, and alertable semantics](03-metrics.md)
