# Multitenancy and security boundaries

A multitenant control plane preserves authorization, confidentiality, fairness, and blast-radius boundaries across API storage, caches, queues, workers, credentials, external providers, status, and audit logs.

## Why it matters

An API can reject cross-tenant reads while a shared controller credential, global cache, error message, or queue still leaks data or lets one tenant consume every worker and provider quota.

## How it works

Define tenant identity and immutable resource scope. Authenticate principals, authorize list, watch, read, write, status, and delete, and prevent user-controlled fields from changing tenant. Filter before pagination and counting so metadata is not leaked through totals or timing.

Carry tenant context through queue keys, logs, metrics, traces, provider calls, and idempotency keys. Use per-tenant or narrowly scoped workload credentials where practical. Validate external ownership before mutation; never trust a user-supplied provider identifier by itself.

Apply layered isolation to storage, encryption keys, caches, workers, networks, and provider accounts according to threat and compliance. Shared infrastructure needs explicit residual blast radius. Enforce per-tenant rate, concurrency, quota, and queue fairness alongside global dependency protection.

Limit status and error detail to authorized information. Audit both user intent and controller side effects with tenant and delegated identity. Test negative paths continuously; configuration review alone does not prove isolation.

## Vocabulary

- **tenant context:** identity and scope carried with an operation
- **fairness:** preventing one tenant from monopolizing shared progress
- **side channel:** indirect information leak through timing, counts, errors, or resource use
- **blast radius:** maximum affected scope of compromise or failure

## See it yourself

Enqueue 10,000 resources for Tenant A and one for Tenant B into FIFO. Predict B's convergence delay. Add fair queues or per-tenant concurrency while retaining global rate limits. Fair scheduling proves progress isolation for this queue; provider-wide quotas may still couple tenants.

## Where it shows up

A SaaS provisioning plane stores tenant-scoped resources, uses tenant-bound provider roles, partitions queue concurrency, and redacts provider account IDs from unauthorized users. Operators use audited break-glass access with expiry rather than a permanent global token.

## When it breaks

List authorization is correct but watch streams leak events. Cache keys omit tenant. Metrics contain resource names, dead-letter queues are globally readable, and one tenant drives provider throttling. Detect with cross-tenant canaries, property-based auth tests, queue-age distribution by tenant, credential-scope inspection, and provider-quota attribution.

## Practice

**Observe:** trace tenant context through create, queue, reconcile, status, logs, metrics, external API, backup, and deletion. Completion means no transition relies on implicit global context.

**Build:** design isolation tiers for a control plane serving regulated and standard tenants. State boundaries, shared dependencies, fairness, credentials, cost, and migration.

**Break:** attempt cross-tenant list, crafted external ID adoption, queue starvation, and log discovery. Define expected denial and evidence without leaking target existence.

**Say it out loud:** explain why API authorization is necessary but insufficient for multitenancy.

## Check yourself

1. Where can tenant identity be lost after admission?
2. How can pagination leak unauthorized resource counts?
3. Which shared dependencies remain cross-tenant failure domains?
4. What evidence supports a claim of tenant isolation?

## Sources

### REQUIRED

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)

### RECOMMENDED

- [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)

### DEEP DIVE

- [AWS SaaS Tenant Isolation Strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html)

## Next

Continue to [Reliability, scaling, and verification](08-reliability-scaling-and-verification.md).
