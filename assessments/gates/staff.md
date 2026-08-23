# Staff Gate

This gate tests whether the learner can convert ambiguous, cross-team AI platform pressure into a decision and operating system that survives dissent, incidents, changed evidence, and the author's absence. It covers [system design](../../34-system-design/README.md) and [senior and staff engineering](../../35-senior-staff-engineering/README.md), while sampling all earlier gates.

## Prerequisites

- Pass the [AI Platform Gate](ai-platform.md) and retain evidence from every earlier gate.
- Complete the [design packet lab](../../34-system-design/90-design-packet-lab.md), [adversarial design review](../../34-system-design/91-adversarial-design-review-lab.md), [staff operating packet](../../35-senior-staff-engineering/90-staff-operating-packet-lab.md), and [organizational pressure simulation](../../35-senior-staff-engineering/91-organizational-pressure-simulation-lab.md).
- Bring an implementation-ready baseline modeled on [Staff AI Platform Strategy and Design Package](../../projects/15-staff-ai-platform-design/README.md).
- Use approved, anonymized stakeholder evidence or evaluator-provided synthetic evidence. Never invent interviews, consensus, budgets, incidents, legal requirements, or production measurements.

## Challenge

An organization has duplicated model pipelines, unpredictable accelerator and serving spend, inconsistent evaluation and release controls, unclear AI risk ownership, and slow onboarding. The candidate must determine whether a shared platform, narrower services, changed team interfaces, or no new platform is justified.

Produce and defend:

- stakeholder and current-state evidence, critical journeys, measurable outcomes, non-goals, constraints, unresolved questions, and baseline;
- demand and capacity ranges, unit economics, sensitivity analysis, quality attributes, invariants, and failure budgets;
- at least three credible options, including a minimal or no-platform option, with reversibility, risk, organizational fit, cost, and decision criteria;
- recommended interfaces and architecture for data and model lineage, training and accelerator capacity, evaluation and governance, serving, agent workloads, identity and tenancy, control planes, telemetry, reliability, disaster recovery, and cost allocation;
- threat and privacy model, residual-risk owners, governance and exception process, incident authority, and ethical limits;
- operating model, team boundaries, decision rights, funding, support, cross-team dependencies, migration, deprecation, and exit path;
- staged roadmap with pilots, evidence gates, stop-investing triggers, and ownership transfer; and
- review log that records dissent, decision changes, and unresolved risks.

The evaluator runs two pressure rounds after the initial recommendation:

1. a material assumption changes, such as demand halving, accelerator supply failing, a regulatory data class being introduced, a vendor price increasing, or platform adoption remaining low;
2. a tabletop incident from earlier assets occurs, such as compromised artifact, lineage recall, runaway inference demand, [queue overload](../../incidents/12-queue-overload/README.md), [GPU OOM](../../incidents/11-gpu-oom/README.md), policy outage, region loss during training, or agent-caused side effect.

The candidate must lead the review and incident decisions, surface dissent, revise or preserve the recommendation based on evidence, assign accountable owners, and leave a handoff that another leader can execute.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- source-tagged stakeholder evidence, current-state map, baseline metrics, problem frame, non-goals, uncertainty, and decision deadline;
- requirements and invariants, load and capacity math with units and ranges, quality scenarios, SLO and recovery objectives, threat and privacy model, and unit-economics model;
- option scorecard, rejected alternatives, ADR set, architecture and trust diagrams, interface and ownership contracts, dependency map, and build-versus-buy criteria;
- risk register with probability or confidence, impact, leading indicator, mitigation, contingency, residual owner, and escalation trigger;
- migration and deprecation plan, compatibility stages, pilot design, roadmap evidence gates, funding and staffing assumptions, and stop-investing criteria;
- review agendas, decision log, dissent and response record, commitments with owners, executive summary, engineering deep dive, FAQ, and handoff test;
- tabletop timeline, roles, communications, mitigation and rollback decisions, recovery criteria, and prevention changes; and
- before/after recommendation showing exactly which evidence changed which decision.

## Dimension requirements

- **Explain:** Give both an executive account and a mechanism-level technical account without changing the underlying claims. Make uncertainty, ownership, limits, and practical consequence explicit.
- **Build:** Produce inspectable decision machinery: models, option comparisons, contracts, risk and decision records, pilot gates, and handoff artifacts that another team can execute and update.
- **Debug:** During the tabletop, separate impact, trigger, contributing conditions, and control gaps; test competing hypotheses; recognize organizational as well as technical failure mechanisms.
- **Operate:** Establish incident and decision authority, communicate uncertainty, choose reversible containment, protect safety and trust, verify recovery, and maintain accountable follow-through across teams.
- **Design:** Integrate requirements, capacity, data, consistency, security, reliability, observability, cost, migration, organizational boundaries, ethics, and evolution; revise coherently under changed assumptions.

## Evaluator instructions

Use a panel with at least two perspectives when possible, such as platform/operator and product/security/finance. Give each reviewer a distinct legitimate concern. Do not manufacture consensus. Record which claims survive specialist challenge and which remain unresolved.

Supply a consistent synthetic organization packet if real evidence cannot be used. Reveal pressure-round changes only after the candidate commits to an initial recommendation and revisit triggers. Ask another reviewer to use the handoff without the candidate's help.

Critical requirements:

- the problem is bounded by stakeholder and system evidence before products or architecture are chosen;
- at least three credible options are compared, and the recommendation may be no new platform;
- capacity and economics are reproducible from inputs and include sensitivity ranges;
- dissent, residual risk, funding, decision authority, dependencies, and accountable owners are explicit;
- incident actions and strategic stages have rollback, exit, or stop conditions; and
- the plan remains operable when the candidate is absent.

## Review prompts

1. Which organizational outcome justifies this scope, and what evidence says the problem is important now?
2. Which assumption has the highest decision sensitivity, and how will it be measured?
3. Why is the recommended option better than the minimal and no-platform options?
4. Where do centralized standards stop, and which team owns each remaining risk and interface?
5. What dissent changed the design, and what dissent remains unresolved?
6. During the tabletop, what is impact, what is hypothesis, and who has authority to contain the effect?
7. Which pilot result would stop, narrow, accelerate, or reverse the investment?
8. How do migration, deprecation, funding, support, and handoff avoid permanent scaffolding or dependence on one person?
9. What ethical or power concern cannot be reduced to a technical control?
10. Which production evidence would cause the strategy to be revisited?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and a Design score of 3. Explain must work at both executive and specialist depth. Operate must include a fresh tabletop pressure round. A polished narrative without dissent, executable ownership, or changed-evidence response does not pass.

A synthetic-organization pass demonstrates staff-level decision, design, review, and handoff performance in simulation. It does not prove real organizational influence, adoption, or durable outcomes. Claiming the Staff AI Platform Engineer track additionally requires independently reviewed evidence of consequential cross-team outcomes that persisted beyond the candidate's direct intervention.

Rework is scoped to the failed mechanism but must preserve coupled decisions. Weak framing requires new stakeholder or baseline evidence before architecture revision. Weak economics requires corrected inputs and sensitivity analysis. Weak influence requires a new adversarial review with recorded dissent. Weak incident leadership requires a different tabletop. Weak durability requires an independent handoff test.

Fabricated stakeholder evidence, hidden conflicts, unsafe authority use, or knowingly misleading certainty is a Stop.

## Remediation

Return to [requirements and boundaries](../../34-system-design/01-requirements-load-and-boundaries.md), [estimation and capacity](../../34-system-design/02-estimation-and-capacity.md), [evolution and review](../../34-system-design/13-evolution-and-design-review.md), [engineering strategy](../../35-senior-staff-engineering/03-engineering-strategy.md), [RFCs, decisions, and dissent](../../35-senior-staff-engineering/05-rfcs-decisions-and-dissent.md), [risk and escalation](../../35-senior-staff-engineering/08-risk-and-responsible-escalation.md), or [incident leadership](../../35-senior-staff-engineering/11-incident-leadership.md). Rework the affected packet section, then test it in a fresh pressure round with a reviewer who did not guide the revision.
