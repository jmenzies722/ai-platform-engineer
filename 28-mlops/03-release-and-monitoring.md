# Release and monitoring

Model release is a controlled experiment whose observability must connect system health to prediction quality.

## Why it matters

Healthy servers can emit harmful predictions, while harmless input drift can trigger noisy alarms.

## How it works

Validate offline, shadow traffic without side effects, canary a small share, and expand only while guardrails hold. Monitor latency, errors, saturation, input schemas, feature distributions, predictions, and delayed outcomes. Drift is a diagnostic signal; rollback decisions should use impact and known-good compatibility.

Release stages answer progressively stronger questions. Offline checks model behavior on fixed evidence; shadowing verifies the live feature and serving path; canaries observe real decisions and feedback. Assignment, duration, and stop thresholds must be chosen before rollout. Monitoring links technical signals to model and business outcomes using the exact deployed digest.

## See it yourself

Move a harmless numeric feature from mean 0 to mean 5 while the model ignores it: drift is large and accuracy unchanged. Then keep all feature distributions fixed but redefine a positive outcome from “clicked” to “purchased”: input drift is absent while validity collapses. These cases prove drift is evidence to investigate, not a direct quality verdict.

## Where it shows up

A fraud-model canary routes 5% of eligible traffic, stratified by region, while comparing loss, review load, latency, and feature validity. Delayed labels are joined to the recorded model digest. A fast guardrail can halt on system errors; a slower decision waits for adjudicated outcomes.

## When it breaks

Feedback loops alter data, outcomes arrive late, canary traffic is unrepresentative, and rollback cannot restore changed features. At an alert, first establish the deployment timeline and affected digest, then compare system signals, feature/schema changes, prediction mix, and available outcomes by cohort. Roll back only after confirming old code can read current data.

## Practice

**Build:** write and rehearse a rollout with assignment, percentages, observation windows, owners, guardrails, and compatible rollback. **Break:** skew the canary to one easy region and change a feature schema; show which monitors detect each. **Explain back:** distinguish drift, degradation, and service failure, naming the first evidence for each.

## Check yourself

1. Why is drift not automatically degradation?
2. What does shadowing miss?
3. Which signals require labels?

## Sources

### REQUIRED

- [Google Cloud model monitoring overview](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview)

### RECOMMENDED

- [Kubernetes deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

### DEEP DIVE

- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## Next

Continue to [GPU Systems](../29-gpu-systems/README.md).
