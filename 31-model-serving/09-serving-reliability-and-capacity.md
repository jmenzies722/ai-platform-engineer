# Serving reliability and capacity

Reliable serving allocates capacity against explicit traffic, latency, quality, availability, and recovery objectives.

## Why it matters

Peak benchmark throughput excludes bursts, failures, cold starts, request-size variation, and maintenance. Running at that number guarantees queues and brittle recovery.

## How it works

Define service-level indicators for valid availability, time to first token, inter-token latency, end-to-end latency, and semantic correctness. Segment by model, region, tenant class, and request size without creating unbounded cardinality. Capacity tests replay arrival and token distributions, not only average requests per second.

Required replicas reflect peak admitted work, per-replica safe throughput, failure headroom, load time, and rollout overlap. Error budgets govern change and reliability investment. Graceful degradation may cap output, select an approved smaller model, disable optional features, or reject low-priority work, but must preserve contract and disclose changed behavior.

## See it yourself

If safe throughput is 40 requests/s and peak demand 400, ten replicas cover demand with no failure margin. Losing two produces 320 requests/s and an unstable queue. Twelve replicas survive two failures at 400 only at full saturation; thirteen add operating headroom.

## Where it shows up

Game days remove replicas, delay storage, corrupt readiness, and burst traffic while operators follow runbooks. Capacity dashboards join arrival work, admitted work, completed work, oldest age, cache pressure, and warm capacity.

## When it breaks

Averages hide size tails, dependencies share a failure domain, probes create false readiness, and degradation violates quality. Diagnose by stage and size cohort, preserve rejected traffic as a first-class outcome, and test recovery while load continues.

## Practice

**Observe:** derive replica counts under two failures. **Build:** write SLOs and a token-workload load test. **Break:** remove 20% capacity during a burst and slow model loading. Completion requires bounded overload, an error-budget calculation, and verified recovery.

## Check yourself

1. Why is benchmark maximum unsafe capacity?
2. Which degradation needs product approval?
3. What proves recovery rather than mere process restart?

## Sources

### REQUIRED

- [Google SRE: service level objectives](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)

### DEEP DIVE

- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

## Next

Continue to [Practical lab: build a tiny model service](03-practical-model-service-lab.md).
