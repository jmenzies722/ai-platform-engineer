# Lab: build an AWS architecture evidence pack

Build and review an evidence-backed AWS architecture without creating, changing, or deleting resources. The result connects IAM, VPC, compute, storage, data, availability, operations, and cost rather than producing an unexamined resource list.

## Safety

Use a sandbox or approved account and a read-only role. Commands are retrieval operations, but results can contain account IDs, ARNs, network ranges, tags, and names; keep raw output in an approved private location. Never broaden a role to complete the lab. If you have no credentials, use a reviewed architecture diagram and mark every claim that lacks direct evidence.

## Setup

Confirm CLI v2 with `aws --version`. Use an approved named profile:

```bash
export AWS_PROFILE=readonly
export AWS_REGION=us-east-1
aws sts get-caller-identity
```

Record UTC time, CLI version, profile, Region, account, and caller ARN. Stop if the account or assumed role is unexpected. An `AccessDenied` response is evidence about the current boundary, not permission to add an allow.

## Collect scoped evidence

```bash
aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName'
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,CIDR:CidrBlock,Default:IsDefault}'
aws ec2 describe-subnets --query 'Subnets[].{Id:SubnetId,Vpc:VpcId,AZ:AvailabilityZone,CIDR:CidrBlock}'
aws ec2 describe-route-tables --query 'RouteTables[].{Id:RouteTableId,Vpc:VpcId,Routes:Routes}'
aws ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,AZ:Placement.AvailabilityZone,Subnet:SubnetId,Role:IamInstanceProfile.Arn}'
aws elbv2 describe-load-balancers --query 'LoadBalancers[].{Name:LoadBalancerName,Scheme:Scheme,Vpc:VpcId,AZs:AvailabilityZones[].ZoneName}'
aws s3api list-buckets --query 'Buckets[].Name'
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,MultiAZ:MultiAZ,AZ:AvailabilityZone,Backup:BackupRetentionPeriod}'
aws cloudwatch describe-alarms --state-value ALARM --query 'MetricAlarms[].{Name:AlarmName,Metric:MetricName,Reason:StateReason}'
aws service-quotas list-service-quotas --service-code ec2 --query 'Quotas[].{Name:QuotaName,Value:Value}' --max-results 20
```

`list-buckets` is account-global; the EC2, load-balancing, RDS, CloudWatch, and quota queries use regional context. Large accounts need pagination and tighter approved filters. Do not dump policies, object contents, database records, Secret values, user data, or log bodies.

## Build the architecture map

Choose one workload and draw account, Region, VPC CIDR, subnets by AZ, routes, load balancer, compute, role attachment, data stores, object stores, and operational signals. For every edge, state protocol, identity, route, security control, timeout, and retry owner. A route to an internet gateway does not prove an instance is publicly reachable.

Create four tables:

1. **Authorization:** principal, requested action, resource scope, condition, and explicit-deny sources.
2. **Failure:** component, AZ or Region dependency, health signal, failover mechanism, RTO, RPO, and untested assumption.
3. **Operations:** user SLI, alarm, deployment or API audit evidence, quota headroom, owner, and runbook.
4. **Cost:** fixed and variable units, transfer boundaries, retention, idle capacity, owner, and technical growth cap.

Every statement must cite a command, approved diagram, or clearly marked assumption.

## Failure review

Tabletop these events without changing resources:

- one compute AZ becomes unavailable;
- the current caller receives `AccessDenied`;
- queue or function concurrency reaches a dependency limit;
- the primary data store is deleted or corrupted;
- daily request volume increases tenfold;
- telemetry ingestion increases tenfold.

For each, predict user symptom, first reliable signal, automatic response, manual decision, evidence to preserve, and recovery verification. Separate AZ failover from data restoration. A green resource health check is insufficient; name a user-visible transaction.

## Cost and governance review

Use the public AWS Pricing Calculator or approved billing views to estimate baseline and tenfold load. Include compute, storage, requests, backups, logs, public addressing, and transfer. State the unit cost denominator. Identify one budget notification and one technical bound such as quota, autoscaling maximum, retention, or admission control. Do not claim that a budget prevents spending.

## Deliverables and completion

The lab is complete when another engineer can review:

- context and evidence manifest with collection times;
- architecture and authorization map;
- service-choice decision for compute, storage, and data;
- failure table with RTO and RPO gaps;
- observability and quota table;
- baseline, burst, and abuse cost model;
- three prioritized changes, each with owner and verification evidence.

Ask the reviewer to select one claim and reproduce it from the cited evidence. Record disagreements and unknowns instead of smoothing them away.

## Finish

Unset temporary shell context:

```bash
unset AWS_PROFILE AWS_REGION
```

No cleanup is otherwise required because the lab creates no resources.
