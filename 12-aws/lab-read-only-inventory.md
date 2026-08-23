# Lab: read-only AWS inventory

Build a precise picture of the active AWS identity and one Region without creating, changing, or deleting resources.

## Safety

Use a sandbox or approved account and a read-only role. Commands below are retrieval operations, but results can contain account IDs, ARNs, network ranges, and names; do not publish them. If you have no credentials, read each command and predict its response shape.

## Setup

Confirm CLI v2 with `aws --version`. Use an approved named profile:

```bash
export AWS_PROFILE=readonly
export AWS_REGION=us-east-1
aws sts get-caller-identity
```

Stop if the account or assumed role is unexpected.

## Inventory

```bash
aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName'
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,CIDR:CidrBlock,Default:IsDefault}'
aws ec2 describe-subnets --query 'Subnets[].{Id:SubnetId,Vpc:VpcId,AZ:AvailabilityZone,CIDR:CidrBlock}'
aws ec2 describe-route-tables --query 'RouteTables[].{Id:RouteTableId,Vpc:VpcId,Routes:Routes}'
aws s3api list-buckets --query 'Buckets[].Name'
```

`list-buckets` is account-global. EC2 queries use the selected Region. Access denial is valid evidence; record which action was denied rather than broadening permissions.

## Analysis

Choose one VPC and draw its subnet-to-AZ placement and route-table associations. Identify public routes, but do not infer public reachability without checking addresses, security groups, and listeners. Record:

- caller ARN, account, profile, and Region;
- each observed fact and the command that supports it;
- unknowns that require a different read permission;
- one cost or security question raised by the inventory.

## Finish

Unset temporary shell context:

```bash
unset AWS_PROFILE AWS_REGION
```

No cleanup is otherwise required because the lab creates no resources.
