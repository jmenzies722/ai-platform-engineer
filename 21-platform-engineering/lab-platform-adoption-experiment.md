# Lab: Run a Platform Adoption Experiment

Test whether one platform capability improves a real user journey and earns repeated voluntary use. The result may support expansion, narrowing, redesign, or stopping; adoption is not a predetermined conclusion.

## Prerequisites

- Lessons 1 through 7 in this module
- One bounded platform capability or credible prototype
- Access to at least three representative users, or a documented synthetic cohort when real-user research is not possible

## Safety and research boundaries

Obtain informed participation and explain what telemetry, notes, and recordings will be retained. Collect the minimum data needed, remove personal identifiers, report cohorts rather than individual rankings, and do not tie participation or criticism to performance evaluation. Use synthetic records when workplace policy does not permit research data in a learning artifact.

Do not force migration, disable an existing safe path, or expose production users to an unreviewed capability. Every trial must have an exit path and a named support contact.

## Experiment contract

Choose one journey, such as creating a service, deploying a change, or obtaining a temporary development environment. Write the following before recruiting participants:

- target segment, eligibility rule, current alternative, and explicit non-goals;
- baseline task-completion time, hands-on effort, failure or rework rate, support demand, and confidence in each measure;
- hypothesis connecting a specific platform mechanism to a user or operational outcome;
- activation and retained-use definitions, observation window, guardrails, and instrumentation gaps;
- success, stop, and rollback criteria that can reject the proposed expansion.

Do not use registration, page views, resources created, or mandate compliance as a proxy for retained adoption.

## Tasks

1. Map the current journey with at least three participants. Preserve observed steps, waits, handoffs, workarounds, and failure points separately from your interpretations.
2. Segment participants by a constraint likely to affect fit, such as workload shape, compliance boundary, team experience, or migration complexity. Explain why friendly early adopters alone would bias the result.
3. Recruit a small design-partner cohort and record the capability contract, unsupported cases, support hours, escalation path, migration plan, rollback path, and data-handling notice they receive.
4. Ask each participant to complete the journey with the current path and the proposed path where a safe comparison is possible. Capture task outcome, elapsed and hands-on time, help requests, errors, abandoned attempts, confidence, and continued use of the old path.
5. Conduct a short interview after the first attempt. Ask what was unclear, unsafe, missing, or unexpectedly useful. Record disconfirming evidence and quotations without personal identifiers.
6. Make one product or support change tied to the evidence. Repeat the task or run a second cohort, preserving the original measurements and versioning the changed capability.
7. Build an adoption funnel from eligible user to evaluation, activation, repeated intended use, and expansion. Give every numerator a denominator, time window, data source, and exclusion rule.
8. Compare outcome and guardrail changes by segment. Account for failed and abandoned attempts, support labor, migration effort, duplicate-path cost, and any behavior caused by incentives or mandates.
9. Write an expand, narrow, redesign, or stop decision. State alternative explanations, confidence, unresolved risk, next test, owner, and review trigger.

If real participants are unavailable, create a synthetic cohort with at least twelve records and three segments. Seed it with abandonment, support contacts, duplicate-path use, and one instrumentation gap. Label all findings as simulation evidence and do not claim user validation.

## Evidence to keep

Keep the research protocol, consent or synthetic-data statement, redacted journey map, segment rationale, baseline, hypothesis, capability version, task script, raw anonymized observations, interview synthesis, measurement dictionary, funnel and cohort calculations, support log, change record, and decision memo.

The evidence is complete only when a reviewer can:

- reproduce each rate from raw records and explain missing data;
- distinguish awareness, activation, compliance, and retained adoption;
- identify at least one segment for which the capability is a poor fit;
- trace a product decision to user and operational evidence;
- verify that failed attempts and old-path use were not discarded;
- apply the stated stop criteria without relying on platform-team opinion.

## Failure injection

Halfway through analysis, introduce a leadership mandate that makes recorded activation reach 100 percent while two participants retain the old path and support demand doubles. Recalculate the funnel without relabeling compliance as product success. Recommend how to preserve any legitimate risk objective while exposing shadow use and protecting truthful feedback.

Then remove failed attempts from a copy of the dataset. Quantify how the omission changes completion rate, time-to-success, support cost, and the expansion decision. Add an automated completeness check or reconciliation query that would detect this instrumentation failure.

## Rubric

- 2 points: establishes a measurable baseline, falsifiable hypothesis, and explicit stop criteria
- 2 points: samples representative segments and handles research data safely
- 2 points: measures task outcomes, retention, old-path use, support, and guardrails with reproducible definitions
- 2 points: changes the capability from evidence and preserves contradictory or failed observations
- 2 points: makes a defensible decision that can be narrow or negative

## Next

Use the experiment decision and evidence as the product input to the [platform control-plane lab](../labs/14-platform-control-plane/README.md), then carry both into the [Secure Developer Platform Control Plane project](../projects/09-developer-platform-control-plane/README.md).
