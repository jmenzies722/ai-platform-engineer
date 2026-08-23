# Cost models, allocation, and optimization

Cloud cost is an architectural signal: every request, byte, retained log, idle reservation, and cross-boundary transfer connects a technical choice to a bill.

## Why it matters

Elastic capacity can reduce waste, but it can also scale an inefficient or attacked workload quickly. Teams that inspect only the monthly total cannot attribute regressions, predict marginal cost, or stop a runaway service before budget impact becomes material.

## How it works

Build a cost model from workload units. Separate fixed cost from variable cost and express a useful denominator such as cost per successful order, tenant, build, or million requests. Include compute duration or reservation, provisioned and consumed capacity, storage by class and retention, requests, backups, support, observability ingestion, public IPv4, and data transfer between Availability Zones, Regions, and the internet.

Cost allocation tags and account structure assign ownership, but not every charge is taggable. Cost Categories and CUR data can encode shared-cost rules. Budgets report actual or forecast spend; Cost Anomaly Detection surfaces unusual patterns. Neither is a hard spending cap. Service quotas, autoscaling maxima, request admission, and organization policy can provide stronger technical bounds.

Optimize after measuring utilization and constraints. Remove idle resources, right-size, schedule nonproduction capacity, choose storage lifecycle rules, then consider Savings Plans or reservations for a stable baseline. Commitments trade flexibility for rate reduction and should not conceal an oversized architecture.

## See it yourself

Use the AWS Pricing Calculator without credentials to model one steady service and a tenfold burst. Predict which line item becomes dominant. If authorized, compare the model with Cost Explorer grouped by service and account. Billing data has latency and allocation limitations, so a match supports the model but does not prove every resource is correctly attributed.

## Where it shows up

An image service can have cheap functions yet expensive object requests, transfer, and logs. A multi-AZ database pays for resilience while cross-AZ chatty application traffic adds variable cost. A per-upload unit metric makes the regression visible even as total business volume grows.

## When it breaks

Untagged shared infrastructure becomes nobody's responsibility. Cardinality explosions inflate telemetry spend. Lifecycle rules delete required recovery points. Spot interruption assumptions violate service objectives. A budget alert reaches an unowned mailbox after costs are incurred. Reserved capacity remains after demand moves.

Investigate by comparing unit volume, architecture changes, rate changes, and usage quantities. Never optimize by removing redundancy, backups, encryption, or evidence without explicitly re-approving the reliability and security requirement.

## Practice

**Observe:** inventory one workload's top five usage quantities and map each to an owner and technical control.

**Build:** create a monthly and per-unit model for baseline, expected peak, and abuse scenario. Add budget thresholds, anomaly routing, autoscaling maxima, and a decision record for shared-cost allocation.

**Break safely:** double one usage driver in the model and simulate an untagged resource. Completion means you can detect the change, identify an accountable owner, and cap further growth without interrupting critical recovery controls.

## Check yourself

1. Why is a budget not a spending cap?
2. Which costs can rise when a workload becomes multi-AZ?
3. When does a commitment increase rather than reduce risk?
4. What makes cost per unit more diagnostic than total spend?

## Sources

### REQUIRED

- [AWS Well-Architected Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)

### RECOMMENDED

- [AWS Cost Management user guide](https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html)

### DEEP DIVE

- [FinOps Framework](https://www.finops.org/framework/)

## Next

[DevOps](../13-devops/README.md)
