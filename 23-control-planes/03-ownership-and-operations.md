# Ownership, policy, and control-plane operations

A production control plane assigns authority over fields and side effects, enforces policy at defined boundaries, and exposes its own operational health. Ownership ambiguity turns retries and independent controllers into data corruption.

## Why it matters

Creating resources is easier than deciding who may mutate them, resolving concurrent intent, preserving audit evidence, and recovering after partial failure. Healthy processes can still operate on stale data or fail to converge.

## How it works

Assign one writer or an explicit merge rule to each desired field, status field, and external object. Track field manager and resource version so conflicting updates fail rather than silently overwrite. Controllers should ignore resources outside their scope and verify tenant and ownership before side effects.

Layer policy: authentication establishes principal, authorization decides action on resource, admission validates and defaults intent, quotas protect capacity, and reconciliation enforces facts known only from external observation. Record actor, decision, policy version, correlation, and result without secrets.

Separate API availability, reconciliation freshness, and data-plane continuity. A control plane can accept writes while queues are stuck, or be unavailable while existing workloads continue. Define indicators for each and communicate degraded behavior.

Protect durable state with tested backup and restoration, stable encryption and identity, schema compatibility, and point-in-time objectives. Canary controller changes against representative resources and ensure only compatible versions write shared status.

## Vocabulary

- **field ownership:** authority to write a specific part of a resource
- **optimistic concurrency:** rejecting updates based on a stale resource revision
- **admission:** synchronous processing before desired state is persisted
- **control-plane freshness:** delay between accepted intent and current observation or action

## See it yourself

Run two controllers that both set `status.ready` for different reasons. Predict what clients observe. Last writer wins and readiness loses meaning. Give each controller a separate condition or make one controller aggregate defined subordinate conditions. Optimistic concurrency prevents accidental overwrite but does not resolve semantic ownership.

## Where it shows up

A policy controller owns compliance conditions, while a database controller owns provider observations and endpoint. Admission rejects unsupported regions synchronously; provider permission loss appears asynchronously. An aggregator computes user-facing readiness from documented dependencies.

## When it breaks

Two controllers fight over fields, status update conflicts hot-loop, restored state points to wrong external identities, and audit logs cannot distinguish a user from a controller. API uptime masks queue backlog. Use conflict rate, status ownership tests, oldest reconcile age, desired-to-observed generation lag, restore drills, and audit correlation.

## Practice

**Observe:** create an ownership matrix for one resource covering metadata, every spec and status field, external objects, policy, and deletion.

**Build:** design operational indicators and SLOs for API writes, reconciliation freshness, and existing workload continuity. Define user-visible degraded states.

**Break:** run incompatible controller versions against one status schema and restore a stale backup. Specify detection, write fencing, rollback, and proof of repaired ownership.

**Say it out loud:** explain why process liveness does not prove control-plane correctness.

## Check yourself

1. When is shared field ownership safe?
2. Why can admission and reconciliation report different failures?
3. Which signals reveal a control plane that is alive but not converging?
4. What must a restore drill verify beyond reading backup bytes?

## Sources

### REQUIRED

- [Kubernetes server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)

### RECOMMENDED

- [Kubernetes API access control](https://kubernetes.io/docs/reference/access-authn-authz/)

### DEEP DIVE

- [CNCF Operator whitepaper](https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## Next

Continue to [Idempotency and external identity](04-idempotency-and-external-identity.md).
