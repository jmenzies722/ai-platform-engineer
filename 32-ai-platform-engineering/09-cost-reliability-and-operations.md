# Cost, reliability, and platform operations

An AI platform is operated as a product and a service: it needs unit economics, SLOs, capacity feedback, incident ownership, migrations, and recovery.

## Why it matters

Feature adoption can rise while reliability, spend, and user toil deteriorate. Shared accelerators, control planes, registries, policy services, and indexes also create costs and failures no tenant can see alone. Operations must connect user impact to platform mechanics and trusted attribution, or teams will optimize local metrics while the whole service becomes less predictable.

## How it works

Define service-level indicators at user-visible boundaries: valid training runs admitted within a threshold, declared artifacts published intact, approved deployments ready, authorized retrieval meeting freshness, and rollback completed. State eligibility and exclusions so an SLO cannot be improved by silently rejecting difficult valid work. Internal indicators such as queue age, reconcile delay, policy latency, metadata integrity, checkpoint throughput, index lag, and capacity saturation explain causes but do not substitute for user outcomes.

Set objectives from user need and achievable design, then use error-budget consumption to govern release and reliability work. Fast burn detects acute incidents; slow burn exposes chronic degradation. A 99.9 percent API SLO is irrelevant if accepted resources remain unreconciled for hours, so asynchronous workflows need age-based indicators.

Capacity is distributional. Forecast workload class, arrival bursts, service time, accelerator and memory shape, topology, storage, and failure headroom. Queue depth alone is ambiguous; oldest age and ingress minus successful egress reveal recovery. Reservations protect critical work, fair-share prevents domination, and admission rejects beyond a documented envelope.

Metering follows trusted tenant and workload identity through accelerator-seconds, tokens, storage, network, APIs, reservations, and shared cost. Usage writes are idempotent and reconciled against scheduler and provider records. Showback creates feedback, quota bounds consumption, budgets trigger decisions, and chargeback allocates spend. Publish shared-cost allocation. Pair unit cost with quality and reliability so cheap failure is not rewarded.

Operational design declares platform, tenant, dependency, security, and model-quality ownership before an incident. Runbooks begin with impact, authority, safe admission stops, evidence preservation, rollback, and recovery checks. The control plane may fail while serving continues; emergency rollback uses pre-authorized, last-known-good evidence. Deprecation inventories consumers, supplies migration tooling, enforces deadlines, and removes the old path.

## See it yourself

Suppose deployment lead time falls from 60 to 30 minutes while rollback rate rises from 2 to 8 percent. For 100 deployments, expected rollbacks rise from two to eight, so speed alone cannot establish improvement. If each rollback consumes 90 engineer-minutes, expected rework rises from 180 to 720 minutes. This bounded calculation justifies adding rollback and toil to the scorecard; it does not quantify customer impact without incident data.

## Where it shows up

A platform review combines journey completion, error-budget burn, capacity, support burden, retention, unit cost, policy outcomes, and incident themes. Dashboards correlate tenant, workload class, resource generation, artifact digest, controller revision, and dependency status without exposing payloads. Planning turns repeated incidents into reliability work, contract changes, or a decision to stop unsupported growth.

## When it breaks

Shared credentials erase cost attribution, averages hide one tenant's starvation, retries amplify a dependency outage, mandated usage inflates adoption, platform and model teams dispute ownership, and permanent dual paths multiply toil. During an incident, preserve request and generation IDs, policy decisions, controller events, dependency calls, usage records, and rollout versions before mitigation destroys correlation. Reduce blast radius with reversible controls, test recovery against user-visible indicators, and reconcile ambiguous side effects. For billing anomalies, compare the ledger with scheduler allocation and provider invoices before changing prices.

## Practice

**Observe:** instrument one end-to-end journey and calculate its error-budget burn and unit cost. **Build:** define SLOs, age-based queue signals, capacity envelope, usage reconciliation, responsibility matrix, and rollback runbook. **Break:** degrade policy, create retry amplification, starve one tenant, and duplicate a usage event. Completion requires safe degraded behavior, bounded queues, exact idempotent billing, ownership clarity, and recovery proven at the user boundary.

## Check yourself

1. Why do asynchronous workflows need age-based indicators?
2. How do quota, budget, chargeback, and capacity differ?
3. What proves an incident recovered and a deprecation completed?

## Sources

### REQUIRED

- [Google SRE Workbook: implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [FinOps Framework](https://www.finops.org/framework/)
- [Google SRE Workbook: alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

### DEEP DIVE

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [AWS Builders Library: timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

## Next

Continue to [Practical lab: verify an AI platform control plane](10-practical-ai-platform-lab.md).
