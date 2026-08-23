# Identity, authorization, and secrets

Strong systems establish who or what is acting, authorize the specific operation, and avoid treating credentials as permanent configuration.

## Why it matters

Authentication without narrow authorization gives compromise broad reach. Copied secrets cannot be reliably recalled and often outlive their original need.

## How it works

Authentication proves identity; authorization evaluates action, resource, context, and policy. Use phishing-resistant MFA and federation for humans. Give workloads distinct identities and short-lived credentials delivered at runtime. Apply least privilege and separation of duties, then audit both successes and denials.

Secrets require generation, encrypted storage, scoped retrieval, rotation, revocation, and leak response. Never store them in source, images, ordinary logs, URLs, or copied example files. Encryption protects confidentiality only when key access and endpoint integrity are sound.

## See it yourself

Compare one shared CI credential with per-repository workload federation. The latter can bind repository, branch, audience, lifetime, and target role without storing a reusable cloud key.

## Where it shows up

SSO, service accounts, TLS identities, cloud roles, database credentials, signing keys, and CI tokens.

## When it breaks

Authorization checks only UI visibility, token audiences are ignored, roles accumulate permissions, or rotation changes storage but not active consumers.

## Practice

Design machine identity for a deployment job. Specify trust subject, audience, role permissions, session duration, audit fields, and revocation.

## Check yourself

1. Why is a short-lived credential still sensitive?
2. What must authorization evaluate beyond identity?

## Sources

### REQUIRED
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

### RECOMMENDED
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

### DEEP DIVE
- [SPIFFE concepts](https://spiffe.io/docs/latest/spiffe-about/overview/)

## Next

[Secure delivery and response](03-secure-delivery-and-response.md)
