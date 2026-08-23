# Operating the platform as a product

A platform succeeds when it improves user outcomes reliably, not when it merely accumulates features.

## Why it matters

Unused abstractions create maintenance cost while teams continue building private alternatives.

## How it works

Identify user journeys, publish service levels, instrument time-to-first-success and workflow completion, and maintain support and deprecation paths. Adoption, retention, reliability, support load, and user-owned lead time reveal different problems. Roadmaps should respond to repeated friction and strategic constraints, not the loudest isolated request.

Journey evidence combines telemetry with interviews: events show where users stop; conversations reveal why. Measures need counterbalances. Faster deployment paired with more rollbacks is not improvement. Platform teams should test prototypes with real consumers, publish limitations, and treat support as a sensing channel whose repeated cases become design inputs.

## See it yourself

Give a new team a representative service and observe without rescuing them. Record elapsed and active time, handoffs, failed commands, documentation searches, and support contacts. If deployment takes two hours but only 12 minutes of active work, reducing build speed will not fix the dominant waiting. The trace converts “hard to use” into specific friction.

## Where it shows up

A platform team can instrument the path from repository creation to healthy production deployment, then correlate completion with later reliability. A portal is one interface in that journey, not the product itself. Support categories reveal missing concepts; migration completion and old-path deletion reveal whether deprecation actually reduced load.

## When it breaks

Vanity adoption masks dissatisfaction, internal users cannot opt out, and deprecations transfer toil without migration help. When adoption stalls, first segment the journey funnel and review recent support cases and interviews. A start-rate problem differs from repeated failure or abandonment after first use. Check mandated usage separately from voluntary retention.

## Practice

**Build:** instrument one journey with completion, elapsed time, reliability, and support burden. **Break:** optimize a vanity metric while worsening rollback rate, then add a countermeasure. **Explain back:** present one roadmap choice grounded in traces and interviews, plus evidence that would reverse it.

## Check yourself

1. Why is resource count a weak success metric?
2. What makes deprecation credible?
3. How do support tickets inform design?

## Sources

### REQUIRED

- [Google Cloud DORA research](https://dora.dev/research/)

### RECOMMENDED

- [CNCF platform engineering whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### DEEP DIVE

- [SPACE framework](https://queue.acm.org/detail.cfm?id=3454124)

## Next

Continue to [Agentic Infrastructure](../33-agentic-infrastructure/README.md).
