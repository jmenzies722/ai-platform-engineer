# Lab: reason from local telemetry

Use shell tools and this synthetic structured log. No collector or hosted service is required.

## Capture

Save the following as `/tmp/requests.jsonl`:

```json
{"trace_id":"a1","route":"/checkout","status":200,"duration_ms":48,"region":"east"}
{"trace_id":"a2","route":"/checkout","status":503,"duration_ms":3010,"region":"west"}
{"trace_id":"a3","route":"/cart","status":200,"duration_ms":22,"region":"west"}
{"trace_id":"a4","route":"/checkout","status":503,"duration_ms":2988,"region":"west"}
{"trace_id":"a5","route":"/checkout","status":200,"duration_ms":51,"region":"east"}
```

## Ask before querying

Write hypotheses for:

1. Which user journey is failing?
2. Is impact global or cohort-specific?
3. Which trace IDs deserve deeper inspection?

If `jq` is installed, test them:

```bash
jq -s 'group_by(.route) | map({route: .[0].route, requests: length, errors: map(select(.status >= 500)) | length})' /tmp/requests.jsonl
jq -s 'group_by(.region) | map({region: .[0].region, requests: length, errors: map(select(.status >= 500)) | length})' /tmp/requests.jsonl
jq 'select(.status >= 500) | {trace_id,route,region,duration_ms}' /tmp/requests.jsonl
```

## Design

Turn this event stream into:

- a request-rate metric with bounded labels;
- an error-ratio metric;
- a latency histogram;
- a structured log schema;
- trace span attributes.

Do not use `trace_id` as a metric label. Explain where it remains useful. Add one deployment annotation and one dependency span that would help distinguish application failure from a west-region dependency failure.

## Optional OpenTelemetry extension

Run a local OpenTelemetry demo or Collector only if already available. Export to a local debug exporter and inspect propagation; no hosted account is needed.

## Cleanup

```bash
rm -f /tmp/requests.jsonl
```
