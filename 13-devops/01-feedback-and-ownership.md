# Feedback loops and shared ownership

DevOps improves the system that turns an idea into reliable behavior and returns production evidence to the people who can act on it.

## Why it matters

Long handoffs hide queues, dilute context, and reward local optimization. A development team measured only on feature output and an operations team measured only on stability will rationally work against each other.

## How it works

Map the complete value stream: decision, code, review, build, test, deployment, release, observation, and learning. Measure elapsed time as well as active work. Shorten feedback by making work small, automating repeatable checks, and putting operational consequences near the change.

Shared ownership does not mean everyone has every permission. It means teams can understand and operate their services within safe boundaries, while specialists build reusable capabilities and coach difficult work. Blameless learning examines system conditions without removing individual accountability for careful action.

## See it yourself

Take one recent change and reconstruct timestamps. If coding took two hours but delivery took six days, optimizing compiler speed is not the current constraint.

## Where it shows up

Service teams carry dashboards and runbooks with code. Platform teams expose tested deployment paths. Security supplies policy and feedback inside delivery instead of acting only as a final gate.

## When it breaks

Renaming operations engineers "DevOps" preserves the handoff. Excess alerts create noise rather than feedback. Full autonomy without standards duplicates undifferentiated work. Metrics used to rank individuals become targets instead of signals.

## Practice

Draw a value-stream map for one production change. Find the longest queue and propose one reversible experiment that shortens it.

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
