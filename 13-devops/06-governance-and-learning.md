# Delivery governance and production learning

Good delivery governance makes risk, authority, evidence, and recovery explicit while using production outcomes to improve the system rather than adding indiscriminate approval queues.

## Why it matters

Fast delivery without guardrails can amplify harm, while uniform manual gates make every change slow and encourage bypasses. Metrics disconnected from decisions become dashboards or targets rather than feedback.

## How it works

Classify changes by blast radius, reversibility, data effects, privilege, novelty, and customer impact. Low-risk repeatable changes can pass automated policy; exceptional changes require focused review and explicit ownership. A change record should connect intent, reviewed source, artifact, configuration, deployment, release cohort, telemetry, and recovery decision.

Use delivery measures as a balanced system: lead time, deployment frequency, change failure rate, failed-deployment recovery time, and reliability outcomes. Compare trends and distributions for a service; do not rank individuals. Production verification tests the intended outcome after deployment. Incidents and near misses feed improvements into code, runbooks, tests, platform controls, and training with named owners.

Emergency change paths should be faster, not uncontrolled: strong authentication, narrow temporary access, peer visibility, complete audit evidence, and mandatory follow-up. Expire elevated access and temporary flags.

## See it yourself

Sample ten recent changes. For each, calculate elapsed time from accepted work to production, whether it caused remediation, and how long restoration took. Predict where the largest queue is, then inspect timestamps rather than relying on recollection. A small sample reveals questions but is not a statistically stable benchmark.

## Where it shows up

A routine dependency patch with complete tests and low blast radius promotes automatically to a canary. A one-way data migration requires compatibility evidence, backup validation, a decision owner, and staged checkpoints. Both use the same traceability chain, but controls match risk.

## When it breaks

Approval is ceremonial or concentrated in one unavailable person. Teams optimize deployment count by splitting meaningless changes. Incident reviews assign blame without changing controls. Emergency access remains permanent. Rollback is declared successful from process health while user errors continue.

Diagnose governance with queue time, bypass frequency, exception age, evidence completeness, cohort outcomes, and action-item closure. Remove controls that do not change a decision and strengthen those that catch demonstrated failure modes.

## Practice

**Observe:** reconstruct one normal and one emergency change from intent to user outcome. Mark missing evidence and every wait state.

**Build:** define three risk classes with automated checks, human decisions, allowed exposure, stop conditions, and recovery evidence. Assign owners and exception expiry.

**Break safely:** tabletop a canary error-rate breach during a schema migration. Completion means the team stops exposure, preserves evidence, chooses rollback or roll-forward from compatibility facts, verifies user recovery, and creates one measurable system improvement.

## Check yourself

1. Which change properties justify stronger controls?
2. Why should delivery metrics not rank individual engineers?
3. What must remain controlled during an emergency path?
4. Which evidence proves recovery reached users?

## Sources

### REQUIRED

- [DORA software delivery performance](https://dora.dev/guides/dora-metrics-four-keys/)

### RECOMMENDED

- [Google SRE: postmortem culture](https://sre.google/sre-book/postmortem-culture/)

### DEEP DIVE

- [Accelerate State of DevOps reports](https://dora.dev/research/)

## Next

[Terraform](../14-terraform/README.md)
