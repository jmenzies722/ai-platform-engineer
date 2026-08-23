# Operations, observability, and safe automation

Operating AWS well means connecting user impact to telemetry, changes, quotas, and audit evidence while ensuring automation has bounded authority and a safe stop.

## Why it matters

Managed services remove some infrastructure work, not operational ownership. Without useful signals and change history, teams respond to symptoms by restarting resources, broaden permissions under pressure, and discover quotas or expired dependencies during an incident.

## How it works

CloudWatch collects service metrics, custom metrics, logs, alarms, and events. CloudTrail records supported API activity for audit and investigation; it is not an application performance monitor. AWS Config can record supported resource configuration and evaluate rules. Systems Manager provides controlled inventory and operational actions without opening general inbound administration paths.

Start with service-level indicators tied to user outcomes: successful request ratio, latency, correctness, durability, and freshness. Add saturation signals such as concurrency, queue age, connection use, throttles, and quota headroom. Logs should be structured, correlated, retained intentionally, and protected from secrets. Alarms need an owner, response, severity, and enough context to distinguish dependency failure from workload failure.

Automation should be idempotent, scoped to resources and actions, rate limited, observable, and reversible where the underlying operation permits it. Use temporary credentials and separate read, deploy, and emergency roles. Record runbook inputs and outputs without recording credentials.

## See it yourself

In an approved account, run `aws cloudwatch describe-alarms --state-value ALARM` and `aws cloudtrail lookup-events --max-results 10`. Predict whether an alarm identifies user impact or only a resource symptom. Correlate one event time with a deployment record. Absence from lookup results does not prove no API call occurred because event coverage, Region, retention, and trail configuration matter.

## Where it shows up

For a queue-backed worker, queue age measures delayed user work better than CPU alone. A deployment annotation explains a sudden error-rate change, CloudTrail identifies a policy edit, and quota dashboards show whether scaling can succeed. An EventBridge rule may invoke a bounded remediation, but repeated remediation failure should page a human rather than loop indefinitely.

## When it breaks

High-cardinality custom metrics create cost and unusable dashboards. Logs leak tokens or customer data. A composite alarm hides the failing component. Missing time synchronization breaks correlation. Automated remediation deletes evidence or oscillates. An expired certificate or exhausted quota has no warning.

During diagnosis, preserve timestamps, request IDs, deployment digests, alarm transitions, and relevant API events before changing state. Test query permissions and retention before incidents.

## Practice

**Observe:** select one request path and identify one user SLI, one dependency signal, one saturation signal, and one change record. Prove each can be queried.

**Build:** create a paper or sandbox alarm design with threshold rationale, evaluation window, owner, runbook, and false-positive test. Add quota and certificate expiry checks.

**Break safely:** replay synthetic failures in a sandbox or tabletop a dependency throttle. Completion means the evidence distinguishes application error, authorization denial, capacity exhaustion, and bad deployment, and automation stops after a bounded attempt count.

## Check yourself

1. Why does CloudTrail not replace application telemetry?
2. Which signal reveals growing asynchronous user delay?
3. What properties keep remediation automation from amplifying failure?
4. Why should a runbook state what evidence to preserve?

## Sources

### REQUIRED

- [AWS Well-Architected Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)

### RECOMMENDED

- [Amazon CloudWatch concepts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html)

### DEEP DIVE

- [AWS Builders' Library: automating safe hands-off deployments](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)

## Next

[Cost models, allocation, and optimization](06-cost-and-governance.md)
