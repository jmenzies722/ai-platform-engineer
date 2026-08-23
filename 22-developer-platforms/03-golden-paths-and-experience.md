# Golden paths and developer experience

A golden path is a tested, supported journey that composes capabilities, defaults, documentation, and operational feedback from first intent through retirement. It is broader than a template and narrower than a universal platform.

## Why it matters

A portal can aggregate links while leaving the hard work unchanged. Developer experience improves when unnecessary decisions disappear, necessary decisions are legible, and users can recover from failure without learning the entire implementation.

## How it works

Design from a researched job and a named user segment. Map prerequisites, decisions, waits, interfaces, handoffs, evidence, and recovery. Define the supported envelope and non-goals. A production service path includes operation, upgrades, incidents, and deletion, not only repository creation.

Use progressive disclosure: safe defaults first, advanced controls when needed, and implementation evidence always reachable. Portal, CLI, API, and Git should invoke the same capability contracts and authorization. Preserve an escape hatch and document the responsibilities it transfers.

Put documentation beside decisions and failures. Explain prerequisites, guarantees, limits, expected duration, cost, ownership, and recovery. Examples must be executable against supported versions. Test the full journey continuously with synthetic and human tasks.

Measure completion, elapsed and hands-on time, error and recovery, support demand, reliability, and perceived effort. Observe users rather than asking only whether they like the interface. Segment evidence by experience and workload.

## Vocabulary

- **golden path:** supported end-to-end journey for a recurring user outcome
- **developer experience:** effectiveness, effort, clarity, and confidence experienced while doing engineering work
- **progressive disclosure:** presenting common decisions first while keeping advanced controls available

## See it yourself

Compare a one-click deployment that reports `failed` with a five-step deployment that identifies an unhealthy readiness endpoint and links logs. Predict which has lower recovery effort. Count decisions, waits, context switches, and successful recovery, not clicks alone. This supports journey quality for the tested case, not every user segment.

## Where it shows up

A Java HTTP golden path supplies a maintained runtime, CI policy, ownership metadata, telemetry, and rollback. A high-throughput stream processor uses a different path because pretending both share one supported envelope would leak complexity into every user journey.

## When it breaks

The path is optimized for creation but not upgrade or deletion. Defaults become policy without risk rationale. Documentation and templates reference incompatible versions. An abstraction hides provider errors needed during incidents. Monitor end-to-end synthetic failures, task drop-off, recovery rate, stale examples, support topics, and escape-hatch use.

## Practice

**Observe:** usability-test one complete journey with three users. Record predictions, decisions, waits, errors, evidence used, and recovery without coaching.

**Design:** specify a golden path for an HTTP service from creation through retirement. Include supported envelope, capabilities, defaults, interfaces, docs, evidence, escape hatch, tests, and owner.

**Break:** make the deployment dependency unavailable and one documentation example stale. Measure whether the user can distinguish and recover from each failure.

**Say it out loud:** explain why fewer clicks can increase cognitive load and operational risk.

## Check yourself

1. What distinguishes a golden path from a template or portal page?
2. Which implementation evidence must remain reachable during incidents?
3. When should a workload receive a separate path rather than another option?
4. How would you test a path after initial creation?

## Sources

### REQUIRED

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### RECOMMENDED

- [DORA: Documentation quality](https://dora.dev/capabilities/documentation-quality/)

### DEEP DIVE

- [Cognitive dimensions of notations](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDtutorial.pdf)

## Next

Continue to [Portals, APIs, and interface coherence](04-portals-apis-and-interface-coherence.md).
