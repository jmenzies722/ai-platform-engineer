# Toil, capacity, and sustainable operations

Sustainable reliability requires limiting repetitive operational work and provisioning capacity before demand removes safety margins.

## Why it matters

Toil grows with service size and consumes the engineering time needed to remove its causes. Capacity shortages create nonlinear latency and cascading failure.

## How it works

Toil is manual, repetitive, automatable, tactical work with little enduring value that scales with service growth. Measure it, eliminate unnecessary work, simplify the system, then automate stable procedures. Automation itself needs ownership, tests, limits, and observability.

Capacity planning combines demand forecasts, per-unit resource cost, headroom, provisioning lead time, quotas, and failure scenarios. Load testing finds saturation points; admission control preserves useful work when demand exceeds capacity.

## See it yourself

If one operator spends five minutes per tenant weekly, 600 tenants consume 50 hours. A self-service workflow matters; automating a rare ambiguous incident may not.

## Where it shows up

Ticket queues, certificate renewal, account provisioning, autoscaling, quotas, queue limits, and on-call load.

## When it breaks

Teams automate a broken process, autoscaling reacts slower than traffic, forecasts ignore failover capacity, or headroom is reclaimed as waste.

## Practice

Inventory one month's operational tasks. Score frequency, duration, risk, growth rate, and automation suitability; select one elimination target.

## Check yourself

1. What distinguishes toil from all operational work?
2. Why is average utilization insufficient for capacity planning?

## Sources

### REQUIRED
- [Google SRE: Eliminating toil](https://sre.google/sre-book/eliminating-toil/)

### RECOMMENDED
- [Google SRE: Software engineering in SRE](https://sre.google/sre-book/software-engineering-in-sre/)

### DEEP DIVE
- [Google SRE: Handling overload](https://sre.google/sre-book/handling-overload/)

## Next

[Security](../20-security/README.md)
