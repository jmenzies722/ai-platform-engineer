# Availability, recovery, and resilient design

AWS provides isolated failure domains and managed recovery mechanisms, but an architecture becomes resilient only when every critical dependency has an explicit failure and restoration story.

## Why it matters

Placing two instances behind a load balancer does not make a service highly available if both use one Availability Zone, one NAT gateway, or an unrecoverable database. Recovery objectives turn vague reliability claims into testable engineering constraints.

## How it works

Design backward from business impact. The recovery time objective (RTO) is the maximum acceptable restoration time; the recovery point objective (RPO) is the maximum acceptable data loss measured in time. Availability Zones are independent infrastructure locations within a Region. Multi-AZ designs tolerate an AZ failure when compute, networking, and stateful dependencies actually span zones and traffic can move without manual reconstruction.

Health checks and load balancers remove unhealthy targets, but they cannot prove business correctness. Auto Scaling replaces capacity from a launch template; it does not restore local disk state. Managed database Multi-AZ features usually improve availability, while read replicas often serve scaling or regional recovery and may be asynchronous. Backups protect against deletion and corruption only when retention, access, restore procedures, and key dependencies are tested.

Multi-Region operation adds data-replication lag, conflict policy, DNS or routing convergence, duplicated controls, and substantial cost. Choose backup-and-restore, pilot light, warm standby, or active-active from RTO, RPO, and failure likelihood rather than prestige.

## See it yourself

Take a production architecture diagram and make a table with component, failure domain, persisted state, detection signal, automatic response, manual decision, RTO, and RPO. Predict the first dependency that violates the service objective if one AZ disappears. Confirm placement with read-only inventory and compare the diagram with deployed reality. This establishes architectural evidence, not proof that failover works.

## Where it shows up

An order API may run stateless instances in three AZs behind an Application Load Balancer, use an RDS Multi-AZ deployment, store receipts in versioned S3, and queue fulfillment in SQS. Losing one AZ should reduce capacity but preserve intake. Corrupt orders require point-in-time recovery or application compensation, a different mechanism from AZ failover.

## When it breaks

Nominally redundant targets share one subnet or quota. Retry storms consume surviving capacity. DNS caches delay regional redirection. Replicated corruption reaches every replica. Backups exist but cannot be decrypted because a key or role was deleted. A failover passes infrastructure health while critical writes fail.

Distinguish these cases with target health by AZ, dependency error rates, replication lag, queue age, restore logs, and user-level synthetic transactions. Do not trigger production failover without an approved runbook, stop conditions, and a named incident owner.

## Practice

**Observe:** map one service's zone placement and backup inventory using approved read-only evidence. Completion means every critical state store has a named recovery mechanism and unknowns are explicit.

**Build:** write an RTO/RPO-driven recovery plan with detection, traffic movement, data validation, communications, and return-to-normal steps.

**Break safely:** tabletop the loss of one AZ and then accidental data deletion. Record where the responses differ, inject one unavailable dependency into a sandbox if possible, and prove recovery with a user-visible transaction rather than resource status alone.

## Check yourself

1. Why can Multi-AZ availability still fail the RPO requirement?
2. Which shared dependencies can invalidate otherwise redundant compute?
3. When is backup-and-restore a better choice than active-active?
4. What evidence proves restored data is usable rather than merely present?

## Sources

### REQUIRED

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

### RECOMMENDED

- [AWS disaster recovery options](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)

### DEEP DIVE

- [AWS Builders' Library: static stability](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/)

## Next

[Operations, observability, and safe automation](05-operations-and-observability.md)
