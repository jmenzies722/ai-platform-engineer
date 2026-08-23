# Observability and operability

Observability is the ability to answer operational questions from system evidence; operability is the ability to act safely on the answers.

## Why it matters

A system that cannot distinguish demand, saturation, dependency failure, bad deployment, and data corruption cannot be restored deliberately.

## How it works

Start from user journeys and invariants. Define service level indicators for successful outcomes, latency, freshness, and correctness where measurable. Metrics summarize rates and distributions, logs preserve discrete evidence, and traces connect causality across boundaries. None substitutes for the others.

Use stable request, tenant, job, source-version, and model-version identifiers while respecting privacy. Prefer structured events with bounded dimensions. High-cardinality values belong in logs or traces, not careless metric labels. Instrument admission, queueing, service time, dependency time, retries, saturation, degraded modes, and terminal outcomes so latency can be decomposed.

Alert on actionable user harm or imminent budget exhaustion. Every page needs an owner, urgency, first diagnostic, and safe response. Dashboards support investigation but do not define reliability. Runbooks include preconditions, expected evidence, rollback, authority, and escalation. Audit trails record sensitive decisions separately from debug logs.

## See it yourself

End-to-end p95 latency rises from 400 milliseconds to four seconds. A single latency metric offers no diagnosis. Split the trace into admission wait, retrieval, model queue, generation, and post-processing, then correlate with saturation and version. If model queue dominates only for one tenant, the response differs from a global provider slowdown.

## Where it shows up

AI services need conventional reliability telemetry plus quality and provenance signals: model, prompt, retrieval corpus, citation coverage, safety-policy result, token use, and evaluator version. Sampling must retain rare harmful outcomes and protect sensitive prompts; “log everything” is neither safe nor economical.

## When it breaks

Telemetry breaks through cardinality explosions, silent sampling bias, missing correlation, unactionable pages, clock confusion, and dashboards that omit degraded success. During an incident, ask one operational question at a time and identify which signal would answer it. Add instrumentation after recovery only when it closes a demonstrated diagnostic gap.

## Practice

**Build:** create an observability specification for inference and ingestion. Define SLIs, event schemas, trace spans, bounded labels, privacy rules, alerts, dashboard questions, and two runbooks. **Break:** inject queue delay, wrong-model routing, and cross-tenant log leakage. **Explain back:** use evidence to distinguish each fault without reading raw customer content.

## Check yourself

1. Why should alerts be tied to an action?
2. Where should high-cardinality identifiers live?
3. Which signals reveal successful but degraded service?

## Sources

### REQUIRED

- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/)

### RECOMMENDED

- [Google SRE Workbook: Monitoring](https://sre.google/workbook/monitoring/)

### DEEP DIVE

- [NIST SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/pubs/sp/800/92/final)

## Next

Continue to [Cost and efficiency](11-cost-and-efficiency.md).
