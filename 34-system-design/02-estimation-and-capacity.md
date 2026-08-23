# Estimation and capacity

Estimation is a model of the system’s pressure points, not a performance promise disguised as arithmetic.

## Why it matters

Without units and distributions, teams overbuild harmless paths, miss bottlenecks, and discover only in production that one tenant, payload shape, or retry storm dominates capacity.

## How it works

Start with a workload envelope: active users, requests per user, read-write mix, payload sizes, retention, growth, geography, and seasonality. Preserve average, percentile, and credible peak values. Convert them with dimensional analysis. Requests per second multiplied by service time gives expected concurrency; bytes per event multiplied by events per day and retention gives raw storage before replication and indexes.

Build a resource budget for CPU, memory, network, storage IOPS, accelerator memory, and external quotas. A bottleneck is the first constrained resource under a scenario, not the largest number on a spreadsheet. Add headroom for failover, deployments, rebalancing, and uncertain forecasts. Then test sensitivity: if context length doubles, which cost and latency terms move?

Separate arrival rate from service rate. A queue can absorb a finite burst but cannot repair sustained overload. Use benchmark results only when payload, concurrency, cache state, and hardware resemble the design. Record every estimate as a range with source, confidence, consequence, and a plan to replace it with telemetry.

## See it yourself

At 600 requests per second and 150 milliseconds mean service time, Little’s Law predicts about 90 requests in service in stable conditions. If traffic jumps to 3,000 requests per second for ten seconds while service capacity remains 1,000, backlog grows by about 20,000. A queue merely delays the visible failure unless admission control sheds work or capacity arrives before the latency budget expires.

## Where it shows up

For retrieval-augmented generation, estimate tokens rather than requests alone. Prompt length changes model time, accelerator memory, provider charges, and attainable batching. Tenant skew matters because a global average can hide one customer consuming the entire context or concurrency budget.

## When it breaks

False precision, missing units, average-only estimates, and benchmark worship are common failures. Diagnose a miss by comparing assumed and observed arrival distributions, service-time distributions, object sizes, cache hit rate, skew, and retry volume. Do not “add 30 percent” until the constrained resource and failure scenario are known.

## Practice

**Build:** create a capacity workbook for interactive inference and batch evaluation. Include three traffic scenarios, unit-carrying formulas, bottleneck resources, failover headroom, and sensitivity to context length. **Break:** introduce a hot tenant, a zone loss, and a retry storm. **Explain back:** identify which assumption most affects user harm and which production metric will replace it.

## Check yourself

1. Why can a stable average still produce an unacceptable tail?
2. What does Little’s Law require you to name?
3. When does buffering make overload worse?

## Sources

### REQUIRED

- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [Amazon Builders’ Library: Using load shedding to avoid overload](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)

### DEEP DIVE

- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

## Next

Continue to [APIs, contracts, and boundaries](03-apis-contracts-and-boundaries.md).
