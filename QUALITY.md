# Curriculum Quality Standard

This document is the repository-wide definition of done. It applies to [lessons](templates/LESSON.md), [guided labs](labs/README.md), [incident drills](incidents/README.md), [projects](projects/README.md), [assessment gates](assessments/README.md), [role tracks](tracks/README.md), [certification overlays](certs/README.md), and [case studies](case-studies/README.md). A structurally valid file is not done unless its claims, evidence, safety, teaching purpose, and ownership are reviewable.

## Universal definition of done

Every artifact must satisfy all of these conditions:

1. **Purpose:** names the learner, prerequisite state, problem, intended capability, non-goals, and relation to canonical curriculum.
2. **Mechanism:** explains why the subject exists, how state and responsibility move across boundaries, what evidence exposes the behavior, and where the abstraction stops.
3. **Evidence:** separates prediction, observation, interpretation, and decision. Commands, measurements, calculations, examples, and outputs are reproducible or explicitly labeled illustrative.
4. **Failure:** includes realistic failure modes, discriminating evidence, unsafe shortcuts, recovery criteria, and limits on the conclusion.
5. **Practice:** asks the learner to produce inspectable work rather than repeat labels. Completion includes explanation and at least one appropriate build, debug, operate, or design proof.
6. **Sources:** important factual claims are traceable to authoritative sources with scope and version boundaries. Quotations, diagrams, data, and adapted material are attributed.
7. **Safety:** authority, environment, data handling, privileges, blast radius, cost, duration, stop conditions, rollback, and cleanup are explicit where relevant.
8. **Navigation:** repository links are relative, fragments resolve, the parent index links the artifact, and the artifact points to prerequisite and next work without creating a dead end.
9. **Presentation:** one H1 names the artifact; headings are ordered; terms are defined; tables have meaningful headers; code and diagrams are introduced and interpreted.
10. **Ownership:** an author, content owner, required specialist reviewers, and a change trigger or review date are identifiable in the issue or pull request.

Unicode arrow glyphs are prohibited in Markdown. They encourage compressed chain explanations and create inconsistent rendering. Explain causality in sentences, numbered stages, tables, or Mermaid. ASCII operators inside code and Mermaid syntax are allowed when they are part of the language.

## Factual and source quality

Prefer, in order, standards and specifications, official product documentation, maintainer design material and source code, primary research, and direct reproducible measurements. A secondary source may provide context but should not be the sole support for a consequential or disputed technical claim.

Each source-dependent claim must make clear:

- which nearby sentence the source supports;
- the product, protocol, exam, or implementation version in scope;
- whether the source describes a guarantee, current behavior, recommendation, or example;
- the date checked when the upstream material is volatile;
- any disagreement between documentation and measured behavior;
- what remains uncertain or implementation-specific.

Do not use invented URLs, search-result summaries, uncited copied text, private material, leaked exam content, or a generated answer as authority. Do not imply that an external link was checked by CI. Reviewers open consequential links manually and verify the claim against the source. Copyrighted material is summarized and linked, not reproduced beyond justified quotation.

Synthetic output, organizations, interviews, incidents, measurements, and data must be labeled where first used. Synthetic evidence can test reasoning and mechanics; it cannot be presented as user research, production performance, hardware benchmarking, or external validation.

## Evidence and reproducibility

Evidence should let another engineer inspect the claim and repeat the bounded proof. A useful evidence record includes environment and versions, immutable input identity where relevant, setup, exact action, expected and observed result, timestamps or ordering, raw output location, interpretation, contradictory evidence, limitations, and cleanup.

Successful output alone is insufficient. The artifact must explain which claim it supports and at least one plausible claim it does not prove. Measurements include units, workload shape, sample or window, aggregation, denominator, missing-data treatment, and uncertainty. Calculations expose inputs and assumptions. Screenshots may supplement machine-readable evidence but do not replace it.

Assistance, reused work, generated material, prior solution access, and evaluator hints are disclosed. Evidence must not be fabricated, selectively altered, or stripped of relevant failures. Redaction removes sensitive values while preserving safe correlation, version, and timing context.

## Safety, privacy, and cost

Use local disposable environments by default. Shared, production, customer, and personal systems are out of scope unless an artifact explicitly requires an authorized read-only review and names the approval and command boundary. Exercises never require real credentials, customer identifiers, unrestricted agent tools, destructive production behavior, or weakened security controls.

Before mutation, the learner verifies repository, account, principal, region, cluster, namespace, process, database, and resource target as applicable. The artifact bounds load, retries, queues, tokens, storage, runtime, and spend. It defines a stop condition for unexpected identity, scope, output, cost, data, or cleanup state.

Cloud work names a cost ceiling, billing dimensions, teardown command, retained evidence, and verification that billable resources are gone. Destructive work names a disposable fixture, backup or recovery assumption, smallest reversible action, rollback trigger, and residual-effect check. Security work uses synthetic inputs and safe demonstrations; it does not publish weaponized steps unnecessary to the learning objective.

Any unauthorized side effect, secret exposure, fabricated evidence, unsafe bypass, or unbounded spend is a stop condition, not a minor quality deduction.

## Links and diagrams

Repository content uses relative Markdown links. Link text names the destination or learner purpose. Fragments target real headings. Every new artifact is linked from its immediate index, and each new curriculum system is linked from root-level contribution and quality guidance. External links use canonical HTTPS pages when available; tracking parameters and unstable search links are avoided.

Mermaid diagrams must:

- use a closed `mermaid` fence with no text after the language name;
- begin with a supported diagram declaration;
- render in the repository workflow;
- have readable labels, direction, and boundaries;
- agree with the prose and be explained immediately before or after;
- distinguish state owners, trust or failure boundaries, and optional paths when those distinctions matter;
- avoid HTML, smart quotes, tabs, secrets, sensitive identifiers, and decorative complexity.

A diagram cannot substitute for causal prose. Decorative diagrams and diagrams that merely repeat a list are removed. Use Mermaid edge syntax rather than Unicode arrow glyphs.

## Lessons

A lesson is done when it follows the [lesson template](templates/LESSON.md), opens with a consequential learner-facing model, and develops purpose, mechanism, evidence, use, failure, practice, checks, sources, and one next step in that order. It distinguishes durable principles from current product behavior and names prerequisites without silently reteaching an entire earlier module.

The practice must test the lesson's central mechanism with observable results. Check-yourself prompts require explanation, prediction, diagnosis, or tradeoff reasoning rather than trivia. Source tiers contain real and appropriately authoritative links. Module indexes place the lesson in sequence and state readiness evidence.

## Guided labs

A lab is done when a learner can execute it in a named bounded environment from clean setup through cleanup. It contains an initial prediction, healthy baseline, controlled fault or changed condition, evidence capture, ranked hypotheses, discriminating tests, correction or mitigation, recovery proof, explain-back, and standard completion record.

Commands identify targets and expected effects. Fault injection is reversible and does not rely on accidental damage. The lab states privileges, versions, resource bounds, time and cost limits, stop conditions, troubleshooting escape hatches, and what the local result cannot establish about production.

## Incident drills

An incident drill is done when it presents user impact, a safe scenario envelope, role expectations, staged evidence, uncertainty, and at least two plausible hypotheses. The learner must preserve evidence, maintain a fact and decision timeline, state a rollback trigger before mitigation, choose the smallest reversible action, and prove sustained recovery at user and subsystem layers.

Trigger, contributing conditions, detection gaps, and root or causal mechanisms remain distinct. A successful restart is not accepted as diagnosis. Facilitator solutions remain separate and do not leak through titles, links, or issue text. Completion uses the incident rubric and produces owned, testable learning actions rather than blame.

## Projects

A project is done when its brief defines a real user or operator problem, measurable quality attributes, constraints, non-goals, milestones, independent repository boundary, and graduation evidence. It integrates multiple curriculum capabilities without prescribing a single product stack.

Graduation requires a reproducible build, tested contracts and negative paths, an induced or observed failure, evidence-led diagnosis, safe operation and recovery, security and cost analysis, an architecture decision with alternatives, user or stakeholder evaluation appropriate to the claim, and a handoff another engineer can use. Screenshots, deployment existence, and feature count are not graduation evidence.

## Assessments

An assessment is done when it names prerequisites, challenge envelope, fresh evaluator-controlled variation, standard and gate-specific evidence, dimension requirements, evaluator instructions, review prompts, critical requirements, pass rule, rework scope, stop conditions, and remediation links.

It assesses Explain, Build, Debug, Operate, and Design independently. Strong performance in one dimension cannot average away unsafe operation, false explanation, missing diagnosis, or unsupported design. The challenge is reproducible across candidates without requiring identical implementation. Evaluator hints, prior solution access, and assistance are recorded. Rework uses new evidence or a fresh variation, not edited prose alone.

Assessment owners review leakage, ambiguity, scoring consistency, prerequisite drift, accessibility, tool-version drift, and whether the challenge still samples the intended capability.

## Role tracks

A role track is done when it defines an outcome role, honest prerequisites, ordered canonical module path with rationale, required labs, incidents and projects, explicit competency gates, and relevant optional certification overlays. It selects existing curriculum rather than duplicating lessons.

The track explains evidence-based placement and transition from adjacent tracks. Role titles, years of experience, course completion, and tool familiarity are not gates. Every required artifact link resolves, every gate states observable proof, and the weakest prerequisite is visible. A track owner reviews it when modules, practice, assessments, or role expectations change.

## Certification overlays

A certification overlay is done when its name, code, domains, weights, task statements, and exam details come from the certification owner's current primary sources. Every official task statement is mapped to exact existing lessons, practice, and competency evidence. Missing and thin product-specific coverage is explicit.

An overlay adds an ordering and assessment lens; it does not copy the blueprint into a parallel course, reproduce protected questions, promise exam success, or equate certification with operational competence. Exam facts include a checked date or review trigger. The owner reviews the overlay when the provider changes its guide, domains, version, retirement status, or linked curriculum.

## Case studies

A case study is done when it is clearly labeled real with attributable sources or synthetic and composite. It provides context, constraints, staged evidence, competing hypotheses, decision boundaries, options and tradeoffs, a reversible decision, consequences, review, reusable lessons, an evidence exercise, teach-back prompts, and links to canonical curriculum and hands-on practice.

The case preserves uncertainty at each stage and asks the reader to decide before revealing later evidence. Numbers are internally consistent, units and denominators are clear, and calculations can be reproduced. Characters and organizations do not map deceptively to real entities. The ending does not reward lucky guessing or imply that one metric proves causality.

## Review ownership

The pull request identifies one content owner and at least one reviewer other than the author. Required review depends on risk:

| Change | Required ownership or review |
|---|---|
| Factual mechanism or lesson | Domain reviewer and curriculum content owner |
| Lab or operational command | Domain reviewer plus an operator who checks safety and cleanup |
| Security, identity, privacy, or agent authority | Security reviewer |
| Cloud or paid service exercise | Operator who checks account boundaries, spend, and teardown |
| Incident or assessment | Facilitator or assessment owner who checks validity and leakage |
| Project, track, or case study | Curriculum owner plus relevant role or domain reviewer |
| Certification overlay | Curriculum owner plus reviewer who verifies the current official blueprint |

One person may hold more than one specialty, but the author cannot supply the independent review. Approval records what was reproduced, which sources were checked, and any accepted limitation. Unresolved correctness, integrity, or safety concerns block completion.

## Change maintenance

Quality continues after merge. Each volatile artifact has an owner and one or more triggers: upstream release, standard revision, exam blueprint change, deprecation, broken link, security advisory, price-model change, failed learner reproduction, assessment leakage, or contradictory evidence.

Maintenance review checks:

- factual and source currency;
- local and external navigation;
- commands against supported versions;
- safety, permissions, cost, and cleanup assumptions;
- diagram rendering and agreement with prose;
- prerequisite, track, gate, and overlay mappings;
- assessment validity and case-study arithmetic;
- learner confusion, accessibility, and repeated support burden.

Corrections preserve source history and explain what evidence changed. Removed or deprecated material leaves an intentional navigation path when learners may still encounter it. A merged artifact with no owner, no response to known breakage, or stale high-risk instructions is no longer done.

## Pull request quality record

A completed contribution records:

```text
Issue and learner problem:
Artifact type and canonical location:
Content owner:
Independent and specialist reviewers:
Primary sources and version scope:
Evidence reproduced:
Safety, privacy, cost, rollback, and cleanup:
Local validation:
Known limitations:
Maintenance triggers or review date:
Post-merge observation:
```

The exact record may live in the issue or pull request. Every field must be answered or marked not applicable with a reason.
