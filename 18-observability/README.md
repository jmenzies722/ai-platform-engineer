# 18 — Observability

Observability is the ability to answer questions about a system from its outputs, including questions you did not predict when instrumenting it.

## What you will learn

- Select metrics, logs, and traces for distinct diagnostic jobs.
- Carry context across service boundaries with OpenTelemetry.
- Control cardinality, sampling, retention, and telemetry cost.

## Lessons

1. [Signals and useful telemetry](01-signals-and-questions.md)
2. [Context propagation and OpenTelemetry](02-context-and-opentelemetry.md)
3. [Cardinality, sampling, and diagnosis](03-cardinality-and-diagnosis.md)

## Practice

Complete the [local telemetry reasoning lab](lab-telemetry.md). It uses a small log set and optional OpenTelemetry tools; no hosted backend is required.

## Ready to continue

You can choose the right signal for a question, follow one request across services, and explain why unbounded attributes damage both queryability and cost.

## Next

Continue to [Site Reliability Engineering](../19-sre/README.md).
