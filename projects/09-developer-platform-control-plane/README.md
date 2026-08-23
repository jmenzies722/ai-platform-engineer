# 09 — Secure Developer Platform Control Plane

Create a narrow, researched paved road in an independent repository: service teams request an application environment and a controller continuously reconciles it.

## Problem and users

Developers lose time assembling inconsistent repositories, infrastructure, policy, and operational defaults. Platform operators then inherit bespoke systems and security teams discover controls too late. Interview at least five representative users and target one high-friction journey; self-service is successful only if teams can understand, trust, and leave it.

## Constraints and product boundaries

- Offer one versioned service API and one reference workload profile across two lifecycle environments.
- Use declarative desired state, asynchronous reconciliation, explicit status, and bounded tenancy.
- Integrate existing source, CI, infrastructure, identity, and catalog systems through adapters.
- Exclude a universal portal, arbitrary infrastructure provisioning, hidden admin credentials, and adoption mandates without user evidence.

## Architecture expectations

Separate product interface, API/auth, desired-state store, work queue, reconcilers, policy, adapters, and status/audit paths. Define idempotency, optimistic concurrency, condition semantics, retries, backoff, finalizers, dependency ordering, deletion, and manual intervention. Make trust boundaries and delegated identities visible. Design migration and escape-hatch contracts before adding templates.

## Milestone plan

1. Research users, map the journey, set adoption/support measures, and publish service boundaries.
2. Define API/status schemas and prove reconciliation against fake adapters.
3. Integrate repository, delivery, environment, policy, catalog, telemetry, and ownership setup.
4. Pilot with real users; run partial-failure, migration, compromise, rollback, and offboarding drills.

## Required artifacts

- Research synthesis, product brief, service blueprint, API schemas, status taxonomy, and roadmap.
- Control-plane architecture, threat model, ADRs, adapter contracts, and policy catalog.
- Golden-path guide, support model, SLOs, dashboards, runbooks, and API migration plan.
- Pilot evidence: task completion, lead time, adoption, abandonment, support burden, and satisfaction.

## Tests and failure drills

Use API compatibility, reconciliation, idempotency, authorization, policy, migration, and end-to-end tests. Inject duplicate events, stale desired state, lost wake-up, adapter timeout, partial provisioning, rate limits, revoked credentials, policy change, orphan deletion, poison resource, and control-plane restart. Demonstrate eventual convergence or a precise terminal condition.

## Observability, security, and cost

Expose queue age, reconcile latency/result, retries, resource condition age, adapter errors, policy denials, and user-journey completion. Use scoped workload identities per adapter, tenant authorization, secret references, audited overrides, signed templates, and approval for high-risk actions. Allocate external resource spend, control-plane compute, vendor/API cost, and support labor; compare paved-road cost with the baseline journey.

## Explicit success rubric

| Product/system outcome | Pass condition |
|---|---|
| User value | Pilot users complete the target journey faster with lower measured cognitive load. |
| Convergence | Fault tests produce correct resources or explicit actionable terminal status, never silent drift. |
| Security | Tenant and adapter boundaries withstand abuse tests; overrides are narrow, expiring, and audited. |
| Evolvability | A backward-compatible API upgrade and one adapter replacement complete without user outage. |
| Platform practice | Ownership, support, adoption, offboarding, and cost are treated as product concerns. |

## Stretch work

Add a composition API, scorecards tied to evidence rather than badges, or safe resource import/adoption.

## Authoritative sources

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [Team Topologies](https://teamtopologies.com/)
- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [NIST Zero Trust Architecture, SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)

## Mapped modules

[20 Security](../../20-security/README.md), [21 Platform Engineering](../../21-platform-engineering/README.md), [22 Developer Platforms](../../22-developer-platforms/README.md), [23 Control Planes](../../23-control-planes/README.md), [34 System Design](../../34-system-design/README.md), and [35 Senior and Staff Engineering](../../35-senior-staff-engineering/README.md).
