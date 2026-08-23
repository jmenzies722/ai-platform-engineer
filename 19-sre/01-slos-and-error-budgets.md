# SLIs, SLOs, and error budgets

An SLO states the reliability a defined user population should receive over a defined window.

## Why it matters

"Always available" is unmeasurable and economically impossible. SLOs align product and engineering around user-visible reliability and the cost of improvement.

## How it works

An SLI is a measured proportion of good events, such as successful eligible requests divided by eligible requests. An SLO sets its target and window. A 99.9% SLO permits 0.1% bad events; that allowance is the error budget.

Choose events, eligibility, goodness, measurement point, target, and rolling window. Burn rate compares current budget consumption with the sustainable rate. Multi-window alerts combine fast detection with protection from brief noise.

## See it yourself

At 1,000,000 eligible requests and 99.9%, the budget is 1,000 bad requests. A release causing 500 bad requests spends half the window's budget regardless of incident duration.

## Where it shows up

Release policy, reliability roadmaps, vendor objectives, and alerting should all refer to the same user promise.

## When it breaks

The SLI measures server uptime instead of user success, excludes hard requests, or becomes a target teams game.

## Practice

Define an SLI and SLO for checkout. List exclusions and the decision made when budget burn is excessive.

## Check yourself

1. What exactly is an error budget?
2. Why alert on burn rate rather than remaining budget alone?

## Sources

### REQUIRED
- [Google SRE: Service level objectives](https://sre.google/sre-book/service-level-objectives/)

### RECOMMENDED
- [Google SRE Workbook: SLOs](https://sre.google/workbook/implementing-slos/)

### DEEP DIVE
- [Multi-window burn-rate alerts](https://sre.google/workbook/alerting-on-slos/)

## Next

[Incidents and learning](02-incidents-and-learning.md)
