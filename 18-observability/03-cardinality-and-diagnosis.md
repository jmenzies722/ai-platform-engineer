# Cardinality, sampling, and diagnosis

Observability design balances diagnostic detail against storage, query, privacy, and processing limits.

## Why it matters

One unbounded metric label can create millions of time series. Naive trace sampling can discard the rare errors you most need.

## How it works

Cardinality is the number of distinct values in a dimension; combined dimensions multiply series. Keep metric labels bounded, such as route template and status class. Put high-cardinality request IDs in logs or traces.

Head sampling decides when a trace begins and is cheap, but cannot know the final outcome. Tail sampling buffers completed traces and can retain errors or slow requests at higher collector cost. Sampling changes diagnostic coverage; account for it when interpreting counts.

During diagnosis, begin with user impact and time window, compare healthy and unhealthy cohorts, then pivot across correlated signals. Preserve raw evidence and annotate deployments or configuration changes.

## See it yourself

Estimate series for 20 services, 30 routes, 5 statuses, 3 Regions, and 10,000 user IDs. Removing `user_id` changes 90 million potential combinations to 9,000.

## Where it shows up

Metrics backends enforce series limits, log platforms charge by ingestion, and tail-sampling collectors need bounded memory.

## When it breaks

Dynamic URL paths become labels, sampling drops all low-volume failures, retention is shorter than incident discovery, or dashboards average unlike cohorts.

## Practice

Review an instrumentation schema. Classify every attribute as bounded, high-cardinality, sensitive, or redundant; assign it to the appropriate signal.

## Check yourself

1. Why should route templates replace raw URLs in metrics?
2. What can tail sampling know that head sampling cannot?

## Sources

### REQUIRED
- [OpenTelemetry sampling](https://opentelemetry.io/docs/concepts/sampling/)

### RECOMMENDED
- [Prometheus instrumentation practices](https://prometheus.io/docs/practices/instrumentation/)

### DEEP DIVE
- [OpenTelemetry Collector tail sampling](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)

## Next

[Site Reliability Engineering](../19-sre/README.md)
