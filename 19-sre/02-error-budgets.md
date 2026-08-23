# Error budgets and burn-rate control

An error budget translates an SLO into allowable unreliability and a decision policy. It balances change and stability only when teams agree in advance what budget consumption changes.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

For target `S`, budget fraction is `1-S`. Burn rate is observed bad-event fraction divided by the budget fraction. A burn rate of one consumes budget exactly at the sustainable pace; fourteen consumes it fourteen times faster.

Multi-window, multi-burn alerts pair a fast window with a longer confirmation window. Policy can slow releases, require reliability review, or prioritize repair. Budgets are not permission to intentionally harm users and do not replace incident response.

## See it yourself

A 99.9% objective has a 0.1% budget. A 1.4% bad-event rate burns at `1.4 / 0.1 = 14`, exhausting a 30-day budget in about `30 / 14`, or 2.14 days, if sustained.

## Where it shows up

Use separate objectives for critical journeys and dependencies where ownership differs. Review budget trends with product and engineering. Record exceptions, expiry, and recovery conditions so policy does not become discretionary during pressure.

## When it breaks

Low-volume ratios can page on one event, delayed data can hide fast burn, and teams can change exclusions to restore budget. Require minimum event evidence, pipeline health checks, and SLI governance.

## Practice

Calculate burn rates for synthetic windows and implement two threshold conditions. Inject a brief spike and a sustained regression. Completion means only policy-worthy patterns page and the release decision follows the written policy.

## Check yourself

1. What does burn rate one mean?
2. Why combine short and long windows?
3. How can an error budget be gamed?
4. Which release action follows sustained overspend in your policy?

## Sources

### REQUIRED

- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

### RECOMMENDED

- [Google SRE: Embracing Risk](https://sre.google/sre-book/embracing-risk/)

### DEEP DIVE

- [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/)

## Next

[Incident response and command](03-incident-command.md)
