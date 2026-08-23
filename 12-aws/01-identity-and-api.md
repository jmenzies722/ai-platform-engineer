# Accounts, IAM, and the AWS API

Every AWS console click becomes an authenticated API request evaluated inside an account. Learn that path before learning service menus.

## Why it matters

Identity is the first boundary in AWS. A leaked long-lived key or broad role can cross every network boundary through service APIs, while a correct least-privilege role limits both mistakes and compromise.

## How it works

An account is an ownership, billing, and policy boundary. A principal signs a request with temporary credentials. AWS authenticates it, builds an authorization context, and evaluates applicable identity policies, resource policies, permission boundaries, session policies, and organization policies. An explicit deny wins; otherwise at least one applicable allow is required. IAM roles are assumed identities, not people or machines. STS issues their short-lived credentials.

Prefer federation for humans and workload roles for software. Keep the root user for account recovery, protect it with MFA, and do not create root access keys.

Authorization is evaluated for a specific principal, action, resource, and request context. Resource-based policies can name principals; role trust policies control who may call `AssumeRole`; permission boundaries cap identity-policy grants; service control policies cap member-account permissions but do not grant them. Conditions such as organization ID, source VPC endpoint, principal tags, and requested Region narrow otherwise valid allows. Cross-account access usually requires both caller-side permission and resource or trust-side permission.

Credential vending is part of the design. A human federation session, EC2 instance profile, task role, and web-identity session all produce temporary credentials but have different trust inputs and delivery paths. Applications should use the standard credential chain, avoid logging environment or metadata responses, and refresh before expiry. CloudTrail evidence should connect sensitive API calls to session issuer, source, and request time.

## Vocabulary

- **principal:** an identity making a request
- **policy:** JSON rules containing effect, action, resource, and optional conditions
- **STS:** service that issues temporary credentials

## See it yourself

Read a policy with `aws iam get-policy-version` only if authorized. Predict whether each statement applies from action, resource, and condition. `aws sts get-caller-identity` reveals the current account and principal without listing resources.

Build a decision table for one allowed and one denied request. Include identity policy, resource policy, boundary, session policy, organization policy, and relevant conditions. Compare the prediction with IAM policy simulation only when approved, remembering that simulation does not reproduce every service-specific control or live resource state.

## Where it shows up

CI uses web identity to assume a deployment role whose trust conditions bind repository, workflow, branch, environment, and audience. EC2 and containers obtain workload-specific role credentials from local metadata endpoints that must be protected from untrusted code. Cross-account access combines trust policy and caller permissions, while resource policies can provide direct access for supported services. Break-glass roles require strong authentication, alerting, session recording where possible, and automatic expiry.

## When it breaks

Common causes are the wrong account, expired credentials, a missing resource-policy allow, an organization deny, a permissions boundary, a key policy, or a condition mismatch. Some services intentionally obscure existence with denial. Do not "fix" `AccessDenied` by adding `Action: "*"`. Preserve request ID and timestamp, inspect caller, action, resource ARN, session issuer, Region, and policy path, then make the narrowest reviewed change.

Credential leaks require more than deleting one key: disable or revoke the credential, inspect API history and created persistence, rotate affected downstream secrets, and repair the issuance path. A successful API call after repair is necessary but does not prove prior compromise caused no side effects.

## Practice

**Observe:** capture caller identity and explain its credential source, session duration, boundary, and organization context without exposing credential material.

**Build:** write a policy allowing reads from one S3 prefix and denying unencrypted object uploads. Add a condition that binds expected account or organization context and identify which requirement cannot be enforced by an allow alone.

**Break safely:** evaluate a sandbox request with wrong prefix, expired session, and explicit deny. Completion means each denial is distinguished from network failure and the repair does not broaden unrelated resources.

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
