# Identity, security, and supply-chain boundaries

An IDP is a privileged coordinator: it reads engineering metadata, delegates identities, creates repositories and infrastructure, and distributes templates and plugins. Its security design must limit what each user, workflow, and artifact can do.

## Why it matters

Compromising the portal or one plugin can become an organization-wide supply-chain incident if broad tokens, mutable templates, cross-tenant search, and unaudited workflows share one trust boundary.

## How it works

Authenticate users through the organizational identity provider and workloads through short-lived machine identity. Authorize every server-side read and action using subject, tenant, entity, intent, environment, and policy. The frontend is not a trusted enforcement point.

Delegate narrowly. A create-service operation can receive a short-lived token scoped to one tenant, repository prefix, workflow, and expiry. Separate human approval identity from execution identity. Store secrets in a managed system, redact logs, and never place credentials in generated repositories or workflow inputs.

Secure software inputs: pin and verify template sources, sign release artifacts, produce provenance and dependency inventory, scan changes, and protect publishing. Treat plugins and workflow actions as executable supply-chain components with review, sandboxing, network controls, and revocation.

Threat-model catalog confidentiality, ID enumeration, cross-tenant search, server-side request forgery, untrusted template parameters, callback spoofing, and audit tampering. Keep immutable security events with actor, delegated subject, action, resource, decision, policy version, and correlation ID.

## Vocabulary

- **workload identity:** non-human identity issued to a running process
- **delegation:** bounded authority granted for a specific operation
- **provenance:** verifiable account of how an artifact was produced
- **confused deputy:** privileged system induced to misuse its authority for another party

## See it yourself

Draw the identity chain for a user launching a workflow that creates a repository and cloud resource. Predict the effect of using one static portal token. Then assign separate short-lived scopes and audit subjects. Reduced scope limits blast radius; it does not prove the workflow validates malicious input.

## Where it shows up

A scaffolder fetches an approved immutable template, renders without secrets, commits through a scoped app identity, and records provenance. Infrastructure provisioning uses another identity bound to the target tenant. The audit log links both to the requesting user and approval.

## When it breaks

Portal administrators can read all tenant secrets, plugin backends inherit core credentials, template parameters execute shell syntax, and stale group membership retains authorization. Audit logs omit delegated identity. Detect with negative authorization tests, token-scope inspection, egress tests, artifact verification, secret scanning, and access reviews.

## Practice

**Observe:** enumerate identities and credentials across one IDP workflow. Record issuer, audience, scope, lifetime, storage, rotation, audit subject, and revocation.

**Design:** threat-model service creation with trust boundaries, five abuse cases, preventive and detective controls, residual risk, and evidence.

**Break:** compromise one plugin token and inject hostile template input. Show how scope, validation, isolation, and logging contain and reveal each attempt.

**Say it out loud:** explain the confused-deputy risk in a self-service portal.

## Check yourself

1. Why must approval and execution identities be distinguishable?
2. Which catalog data may require read authorization?
3. How does artifact provenance differ from vulnerability scanning?
4. What evidence demonstrates that plugin compromise is tenant-bounded?

## Sources

### REQUIRED

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)

### RECOMMENDED

- [SLSA specification](https://slsa.dev/spec/v1.0/)

### DEEP DIVE

- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

## Next

Continue to [Operating an IDP and its golden paths](08-operating-the-idp.md).
