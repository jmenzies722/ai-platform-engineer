# Lab: Perform a Read-Only AWS Architecture Review

Build a bounded architecture inventory from read-only AWS APIs, test it against reliability and security questions, and produce findings without changing cloud state.

## Prerequisites

- AWS CLI v2 and `jq`
- An approved sandbox account and profile with read-only permissions
- Familiarity with IAM, VPC, EC2, load balancing, RDS, and tagging

## Safety

Obtain account-owner approval. Use only `Get`, `List`, and `Describe` APIs. Never run a command containing create, put, update, modify, delete, start, stop, reboot, attach, detach, authorize, revoke, associate, or disassociate. Set one approved region and stop on unexpected accounts, access-denied scope, sensitive tags, or more than 200 returned resources. API calls can appear in audit logs.

## Setup and baseline

```bash
mkdir -p .work
export AWS_PROFILE=approved-read-only
export AWS_REGION=us-east-1
export AWS_PAGER=
aws sts get-caller-identity | tee .work/identity.json
aws configure list | tee .work/config.txt
```

Verify account ID and principal with the owner before continuing. Do not copy account IDs, ARNs, IP addresses, or tags into public evidence.

## Tasks

1. Create a command allowlist in `.work/allowlist.txt`: `sts get-caller-identity`, `ec2 describe-vpcs`, `ec2 describe-subnets`, `ec2 describe-route-tables`, `ec2 describe-security-groups`, `elbv2 describe-load-balancers`, `rds describe-db-instances`, and `cloudwatch describe-alarms`.
2. Run only approved entries with `--max-items 200` where supported and save JSON under `.work/raw/`.
3. Use `jq` to produce counts and redacted relationships: VPC to subnet, subnet to availability zone, load balancer to subnet, and database to Multi-AZ status.
4. Review five questions: failure-domain coverage, public ingress, unrestricted egress, database resilience, and alarm coverage.
5. For every finding include evidence, risk, uncertainty, and a proposed validation. Do not recommend a mutation as though it has already been approved.
6. Record denied APIs as visibility gaps, not proof that a resource does not exist.

## Evidence to keep

Keep timestamp, CLI version, account alias chosen for the lab, region, command allowlist, redacted inventory, query scripts, findings, and limitations. Hash raw files with `sha256sum`; retain raw cloud data only in an approved encrypted location.

## Failure injection

Copy the redacted inventory to `.work/incomplete.json` and remove one availability-zone field locally:

```bash
jq 'if length > 0 then .[0].availability_zone = null else . end' \
  .work/redacted-subnets.json >.work/incomplete.json
```

Run the review check against this fixture. Expected result: `unknown` or `insufficient evidence`, never a healthy assertion. No cloud resource is changed.

## Cleanup

```bash
unset AWS_PROFILE AWS_REGION AWS_PAGER
rm -rf .work
```

Follow the account owner's evidence-retention policy and verify no credentials were written.

## Rubric

- 2 points: verifies principal, account, region, and allowlist
- 3 points: maps key relationships with bounded read-only calls
- 2 points: produces evidence-linked findings with uncertainty
- 2 points: treats denial and missing fields as unknown
- 1 point: redacts and removes local cloud inventory safely

## Sources

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS CLI command reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
