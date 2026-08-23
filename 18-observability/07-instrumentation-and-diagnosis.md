# Instrumentation strategy and evidence-led diagnosis

Instrumentation is complete when responders can move from user impact to the responsible change or dependency with bounded uncertainty. More dashboards do not substitute for a disciplined diagnostic path.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Start with user-visible SLIs, then instrument boundaries using stable semantic conventions. Add deployment and configuration markers. During diagnosis, establish impact and time window, compare cohorts, identify saturation and errors, follow representative traces, inspect structured events, and test a falsifiable hypothesis.

Use telemetry-as-code tests for names, units, context propagation, redaction, and expected events. Synthetic checks observe outside-in availability; continuous profiling explains resource use; exemplars connect aggregate histogram buckets to traces.

## See it yourself

If errors occur only in version B while A and B receive comparable traffic, version is evidence for a release hypothesis. It is not proof: version may correlate with region or customer cohort. Conditioning on both dimensions tests the confounder.

## Where it shows up

A runbook should state symptom, SLI query, cohort pivots, dependency checks, recent changes, and safe mitigations. Record negative evidence because disproved hypotheses prevent repeated work during handoff.

## When it breaks

Dashboards can hide missing data, high-cardinality queries can time out during incidents, alert labels can disagree with trace attributes, and instrumentation changes can create apparent regressions. Verify pipeline health and raw events before concluding the service changed.

## Practice

Instrument a toy checkout with request count, latency histogram, one structured failure event, and nested spans. Break context propagation and add a version-specific fault. Completion means a responder identifies impact, isolates the version, finds the orphan span, and proves the correction.

## Check yourself

1. What is the first question in evidence-led diagnosis?
2. How do deployment markers change an investigation?
3. Why is cohort correlation not causation?
4. Which instrumentation properties should CI test?

## Sources

### REQUIRED

- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)

### RECOMMENDED

- [Google SRE Workbook: Monitoring](https://sre.google/workbook/monitoring/)

### DEEP DIVE

- [Brendan Gregg: USE Method](https://www.brendangregg.com/usemethod.html)

## Next

[Site Reliability Engineering](../19-sre/README.md)
