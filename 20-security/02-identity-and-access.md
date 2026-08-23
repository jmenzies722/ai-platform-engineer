# Identity, authentication, and authorization

Identity names a principal, authentication establishes evidence about it, and authorization decides whether that principal may perform a specific action on a resource under current policy.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Human authentication should resist phishing with passkeys or hardware-backed factors and protect recovery paths. Workload identity should use short-lived, audience-bound credentials rooted in attested platform identity. Authorization can combine roles, attributes, relationships, and policy; deny by default and evaluate server-side.

Least privilege covers actions, resources, conditions, duration, and delegation. Separate control-plane and data-plane authority. Log policy decision, principal, resource, action, and reason without logging credentials.

## See it yourself

If a role permits `read` on 10,000 resources but a job needs two for one hour, action-only least privilege still grants 5,000 times the resource scope plus excess duration. Privilege is multidimensional, not a role-name property.

## Where it shows up

Cloud federation, service-to-service calls, support tools, and break-glass access need explicit trust policies and revocation. Test both allowed and denied cases, including cross-tenant object identifiers.

## When it breaks

Confused deputies use a service’s authority for an attacker, stale groups preserve access, wildcard policies expand silently, and local checks diverge. Inspect credential issuer, subject, audience, policy version, decision logs, and resource ownership.

## Practice

Write an authorization matrix for a multi-tenant document API and executable deny tests. Inject a user-controlled tenant ID. Completion means object ownership is derived from trusted context, cross-tenant access fails, and break-glass use is time-bound and audited.

## Check yourself

1. How do authentication and authorization differ?
2. What makes a credential audience-bound?
3. How does a confused deputy arise?
4. Which dimensions make a policy least-privileged?

## Sources

### REQUIRED

- [NIST SP 800-63 Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

### RECOMMENDED

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

### DEEP DIVE

- [SPIFFE specification](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)

## Next

[Cryptography, key management, and TLS](03-cryptography-and-tls.md)
