# Requirements, load, and boundaries

System design starts by turning an ambiguous request into measurable behavior, constraints, and ownership boundaries.

## Why it matters

Architecture cannot compensate for solving the wrong problem or sizing against an unstated workload.

## How it works

Identify actors, core journeys, correctness rules, SLOs, security needs, cost limits, and non-goals. Estimate average and peak requests, payloads, storage growth, concurrency, and skew with units. Define components around cohesive responsibilities and explicit interfaces, then mark trust and failure boundaries.

Functional requirements describe observable behavior; quality attributes state conditions such as p95 latency at peak load or recovery after a zone loss. Estimates should be ranges with named assumptions. Boundaries follow invariants and rates of change: keeping one owner for a fact is often more valuable than maximizing component count.

## See it yourself

At 500 requests/s and 200 ms average time, Little's Law predicts about 100 in-flight requests in stable conditions. A tenfold burst sustained for two seconds brings 10,000 arrivals while capacity sized for average may complete only 1,000; the remainder must queue or be rejected. This proves average throughput does not size burst absorption or tail latency.

## Where it shows up

For an inference API, requirements connect tenant arrival patterns, context sizes, model latency, and availability to admission and replica count. Trust boundaries separate callers, gateway, model workers, and data stores. The capacity worksheet records assumptions so production measurements can replace guesses after launch.

## When it breaks

False precision hides assumptions, peak behavior is omitted, and component boundaries mirror org charts rather than invariants. When a design misses load, first compare actual arrival, size, service-time, and skew distributions with the assumption table. When ownership failures recur, trace the violated invariant across boundaries before adding another service.

## Practice

**Build:** write measurable requirements, non-goals, estimates, and trust/failure boundaries for an inference API. **Break:** inject a tenfold burst and one heavy tenant; show queue or rejection behavior. **Explain back:** defend each major component from an invariant or measured constraint, and name the first assumption to validate.

## Check yourself

1. Why state non-goals?
2. Which estimate drives concurrency?
3. What belongs at a trust boundary?

## Sources

### REQUIRED

- [Google SRE: service level objectives](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

### DEEP DIVE

- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

## Next

Continue to [Data, consistency, and reliability](02-data-consistency-and-reliability.md).
