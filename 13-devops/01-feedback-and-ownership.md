# Feedback loops and shared ownership

DevOps improves the system that turns an idea into reliable behavior and returns production evidence to the people who can act on it.

## Why it matters

Long handoffs hide queues, dilute context, and reward local optimization. A development team measured only on feature output and an operations team measured only on stability will rationally work against each other.

## How it works

Map the complete value stream: decision, code, review, build, test, deployment, release, observation, and learning. Measure elapsed time as well as active work. Shorten feedback by making work small, automating repeatable checks, and putting operational consequences near the change.

Shared ownership does not mean everyone has every permission. It means teams can understand and operate their services within safe boundaries, while specialists build reusable capabilities and coach difficult work. Blameless learning examines system conditions without removing individual accountability for careful action.

Feedback operates at several speeds: editor and unit-test feedback in seconds, integration and policy feedback in minutes, deployment verification in minutes to hours, and operational and customer learning over longer windows. Optimize the slowest decision-relevant loop rather than maximizing raw automation. Limit work in progress so blocked changes become visible instead of joining a larger queue.

Ownership needs explicit interfaces. A service team owns user outcomes, on-call response, dependency budgets, and lifecycle decisions. A platform team owns the paved-road contract and reliability of shared capabilities. Security and reliability specialists define constraints, supply reusable controls, and retain escalation paths. Runbooks, service catalogs, and escalation policies make those boundaries executable.

## See it yourself

Take one recent change and reconstruct timestamps for request, start, review, queue, build, deploy, release, first production verification, and recovery if needed. Separate touch time from wait time. If coding took two hours but delivery took six days, optimizing compiler speed is not the current constraint. Compare one normal and one failed change so speed is not studied without safety.

## Where it shows up

Service teams carry dashboards, alerts, runbooks, and ownership metadata with code. Platform teams expose tested deployment paths and measure adoption and task success. Security supplies policy and feedback inside delivery instead of acting only as a final gate. Incident reviews return concrete changes to these systems, and product feedback tests whether faster delivery improved outcomes.

## When it breaks

Renaming operations engineers "DevOps" preserves the handoff. A central ticket queue becomes an invisible dependency. Excess alerts create noise rather than feedback. Full autonomy without standards duplicates undifferentiated work, while centralized control disconnects decisions from consequences. Metrics used to rank individuals become targets; deployment frequency can rise while user value and reliability decline.

Diagnose the system with queue age, rework, blocked time, escaped defects, change failure, recovery time, reliability objectives, and qualitative operator evidence. Never infer individual performance from a socio-technical system metric.

## Practice

**Observe:** draw a value-stream map for one production change with touch and wait time, owners, information handoffs, and returned evidence.

**Build:** define service and platform ownership contracts, including permissions, support, reliability objectives, and escalation. Propose one reversible experiment against the longest queue.

**Break safely:** tabletop an incident spanning service, platform, and security teams. Completion means one incident lead is clear, evidence routes to decision owners, temporary authority expires, and learning produces a measurable system change.

## Check yourself

1. Why is shared ownership different from universal access?
2. Which measure reveals waiting hidden by activity?

## Sources

### REQUIRED
- [Google Cloud: DevOps capabilities](https://cloud.google.com/architecture/devops)

### RECOMMENDED
- [The DevOps Handbook resources](https://itrevolution.com/product/the-devops-handbook-second-edition/)

### DEEP DIVE
- [DORA research](https://dora.dev/research/)

## Next

[Continuous integration and delivery](02-continuous-delivery.md)
