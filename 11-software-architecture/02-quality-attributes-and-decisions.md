# Quality Attributes and Decisions

Architecture is a set of consequential tradeoffs among qualities such as reliability, latency, security, cost, and changeability.

## Why it matters

“Make it highly available and cheap” is not a design requirement because it offers no load, failure, response, or measure for comparing options. Teams then debate technology preferences rather than consequences. Quality scenarios and decision records turn architecture into testable tradeoffs whose assumptions can later be revisited.

## How it works

A quality-attribute scenario names a stimulus, environment, affected part, response, and measurable response. Architecture decisions should record context, chosen option, alternatives, and consequences. Tactics improve one quality but often spend another: replication aids availability while increasing consistency work.

A quality attribute describes system behavior under conditions, not a component brand. A scenario identifies the source and stimulus, operating environment, affected artifact, expected response, and measurable response. Reliability might specify recovery after one-zone loss; performance might specify percentile latency under a request rate; security might specify blocked unauthorized access with audit evidence. Tactics shift these outcomes: replication can increase availability but adds consistency and cost, caching reduces read latency but adds staleness, and queues absorb bursts but add delay and operational state. An architecture decision record captures context, forces, chosen option, alternatives, consequences, and status. It should state evidence and a reconsideration trigger, allowing a reversible choice to remain lightweight and an expensive choice to receive deeper validation.

## See it yourself

Predict that the printed scenario is more testable than “fast”: it names a dependency timeout, peak environment, bounded failure response, and a 300 ms measure. Identify the missing workload details you would add before a load test.

```bash
python3 - <<'PY2'
scenario={'stimulus':'dependency timeout','environment':'peak traffic','response':'fail within budget','measure':'99% under 300 ms'}
for key,value in scenario.items(): print(f'{key}: {value}')
PY2
```

Expected observation: The statement is testable because it names conditions and a measure, unlike “the service should be fast.”

Limits of the quality attributes and decisions observation: The dictionary does not prove the target is achievable, capture every stakeholder, or compare architectural options. It only demonstrates the shape of a measurable scenario.

## Where it shows up

Choosing a multi-region database shows competing qualities. It may improve continuity after a regional failure, but synchronous coordination can raise write latency and cost, while asynchronous replication can expose recovery-point loss. A decision record connects business recovery objectives, measured network latency, failover testing, data residency, and operational skill to the chosen topology. The product name is secondary to those consequences.

## When it breaks

A system meeting average latency but failing users at the tail suggests the wrong measure; frequent decision reversals suggest undocumented forces; an option that cannot be tested suggests a vague scenario; rising cost may reveal an ignored quality. First rewrite the disputed goal as a stimulus-response-measure scenario and gather current baseline evidence. Then compare alternatives against the same scenarios rather than moving directly to a proof of concept for a favored tool.

## Practice

**Build:** write two conflicting scenarios for one service and an ADR comparing at least two options against them. **Break:** inject the named failure or load in a safe test and record where the response misses its measure. **Explain back:** state which quality improved, which worsened, and what evidence would reverse the decision. Success is an ADR another engineer can challenge using explicit assumptions, results, consequences, and a review trigger.

## Check yourself

1. Why is “highly available” not yet a requirement?
2. What makes an architecture decision reversible?

## Sources

### REQUIRED

- [ISO/IEC 25010:2023 product quality model](https://www.iso.org/standard/78176.html)

### RECOMMENDED

- [Architectural Decision Records](https://adr.github.io/)

### DEEP DIVE

- [Documenting Software Architectures](https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-second-edition/)

## Next

Continue to [Data Ownership and Evolution](./03-data-ownership-and-evolution.md).
