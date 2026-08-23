# Compute, storage, and managed data

Choose AWS services from workload behavior and failure requirements, not from product popularity.

## Why it matters

EC2, Lambda, containers, S3, EBS, RDS, and DynamoDB expose different scaling units, consistency contracts, operational duties, and prices. The wrong fit creates fragile workarounds.

## How it works

EC2 provides virtual machines and host-level control. Managed container services schedule images while retaining container semantics. Lambda runs bounded event-driven invocations. For data, S3 stores immutable object values by key, EBS exposes AZ-scoped block devices, and EFS exposes a shared filesystem.

RDS manages relational database infrastructure while you still own schema, queries, connections, and much capacity planning. DynamoDB partitions items by key and scales around access patterns. Queues such as SQS decouple producers from consumers but may redeliver, so consumers must be idempotent.

Evaluate total cost: idle capacity, requests, storage, data transfer, logs, backups, and operator time. Tagging helps attribution but does not enforce architecture.

## See it yourself

For a thumbnail job, compare: an always-on VM polling a queue, a container worker that scales on depth, and a function triggered by messages. Include burst size, execution time, retry behavior, and idle cost.

## Where it shows up

A common service uses a load balancer, stateless compute across AZs, a managed database, S3 for objects, and a queue for asynchronous work. Each boundary needs timeout, retry, identity, and observability decisions.

## When it breaks

Lambda concurrency can overwhelm a database. Hot partition keys limit DynamoDB. An EBS volume cannot silently become multi-AZ shared storage. Queue retries duplicate side effects. S3 data transfer and observability volume can dominate expected compute savings.

## Practice

Write a decision record for a small upload-processing service. Specify scaling unit, durable state, delivery guarantee, recovery point, recovery time, and top cost drivers.

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
