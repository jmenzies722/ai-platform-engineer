# SRE and Observability

SRE makes reliability an explicit engineering goal, while observability provides the evidence needed to understand system behavior.

## Why it matters

**Prerequisite:** [Kubernetes](./13-kubernetes.md).

Host checks and heroic response were poor tools for services spread across many machines. Teams needed a way to define acceptable reliability and infer internal behavior from evidence produced by the system.

Service-level objectives, error budgets, automation, metrics, logs, and traces made reliability measurable. They also created alert noise, high-cardinality data, and telemetry cost; AI systems add model quality, drift, and accelerator health to the same operational problem.

## How it works

An SLO is a product reliability contract measured by SLIs; an error budget is the allowed unreliability that governs risk.

Events become telemetry; queries calculate good events over valid events; burn-rate alerts detect rapid budget consumption; traces connect request spans; incident response stabilizes service and preserves evidence.

Percentile latency is not additive, and averages hide tails. Multi-window burn alerts balance speed and noise. Observability requires useful internal state exposure, not simply possessing three telemetry types.

## Vocabulary

- **SLI:** A quantitative measure of service behavior relevant to users.
- **SLO:** A target for an SLI over a defined window.
- **SLA:** A service commitment with business or contractual consequences.
- **Error budget:** The tolerated amount of behavior outside an SLO target.
- **Burn rate:** The speed at which a service consumes its error budget.
- **Toil:** Manual, repetitive, automatable operational work that scales with service growth.
- **Observability:** The ability to investigate internal behavior from system evidence.
- **Trace:** A representation of one request or workflow across components.
- **Span:** A timed operation within a trace.
- **Cardinality:** The number of distinct values in a telemetry dimension.
- **Saturation:** The degree to which a constrained resource is fully demanded.

## See it yourself

```promql
sum(rate(http_requests_total{code=~"2.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

Choose sample counts for successful and total requests and predict the ratio before evaluating the expression. The query should return the proportion of matching successful requests over all selected requests. This supports an event-based availability SLI. It does not prove that the event filter represents user success, handles no-traffic periods correctly, or defines a suitable objective.

## Where it shows up

An inference endpoint may return HTTP 200 within its latency target while producing unusable answers. Availability and latency SLIs describe transport service, not model quality. A practical service contract combines request-level reliability with versioned evaluation slices and product signals, keeping online user harm distinct from infrastructure failure while still governing releases with both.

## When it breaks

On-call engineers may receive many pages while users see little harm, or no page during a real outage. Alerts may target internal causes, use averages that hide tails, omit a valid-event denominator, or depend on missing telemetry. First inspect the affected SLI and budget window from the user perspective, then verify telemetry completeness and recent changes.

## Practice

### Observe

Define availability and latency SLIs for an inference API, calculate budget for a target, and design fast/slow burn alerts.

### Build

Instrument a request path with structured logs, one bounded-cardinality metric, and trace context; create an SLO dashboard.

### Break

Add label explosion, telemetry delay, and a dependency slowdown. Detect which conclusions become unsafe.

### Say it out loud

Explain an SLO as an engineering decision rather than a dashboard number.

**Success:** Define the user event, target window, error budget, alert behavior, and one way telemetry can mislead.

## Check yourself

1. Why avoid 100% SLOs?
2. What does burn rate express?
3. How is observability different from monitoring?

### Interview stretch

- Design SLOs for model serving.
- Reduce noisy alerts.
- Diagnose rising p99 with stable averages.

## Sources

### REQUIRED

- “Site Reliability Engineering” — Google. [Official free book](https://sre.google/sre-book/table-of-contents/). Defines SRE principles and practice.

### RECOMMENDED

- “The Site Reliability Workbook” — Google. [Official free book](https://sre.google/workbook/table-of-contents/). Practical SLO and alerting guidance.

### DEEP DIVE

- “Distributed Tracing in Practice” foundations via Dapper — Sigelman et al., Google. [Research paper](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/). Explains scalable request tracing.

## Next

Continue with [./15-platform-engineering.md](./15-platform-engineering.md).
