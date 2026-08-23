# Organizational interfaces

Organizational interfaces are contracts for responsibility, information, support, and change between teams.

## Why it matters

Many “architecture problems” persist because no team owns the decision at a seam, consumers cannot predict change, or operational burden crosses boundaries without resources.

## How it works

Map capabilities and value flow before redrawing teams. For each interface, name provider, consumers, service or artifact, support model, decision rights, compatibility, SLOs, escalation, funding, and deprecation. Match team ownership to a coherent cognitive load and give responsibility the access and authority it requires.

Use collaboration for uncertain high-coupling work, a service relationship for stable repeatable needs, facilitation to build capability, and enabling work with an explicit exit. A platform is a product only when it has users, discovery, reliability, support, adoption economics, and a feedback loop.

Review interfaces after incidents and reorganizations. Informal glue can be valuable discovery, but convert recurring coordination into an explicit mechanism or funded role. Do not make one staff engineer the human API between teams.

## See it yourself

Application teams blame platform latency; platform owners cannot reproduce payloads and do not control client retries. An interface contract adds workload envelope, client budget, telemetry identity, support path, and joint load test. The fix is socio-technical, not merely a faster endpoint.

## Where it shows up

Interfaces shape platform and product teams, security review, data ownership, model governance, SRE engagement, procurement, and vendor operations.

## When it breaks

Failures include responsibility without authority, platforms mandated without migration funding, shared ownership, ticket queues replacing collaboration, and permanent enabling teams. Trace one user outcome across teams and identify every uncertain handoff.

## Practice

**Build:** map organizational interfaces for an AI platform and three application teams. Specify decision rights, support, SLOs, compatibility, adoption, and escalation. **Break:** move identity ownership to another organization. **Explain back:** revise interfaces without making a person the integration layer.

## Check yourself

1. Which interaction mode fits uncertain high-coupling work?
2. Why is a mandated internal service not automatically a platform product?
3. How do you detect a human API?

## Sources

### REQUIRED

- [Team Topologies: Key concepts](https://teamtopologies.com/key-concepts)

### RECOMMENDED

- [Google SRE Book: The evolving SRE engagement model](https://sre.google/sre-book/evolving-sre-engagement-model/)

### DEEP DIVE

- [Conway’s law paper record](https://www.melconway.com/Home/Committees_Paper.html)

## Next

Continue to [Incident leadership](11-incident-leadership.md).
