# The platform that shipped but did not land

> **Synthetic/composite case:** Meridian Works, its organization, services, survey results, costs, and events are fictional. The case combines recurring platform-product and governance patterns for teaching and does not describe a real company.

## Context and constraints

Meridian's 46 application teams deploy 212 production services. Creating a new service requires repository setup, CI, cloud identity, a runtime environment, catalog registration, policy review, telemetry, and on-call ownership. The median elapsed time is nine business days, but the spread is wide: experienced teams finish in three days while regulated teams often need sixteen.

A six-person platform group builds Launchpad, a control plane and portal for one supported HTTP-service path. A request persists desired state, runs policy, and reconciles source, CI, identity, Kubernetes, telemetry, and catalog adapters. Status conditions expose partial failure. The implementation has:

- idempotent reconciliation and bounded retries;
- scoped adapter identities and tenant authorization;
- a signed service template with tested rollback;
- an ownership and data-classification guardrail;
- golden dashboards and a documented escape hatch;
- 99.9 percent control-plane availability over the pilot.

The system passes its conformance tests. Leadership calls the launch technically complete and proposes requiring all new services to use it next quarter.

Important constraints complicate that decision:

- Launchpad supports stateless HTTP services only.
- Twelve teams use a sidecar required by a regulated data path; Launchpad rejects it.
- Seven teams need asynchronous workers in the same repository and deployment unit.
- Security needs authoritative owner and classification metadata for every production service.
- The platform support rotation can absorb about 25 tickets a week without displacing roadmap work.
- Existing teams may keep their current delivery path for rollback during migration.
- The executive sponsor wants a credible risk and value decision, not a prettier registration count.

This case draws from [Adoption, governance, and measurement](../21-platform-engineering/03-adoption-and-governance.md), [Policy, exceptions, and deprecation](../21-platform-engineering/06-policy-exceptions-and-deprecation.md), [Adoption and organizational change](../21-platform-engineering/07-adoption-and-change.md), [Metrics and platform economics](../21-platform-engineering/08-metrics-and-economics.md), [Golden paths and developer experience](../22-developer-platforms/03-golden-paths-and-experience.md), and [Scorecards and engineering governance](../22-developer-platforms/06-scorecards-and-governance.md). The [control-plane lab](../labs/14-platform-control-plane/README.md) covers the mechanism; the [developer platform project](../projects/09-developer-platform-control-plane/README.md) requires both mechanism and product evidence.

## Stage 1: delivery looks like success

Launchpad pilots with eight volunteer teams. The platform dashboard after six weeks reads:

| Measure | Result |
|---|---:|
| Eligible pilot teams invited | 8 |
| Teams registered | 8 |
| Repositories created | 11 |
| Successful environment reconciliations | 94% |
| Median environment creation | 22 minutes |
| Policy-compliant resources | 100% |
| Portal satisfaction | 4.5/5 |

The old ticket path took a median of four business days to provision an environment. The sponsor writes, "Launchpad adoption is 100 percent and provisioning is now 99 percent faster."

Both claims outrun the evidence. Registration is not retained use. The comparison covers environment provisioning, not the full service journey. Volunteer teams may not represent regulated or mixed-workload teams. Successful reconciliation says desired resources converged; it does not say a team shipped, operated, upgraded, or retired a service.

### Timeline

| Week | Event |
|---|---|
| 0 | Eight design partners recruited from teams already asking for self-service |
| 2 | First repository and environment created |
| 3 | Ownership policy changes from report-only to blocking |
| 4 | Portal dashboard announces eight registered teams |
| 5 | Support demand reaches 38 tickets |
| 6 | Leadership proposes an organization-wide mandate |

## Competing explanations

1. Launchpad solves the target journey and needs only communication to spread.
2. The selected design partners are unusually platform-fluent, inflating apparent success.
3. Fast infrastructure creation shifts work into debugging, migration, and support rather than reducing total effort.
4. Unsupported sidecars and mixed service-worker repositories exclude important segments.
5. The ownership guardrail is correct but its source of truth and remediation path are poor.
6. Teams do not trust rollback or support enough to retire the old path.
7. The portal is pleasant while adapters and documentation fail at the moments that matter.

Before continuing, define the adoption funnel you would need. Specify "eligible," "activated," and "retained" for this exact journey.

## Stage 2: journey evidence

The product manager reconstructs events from request IDs, CI, deployment records, support tickets, and interviews. Unknown states remain unknown rather than being counted as success.

| Pilot outcome after 30 days | Teams | Services |
|---|---:|---:|
| Registered | 8 | 11 |
| First production deployment through Launchpad | 6 | 8 |
| Second production deployment through Launchpad | 3 | 4 |
| Still using old path for production changes | 5 | 7 |
| Old path retired | 1 | 1 |

Segmented evidence is more revealing:

| Segment | Activated / eligible | Median hands-on time | Tickets per service | Main blocker |
|---|---:|---:|---:|---|
| Standard stateless HTTP | 5/5 | 2.8 h | 1.2 | Status language |
| HTTP plus worker | 1/2 | 7.4 h | 4.0 | Unsupported composition |
| Regulated sidecar | 0/1 | 6.1 h before abandonment | 6.0 | Policy/runtime conflict |

Interview excerpts:

```text
"The environment appeared in 22 minutes. Then we spent half a day finding which
adapter owned a red Unknown condition."

"We kept the old pipeline because the new rollback stopped at the environment
boundary. We did not know who owned data repair."

"The owner check is reasonable. It rejected the group from the catalog even
though that group is authoritative in the identity directory."

"The portal is clean. That is not the same as supporting our service."
```

Ticket demand averages 31 per week, above sustainable support capacity. Forty-two percent concern ambiguous status or ownership denial, 29 percent concern unsupported workload shape, and 18 percent concern migration and rollback. Only 11 percent are basic how-to questions.

The evidence supports a valuable path for standard stateless HTTP services. It does not support broad applicability or an organization-wide product success claim.

## Decision boundary 1: mandate, expand, or narrow

### Options

| Option | Benefit | Risk and cost |
|---|---|---|
| Mandate Launchpad for every new service | Rapid compliance on measured interfaces | Forces unsupported work into exceptions or shadow paths; support queue grows |
| Add every requested workload option | Broad apparent coverage | Turns one coherent path into a configuration surface; delays improvements for proven users |
| Narrow the supported segment and deepen the journey | Makes product promise honest and testable | Adoption count grows more slowly; leadership must accept explicit non-goals |
| Stop Launchpad and return to tickets | Avoids further build cost | Gives up demonstrated value for the standard segment and preserves known toil |
| Mandate only authoritative metadata | Addresses a cross-cutting risk objective | Needs a usable source-of-truth and exception route independent of Launchpad adoption |

## Decision

The steering group separates three decisions that had been incorrectly bundled:

1. **Product scope:** Launchpad remains a voluntary, supported golden path for standard stateless HTTP services. HTTP-plus-worker is a discovery candidate, not another checkbox. The regulated sidecar remains explicitly unsupported until security and platform owners design a compatible contract.
2. **Governance:** authoritative ownership and data classification become requirements for all production services, regardless of deployment path. Enforcement begins in report-only mode while identity-directory reconciliation and remediation are fixed. Blocking follows only after false-positive and support thresholds are met.
3. **Migration:** design partners may keep a time-bounded old path as a rollback control. Each duplicate path has an owner, expiry, exit evidence, and reviewed extension. Nobody is required to destroy a working rollback before Launchpad proves the complete lifecycle.

This decision declines the broad mandate without weakening the underlying risk objective. It also prevents Launchpad usage from becoming a proxy for compliance.

## Stage 3: product and governance changes

For the next cohort, the team changes work rather than marketing:

- Status conditions name the failing adapter, observed generation, owner, retry state, and remediation.
- The portal, CLI, and API return the same policy decision and status vocabulary.
- Ownership can be imported from the authoritative identity directory; denials include evaluated facts and an exception route.
- A migration check inventories unsupported sidecars and mixed workload shapes before a team starts.
- The service guide covers first deployment, routine change, rollback, incident evidence, ownership transfer, and deletion.
- Platform and application owners rehearse rollback, including what Launchpad does not repair.
- Two weekly office-hour blocks and a published severity model replace private champion escalation.
- Product review combines funnel, cohort retention, hands-on time, failures, support load, exceptions, reliability, and full cost.

The team recruits ten new design partners: six standard HTTP teams, two less experienced teams, one team migrating a busy service, and one team expected to fail because of a known unsupported shape. A design partner's failure remains evidence; it is not silently removed from the denominator.

### Governance release criteria

The ownership rule may become blocking when:

- authoritative-source reconciliation covers at least 98 percent of applicable services;
- false denials stay below 1 percent for four weeks;
- the median remediation time is below 15 minutes;
- exceptions have a named risk owner, compensating control, expiry, and review;
- denial-related support remains inside the team's service objective;
- rollback of the policy version has been rehearsed with audit evidence preserved.

No aggregate score can hide a critical failed control behind trivial passing checks. `Unknown`, `Failed`, `Exempt`, and `Passed` remain distinct.

## Consequence and review

After another eight weeks:

| Outcome | First cohort | Second cohort |
|---|---:|---:|
| Eligible standard-path services | 9 | 13 |
| Activated | 8 | 12 |
| Retained at 30 days | 4 | 10 |
| Median hands-on time | 4.1 h | 2.3 h |
| p90 hands-on time | 10.8 h | 4.9 h |
| Tickets per activated service | 3.9 | 1.4 |
| Duplicate path retired by agreed date | 1/7 | 7/9 |
| Successful rollback drill | 3/8 | 11/12 |

Organization-wide portal registrations rise only from 8 to 17, less than the original mandate forecast. That is not a failure. For the supported segment, retained use and lifecycle evidence improve while support demand becomes sustainable.

The ownership rule enters blocking mode after report-only data exposes two directory synchronization defects. One regulated team receives a 60-day exception with an accountable risk owner and a compensating on-call record while directory migration completes. Exception clustering around the sidecar segment becomes product discovery input, not evidence that all ownership checks should be relaxed.

The full-cost review also changes the investment story:

- Platform infrastructure costs more than the ticket system it replaces.
- Fulfillment labor and repeated application-team setup effort fall for the supported segment.
- Support labor was initially omitted and erased the apparent saving in cohort one.
- In cohort two, lower support and migration effort produce a defensible reduction in cost per successful, retained service journey.
- There is still no evidence that Launchpad should serve data pipelines or stateful systems.

Leadership funds another increment focused on lifecycle reliability and the HTTP-plus-worker contract. It does not fund a universal portal expansion.

## Review: why technical delivery was insufficient

Launchpad's reconciler worked. Its interfaces were secure, its resources converged, and its template was maintained. The first adoption result still failed because the delivered unit was narrower than the user's job.

The corrective decisions were not primarily coding decisions:

- choose a segment and publish non-goals;
- define activation and retention rather than count registrations;
- separate a universal risk requirement from use of one platform product;
- govern exceptions and duplicate paths with owners and expiry;
- fund support and migration as part of product cost;
- preserve an escape hatch while making transferred responsibilities explicit;
- decide which unsupported demand deserves a separate path.

Technical changes mattered because they served those decisions: coherent statuses reduced recovery effort, authoritative import made governance usable, and lifecycle drills created trust. Delivery and product practice reinforced each other.

## Reusable engineering lessons

1. A platform capability is successful when a defined user segment completes and repeats a valuable journey with acceptable outcomes, not when resources exist.
2. Registration, compliance, activation, retention, and improved outcomes are different measures.
3. Segment before averaging. An excellent standard HTTP path can coexist with a failed regulated path.
4. Governance should follow a named risk objective. Requiring Launchpad use is not the same as requiring ownership evidence.
5. Report-only policy, actionable denial, governed exception, and policy rollback are parts of a control's product surface.
6. A golden path spans operation, rollback, migration, and retirement. Fast creation can shift toil downstream.
7. Duplicate paths can be a temporary safety mechanism, but unmanaged duplication creates cost and incident ambiguity.
8. Support load, migration effort, and opportunity cost belong in platform unit economics.
9. Design partners should represent hard segments, and their failures should remain in the evidence.
10. An explicit non-goal preserves coherence. Not every request should become another template switch.

## Evidence exercise

Prepare a decision packet containing:

1. An adoption funnel with exact eligibility, awareness, activation, 30-day retention, and old-path retirement definitions. Name each event source and unknown-state treatment.
2. A cohort table segmented by workload shape and team experience. Explain what causal claim the data cannot support.
3. A journey map from service intent through retirement, including waits, handoffs, failure evidence, support, rollback, and escape-hatch responsibility.
4. A governance record for the ownership rule: risk statement, applicability, evidence authority, policy version, positive and negative tests, denial, remediation, exception, audit, and rollback criteria.
5. A total-cost model per successful retained service journey. Include platform labor, cloud, support, migration, training, application-team effort, and duplicate-path cost.
6. A one-page decision among expanding to workers, improving the existing path, or stopping investment. Include evidence, dissent, owner, stop criteria, and the next reversible experiment.
7. A mapping from the case's product requirements to mechanisms you could test in the [reconciliation control-plane lab](../labs/14-platform-control-plane/README.md). Mark which adoption claims no simulator can prove.

## Teach-back prompts

1. Why was declining the broad mandate compatible with stronger governance?
2. Which first-cohort metric was valid but misleading, and why?
3. When is an escape hatch healthy product design, and when does it become permanent shadow infrastructure?
4. Should the HTTP-plus-worker need become a new golden path, an extension, or a non-goal? What evidence decides?
5. What must be true before a scorecard check blocks delivery?
6. How would you explain to leadership that slower registration growth can represent a better platform outcome?
7. Which technical improvement most directly earned trust, and which product decision made that improvement useful?
