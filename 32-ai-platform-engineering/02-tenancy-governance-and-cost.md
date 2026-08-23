# Tenancy, governance, and cost

Shared AI platforms must isolate tenants, enforce policy, and make scarce-resource consumption attributable.

## Why it matters

One workload can exhaust accelerators, expose another tenant's data, poison a shared cache, or create spend no owner can explain. A namespace is an organizational label, not a complete security boundary. Multi-tenancy is a chain of enforcement points, and the weakest unscoped credential, query, queue, cache, or usage record can invalidate the whole claim.

## How it works

Begin with an authenticated principal issued by a trusted identity provider. The server maps that principal to a tenant and propagates an unforgeable tenant context into authorization, workload identity, namespaces, storage predicates, vector indexes, cache keys, queues, secrets, network policy, telemetry, and the usage ledger. Tenant labels supplied in a request are useful metadata but cannot authorize access or determine billing.

Isolation is layered because each control has a different failure boundary. API authorization controls requested actions; scheduler quotas control allocation; network policy controls reachable endpoints; workload identity controls downstream API calls; storage predicates and tenant-specific encryption context protect data. Stronger isolation may require separate nodes, accounts, projects, keys, or clusters when side channels, noisy neighbors, or regulatory boundaries exceed the assurance of logical controls. Document the threat model instead of calling either model universally secure.

Admission policy should be deterministic, versioned, and logged with principal, resource, action, decision, reason, and policy version, while omitting prompt and document bodies. Deny high-risk mutations when policy is unavailable. Pre-authorized emergency rollback may remain available because it reduces exposure to a previously approved state; the exception and its audit path must be designed before an outage.

Cost attribution follows the same trusted identity. Meter GPU-seconds, tokens, storage byte-hours, network, reserved capacity, and supportable shared allocations with idempotent usage records keyed by tenant and operation. Quotas bound instantaneous or cumulative harm, budgets trigger owner decisions, showback supplies feedback, and chargeback allocates money. None creates physical capacity. Global recovery reserves and per-tenant concurrency limits protect the platform from exhaustion.

## See it yourself

Create two synthetic tenants with the same resource ID `shared-name`. Query by resource ID alone and observe that both records match; the result proves the query is ambiguous, not that data was disclosed in production. Add the server-derived tenant predicate and assert exactly one result. Repeat with a cache key, quota bucket, and usage row. Replaying one request ID must count usage once. These bounded tests demonstrate tenant scoping and accounting idempotency at four boundaries, but they do not prove kernel, hypervisor, hardware, or cryptographic isolation.

## Where it shows up

In a shared model gateway, authenticated identity selects allowed models, retrieval namespace, regional and retention policy, quota, and cost center. Prompt bodies stay out of normal billing logs; tenant, request ID, model digest, token counts, policy version, and charge dimensions remain. Tenant-scoped response and prefix caches prevent identical inputs from crossing boundaries. Support access is approved, time-bounded, attributable, and reviewed rather than granted through a permanent administrator credential.

## When it breaks

Shared credentials erase attribution, labels are trusted as identity, storage queries omit tenant predicates, caches omit policy or corpus version, quotas ignore secondary resources, and logs contain sensitive content. For suspected crossover, stop risky reads if necessary, preserve authenticated principal, authorization decision, query/index namespace, cache key dimensions, workload credential, network flow, and audit event. Determine whether the fault is authorization, routing, storage, or observability before rotating unrelated secrets. For cost anomalies, reconcile idempotent gateway usage against scheduler allocations and provider bills; do not “fix” unexplained variance by changing rates.

## Practice

**Build:** define identity propagation, isolation controls, policy-outage behavior, quotas, metering, and redaction for two tenants sharing GPUs. **Break:** omit tenant from a query and cache key, use a shared workload credential, replay usage, and exhaust storage while within GPU quota. **Explain back:** state what each test proves, what it does not prove, and distinguish quota, budget, attribution, and capacity using auditable events.

## Check yourself

1. Why are namespaces insufficient isolation?
2. What should audit logs omit?
3. How do quota and budget differ?

## Sources

### REQUIRED

- [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)
- [NIST Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)

### RECOMMENDED

- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs/latest/)

### DEEP DIVE

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## Next

Continue to [Operating the platform as a product](03-operating-the-platform-as-a-product.md).
