# Cost, reliability, and platform operations

An AI platform is operated as a product and a service: it needs unit economics, SLOs, support, incident ownership, migrations, and capacity feedback.

## Why it matters

Feature adoption can rise while reliability, spend, and user toil deteriorate. Shared infrastructure also creates costs and failures no single tenant can see.

## How it works

Platform SLOs cover user journeys such as run admission, artifact publication, and deployment readiness. Internal indicators measure reconciliation, queueing, policy availability, and metadata integrity. Metering follows trusted tenant and workload identity across accelerator time, tokens, storage, network, and reserved capacity.

Showback creates feedback; quota bounds consumption; budgets trigger decisions; chargeback allocates spend. None replaces physical capacity planning. Product evidence combines journey completion, lead time, voluntary retention, support burden, reliability, and unit cost. Deprecation includes inventory, migration tooling, deadlines, and old-path deletion.

## See it yourself

Deployment lead time falls from 60 to 30 minutes, but rollback rate doubles from 2% to 8%. Speed alone is not improvement. Expected rework and user impact must enter the scorecard.

## Where it shows up

On-call runbooks begin with ownership and blast radius, preserve control-plane audit events, and identify safe admission stops. Quarterly reviews connect repeated incidents and support cases to roadmap choices.

## When it breaks

Shared credentials erase cost attribution, mandated usage inflates adoption, platform and tenant teams dispute incident ownership, and migrations leave permanent dual paths. Reconcile usage to trusted identity and publish responsibility before incidents.

## Practice

**Observe:** instrument one end-to-end journey. **Build:** define SLO, error budget, unit metric, and responsibility matrix. **Break:** degrade policy service and misattribute shared cost. Completion requires graceful behavior, an auditable bill, and a roadmap decision grounded in evidence.

## Check yourself

1. How do quota and budget differ?
2. Why segment voluntary from mandated adoption?
3. What proves a deprecation completed?

## Sources

### REQUIRED

- [Google SRE Workbook: SLOs](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [FinOps Framework](https://www.finops.org/framework/)

### DEEP DIVE

- [CNCF platform engineering whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

Continue to [Practical lab: design an AI platform control plane](09-practical-ai-platform-lab.md).
