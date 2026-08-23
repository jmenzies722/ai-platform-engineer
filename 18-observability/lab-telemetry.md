# Lab: diagnose a telemetry pipeline

Create a local telemetry dataset, introduce a propagation and cardinality defect, and diagnose from user impact back to instrumentation.

## Goal

Produce bounded metrics, correlated structured events, and trace relationships for a synthetic checkout; prove the baseline identifies a version-specific failure without indexing request IDs as metric dimensions.

## Before you start

Read lessons 2, 5, 6, and 7. Use Python 3 and temporary JSON files; no Collector, backend, account, privilege, network, or cost is required. Stop before adapting commands to production data. Predict the error cohort and number of metric series.

## Establish a baseline

`python3 --version` must show Python 3. Create `/tmp/telemetry-lab/events.jsonl`:

```bash
mkdir -p /tmp/telemetry-lab
cat > /tmp/telemetry-lab/events.jsonl <<'EOF'
{"route":"/checkout","version":"a","status":200,"duration_ms":40,"trace_id":"t1","span_id":"s1","parent_id":"root"}
{"route":"/checkout","version":"a","status":200,"duration_ms":50,"trace_id":"t2","span_id":"s2","parent_id":"root"}
{"route":"/checkout","version":"b","status":503,"duration_ms":900,"trace_id":"t3","span_id":"s3","parent_id":"root"}
{"route":"/checkout","version":"b","status":503,"duration_ms":800,"trace_id":"t4","span_id":"s4","parent_id":"root"}
{"route":"/cart","version":"b","status":200,"duration_ms":20,"trace_id":"t5","span_id":"s5","parent_id":"root"}
EOF
python3 - <<'PY'
import json
required = {"route", "version", "status", "duration_ms", "trace_id", "span_id", "parent_id"}
events = [json.loads(line) for line in open("/tmp/telemetry-lab/events.jsonl")]
assert all(required <= event.keys() for event in events)
print("schema valid", len(events))
PY
```

Passing validation establishes a complete baseline schema, not correct propagation or bounded dimensions.

## Make it work

Save this as `/tmp/telemetry-lab/analyze.py`:

```python
import json
from collections import Counter, defaultdict

events = [json.loads(line) for line in open("/tmp/telemetry-lab/events.jsonl")]
series = Counter((e["route"], e["version"], e["status"] // 100) for e in events)
versions = defaultdict(lambda: [0, 0])
for event in events:
    versions[event["version"]][0] += 1
    versions[event["version"]][1] += event["status"] >= 500
buckets = {bound: sum(e["duration_ms"] <= bound for e in events) for bound in (50, 100, 500, 1000)}
orphans = [e["span_id"] for e in events if not e["parent_id"]]
print({"series": len(series), "versions": dict(versions), "buckets": buckets, "orphans": orphans})
assert versions["b"][1] == 2 and not orphans
```

Run `python3 /tmp/telemetry-lab/analyze.py`. Confirm version B owns both errors, histogram buckets are cumulative, and the route dimension contains only templates.

## Break it

Replace the last route with `/orders/7b7a3c10-2535-4b30-99e8-d387cf333537` and its `parent_id` with an empty string. Comment out the final assertion and rerun. Expected symptoms are a new raw-path series and one orphan span; request-level errors remain unchanged. These are two independent defects, so record and correct them one at a time.

## Diagnose it

Begin with the failing user cohort, then inspect version ratios, route-series growth, and orphan count. Normalize the route and restore propagation. Rerun identical assertions to prove both defects disappear without hiding the version-specific application failure.

## Clean up

```bash
rm -rf /tmp/telemetry-lab
test ! -e /tmp/telemetry-lab
```

## What to keep

Keep predictions, series counts, cohort ratios, the failed hypothesis, and corrections. Add a production budget for active series, exporter drops, and telemetry bytes per request, then explain which evidence supports impact, localization, and cause.

## Sources

- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
