# Cardinality, retention, and telemetry cost

Telemetry cost is set by event volume, attribute diversity, bytes, processing, indexing, retention, and query patterns. Cardinality is a correctness and availability concern because an unbounded label can exhaust both backend and producer.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

A metric series is one unique combination of metric name and attributes. Ten regions, fifty routes, five status classes, and twenty versions can create `10 × 50 × 5 × 20 = 500,000` series before replicas. Histograms multiply storage further by bucket count.

Use bounded semantic attributes, normalize routes, aggregate before export, apply views to drop dimensions, and enforce budgets. Logs and traces also pay for indexed fields and span count. Tier retention by operational value and legal need; deletion, archive, and access policy are part of design.

## See it yourself

Adding `user_id` with one million active users to a metric that otherwise has 100 series can produce up to 100 million series. The multiplicative bound demonstrates why “only one extra label” can be catastrophic.

## Where it shows up

Maintain a telemetry inventory with owner, daily volume, series count, indexed bytes, retention, consumers, and deletion date. Chargeback can reveal cost, but governance should preserve shared incident evidence rather than reward blind deletion.

## When it breaks

Route templates can regress to raw paths, ephemeral pod IDs can churn series, debug logging can remain enabled, and retrying exporters can duplicate billed bytes. Alert on active series growth, bytes per request, rejection, and top attribute contributors.

## Practice

Estimate series and daily bytes before adding an attribute. Build a guard that rejects raw UUID route labels, then inject one. Completion means the guard identifies the source and your design offers a bounded alternative without losing the diagnostic question.

## Check yourself

1. How do label dimensions combine?
2. Why can low traffic still create high cardinality?
3. Which controls belong before ingestion?
4. How would you remove cost while preserving incident utility?

## Sources

### REQUIRED

- [OpenTelemetry attribute limits](https://opentelemetry.io/docs/specs/otel/common/)

### RECOMMENDED

- [Prometheus naming practices](https://prometheus.io/docs/practices/naming/)

### DEEP DIVE

- [OpenTelemetry SDK views](https://opentelemetry.io/docs/specs/otel/metrics/sdk/)

## Next

[Instrumentation strategy and evidence-led diagnosis](07-instrumentation-and-diagnosis.md)
