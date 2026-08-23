# Traces, causality, and sampling

A trace represents one sampled execution graph. Its value comes from correct parentage, meaningful span boundaries, and an explicit sampling policy, not from producing a span for every function.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Spans record operation, start and end, parent, status, attributes, events, and links. Use links for batch work or fan-in where one parent is misleading. Head sampling decides near trace start and controls cost predictably; tail sampling decides after observing more of the trace but requires buffering and consistent routing.

Sampling probabilities must travel with context. Probability sampling supports unbiased rate estimates only when selection probabilities are known and data is weighted correctly. Always-on collection can overwhelm applications, Collectors, networks, and storage.

## See it yourself

At a 1% independent sample, observing 20 errors estimates roughly 2,000 source errors, but variance is large. Selecting only errors is excellent for examples and invalid for estimating the overall error rate unless the selection scheme and weights are incorporated.

## Where it shows up

Trace service maps reveal observed calls, not all possible architecture. Instrument ingress, egress, queues, and durable state transitions. Keep span names low-cardinality; put specific IDs in attributes.

## When it breaks

Tail-sampling buffers can exhaust memory, inconsistent routing can fragment traces, async boundaries can create false roots, and status conventions can label expected errors as failures. Compare received spans, completed traces, sampling reasons, late spans, and orphan rates.

## Practice

Generate 1,000 synthetic traces with rare slow errors. Compare 1% head sampling with a policy retaining errors and slow traces. Completion means you quantify cost and bias and can explain which dataset supports diagnosis versus population estimates.

## Check yourself

1. When should spans use links instead of parent-child edges?
2. Why does tail sampling need trace affinity?
3. Which sampling policy supports unbiased incidence estimates?
4. What does an orphan-span increase suggest?

## Sources

### REQUIRED

- [OpenTelemetry tracing specification](https://opentelemetry.io/docs/specs/otel/trace/)

### RECOMMENDED

- [OpenTelemetry sampling](https://opentelemetry.io/docs/concepts/sampling/)

### DEEP DIVE

- [Dapper paper](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/)

## Next

[Cardinality, retention, and telemetry cost](06-cardinality-and-cost.md)
