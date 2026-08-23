# Release engineering and resilience

A release is a controlled reliability experiment. Safe delivery limits simultaneous exposure, defines automatic evidence, preserves rollback or roll-forward paths, and separates deployment from activation.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Build once, promote immutable artifacts, verify provenance, and deploy through progressive stages. Canary analysis compares user outcomes and guardrails against a valid control. Feature flags decouple code arrival from behavior but create configuration state that needs ownership and expiry.

Rollback must account for database and message compatibility. Expand-and-contract migrations add compatible schema, shift readers and writers, then remove old paths. Resilience testing injects one bounded failure with an explicit steady-state hypothesis and abort condition.

## See it yourself

A 1% canary limits direct exposure only if traffic is representative and the canary does not mutate globally shared state. The percentage is not a risk proof; shared databases and migrations can make blast radius 100%.

## Where it shows up

Release policy should consume SLO and error-budget evidence. Track artifact identity, configuration, cohort, start time, comparison windows, and rollback verification. Exercise rollback before it is needed.

## When it breaks

Canaries can receive only easy traffic, flags can remain permanently divergent, rollback can meet incompatible data, and automatic analysis can pass on missing metrics. Require telemetry health, minimum sample size, compatibility tests, and a human stop control.

## Practice

Design a three-stage rollout for an API and backward-compatible migration. Inject a version-specific 1% error increase. Completion means promotion halts from SLI evidence, rollback preserves data compatibility, and the flag and old schema have removal conditions.

## Check yourself

1. Why does a small canary not always mean a small blast radius?
2. What makes a migration rollback-safe?
3. How should missing release telemetry be treated?
4. Which resilience experiment validates your largest assumption?

## Sources

### REQUIRED

- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/)

### RECOMMENDED

- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)

### DEEP DIVE

- [Principles of Chaos Engineering](https://principlesofchaos.org/)

## Next

[Security](../20-security/README.md)
