# Authentication, Authorization, and API Evolution

An API must establish who is calling, decide what that identity may do to this resource, and evolve without turning old clients into security exceptions.

## Why it matters

A valid token does not authorize reading every invoice. A role check performed only in the UI is not enforcement. A seemingly harmless response field can leak tenant data to old caches. Identity and API compatibility are production contracts that must survive proxies, retries, rolling deployments, and adversarial input.

## How it works

Authentication verifies a credential and constructs a principal with issuer, subject, audience, assurance, and other trusted claims. Authorization evaluates that principal, action, resource, and context against policy. The resource must be loaded or identified in a way that prevents insecure direct object reference: changing `/accounts/17` to `/accounts/18` must trigger another object-level decision.

Opaque session identifiers let a server revoke and rotate state centrally. Signed tokens let a service validate claims locally but require strict algorithm, issuer, audience, expiry, and key-selection checks. A JWT is an encoding and signature container, not a session policy. Store browser session credentials in secure, HTTP-only cookies when appropriate, protect cookie-authenticated state changes against CSRF, rotate sessions across privilege changes, and never put bearer credentials in URLs or logs.

Password storage uses a purpose-built, salted, adaptive password hash with parameters that can be upgraded. Rate limits and abuse controls supplement authentication but must avoid making account enumeration easy. Service-to-service identity needs the same audience and authorization discipline as users.

API evolution prefers additive changes. Clients must tolerate unknown response fields, while servers cannot assume new request fields exist until old clients are gone. Renaming or changing semantics needs a versioned migration, telemetry, and a sunset policy. Cursor pagination uses an opaque position tied to a stable ordering; offset pagination can skip or repeat records under concurrent writes. Error bodies should expose a stable machine code and safe detail, not internal stack traces.

## See it yourself

Predict that Alice may read her own record, cannot read Bob’s record, and an administrator can read either. Notice that authentication alone never decides this.

```bash
python3 - <<'PY'
def authorize(principal, action, resource):
    if action != "invoice:read":
        return False
    return "admin" in principal["roles"] or resource["owner"] == principal["sub"]
alice = {"sub": "alice", "roles": []}
admin = {"sub": "ops", "roles": ["admin"]}
for p in (alice, admin):
    for owner in ("alice", "bob"):
        print(p["sub"], owner, authorize(p, "invoice:read", {"owner": owner}))
PY
```

Expected observation: the decision includes principal, action, and resource ownership rather than trusting possession of an identifier.

Limits of the observation: this policy has no credential verification, tenant boundary, delegation, policy version, audit log, or denial reason. A production check must use trusted resource attributes and default to denial.

## Where it shows up

A bulk export endpoint authenticates a support user, authorizes export for one tenant, limits fields by policy, creates an asynchronous job, and returns a status resource. The download uses a short-lived scoped capability. Audit records capture actor, tenant, policy decision, and export ID without copying the exported personal data into logs.

## When it breaks

401 generally means usable authentication is absent; 403 means the authenticated principal is not permitted, though APIs may return 404 to conceal resource existence. Sudden token rejection can come from clock skew, audience mismatch, issuer confusion, or key rotation. Cross-tenant access is a critical authorization failure. Capture sanitized token metadata, policy version, principal ID, action, resource tenant, decision, request ID, and clock state. Never paste a live bearer token into a ticket or decode it on an untrusted website.

## Practice

**Build:** define an API for tenant-scoped invoices with stable errors, cursor pagination, session rotation, and object-level policy tests. **Break:** alter object IDs, use expired and wrong-audience tokens, omit new fields from an old client, and rotate signing keys. **Explain back:** separate authentication evidence from each authorization input. Success includes deny-by-default tests, redacted logs, compatibility tests, and a migration plan for one breaking field.

## Check yourself

1. Why is a valid signed token insufficient to authorize a resource read?
2. How can adding a response field create a compatibility or security problem?

## Sources

### REQUIRED

- [OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)

### RECOMMENDED

- [RFC 7519: JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

### DEEP DIVE

- [Google Zanzibar](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/)

## Next

Continue to [Queues, Delivery, and Workflow State](./05-queues-delivery-and-workflow-state.md).
