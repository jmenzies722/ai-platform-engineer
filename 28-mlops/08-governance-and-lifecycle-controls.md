# Governance and lifecycle controls

ML governance assigns accountable decisions and evidence from proposal through retirement; it is an engineering control system, not a document written after release.

## Why it matters

[Model monitoring and response](07-model-monitoring-and-response.md) detects symptoms. High-impact systems also need risk classification, independent approval, auditability, incident handling, and an enforceable end of life.

## How it works

Inventory every model and consequential automated rule with owner, purpose, affected populations, data, dependencies, environments, risk tier, approvals, and status. Higher risk requires stronger evidence and separation of duties. A model card records intended use, exclusions, metrics, slices, limitations, and ethical considerations; it does not replace controls.

Lifecycle gates cover proposal, data approval, development, independent validation, release, material change, periodic review, incident response, and retirement. Policy as code enforces required evidence in registries and deployment systems. Exceptions have scope, owner, expiry, compensating controls, and review.

Audit logs record who decided what, based on which immutable evidence, without copying secrets or unnecessary personal data. Retirement disables routes and credentials, preserves required records, deletes data under retention policy, communicates downstream impact, and verifies no traffic remains.

## See it yourself

Suppose a low-risk summarizer gains a tool that can approve refunds. Model weights did not change, but authority and potential harm did. Risk must be reassessed because material change includes system capabilities, data, users, and decisions.

This counterexample proves governance cannot key only on model version.

## Where it shows up

A lending model requires legal and risk review, independent validation, adverse-action explanation testing, monitored rollout, periodic performance review, and a rollback owner. Registry policy blocks promotion when any required evidence digest is absent or expired.

## When it breaks

Shadow models become unowned production dependencies, approvals become checkbox rituals, exceptions never expire, vendors change behavior silently, and retired endpoints still receive traffic. Excessive evidence collection itself violates privacy.

Reconcile inventory against deployed endpoints, credentials, registry access, and billing. Sample audit records and trace each to immutable artifacts. Alert before approvals and exceptions expire.

## Practice

**Observe:** classify material changes beyond weights. **Build:** create a risk-tiered release and retirement checklist enforced by a mock policy. **Break:** add write authority without changing model digest and prove the gate requires reassessment.

## Check yourself

1. Why is a model card insufficient governance?
2. What changes can trigger reassessment?
3. How should exceptions end?
4. What proves retirement is complete?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [OECD AI Principles](https://oecd.ai/en/ai-principles)

### DEEP DIVE

- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

## Next

Continue to [Reproducible release lab](lab-reproducible-release.md).
