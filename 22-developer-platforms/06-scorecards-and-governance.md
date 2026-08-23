# Scorecards and engineering governance

An engineering scorecard translates explicit standards into evidence, explanation, and prioritized remediation. It should help owners improve systems, not compress unlike risks into a competitive leaderboard.

## Why it matters

Teams cannot act on vague maturity expectations. Poor scorecards reward metadata completion, hide stale evidence, treat all services alike, and create incentives to game a number rather than reduce risk.

## How it works

Start with a control or capability objective and define applicability. A public production API may require tested recovery and an on-call owner; an archived prototype should not be graded against the same standard. Each check needs authority, query, freshness, pass semantics, severity, rationale, owner, remediation, exception, and version.

Preserve raw evidence and unknown state. Missing telemetry is not a pass and may differ from a confirmed failure. Show check-level results before aggregation. If a summary is necessary, avoid allowing many trivial checks to hide one critical failure.

Use scorecards in a governance loop: notify owners, provide self-service remediation, track exceptions, verify changes, and review whether checks predict desired outcomes. Roll out new checks in report-only mode, measure false positives, then enforce only when risk and remediation justify it.

Protect access to sensitive findings and avoid individual ranking. Record changes to definitions so historical trends are interpretable. Catalog ownership and lifecycle determine routing and applicability, but a scorecard must tolerate catalog uncertainty.

## Vocabulary

- **applicability:** conditions under which a check is relevant
- **evidence freshness:** maximum acceptable age of an observed fact
- **unknown:** result that cannot be established from current evidence
- **scorecard:** set of contextual checks and evidence for an entity

## See it yourself

Evaluate a service with nine passing documentation checks and one failed public-access control. Predict the result of a 90% aggregate score. A green summary would conceal critical risk. Preserve severity and failed objective. This demonstrates aggregation failure, not that every check should block delivery.

## Where it shows up

A production readiness scorecard reads catalog lifecycle, repository protection, deployment evidence, SLO configuration, restore tests, and ownership. A failing restore test links the exact evidence, supported database workflow, and exception owner rather than assigning a generic grade.

## When it breaks

Checks query stale replicas, teams add empty files to pass, waived failures appear green, and applicability tags are self-declared without validation. Standards change without versioning, causing unexplained trend drops. Detect with evidence-age metrics, spot audits, false-positive reports, remediation completion, and incidents mapped to checks.

## Practice

**Observe:** take one scorecard and trace three checks to control objective, applicability, source, query, freshness, and remediation. Mark unverifiable claims.

**Build:** design a production-readiness scorecard with six checks across ownership, security, reliability, and lifecycle. Include failed, passed, unknown, and exempt examples.

**Break:** stale the evidence source and game one check with metadata only. Show the expected result and a validation that detects both conditions.

**Say it out loud:** explain why a high score is not proof that a service is safe or reliable.

## Check yourself

1. When should unknown differ from failed?
2. Why can weighted aggregate scores hide important risk?
3. What must happen before a check becomes blocking?
4. How do you test whether a scorecard improves outcomes?

## Sources

### REQUIRED

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

### RECOMMENDED

- [Backstage catalog well-known annotations](https://backstage.io/docs/features/software-catalog/well-known-annotations/)

### DEEP DIVE

- [Google SRE: Production readiness review](https://sre.google/sre-book/evolving-sre-engagement-model/)

## Next

Continue to [Identity, security, and supply-chain boundaries](07-identity-security-and-supply-chain.md).
