# Accounts, IAM, and the AWS API

Every AWS console click becomes an authenticated API request evaluated inside an account. Learn that path before learning service menus.

## Why it matters

Identity is the first boundary in AWS. A leaked long-lived key or broad role can cross every network boundary through service APIs, while a correct least-privilege role limits both mistakes and compromise.

## How it works

An account is an ownership, billing, and policy boundary. A principal signs a request with temporary credentials. AWS authenticates it, builds an authorization context, and evaluates applicable identity policies, resource policies, permission boundaries, session policies, and organization policies. An explicit deny wins; otherwise at least one applicable allow is required. IAM roles are assumed identities, not people or machines. STS issues their short-lived credentials.

Prefer federation for humans and workload roles for software. Keep the root user for account recovery, protect it with MFA, and do not create root access keys.

## Vocabulary

- **principal:** an identity making a request
- **policy:** JSON rules containing effect, action, resource, and optional conditions
- **STS:** service that issues temporary credentials

## See it yourself

Read a policy with `aws iam get-policy-version` only if authorized. Predict whether each statement applies from action, resource, and condition. `aws sts get-caller-identity` reveals the current account and principal without listing resources.

## Where it shows up

CI uses web identity to assume a deployment role. EC2 and containers obtain role credentials from local metadata endpoints. Cross-account access combines trust policy and caller permissions.

## When it breaks

Common causes are the wrong account, expired credentials, a missing resource-policy allow, an organization deny, or a condition mismatch. Do not "fix" `AccessDenied` by adding `Action: "*"`. Inspect the caller, action, resource ARN, and policy evaluation path.

## Practice

Write a policy allowing reads from one S3 prefix and denying unencrypted object uploads. Identify which requirement cannot be enforced by an allow alone.

## Check yourself

1. Why does an identity-policy allow not always authorize a request?
2. Why are temporary role credentials safer than distributed access keys?

## Sources

### REQUIRED
- [AWS IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

### RECOMMENDED
- [AWS security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### DEEP DIVE
- [AWS Organizations service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)

## Next

[Regions, VPCs, and network boundaries](02-regions-and-vpcs.md)
