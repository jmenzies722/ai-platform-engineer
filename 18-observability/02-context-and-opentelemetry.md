# Context propagation and OpenTelemetry

OpenTelemetry defines vendor-neutral APIs, SDKs, semantic conventions, and protocols for producing and transporting telemetry.

## Why it matters

A trace is only coherent when every boundary preserves context. Proprietary instrumentation couples application code to one backend and makes migrations expensive.

## How it works

A trace contains spans identified by trace and span IDs. Each span describes an operation, timing, status, attributes, events, and links. W3C Trace Context carries `traceparent` and optional `tracestate` headers across HTTP. Messaging often uses propagated context plus span links to represent asynchronous causality.

Application instrumentation uses an OpenTelemetry SDK. Exporters send OTLP to a Collector, which can receive, process, sample, redact, batch, and export data. Baggage carries application context but is propagated widely; never place secrets or unbounded user data in it.

## See it yourself

Inspect a valid `traceparent`: version, 16-byte trace ID, 8-byte parent ID, and flags. Follow that trace ID through two structured log records and a backend query.

## Where it shows up

HTTP middleware, database client instrumentation, queue producers and consumers, serverless runtimes, and sidecar or gateway collectors.

## When it breaks

Headers are dropped, invalid IDs create new traces, sampling decisions conflict, attributes contain sensitive data, or synchronous exporters add latency to request paths.

## Practice

Draw instrumentation for browser, API, queue, worker, and database. Mark propagation format, span kind, retry spans, and where redaction occurs.

## Check yourself

1. What role does the Collector play?
2. Why can baggage be a security and cost risk?

## Sources

### REQUIRED
- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)

### RECOMMENDED
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)

### DEEP DIVE
- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)

## Next

[Cardinality, sampling, and diagnosis](03-cardinality-and-diagnosis.md)
