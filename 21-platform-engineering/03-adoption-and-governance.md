# Adoption, governance, and measurement

Adoption, governance, and measurement form one feedback system: teams choose or are required to use capabilities, controls shape those choices, and evidence reveals whether the result is safer and more effective.

## Why it matters

Portal visits and resource counts measure activity, not value. Mandates can produce apparent adoption while teams retain shadow paths. Heavy approval gates move work outside observable systems and can increase rather than reduce risk.

## How it works

Define an adoption funnel for a real journey: eligible teams, aware teams, first successful use, repeated use, and retained use. Pair it with task outcomes such as elapsed and hands-on time, success without support, change failure, recovery, security posture, and cost. Segment by workload and maturity because an average can hide exclusion.

Choose controls according to risk. Safe defaults guide; guardrails reject known-dangerous states; detective controls find drift; human review handles contextual judgment. Every denial should identify the rule, evidence, owner, and remediation or exception route. Log decisions for audit without exposing secrets.

Treat exceptions as data. Record requester, scope, rationale, risk owner, controls, expiry, and review outcome. A cluster of similar exceptions may expose a missing platform tier or a bad policy. It does not automatically justify weakening the rule for everyone.

Create a regular review that joins product, governance, reliability, and economics. Compare promised outcomes with user research, telemetry, incidents, exception trends, support demand, and unit cost. Decide to invest, narrow, migrate, or retire.

## Vocabulary

- **adoption:** meaningful use by an eligible user for an intended job
- **retention:** repeated use after initial success
- **guardrail:** automated boundary that prevents a known unsafe state
- **exception:** explicit, owned acceptance or mitigation of risk outside a standard rule

## See it yourself

Consider this monthly report:

```text
Eligible services: 200
Registered in portal: 170
Deployed through paved road: 120
Repeated use next month: 68
Median lead time: 2.1 days, previously 1.4
Tickets per 100 deployments: 31, previously 12
```

Predict whether “85% adoption” is defensible. Registration is 85%, but retained journey use is 34%, and outcomes worsened. The evidence suggests a drop after first use and a likely workflow or support problem; it does not yet identify the cause.

## Where it shows up

A platform team introduced mandatory ownership metadata. Immediate API validation increased failed submissions, but contextual errors and an import tool reduced incident-routing time. Governance succeeded only after measuring both short-term friction and the operational outcome the rule was meant to improve.

## When it breaks

Metrics fail when definitions drift, missing events are counted as success, or teams optimize the measure instead of the outcome. Governance fails when policy has no owner, exception queues exceed the stated response objective, or approved exceptions never expire. Adoption fails when users cannot leave feedback safely or alternatives are hidden from measurement.

Correlating platform use with better outcomes is not causal proof: stronger teams may adopt first. Use staged rollouts, matched segments, journey-level baselines, and qualitative evidence before claiming impact.

## Practice

**Observe:** construct an adoption funnel from existing logs or a synthetic dataset. Define eligibility and retention explicitly. Completion means totals reconcile and unknown states are not silently counted as failures or successes.

**Design:** create a governance and measurement plan for production database provisioning. Include three controls, an exception record, five balanced measures, data owners, segmentation, and review cadence.

**Break:** simulate a mandate that doubles registrations but increases task failures by 50%. Write the decision memo explaining what can be concluded, what cannot, and the next experiment.

**Say it out loud:** distinguish adoption, compliance, and improved outcomes.

## Check yourself

1. Which evidence can reveal coerced adoption or shadow workflows?
2. When should policy require contextual human judgment?
3. Why should exception trends feed product discovery?
4. How would you test whether platform use caused an outcome improvement?

## Sources

### REQUIRED

- [DORA metrics guidance](https://dora.dev/guides/dora-metrics-four-keys/)

### RECOMMENDED

- [CNCF Platform Engineering maturity model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/)

### DEEP DIVE

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

## Next

Continue to [Self-service and tenancy](04-self-service-and-tenancy.md).
