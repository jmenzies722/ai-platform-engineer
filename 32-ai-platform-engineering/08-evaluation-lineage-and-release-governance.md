# Evaluation, lineage, and release governance

Release governance binds an immutable candidate to reproducible evidence, policy decisions, deployment history, and accountable approval.

## Why it matters

A score without dataset, evaluator, threshold, uncertainty, and artifact identity cannot justify promotion or support recall after a defect. AI evaluation is especially easy to overstate: aggregate metrics hide weak slices, changing judges invalidate comparisons, and offline tests do not establish production behavior. Governance should preserve the claim, its evidence, and its limits rather than turn judgment into one opaque score.

## How it works

The lineage graph links source manifests, transformations, code, environment, training run and attempts, checkpoints, conversion or quantization, evaluation suites, attestations, approvals, deployments, retrieval indexes, and observations. Nodes use immutable digests or versioned identities; edges record operation, principal, time, and policy. Append-only history permits superseding an assertion without rewriting what supported an earlier release.

An evaluation contract versions scenarios, dataset manifests, split and contamination checks, metric implementations, slices, random seeds, inference configuration, judge model and prompt, repetitions, uncertainty method, and acceptance policy. Compare candidates only under compatible contracts. For stochastic systems, report distributions or confidence intervals and predeclare a tolerance. A measured pass demonstrates behavior on those samples under that evaluator; it does not prove absence of harm or future production quality.

Keep non-compensable gates separate. Artifact signature, required lineage, prohibited-data checks, severe safety cases, and legal approval cannot be averaged away by a high relevance score. Quality objectives may use a scorecard, but thresholds and slice floors remain explicit. Human approval records the accountable review of evidence and residual risk; it does not repair missing evidence.

The evaluation runner emits a signed or otherwise integrity-protected attestation containing subject digest, predicate type, suite and evaluator versions, results, environment, timestamps, and invocation identity. A promotion controller verifies subject identity, evidence freshness, mandatory gates, policy version, separation of duties, and target environment, then appends a decision. Exceptions have narrow scope, rationale, compensating control, approver, owner, expiry, and automatic re-evaluation. Deployment accepts only a promotable digest and records the exact decision.

Continuous evaluation observes drift, outcome proxies, incidents, and sampled production cases. It creates new evidence and may trigger halt, rollback, or recall; it never changes the historical attestation. Recall traverses lineage from affected data, evaluator, runtime, index, or model to active deployments and owners. Completeness is bounded by graph coverage, so orphan imports are quarantined rather than treated as safe.

## See it yourself

Candidate A scores 0.91 on suite v1 and B scores 0.90 on harder suite v2. The values are not directly comparable because two variables changed. Replay both on pinned suite v2 with identical inference settings and seeds; now their measured difference is attributable to candidate identity within the run's tolerance and nondeterminism. Next change one byte of the candidate after attestation and assert promotion fails because the subject digest differs. These checks prove evidence binding and comparison compatibility, not production superiority.

## Where it shows up

A model registry exposes cards, lineage, evaluation reports, signatures, approvals, active deployments, exceptions, and recall status. The same mechanism governs prompt bundles, rerankers, embedding models, and retrieval indexes. A canary adds operational and domain evidence by version; the release controller evaluates those signals before increasing traffic. Reviewers can answer which policy admitted a deployment and which active services depend on a revoked dataset.

## When it breaks

Test contamination inflates scores, benchmark tuning overfits the suite, judge changes masquerade as candidate changes, averages hide critical slices, manual uploads bypass provenance, attestations go stale, and approvals become rubber stamps. Debug by comparing immutable identities at the first lineage divergence: subject, data, transforms, runtime, evaluator, policy, then deployment. Preserve raw result artifacts and decision logs, quarantine unverifiable candidates, and distinguish “failed” from “not evaluated.” Missing evidence is not a pass. During recall, inventory active and cached copies before deleting metadata needed to prove impact.

## Practice

**Observe:** reconstruct one synthetic prediction's release ancestry and identify every mutable reference. **Build:** define an evaluation contract, attestation schema, non-compensable gates, promotion policy, exception expiry, and recall query. **Break:** swap evaluator version, regress one critical slice, upload an orphan model, expire evidence, and mutate the attested digest. Completion requires non-comparability detection, actionable denied promotion, precise affected-deployment inventory, and preserved historical evidence.

## Check yourself

1. Why must evaluator identity and inference settings be versioned?
2. Which gates should never be averaged away?
3. What evidence bounds a claim of precise model recall?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [Model Cards for Model Reporting](https://doi.org/10.1145/3287560.3287596)

### RECOMMENDED

- [SLSA provenance](https://slsa.dev/spec/v1.0/provenance)
- [in-toto attestation framework](https://in-toto.io/)

### DEEP DIVE

- [ML Metadata](https://www.tensorflow.org/tfx/guide/mlmd)
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## Next

Continue to [Cost, reliability, and platform operations](09-cost-reliability-and-operations.md).
