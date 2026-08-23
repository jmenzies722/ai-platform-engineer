# Platform operating model and support

A platform operating model assigns product, engineering, reliability, security, and support decisions so the platform remains useful after launch. Team structure and service boundaries are part of the technical design.

## Why it matters

Shared capabilities become dependencies. If roadmap ownership, on-call response, migrations, and consumer responsibilities are implicit, every incident becomes a negotiation and platform engineers become an unbounded ticket queue.

## How it works

Define decision rights for product direction, architecture, capability ownership, risk acceptance, incident command, and funding. A platform product manager may prioritize outcomes, but capability owners remain accountable for contracts and reliability. Security and finance should supply constraints and expertise without becoming invisible queues.

Publish a service model with support channels, severity definitions, response objectives, escalation, maintenance, and excluded work. Separate product feedback, usage help, defects, incidents, and exceptions because they need different workflows and data. Office hours can teach and discover problems; they must not become undocumented fulfillment.

Organize around durable capabilities rather than frontend components. Each capability needs code ownership, operational telemetry, runbooks, dependency maps, and a lifecycle plan. Federated contributors can extend the platform when interface standards, review authority, release ownership, and long-term maintenance are explicit.

Plan capacity across roadmap, reliability, security, migration, and support load. Track interruption and toil rather than assuming feature capacity is constant. If a platform operates continuously, fund on-call staffing and dependency management as product costs.

## Vocabulary

- **operating model:** assignment of responsibilities, decisions, funding, and interaction modes
- **service model:** published support and reliability obligations
- **toil:** repetitive operational work that is manual, automatable, tactical, and without enduring value
- **federation:** contribution or operation distributed across teams under shared contracts

## See it yourself

Take 20 support requests and classify them as incident, defect, question, product gap, exception, or consumer-owned failure. Predict whether one generic backlog can represent urgency and learning. Compare age, recurrence, and owner by class. Classification supports routing and product evidence; it does not excuse handoffs without resolution.

## Where it shows up

A central platform team owns runtime contracts and release engineering; domain teams own approved capability plugins. A production incident has one platform incident commander, while affected service teams retain application mitigation authority. Post-incident actions feed both reliability work and product discovery.

## When it breaks

The platform team owns every application failure because boundaries are vague. Security approval has no response objective. Community plugins have no maintainer after their author moves. Feature delivery crowds out upgrades until unsupported dependencies become emergencies.

Evidence includes ticket reassignments, pages outside ownership, interruption rate, unresolved escalation age, abandoned components, and roadmap work repeatedly displaced by operations.

## Practice

**Observe:** sample one month of support and on-call work. Classify demand, time, recurrence, and final owner. Completion means the totals reconcile with available capacity and expose unknown work.

**Design:** write an operating model for a ten-person platform team serving 100 developers. Include decision rights, capability ownership, support tiers, on-call, contribution rules, and capacity allocation.

**Break:** remove one capability owner and double support demand. Identify which promises fail first, what work stops, and which structural change reduces recurrence.

**Say it out loud:** explain why support demand is product evidence and an economic cost.

## Check yourself

1. Which decisions cannot be delegated to a generic governance committee?
2. How does a service model protect both users and platform engineers?
3. When does federation reduce bottlenecks, and when does it create orphaned code?
4. Which evidence shows that support work is masking a product defect?

## Sources

### REQUIRED

- [Team Topologies: key concepts](https://teamtopologies.com/key-concepts)

### RECOMMENDED

- [Google SRE: Eliminating toil](https://sre.google/sre-book/eliminating-toil/)

### DEEP DIVE

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

Continue to [Policy, exceptions, and deprecation](06-policy-exceptions-and-deprecation.md).
