# Operating the platform as a product

A platform succeeds when it improves user outcomes reliably, not when it merely accumulates features.

## Why it matters

Unused abstractions create maintenance cost while teams continue building private alternatives. Mandated adoption can make a platform look successful even when it lengthens delivery, shifts toil to users, or cannot support important workloads. Product practice makes investment conditional on evidence that a defined user journey improved without degrading reliability, safety, or cost.

## How it works

Start with a bounded user and job, such as “a model team promotes an evaluated digest to staging.” Map the service blueprint: visible steps, platform actions, dependencies, handoffs, waits, failure states, and responsibility. Publish eligibility, non-goals, service levels, support channels, and escape conditions. A portal screen is one touchpoint; the product is the complete path to a safely operated outcome.

Instrument the journey with server-side events tied to a privacy-preserving journey ID. Measure time to first success, active versus elapsed time, completion, abandonment stage, failure reason, support contacts, and later operational outcomes. Segment new and experienced users, workload class, voluntary and mandated consumers, and platform version. Adoption counts reach; voluntary retention suggests recurring value; neither proves causation. Pair quantitative funnels with task observation and interviews because events show where users stopped but usually not why.

Use counterbalanced measures. A lead-time reduction accompanied by higher rollback, policy bypass, support burden, or unit cost is not an unqualified improvement. Establish a baseline, define the expected mechanism, pilot with a representative cohort, and compare the same journey under explicit workload assumptions. This is bounded evidence, not a randomized proof: staffing, seasonality, and workload mix may confound the result.

Treat support and lifecycle as product mechanisms. Categorize cases by journey step and root cause, preserve useful rejection evidence, and convert repeated problems into documentation, API, default, or capability changes. Deprecation requires consumer inventory, migration tooling, compatibility tests, owner communication, deadlines, and deletion of the old path. Maintaining two permanent roads doubles operational states and prevents the claimed simplification.

## See it yourself

Give a new team a synthetic but representative service and observe without rescuing them. Record elapsed and active time, handoffs, failed commands, searches, policy rejections, and support contacts. Suppose deployment takes 120 minutes but only 12 minutes are active: 75 minutes await access approval and 25 await capacity. A faster build can recover at most the remaining eight minutes, so it cannot halve lead time. The arithmetic bounds the likely gain; observation and interviews still determine whether approval, documentation, or the task design caused the wait.

## Where it shows up

A training platform can follow a team from dataset selection through first reproducible run, or a serving platform from approved artifact to healthy canary. A journey dashboard links completion to later reliability and cost without storing model inputs. A quarterly review can fund a better policy explanation over a new feature if denials dominate abandonment. Product boundaries also make a valid “do not build” decision possible when an existing service or documentation change solves the observed problem.

## When it breaks

Vanity adoption masks dissatisfaction, surveys sample only successful users, telemetry records starts but not outcomes, and deprecations transfer toil without migration help. When adoption stalls, segment the funnel before changing the roadmap. Low starts may indicate discovery or eligibility; repeated policy denial indicates contract mismatch; first-use completion followed by abandonment indicates weak recurring value. Check instrumentation changes and mandated usage before interpreting a trend. Debug a support spike by release, journey step, tenant cohort, and root cause rather than treating ticket volume as user incompetence.

## Practice

**Build:** define one persona, job, service blueprint, baseline, funnel, SLO, countermetrics, and support taxonomy. **Break:** increase deployment starts while worsening rollback and abandonment, then show why the original dashboard misled. **Explain back:** make one roadmap or stop-investing choice grounded in traces and interviews, identify confounders, and name evidence that would reverse the decision.

## Check yourself

1. Why is resource count a weak success metric?
2. What makes deprecation credible?
3. How do support tickets inform design?

## Sources

### REQUIRED

- [Google Cloud DORA research](https://dora.dev/research/)
- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### RECOMMENDED

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

### DEEP DIVE

- [SPACE framework](https://queue.acm.org/detail.cfm?id=3454124)

## Next

Continue to [Data and feature platform contracts](04-data-and-feature-platform-contracts.md).
