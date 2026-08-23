# 12 — AWS

AWS is a large catalog built from a small set of ideas: identity authorizes API calls, networks constrain reachability, and managed services trade control for operational leverage.

## What you will learn

- Trace a request through accounts, IAM, Regions, Availability Zones, and VPCs.
- Choose compute, storage, and data services from workload requirements.
- Use AWS safely: scoped credentials, read-only inspection, explicit cost awareness.

## Lessons

1. [Accounts, IAM, and the AWS API](01-identity-and-api.md)
2. [Regions, VPCs, and network boundaries](02-regions-and-vpcs.md)
3. [Compute, storage, and managed data](03-compute-storage-data.md)

## Practice

Complete the [read-only AWS inventory lab](lab-read-only-inventory.md). It works without credentials in planning mode and makes no resource changes when credentials are used.

## Ready to continue

You can explain why an IAM allow may still be denied, distinguish an Availability Zone from a subnet, and justify a service choice using failure, scaling, and cost constraints.

## Next

Continue to [DevOps](../13-devops/README.md).
