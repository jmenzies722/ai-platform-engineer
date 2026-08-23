# Adoption and organizational change

Platform adoption is a behavior change that must earn trust through useful outcomes, credible migration, and responsive support. Communication can create awareness, but repeated successful use creates adoption.

## Why it matters

A technically sound capability can fail because users discover it too late, cannot migrate safely, or distrust its support model. A mandate may increase recorded usage while teams route critical work around the platform.

## How it works

Map eligible users by journey, constraints, current alternative, migration cost, and influence. Establish a baseline before launch. Recruit design partners who represent important segments, not only friendly early adopters. Agree on success and stop criteria and retain their failures as product evidence.

Stage adoption through awareness, evaluation, first success, repeated use, and expansion. At each stage, identify the user question and observable drop-off. Supply examples, migration tools, compatibility checks, office hours, and published support. Champions can translate local context but must not become unpaid platform operators.

Prefer incentives built into the product: lower effort, better reliability evidence, faster approvals, or funded migration help. Use mandates when a documented organization-wide risk requires them, and measure outcome and workaround behavior separately from compliance.

Close the loop visibly. Publish changes linked to research and incidents, explain declined requests, and report known limits. Trust falls when roadmap promises repeatedly outrun delivery or telemetry is used to rank individual developers.

## Vocabulary

- **design partner:** representative user who tests a product increment against agreed outcomes
- **activation:** first successful completion of the intended journey
- **retained adoption:** repeated intended use after activation
- **change network:** local participants who help interpret and communicate a change

## See it yourself

Construct a cohort table for teams first using a deployment path in January, February, and March. Predict what a single cumulative adoption percentage hides. Measure activation and repeated use after 30 and 60 days. Cohorts reveal abandonment and improvement over releases, but interviews are still needed to explain why.

## Where it shows up

A deployment platform starts with five design partners. Two fail because its runtime lacks sidecar support, one succeeds but keeps the old path for rollback, and two retain use. Instead of announcing broad availability, the team narrows the target segment, fixes rollback evidence, and publishes the unsupported workload class.

## When it breaks

Early adopters are unusually skilled and hide usability problems. Migration estimates omit test and rollback work. Registration is reported as adoption. Teams keep duplicate paths indefinitely, increasing cost and incident ambiguity. Champions absorb support without authority or capacity.

Track funnel conversion, cohort retention, time to first success, migration effort, duplicate-path age, support demand, and outcome changes by segment. Pair telemetry with interviews; neither alone explains behavior.

## Practice

**Observe:** choose a platform journey and build an adoption funnel with eligibility, activation, 30-day retention, and known alternative use. Completion means every numerator has a defined denominator and data source.

**Design:** create a rollout for three user segments. Include design-partner selection, migration help, feedback channels, success and stop criteria, support capacity, and communication.

**Break:** assume leadership mandates the platform after weak retention. Design measurements that expose shadow use and a response that preserves the risk objective without claiming false product success.

**Say it out loud:** distinguish awareness, activation, compliance, and retained adoption.

## Check yourself

1. Why can design partners produce misleading evidence?
2. Which incentives are evidence of product value rather than coercion?
3. How would you detect teams maintaining two delivery paths?
4. When is a mandate justified, and what must still be measured?

## Sources

### REQUIRED

- [DORA platform engineering research](https://dora.dev/research/2024/dora-report/)

### RECOMMENDED

- [CNCF Platform Engineering maturity model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/)

### DEEP DIVE

- [Accelerate State of DevOps research program](https://dora.dev/research/)

## Next

Continue to [Metrics and platform economics](08-metrics-and-economics.md).
