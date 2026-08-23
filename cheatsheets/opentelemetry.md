# OpenTelemetry operator sheet

Trace one known signal through generation, context propagation, SDK processing,
export, Collector processing, backend ingestion, and query. "No telemetry" is
not one failure mode.

## Frame the question

Name the signal (traces, metrics, or logs), service and instance, environment,
time window, expected attribute, protocol and endpoint, Collector path, and
backend query. Use a synthetic request with a unique non-sensitive marker when
production policy permits.

Do not put credentials, customer identifiers, request bodies, or unbounded user
input in span names, attributes, metric labels, baggage, or logs.

## 1. Was telemetry created and sampled?

Verify the SDK is initialized before instrumentation, the expected resource and
instrumentation scope exist, and shutdown/flush hooks run for short-lived
processes. For traces, capture a trace ID from application-safe diagnostics or a
response correlation header.

Sampling decisions are made before export. `ParentBased` sampling follows the
incoming parent decision; a downstream service cannot export a trace that was
never recorded without deliberately changing policy. Head sampling cannot know
the eventual error outcome. Tail sampling requires all relevant spans to reach
the same decision point and consumes Collector memory.

**Interpretation:** Application work with zero created spans suggests
initialization or instrumentation. Created but non-recording spans suggest
sampling. Recording spans with no export evidence moves the question to the
processor/exporter.

## 2. Did context cross the boundary?

For an approved test, inspect sanitized request metadata at both sides. W3C
Trace Context uses `traceparent`; `tracestate` is optional. A valid trace ID is
32 lowercase hexadecimal characters and a span ID is 16.

```text
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

The final byte contains trace flags; `01` has the sampled bit set. Valid syntax
does not prove trusted provenance. Proxies, queues, custom clients, and async
workers can drop or incorrectly reuse context. Baggage is separate, propagates
application-defined values, and can create security and cardinality risk.

**Caution:** Never inject a fabricated trace ID into real traffic to "repair"
traces. Fix propagators and boundary instrumentation.

## 3. Can the exporter reach the configured endpoint?

Confirm effective configuration without printing secret headers. OTLP commonly
uses gRPC on port 4317 and HTTP on port 4318, but deployments may differ.
Endpoint path and TLS expectations depend on protocol and SDK configuration.

```bash
# Read-only network probes; does not validate OTLP payload acceptance
getent ahosts <collector-host>
nc -vz -w 3 <collector-host> <collector-port>
openssl s_client -connect <collector-host>:<collector-port> \
  -servername <collector-host> -verify_hostname <collector-host> \
  -verify_return_error </dev/null
```

Connect success proves transport only. TLS success proves the tested identity
and trust path only. `UNAVAILABLE` often indicates reachability or transient
server failure; `UNAUTHENTICATED` and `PERMISSION_DENIED` point to identity or
policy; `RESOURCE_EXHAUSTED` indicates a limit. Preserve protocol status and
server response before retrying.

## 4. Did the Collector receive, process, and export it?

```bash
# Read-only; if Collector exposes Prometheus internal telemetry locally
curl --connect-timeout 2 --max-time 5 -sS http://<collector-host>:8888/metrics \
  -o /tmp/otelcol-metrics.txt
```

Review the local file without publishing it. Compare accepted, refused, sent,
failed, queue-size, queue-capacity, and dropped telemetry counters for the
specific receiver/exporter over the incident window. Exact metric names can
change across Collector versions; use the Collector's own versioned
documentation and `/metrics` output.

Reason by deltas:

- Receiver accepted count rises, exporter sent count does not: inspect
  processor routing, filtering, queues, and exporter failures.
- Refused or dropped counts rise: capacity, memory limiter, queue, or malformed
  data is implicated.
- Export failures rise with queue growth: backend or network is slower than
  arrival; retries may only delay drops.
- Collector is healthy but no accepted count rises: wrong endpoint/protocol,
  application export, DNS, routing, or load-balancer path.

Collector health endpoints generally prove process health, not end-to-end
telemetry delivery.

## 5. Did processing alter or discard data?

Inspect the deployed Collector configuration through its normal configuration
source. Follow the named pipeline:

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/backend]
```

Presence in a component definition does not place it in a pipeline. Check
filter, transform, attribute, routing, tail-sampling, batch, and memory-limiter
semantics. Processor order matters. Debug exporters can disclose payloads and
increase load; enable them only briefly in an approved non-sensitive path.

## 6. Did the backend ingest but the query hide it?

Search first by exact trace ID or unique marker, then validate time zone,
ingestion delay, tenant, dataset, environment, service resource attributes, and
query filters. A service name mismatch can fragment one service into several.
Clock skew distorts span timelines. Metric temporality and monotonicity must
match backend expectations; label cardinality can cause rejection or cost
controls.

## Controlled change and rollback

Before changing sampling, batch size, queue capacity, memory limits, or log
level, estimate telemetry rate and memory impact, define drop/error and process
health guardrails, canary one Collector or service, and preserve the prior
configuration. More queue capacity moves pressure into memory; 100 percent
sampling can overload the pipeline and backend.

Rollback configuration if drops, memory, latency, cardinality, or backend cost
accelerates. Escalate for telemetry containing sensitive data, widespread loss,
backend quota or tenant errors, persistent queue saturation, schema changes
affecting alerts or billing, or an unknown trust boundary.

## Authoritative sources

- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)
- [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)
- [Collector documentation](https://opentelemetry.io/docs/collector/)
- [Collector internal telemetry](https://opentelemetry.io/docs/collector/internal-telemetry/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- Repository lesson: [Observability](../18-observability/README.md)
