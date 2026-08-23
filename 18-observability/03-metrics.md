# Metrics, distributions, and alertable semantics

Metrics efficiently summarize populations when instrument type, unit, attributes, and aggregation match the question. A number without those semantics is not a reliable metric.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Counters increase and support rates; up-down counters represent changing totals; gauges sample current state; histograms aggregate value distributions into buckets. A ratio requires compatible numerator and denominator populations. Cumulative and delta temporality place reset and state responsibilities in different pipeline stages.

Latency percentiles generally cannot be averaged across instances. Histograms with common buckets can be merged by adding bucket counts. Choose boundaries around user and system thresholds, not visually pleasing powers of ten alone.

## See it yourself

Two instances each report a p99: one serves 100 requests, the other 100,000. Their average gives equal weight to unequal populations and cannot reconstruct global p99. Bucket counts remain additive, which is the tiny proof for histogram aggregation.

## Where it shows up

RED metrics cover request rate, errors, and duration; USE covers utilization, saturation, and errors for resources. Domain counters such as completed checkouts prevent infrastructure health from masquerading as product health.

## When it breaks

Counter resets can create negative deltas, missing series can look like zero, label drift can split totals, and coarse buckets can hide threshold violations. Inspect raw series, scrape/export gaps, process starts, and bucket layouts before changing alerts.

## Practice

Instrument a synthetic request list with a counter and fixed-bucket histogram. Calculate error ratio and a latency bound. Break it with inconsistent units. Completion means an assertion catches milliseconds mixed with seconds and the ratio denominator is documented.

## Check yourself

1. Why are per-instance percentiles not safely averageable?
2. When is a gauge preferable to a counter?
3. What does a histogram percentile actually bound?
4. How can missing telemetry mimic recovery?

## Sources

### REQUIRED

- [OpenTelemetry metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/)

### RECOMMENDED

- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)

### DEEP DIVE

- [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## Next

[Structured logs and event design](04-logs.md)
