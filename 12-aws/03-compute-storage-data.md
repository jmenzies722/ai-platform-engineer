# Compute, storage, and managed data

Choose AWS services from workload behavior and failure requirements, not from product popularity.

## Why it matters

EC2, Lambda, containers, S3, EBS, RDS, and DynamoDB expose different scaling units, consistency contracts, operational duties, and prices. The wrong fit creates fragile workarounds.

## How it works

EC2 provides virtual machines and host-level control. Managed container services schedule images while retaining container semantics. Lambda runs bounded event-driven invocations. For data, S3 stores immutable object values by key, EBS exposes AZ-scoped block devices, and EFS exposes a shared filesystem.

RDS manages relational database infrastructure while you still own schema, queries, connections, and much capacity planning. DynamoDB partitions items by key and scales around access patterns. Queues such as SQS decouple producers from consumers but may redeliver, so consumers must be idempotent.

Evaluate total cost: idle capacity, requests, storage, data transfer, logs, backups, and operator time. Tagging helps attribution but does not enforce architecture.

Choose by invariants before features. Compute decisions include startup latency, execution duration, privilege, networking, concurrency, state, architecture, and deployment unit. Storage decisions include access pattern, latency, mutability, sharing, durability, topology, lifecycle, and restore. Data decisions include schema and query shape, transaction boundaries, consistency, partition key, connection behavior, recovery, and ownership.

Managed does not mean unbounded. Lambda concurrency, ECS task counts, EC2 quotas, RDS connections and IOPS, DynamoDB partitions, S3 request patterns, and SQS in-flight limits expose distinct saturation signals. Backpressure and admission should protect the slowest stateful dependency. Encrypt in transit and at rest with a recoverable key policy, scope workload roles, and avoid putting credentials in images or user data.

## See it yourself

For a thumbnail job, compare an always-on VM polling a queue, a container worker scaling on age and depth, and a function triggered by messages. Include burst size, duration, cold start, concurrency, retry, dead-letter handling, database pressure, idle cost, transfer, observability, and operator work. Predict the first quota or dependency to saturate at tenfold load.

## Where it shows up

A common service uses a load balancer, stateless compute across AZs, a managed database, S3 for objects, and a queue for asynchronous work. Each boundary needs timeout, retry budget, idempotency, identity, encryption, saturation, and observability decisions. The request record can commit in the database before a transactional outbox publishes asynchronous work, avoiding an unsafe dual write.

## When it breaks

Lambda concurrency can overwhelm a database. Hot partition keys limit DynamoDB. Connection storms follow scale-out. An EBS volume cannot silently become multi-AZ shared storage. Queue retries duplicate side effects and poison messages block progress without isolation. S3 lifecycle mistakes remove recovery data. Regional service quotas stop scaling even when metrics request more capacity. Transfer and observability volume can dominate compute savings.

Distinguish these with concurrency, throttles, partition consumption, connection use, queue age and receive count, IOPS and latency, quota headroom, and user transactions. Retrying every error without a deadline or idempotency key often amplifies the incident.

## Practice

**Observe:** choose one workload and map runtime, storage, database, and queue usage to scaling units, quotas, failure domains, and cost units.

**Build:** write a decision record for an upload-processing service. Specify access patterns, scaling unit, durable state, consistency, delivery guarantee, idempotency, RPO, RTO, security boundary, and top cost drivers.

**Break safely:** tabletop duplicate delivery, database connection exhaustion, and one-AZ loss. Completion means the design bounds retries, preserves accepted work, exposes saturation before failure, and verifies recovery through a processed upload.

## Check yourself

1. Which responsibilities remain yours when using a managed database?
2. Why does queue-based scaling require idempotent consumers?

## Sources

### REQUIRED
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

### RECOMMENDED
- [AWS decision guides](https://aws.amazon.com/getting-started/decision-guides/)

### DEEP DIVE
- [AWS Builders' Library](https://aws.amazon.com/builders-library/)

## Next

[Availability, recovery, and resilient design](04-availability-and-recovery.md)
