# AWS operator sheet

Use the AWS CLI to gather scoped evidence, not to browse production by trial and
error. Service APIs, IAM evaluation, regions, and eventual consistency make
empty or denied results ambiguous.

## Confirm identity, region, and partition

```bash
# Read-only
aws sts get-caller-identity
aws configure get region
aws configure list
```

`Account` and `Arn` establish the current principal. They do not prove intended
role, effective permissions, or resource ownership. A blank configured region
may still be supplied by environment, profile, or command flags. Always pass
`--region <region>` for regional incident queries.

**Caution:** `aws configure list` identifies credential sources. Do not print
environment variables, credential files, session tokens, presigned URLs, or
Secret values.

## Is this a lookup, permission, or location problem?

```bash
# Read-only examples
aws ec2 describe-instances --region <region> \
  --filters Name=tag:Service,Values=<service> \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,AZ:Placement.AvailabilityZone,PrivateIp:PrivateIpAddress}' \
  --output table

aws resourcegroupstaggingapi get-resources --region <region> \
  --tag-filters Key=Service,Values=<service> \
  --resources-per-page 50
```

An empty list can mean wrong region/account, filters, unsupported resource type,
eventual consistency, or genuinely no resource. `AccessDenied` is useful
evidence: capture operation, resource ARN, principal ARN, request ID, and encoded
authorization message if supplied. Do not switch to broader credentials merely
to bypass policy.

Use explicit `--max-items` or service pagination for broad listings. CLI
`--query` filters returned data; it does not always reduce service-side work.

## Is compute unhealthy or only reported unhealthy?

```bash
# Read-only
aws ec2 describe-instance-status --region <region> \
  --instance-ids <instance-id> --include-all-instances

aws elbv2 describe-target-health --region <region> \
  --target-group-arn <target-group-arn>
```

EC2 system checks concern AWS infrastructure; instance checks concern the guest
network/software path. A passing EC2 check does not prove application health.
Target health reason codes distinguish registration, draining, health-check
failure, and unused targets. Correlate target port, path, matcher, security
groups, application logs, and deployment time.

## Is the network policy path plausible?

```bash
# Read-only
aws ec2 describe-security-groups --region <region> \
  --group-ids <security-group-id>
aws ec2 describe-route-tables --region <region> \
  --filters Name=association.subnet-id,Values=<subnet-id>
aws ec2 describe-network-acls --region <region> \
  --filters Name=association.subnet-id,Values=<subnet-id>
```

Security groups are stateful; network ACLs are stateless and ordered. A route
marked `blackhole` has an unavailable target. Configuration plausibility does
not prove packet traversal. Include source and destination IP, ports, protocol,
subnets, both directions, and any load balancer or transit layer.

**Caution:** Opening `0.0.0.0/0`, adding broad egress, or attaching another
security group is a remote security mutation, not a diagnostic shortcut.

## Did metrics or audit history change?

```bash
# Read-only; choose bounded UTC timestamps
aws cloudwatch get-metric-data --region <region> \
  --metric-data-queries file://<reviewed-query.json> \
  --start-time <utc-start> --end-time <utc-end>

aws cloudtrail lookup-events --region <region> \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-id> \
  --start-time <utc-start> --end-time <utc-end> --max-results 50
```

CloudWatch periods, dimensions, statistic, ingestion delay, and missing-data
semantics affect interpretation. Missing points are not zero unless the metric
contract says so. CloudTrail Event history covers management events with
documented scope and retention; absence does not prove no data event or
cross-region action occurred. Preserve event ID, request ID, actor, source IP,
and event time.

## Is throttling or dependency health the cause?

AWS SDK/CLI errors include a service code and request ID. Distinguish
`Throttling`, `AccessDenied`, validation errors, and service-side `5xx`.
Retries can amplify an outage. Respect SDK retry guidance, apply jittered
backoff, and bound attempts. Check the
[AWS Health Dashboard](https://health.aws.amazon.com/health/status) and account
Health events, but do not assume a public green status excludes account-specific
failure.

## Controlled change and rollback

Before any remote mutation:

1. Save a redacted current-state description and resource tags.
2. Confirm account, region, resource ARN, owner, and change approval.
3. Define application success, CloudWatch guardrails, and a time-bounded watch.
4. Specify rollback API/configuration and validate that stateful effects are
   reversible.
5. Prefer infrastructure-as-code and normal deployment paths over CLI mutation.

`--dry-run` is service-specific, often checks authorization rather than full
validity, and is not universal. Do not infer safety from the flag's name.

Escalate for root or organization-level access, KMS key policy, IAM trust or
permission boundaries, public exposure, data deletion, cross-account routing,
security findings, or any resource whose rollback depends on backups not yet
verified.

## Authoritative sources

- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/)
- [AWS API references](https://docs.aws.amazon.com/index.html)
- [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/)
- Repository lesson: [AWS](../12-aws/README.md)
