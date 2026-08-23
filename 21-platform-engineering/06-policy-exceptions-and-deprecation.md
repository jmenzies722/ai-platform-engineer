# Policy, exceptions, and deprecation

Platform governance turns risk decisions into understandable defaults, automated constraints, auditable exceptions, and safe lifecycle changes. Good governance changes behavior without hiding accountability behind a policy engine.

## Why it matters

Unreviewed freedom repeats preventable failures. Blanket approval gates create queues and shadow systems. Abrupt deprecation can force risky migrations or strand production workloads on components no team supports.

## How it works

Begin with a named risk, affected asset, threat or failure, and control objective. Choose the least costly mechanism that provides evidence: documented default, warning, admission rule, continuous detection, or human review. Policy code must be versioned, tested against positive and negative cases, and released with owners and rollback criteria.

Return denials at the earliest useful boundary with rule identifier, evaluated facts, remediation, documentation, and exception path. Do not expose secrets in messages or logs. For contextual risks, issue an exception with scope, compensating controls, accountable risk owner, expiry, and review history.

Deprecation is a product migration. Inventory consumers and versions, publish compatibility and dates, provide an equivalent path, canary the change, measure blockers, and communicate through channels users actually consume. Define who changes generated code, infrastructure state, and data. Removal occurs only after exit criteria or an explicit residual-risk decision.

Use decision records for durable tradeoffs and audit logs for events. A decision record explains why a policy exists; an audit event proves which subject attempted which action under which policy version.

## Vocabulary

- **control objective:** outcome a control is intended to achieve
- **policy as code:** machine-evaluated rule managed through software lifecycle practices
- **compensating control:** alternate mechanism reducing risk when the standard control cannot apply
- **deprecation:** supported transition away from a contract before removal

## See it yourself

Write tests for a rule requiring owner and data classification on production databases: one valid request, one missing owner, one invalid classification, and one approved exception. Predict which evidence an auditor can reconstruct. A passing policy test proves rule behavior for those inputs, not that the control objective is effective in production.

## Where it shows up

A runtime version reaches end of support. The platform identifies workloads from authoritative inventory, blocks only new creation on the old version, supplies an automated compatibility check, tracks migration failures, and escalates residual workloads to named owners before removing runtime support.

## When it breaks

Rules encode style preferences as security requirements, produce generic denial messages, or disagree across interfaces. Exceptions have no expiry. Migration dashboards count repositories rather than running workloads. A deadline arrives while the replacement lacks a required capability.

Inspect denial volume by rule, false-positive reports, exception age, consumer inventory freshness, migration success, and incidents caused by the control or its absence.

## Practice

**Observe:** select one platform rule and trace its risk statement, code, tests, production decisions, exception path, and owner. Completion means missing links are documented as governance gaps.

**Design:** create a deprecation plan for one runtime version. Include inventory confidence, compatibility contract, phases, communication, automation, telemetry, stop conditions, and residual-risk authority.

**Break:** introduce a policy release that rejects 20% of valid requests. Specify detection, rollback, audit preservation, user communication, and tests preventing recurrence.

**Say it out loud:** explain why enforcement strength should follow risk evidence rather than organizational preference.

## Check yourself

1. When is a warning more effective than a blocking rule?
2. What evidence makes an exception governable?
3. Why is identifying repository versions insufficient for deprecation?
4. Who may accept the risk of removing support with consumers remaining?

## Sources

### REQUIRED

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

### RECOMMENDED

- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs/latest/)

### DEEP DIVE

- [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

## Next

Continue to [Adoption and organizational change](07-adoption-and-change.md).
