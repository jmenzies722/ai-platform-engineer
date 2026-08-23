# Structured logs and event design

A production log is a typed event with stable semantics, not an improvised sentence. Structure enables correlation and safe queries; restraint prevents sensitive data leakage and ingestion collapse.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Define event name, timestamp, severity, outcome, stable identifiers, bounded dimensions, schema version, and selected context. Keep high-cardinality request and trace IDs in logs, where direct lookup is appropriate, rather than metric labels. Log at decision boundaries and once per owned error.

Severity should communicate required action, not emotional intensity. Sampling repeated informational events is acceptable only when counts are not inferred from sampled logs. Redaction is weaker than not collecting; classify fields before emission and enforce size limits.

## See it yourself

If five layers log the same exception, one failure produces five apparent errors. Logging once where the error is handled preserves one event count; lower layers can add span events or structured context. This explains why log volume is not an error metric.

## Where it shows up

Audit logs emphasize actor, authorization decision, target, and integrity; diagnostic logs emphasize execution context. Separate access, audit, and debug retention and permissions. Correlate using trace ID without treating it as proof of causality.

## When it breaks

Multiline text breaks parsers, stack traces explode volume, user input forges fields, and secrets persist in indexes and backups. Inspect pre-export payloads, schema rejects, truncation counters, and access controls; rotate exposed credentials rather than merely deleting a log.

## Practice

Define schemas for authorization denial and payment failure. Build validation for required fields and maximum bytes. Inject a token-shaped value. Completion means emission is rejected or scrubbed before transport and valid events remain queryable by trace ID.

## Check yourself

1. Why should an owned error usually be logged once?
2. When is a trace ID useful but insufficient?
3. Why is post-ingestion deletion not adequate secret handling?
4. Which fields distinguish an audit event from debug output?

## Sources

### REQUIRED

- [OpenTelemetry logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)

### RECOMMENDED

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

### DEEP DIVE

- [NIST SP 800-92](https://csrc.nist.gov/pubs/sp/800/92/final)

## Next

[Traces, causality, and sampling](05-traces-and-sampling.md)
