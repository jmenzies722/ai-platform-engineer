# Model monitoring and response

Model monitoring connects service health, input validity, prediction behavior, and delayed outcomes to explicit response playbooks.

## Why it matters

[Model packaging and deployment](06-model-packaging-and-deployment.md) limits rollout risk. After release, distributions, labels, dependencies, and user behavior continue changing.

## How it works

Service monitoring covers availability, latency, saturation, and errors. Data monitoring covers schema, missingness, freshness, ranges, categories, and source health. Prediction monitoring covers score, class, confidence, abstention, and slice distributions. Outcome monitoring joins matured labels to the exact prediction and computes task metrics, calibration, and harm indicators.

Covariate drift changes \(P(X)\); label shift changes \(P(Y)\); concept drift changes \(P(Y|X)\). Unlabeled feature drift does not prove quality loss, and stable marginals do not prove quality stability. Drift metrics such as PSI or divergence need reference windows, sample counts, slice context, and actionable thresholds.

Every alert maps to owner, severity, diagnostic evidence, and action: inspect, shadow candidate, stop retraining, disable a feature, route to fallback, rollback, or escalate. Feedback loops need special care because model actions alter which labels become observable.

## See it yourself

A review model sends only high scores to humans, so labels exist mainly for high scores. Calculating accuracy on reviewed cases estimates a selected population, not all traffic.

Random audits or propensity-aware analysis can recover evidence under assumptions. The tiny selection argument explains why “production accuracy” may be biased despite many labels.

## Where it shows up

A fraud service records prediction ID, model and feature versions, decision, exposure, review route, and eventual adjudication. Dashboards show freshness, score shift, review capacity, precision and recall on matured audited samples, and confidence intervals.

## When it breaks

Labels arrive late, dashboards join to the wrong model, alert thresholds flap, aggregate stability hides a slice, and retraining automates corrupted data. Sensitive attributes may be required for fairness auditing but demand strict governance.

On quality alert, verify join integrity and maturation first. Compare traffic, feature validity, score distribution, policy, and route mix. Preserve incident examples and freeze automatic promotion until cause is understood.

## Practice

**Observe:** classify service, data, prediction, and outcome signals. **Build:** define a monitoring table with prediction-label lineage and four playbooks. **Break:** evaluate only reviewed cases and demonstrate selection bias.

## Check yourself

1. Why does feature drift not prove model decay?
2. How do delayed labels alter recent metrics?
3. What metadata joins an outcome to its model?
4. Why can feedback make labels unrepresentative?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [Google Rules of ML: monitoring](https://developers.google.com/machine-learning/guides/rules-of-ml)

### DEEP DIVE

- [Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift](https://arxiv.org/abs/1810.11953)

## Next

Continue to [Governance and lifecycle controls](08-governance-and-lifecycle-controls.md).
