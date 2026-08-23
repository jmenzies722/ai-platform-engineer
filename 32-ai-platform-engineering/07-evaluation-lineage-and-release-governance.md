# Evaluation, lineage, and release governance

Release governance binds an immutable candidate to reproducible evidence, policy decisions, deployment history, and accountable approval.

## Why it matters

A score without dataset, evaluator, threshold, and artifact identity cannot justify promotion or support recall after a defect.

## How it works

The lineage graph links source data, code, environment, training run, checkpoint, conversion, quantization, evaluation suite, approval, deployment, and observations. Evaluation contracts version scenarios, metrics, slices, judges, seeds, and acceptance policy. Hard safety and compliance gates remain separate from weighted quality objectives.

A promotion controller evaluates attestations and separation-of-duty rules, then records an append-only decision. Exceptions include scope, rationale, compensating control, owner, and expiration. Continuous evaluation detects drift but does not rewrite historical evidence.

## See it yourself

Candidate A scores 0.91 and B 0.90, but A used suite v1 while B used harder suite v2. The numbers are not directly comparable. Replaying both on one pinned suite creates valid evidence; it still may not predict production outcomes.

## Where it shows up

A registry exposes model cards, complete lineage, test reports, signatures, approvals, active deployments, and recall status. Deployment APIs accept only promotable digests.

## When it breaks

Test contamination inflates scores, judge changes masquerade as model changes, manual uploads bypass lineage, and approvals become rubber stamps. Compare artifacts at the first lineage divergence and quarantine unverifiable candidates. Missing evidence is not a pass.

## Practice

**Observe:** reconstruct one prediction's release ancestry. **Build:** define an evaluation attestation and promotion policy. **Break:** swap evaluator version and upload an orphan model. Completion requires non-comparability detection and denied promotion with actionable evidence.

## Check yourself

1. Why must evaluator identity be versioned?
2. Which gates should not be averaged away?
3. What enables precise model recall?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [SLSA provenance](https://slsa.dev/spec/v1.0/provenance)

### DEEP DIVE

- [ML Metadata](https://www.tensorflow.org/tfx/guide/mlmd)

## Next

Continue to [Cost, reliability, and platform operations](08-cost-reliability-and-operations.md).
