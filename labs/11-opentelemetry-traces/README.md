# Lab: Investigate an OpenTelemetry Trace

Send a synthetic distributed trace to a local collector, query it in Jaeger, and locate latency and error evidence without relying on logs alone.

## Prerequisites

- Docker Engine, Docker Compose v2, `curl`, and `jq`
- Ports 14318 and 16686 unused
- Basic knowledge of trace IDs, span IDs, parentage, attributes, and status

## Safety

Bind all ports to loopback. Synthetic attributes must contain no credentials, personal data, URLs with tokens, or production identifiers. Limit the lab to fewer than 20 spans and remove all containers and volumes afterward.

## Setup and baseline

```bash
mkdir -p .work
cat >.work/compose.yaml <<'YAML'
services:
  jaeger:
    image: jaegertracing/all-in-one:1.68.0
    environment:
      COLLECTOR_OTLP_ENABLED: "true"
    ports:
      - "127.0.0.1:14318:4318"
      - "127.0.0.1:16686:16686"
YAML
docker compose -f .work/compose.yaml up -d
curl --retry 20 --retry-delay 1 --fail http://127.0.0.1:16686/
```

Record the image digest. Predict the critical path for a root span with sequential 100 ms and 400 ms children.

## Tasks

1. Build `.work/trace.json` in OTLP JSON form with one resource named `checkout`, a root SERVER span, and two child CLIENT spans named `inventory` and `payment`. Use valid 32-hex trace IDs, 16-hex span IDs, Unix-nanosecond start/end times, and explicit parent IDs.
2. Give spans low-cardinality attributes such as `service.name`, `http.request.method`, and `server.address`. Do not use customer IDs as attributes.
3. Send the trace:

   ```bash
   curl --fail --max-time 5 -H 'Content-Type: application/json' \
     --data-binary @.work/trace.json \
     http://127.0.0.1:14318/v1/traces
   ```

4. Query `http://127.0.0.1:16686/api/services`, then `/api/traces?service=checkout&limit=10`; save and inspect the result with `jq`.
5. Reconstruct parent-child relationships, compute each duration, identify the longest child, and explain the difference between span duration and summed child duration.
6. Check trace completeness: one root, unique span IDs, matching trace ID, valid parents, and child intervals within the root interval.

## Evidence to keep

Keep sanitized OTLP payload, collector response, queried trace JSON, a span table, critical-path explanation, completeness checks, image digest, and one statement about what traces cannot prove without metrics or logs.

## Failure injection

Create a second trace in which `payment` has status code `STATUS_CODE_ERROR`, attribute `error.type="timeout"`, and 900 ms duration. Keep HTTP status as an attribute only if known. Query by service and compare traces. Expected diagnosis: the error is localized to one span, while root status must be interpreted independently.

Also create an orphan fixture locally by changing a parent span ID, but do not send it. Your validator should reject it.

## Cleanup

```bash
docker compose -f .work/compose.yaml down --volumes --remove-orphans
rm -rf .work
```

## Rubric

- 2 points: emits valid, sanitized OTLP trace data locally
- 3 points: reconstructs parentage, timing, and critical path correctly
- 2 points: localizes the injected error without overclaiming cause
- 2 points: detects orphan, duplicate, or interval-invalid spans
- 1 point: removes telemetry containers and artifacts

## Sources

- [OpenTelemetry trace specification](https://opentelemetry.io/docs/specs/otel/trace/)
- [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
