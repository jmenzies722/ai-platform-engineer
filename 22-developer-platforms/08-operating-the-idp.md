# Operating an IDP and its golden paths

An IDP is a production service and a portfolio of golden paths. Operating it requires reliability objectives, ownership, release and compatibility discipline, support, adoption evidence, and explicit retirement of capabilities that no longer earn their cost.

## Why it matters

The portal can be healthy while catalog data is stale, workflows are stuck, and generated services depend on vulnerable versions. Without end-to-end objectives and lifecycle ownership, surface availability hides user failure.

## How it works

Define service-level indicators at contract boundaries: catalog freshness and correctness, search success, workflow completion and age, API availability, status propagation, documentation freshness, and golden-path task success. Separate portal availability from capability and provider availability. Publish degraded behavior.

Assign an owner and support tier to every path, plugin, template, workflow, and API. Maintain compatibility matrices and release rings. Test representative journeys against candidate releases, canary changes with real segments, and preserve rollback or forward-fix plans. Back up authoritative state and test restoration.

Use telemetry, support, incidents, security findings, user research, adoption cohorts, and unit cost in portfolio review. Invest where repeated outcomes improve; split paths whose envelopes diverge; deprecate paths with unsafe dependencies or weak value. Migrations need inventory, compatibility checks, ownership, progress evidence, and stop conditions.

Keep an IDP escape route for emergencies. Document which operations continue through API or Git when the portal fails and how users discover status. Disaster exercises should include identity-provider outage, stale catalog ingestion, workflow backlog, plugin failure, and unavailable downstream providers.

## Vocabulary

- **path portfolio:** set of supported journeys managed as lifecycle investments
- **release ring:** staged consumer cohort used to limit change blast radius
- **end-to-end SLI:** measure spanning the user's complete intended task
- **degraded mode:** intentionally reduced behavior during dependency failure

## See it yourself

Build a dependency matrix for catalog, portal, workflow engine, identity provider, and cloud API. Predict which user journeys survive each outage. A green portal probe proves only surface availability. Synthetic create, inspect, update, and delete journeys reveal stale or stuck dependencies, but must use safe disposable resources.

## Where it shows up

During catalog ingestion failure, the portal marks metadata stale, blocks ownership-sensitive destructive actions, and permits read-only access to last-known data. Existing deployments continue because the runtime API does not depend synchronously on portal availability.

## When it breaks

All components share one deployment and fail together, migrations have no consumer inventory, synthetic tests create orphaned resources, and release canaries contain only platform engineers. Backups exist but restoration changes IDs. Measure dependency-specific errors, operation age, stale facts, path version skew, support volume, restore tests, and end-to-end success.

## Practice

**Observe:** build an SLI tree for one golden path from discovery through operation. Completion means each user-visible failure maps to an owner and evidence source.

**Design:** create an operating plan covering SLOs, dependencies, release rings, compatibility, backup and restore, support, security response, and portfolio review.

**Break:** simulate portal outage, stale catalog, and downstream timeout separately. Specify expected degraded behavior, user evidence, alert, mitigation, and recovery proof.

**Design review:** present an IDP architecture with catalog authorities, entity schema, template ownership, resumable workflow, portal and API contracts, plugin boundary, scorecard, threat model, and golden-path lifecycle. Include one rejected design option and the evidence behind the decision.

## Check yourself

1. Why is portal uptime an insufficient IDP SLI?
2. Which IDP state must be restored with stable identity?
3. How should a downstream provider outage appear to users?
4. What evidence supports retiring a golden path?

## Sources

### REQUIRED

- [Google SRE: Service level objectives](https://sre.google/sre-book/service-level-objectives/)

### RECOMMENDED

- [Backstage deployment documentation](https://backstage.io/docs/deployment/)

### DEEP DIVE

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

Continue to [Control Planes](../23-control-planes/README.md).
