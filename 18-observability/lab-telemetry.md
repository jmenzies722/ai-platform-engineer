# Lab: diagnose a telemetry pipeline

Create a local telemetry dataset, introduce a propagation and cardinality defect, and diagnose from user impact back to instrumentation.

## Goal

Produce bounded metrics, correlated structured events, and trace relationships for a synthetic checkout; prove the baseline identifies a version-specific failure without indexing request IDs as metric dimensions.

## Before you start

Read lessons 2, 5, 6, and 7. Use Python 3 and temporary JSON files; no Collector, backend, account, privilege, network, or cost is required. Stop before adapting commands to production data. Predict the error cohort and number of metric series.

## Establish a baseline

`python3 --version` must show Python 3. Create five known request events and assert all contain route templates, version, status, duration, trace ID, span ID, and parent ID. Passing validation establishes a complete baseline schema.

## Make it work

Write a Python analyzer that groups request count and errors by route template, version, and status class; builds fixed latency buckets; and reports missing parents. Include a failing version with two errors. Confirm bounded series, a higher error ratio in that version, and no missing parent.

## Break it

Replace one route template with `/orders/<uuid>` and remove one parent ID. Expected symptoms are a new metric series and one orphan span; request-level errors remain unchanged.

## Diagnose it

Begin with the failing user cohort, then inspect version ratios, route-series growth, and orphan count. Normalize the route and restore propagation. Rerun identical assertions to prove both defects disappear without hiding the version-specific application failure.

## Clean up

Remove temporary JSON and scripts and verify the directory is absent.

## What to keep

Keep predictions, series counts, cohort ratios, the failed hypothesis, and corrections. Add a production budget for active series, exporter drops, and telemetry bytes per request, then explain which evidence supports impact, localization, and cause.

## Sources

- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
