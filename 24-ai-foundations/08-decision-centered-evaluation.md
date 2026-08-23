# Decision-centered evaluation

Evaluation is the design of evidence for a decision, not the collection of every convenient metric.

## Why it matters

[Statistical estimation and uncertainty](07-statistical-estimation.md) explains noisy estimates. Engineers must still connect those estimates to users, costs, safety constraints, and a release decision.

## How it works

Begin with the deployment unit, target population, action, and failure cost. Define a primary metric that reflects the desired decision, guardrails that must not regress, and diagnostic slices that explain failures. Keep training, validation, and final test roles separate; repeated test-driven development turns the test set into training data.

A confusion matrix retains true and false positives and negatives. Precision and recall select different denominators. ROC curves summarize ranking across thresholds but can obscure operational burden under rare positives; precision-recall curves expose it. Proper scoring rules such as log loss assess probability quality. Calibration and discrimination are separate.

Offline evaluation estimates behavior on recorded data. Online experiments include interaction effects, latency, fallback, and changed user behavior. Neither establishes every safety claim. Shadowing measures production inputs without exposing outputs; canaries expose a bounded population; rollback limits harm. Human evaluation needs a rubric, blinded ordering, disagreement measurement, and adjudication.

An evaluation should be executable and versioned: dataset digest, label policy, model and prompt revision, inference settings, metric code, uncertainty, slice definitions, and known exclusions.

## See it yourself

For 1,000 cases with 20 positives, model A finds 18 and raises 82 false alarms. Precision is 18%, recall 90%, and accuracy 90%. A model predicting “negative” always has 98% accuracy and zero recall.

Now assign false negatives a cost of 50 and false positives a cost of 1. A costs \(2\times50+82=182\); the trivial model costs \(20\times50=1000\). This proves accuracy can rank models opposite to stated consequences. The cost values remain assumptions requiring owner approval.

## Where it shows up

For a document triage system, release gates might require expected handling cost improvement, no recall regression on urgent cases, p95 latency below a budget, and calibrated abstention under poor scans. A slice report identifies which document types need data or routing changes. The final artifact links failures to examples, not just aggregates.

## When it breaks

Benchmark contamination inflates scores. Aggregate metrics hide harmed groups. Labelers infer the model identity from style. A proxy metric improves while the user outcome worsens. Thresholds evaluated on one prevalence fail under another.

On regression, preserve exact failed examples and compare model outputs pairwise. Check dataset, code, and decoding digests before diagnosing model behavior. In production, correlate outcome changes with traffic mix, policy version, fallback rate, and latency before attributing causality.

## Practice

**Observe:** compute all confusion-matrix rates for a rare-event example. **Build:** write an evaluation card with one primary metric, two guardrails, three slices, uncertainty, and a release rule. **Break:** tune a threshold repeatedly on the test set, then evaluate once on untouched data and document the optimism.

**Say it out loud:** state what your evaluation supports, what it excludes, and who owns the release decision.

## Check yourself

1. Why can ROC AUC be insufficient for a review queue?
2. What turns a metric report into reproducible evidence?
3. When should a canary follow an offline test?
4. How can a model improve a proxy while harming users?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [Google Rules of ML, evaluation guidance](https://developers.google.com/machine-learning/guides/rules-of-ml)

### DEEP DIVE

- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

## Next

Continue to [Foundations evidence lab](lab-foundations-evidence.md).
