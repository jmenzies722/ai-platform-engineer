# Curriculum Tracks

Tracks are role-shaped compositions of the existing curriculum. They do not replace the numbered modules, their lesson order, or the evidence standards in the [roadmap](../ROADMAP.md). A track answers a narrower question: which capabilities should I prove, and in what order, for the work I want to do?

## Available tracks

| Track | Outcome |
|---|---|
| [Software Engineer](software-engineer.md) | Build, test, reason about, and operate production software across runtime and service boundaries |
| [Backend Engineer](backend-engineer.md) | Own durable APIs, data, asynchronous work, and service reliability |
| [Cloud and DevOps Engineer](cloud-devops-engineer.md) | Build secure, reproducible cloud delivery and infrastructure |
| [Site Reliability Engineer](sre.md) | Set reliability policy and diagnose, mitigate, and prevent production failure |
| [Platform Engineer](platform-engineer.md) | Productize shared delivery capabilities through safe self-service |
| [AI Platform Engineer](ai-platform-engineer.md) | Operate governed, multi-tenant training, serving, and agent capabilities |
| [Staff AI Platform Engineer](staff-ai-platform-engineer.md) | Lead cross-team AI platform strategy, architecture, economics, and governance |

The [roadmap](../ROADMAP.md) remains the broad capability map. The track documents select and sequence parts of it; links point back to the canonical modules, labs, incidents, and project briefs.

## Evidence-based placement

Do not place yourself by title, years of experience, courses completed, or tools used. Start at the first gate for which you cannot produce current evidence. For each prerequisite capability:

1. Explain the mechanism without relying on product slogans.
2. Demonstrate it in a bounded environment.
3. Introduce a controlled failure and diagnose it from evidence.
4. State the limits of the evidence and the unsafe conditions under which you would stop.
5. Have another engineer review or reproduce the result.

Use the gate records for [foundations](../assessments/gates/foundations.md), [systems, Linux, and networking](../assessments/gates/systems-linux-networking.md), [cloud delivery](../assessments/gates/cloud-delivery.md), [Kubernetes reliability](../assessments/gates/kubernetes-reliability.md), [platform engineering](../assessments/gates/platform.md), [AI platform engineering](../assessments/gates/ai-platform.md), and [Staff engineering](../assessments/gates/staff.md). A missing or incomplete record means the gate has not been claimed.

The [labs](../labs/README.md) produce focused mechanism evidence, [incident drills](../incidents/README.md) test diagnosis under uncertainty, and [projects](../projects/README.md) integrate capabilities into portfolio-scale proof. Reading is preparation. The gate is passed by defensible work.

## Switching tracks

Tracks share foundations intentionally. When switching:

1. Compare the destination prerequisites and gates with evidence you already possess.
2. Reuse evidence only when it demonstrates the same mechanism, independence, and operational depth.
3. Enter at the earliest unmet gate, not at module 00 by default and not at the destination's final module.
4. Add only the destination-specific modules, labs, incidents, and project proof.
5. Re-run stale operational evidence when environments, responsibilities, or expected failure modes have materially changed.

For example, a backend engineer with strong systems, database, and service evidence can enter the cloud track at delivery and infrastructure. A cloud engineer moving to SRE can retain Kubernetes operations evidence but must still demonstrate SLI design, error-budget decisions, incident command, and overload reasoning. A platform engineer moving into AI platform work must add quantitative AI foundations, model lifecycle, GPU, and serving evidence; portal or Kubernetes experience alone does not establish those capabilities.

Switching is not a demotion. It is a change in the evidence required for the next outcome.

## How to use a track

- Follow modules in the listed order unless the track explicitly permits parallel study.
- Complete each module's own practice as well as the track's required shared labs.
- Treat incident solutions as facilitator material; write hypotheses and select a reversible mitigation before reading them.
- Build selected projects in separate repositories as required by the [project briefs](../projects/README.md).
- Record gate evidence with versions, assumptions, commands, observations, failure injections, recovery proof, and reviewer feedback.
- Revisit the weakest relevant competency rather than accumulating unrelated completions.

## Certification overlays

Certification is an optional overlay, not a curriculum gate. The [AWS Certified DevOps Engineer - Professional (DOP-C02) overlay](../certs/aws-dop-c02.md) indexes the repository's underlying cloud material, including the [AWS module](../12-aws/README.md). It can help organize review of AWS delivery, operations, security, and resilience, but an exam result does not replace plans, deployments, incident evidence, or project work.
