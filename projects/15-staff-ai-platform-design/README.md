# 15 — Staff AI Platform Strategy and Design Package

Produce an implementation-ready design package in its own repository. This capstone is evaluated on decision quality, cross-team execution, and durable ownership; a prototype may validate risks, but software volume is not the goal.

## Problem and stakeholders

A growing organization has duplicated model pipelines, unpredictable GPU spend, inconsistent serving, unclear AI risk ownership, and slow onboarding. Product/model teams, infrastructure, security/privacy, finance, support, and executives value different outcomes. Frame the problem from interview evidence and decide whether a shared platform, narrower services, or no new platform is justified.

## Constraints and decision boundaries

- Use explicit workload forecasts, current-state evidence, regulatory/data classes, team capabilities, and budget.
- Cover a three-year evolution through sequenced, reversible decisions without pretending forecasts are facts.
- Identify organizational ownership, migration, deprecation, and funding alongside technical architecture.
- Do not prescribe products before requirements, claim consensus without dissent, or bury uncertainty in polished diagrams.

## Architecture expectations

Compare at least three credible options. The recommended design must cover developer interfaces, data/model lineage, training and GPU capacity, evaluation/governance, model serving, agent workloads, identity/tenancy, control planes, telemetry, reliability, disaster recovery, and cost allocation. Define invariants, failure domains, build-versus-buy criteria, dependency contracts, and where centralized standards stop.

## Milestone plan

1. Interview stakeholders; document current journeys, system inventory, pain, constraints, and baseline metrics.
2. Forecast workloads and economics; establish quality attributes, risks, options, and decision criteria.
3. Review architecture, operating model, security/privacy, reliability, migration, and investment proposal.
4. Run tabletop incidents and pre-mortem; revise decisions, define pilots/stage gates, and transfer ownership.

## Required artifacts

- One-page strategy, six-page narrative or equivalent, requirements, stakeholder map, and current-state assessment.
- Context/container/deployment/data/trust diagrams; interface specs; ADR set; option scorecard; risk register.
- Capacity and unit-economics model with sensitivity ranges; SLO/error-budget and disaster-recovery strategy.
- Threat/privacy model, governance and exception process, migration/deprecation plan, team topology/RACI, roadmap with evidence gates.
- Review log recording dissent and resolution; executive briefing, engineering deep dive, FAQ, and handoff package.

## Tests, simulations, and failure drills

Validate forecasts against historical traces and compare model outputs with hand calculations. Prototype only the riskiest assumptions, such as queue fairness, control-plane convergence, tenant isolation, or serving economics. Facilitate tabletop exercises for region loss during training, compromised model artifact, runaway inference demand, GPU supply shortfall, lineage recall, policy outage, and agent-caused side effect. Record decision changes caused by evidence.

## Observability, security, and cost

Define a platform scorecard spanning developer lead time, adoption, reliability, model quality/safety, accelerator goodput, serving latency, policy coverage, incidents, toil, and unit cost. Specify identity, tenant/data isolation, provenance, retention/deletion, approvals, audit, incident authority, and residual risk owners. Present demand scenarios, reservations versus on-demand tradeoffs, headroom, vendor concentration, staffing/operations cost, showback/chargeback, and stop-investing triggers.

## Explicit success rubric

| Staff-level outcome | Passing evidence |
|---|---|
| Framing | Stakeholder evidence, non-goals, and measurable outcomes bound the problem before architecture. |
| Judgment | Options and rejected alternatives are compared with uncertainty, reversibility, economics, and risk. |
| Technical depth | Interfaces, invariants, capacity, failure, security, operations, and migrations withstand specialist review. |
| Influence | Dissent is surfaced; decisions, owners, funding, and cross-team dependencies are explicit. |
| Durable impact | Pilots have evidence gates, ownership survives the author, and deprecation/exit paths prevent permanent scaffolding. |

## Stretch work

Run an external architecture review, negotiate a mock vendor contract against portability requirements, or revisit the recommendation after a materially changed workload forecast.

## Authoritative sources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [Google SRE books](https://sre.google/books/)
- [Architecture Decision Records](https://adr.github.io/)

## Mapped modules

[21 Platform Engineering](../../21-platform-engineering/README.md), [30 AI Infrastructure](../../30-ai-infrastructure/README.md), [31 Model Serving](../../31-model-serving/README.md), [32 AI Platform Engineering](../../32-ai-platform-engineering/README.md), [33 Agentic Infrastructure](../../33-agentic-infrastructure/README.md), [34 System Design](../../34-system-design/README.md), and [35 Senior and Staff Engineering](../../35-senior-staff-engineering/README.md).
