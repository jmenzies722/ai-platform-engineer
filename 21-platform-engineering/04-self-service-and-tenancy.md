# Self-service and tenancy

Self-service delegates a bounded decision to a user and completes it through an auditable contract. Tenancy defines who may act on which resources, how shared capacity is isolated, and who pays when demand or failure crosses boundaries.

## Why it matters

Replacing a ticket with a button does not remove waiting if fulfillment still depends on hidden approvals. Poor tenant boundaries let one team see another team's data, exhaust shared capacity, or create costs no owner can explain.

## How it works

Start with the smallest intent the user can safely own: service class, region, capacity tier, data classification, and owner. Derive implementation choices from policy and defaults. Validate synchronously when possible, return a plan for material or destructive changes, and expose durable operation state for asynchronous work.

Define tenant identity independently of a single tool. Map people and workload identities to organizations, teams, environments, and resources. Authorization must cover discovery, mutation, logs, secrets, billing, support, and delegation. Namespace alone is not isolation; evaluate shared compute, network, credentials, caches, logs, backups, and provider quotas.

Choose an isolation tier based on threat, compliance, noisy-neighbor risk, blast radius, and cost. Shared infrastructure with logical policy may fit low-risk development. Dedicated accounts, clusters, keys, or control-plane partitions may be necessary for stronger boundaries. Publish which failures remain shared.

Apply quotas at dimensions users can understand, with current usage, forecast, and remediation. Attribute resource and support cost to a durable owner. For privileged or expensive actions, combine policy, explicit confirmation, and time-bounded approval without turning every request into manual fulfillment.

## Vocabulary

- **self-service:** user-initiated fulfillment within a published contract
- **tenant:** administrative and isolation boundary for a consumer or group
- **noisy neighbor:** tenant whose demand degrades service for others
- **delegation:** granting a principal bounded authority to act for another scope

## See it yourself

Threat-model a shared build service with two teams. Predict what happens if Team A submits 1,000 concurrent builds. Check CPU, queue, artifact namespace, logs, secret access, and spend. A per-team queue limit protects scheduling but does not prove artifact or credential isolation; each boundary needs separate evidence.

## Where it shows up

An environment-vending API accepts team, purpose, region, data class, and expiry. Policy selects a tenant account and network profile, quota admission checks capacity, and status returns operation progress and cost owner. Support staff can inspect state but cannot read workload secrets.

## When it breaks

Authorization checks only the create action while logs and search leak cross-tenant metadata. Global provider quotas create unexplained failures for unrelated teams. Shared service identities erase attribution. Long-running requests time out at the portal even though work continues, so users retry and create duplicates.

Distinguish capacity exhaustion from authorization denial and dependency outage in status and metrics. Monitor per-tenant saturation, queue age, denial reasons, cross-tenant access tests, and unattributed spend.

## Practice

**Observe:** trace one self-service request from identity to external resource. List every authorization, tenancy, quota, audit, and cost boundary. Completion means each boundary has an owner and evidence source.

**Design:** specify three isolation tiers for a build platform. State threat assumptions, shared dependencies, quotas, cost tradeoffs, and migration between tiers.

**Break:** simulate one tenant exhausting concurrency and another losing team ownership. Define expected API responses, alerts, containment, and recovery without exposing tenant data.

**Say it out loud:** explain why self-service is an authorization and operations design, not a portal feature.

## Check yourself

1. Which platform decisions should remain with the consumer?
2. Why does a namespace not prove tenant isolation?
3. How should quota denial differ from an infrastructure failure?
4. When is stronger physical isolation economically justified?

## Sources

### REQUIRED

- [NIST SP 800-204A: Building Secure Microservices-based Applications Using Service-Mesh Architecture](https://csrc.nist.gov/pubs/sp/800/204/a/final)

### RECOMMENDED

- [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)

### DEEP DIVE

- [AWS SaaS Tenant Isolation Strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html)

## Next

Continue to [Platform operating model and support](05-operating-model-and-support.md).
