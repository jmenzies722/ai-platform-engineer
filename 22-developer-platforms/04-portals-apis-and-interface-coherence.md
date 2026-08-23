# Portals, APIs, and interface coherence

A developer portal is a discovery and interaction surface over platform contracts, not the platform's system of record. APIs, CLI, Git workflows, and portal actions must preserve the same intent, authorization, status, and audit semantics.

## Why it matters

Portal-only automation becomes a bottleneck for CI and expert users. Independently implemented interfaces drift: a form may omit a security field, a CLI may bypass approval, and a Git workflow may expose no operation status.

## How it works

Place durable resource and workflow APIs beneath interfaces. The portal discovers catalog entities, documentation, capabilities, and operation status through those APIs. It may hold presentation preferences, but business state belongs to an authoritative service with backup, concurrency, and lifecycle semantics.

Design task-focused views rather than mirroring provider consoles. Show prerequisites, effective policy and defaults, plan, cost or quota effects, operation state, evidence, and recovery. Deep links should retain stable entity and operation identity, not fragile UI routes.

Use a shared identity model and central authorization decision. Each interface submits actor, delegated subject when applicable, tenant, intent, and idempotency key. Record the evaluated policy version and result. Machine interfaces need the same actionable errors as humans, with stable codes and redacted messages.

Manage frontend and API compatibility independently. Feature-detect supported capabilities, version breaking contracts, and test representative journeys through every supported interface. Accessibility, latency, search quality, and degraded behavior are operational requirements.

## Vocabulary

- **portal:** user-facing aggregation and interaction surface
- **system of record:** authority for durable state
- **interface parity:** equivalent contract and control semantics across supported channels
- **deep link:** stable URL to identified context or operation

## See it yourself

Submit the same invalid service request through portal, CLI, and Git. Predict the result if validation is duplicated in each client. Contract tests should show the same error code, rule, and remediation, while presentation differs. Equality of one error does not prove full semantic parity.

## Where it shows up

A deployment page resolves service ownership from the catalog, submits desired release to a deployment API, and displays controller status and logs. If the portal is unavailable, CI continues through the same API and users can recover from durable operation records.

## When it breaks

The portal stores approval state locally, admin views bypass tenant authorization, search reveals restricted entities, or frontend timeout is presented as operation failure. Client-side validation differs from API policy. Detect with cross-interface contract tests, authorization probes, operation correlation, accessibility tests, and synthetic journeys.

## Practice

**Observe:** trace one portal action to its systems of record. Mark state stored only in the UI, duplicate validation, identity transitions, and evidence links.

**Build:** design portal, CLI, and Git interactions for one environment request. Specify common API intent, errors, operation status, auth context, and idempotency behavior.

**Break:** take the portal offline after submission. Prove the operation remains inspectable and controllable through another supported interface without duplicate creation.

**Say it out loud:** explain why a portal can disappear while a well-designed platform continues operating.

## Check yourself

1. Which state may safely live only in a portal?
2. How can interface parity be tested without requiring identical presentation?
3. Why should authorization be re-evaluated server-side?
4. What does a user need when the interface times out but work continues?

## Sources

### REQUIRED

- [Backstage architecture overview](https://backstage.io/docs/overview/architecture-overview/)

### RECOMMENDED

- [W3C Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)

### DEEP DIVE

- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)

## Next

Continue to [Plugin architecture and extensibility](05-plugin-architecture-and-extensibility.md).
