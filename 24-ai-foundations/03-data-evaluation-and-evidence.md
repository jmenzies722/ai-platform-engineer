# Data, evaluation, and evidence

Evaluation is an argument that measured behavior on selected data predicts behavior in a real setting. Strong evaluation makes every part of that argument inspectable.

## Why it matters

Most costly AI failures are not arithmetic mistakes. They come from unrepresentative data, leaked labels, vague success criteria, or averages that hide important failures.

## How it works

Training data fits parameters, validation data guides choices, and test data estimates performance after choices are fixed. The split must respect the unit of independence: records from one person, device, or future period often belong together.

Metrics encode tradeoffs. Precision measures how often positive predictions are correct; recall measures how much of the positive class is found. Confusion matrices retain the underlying counts. For generation, task-specific human or programmatic judgments are often more informative than one generic similarity score.

An estimate also needs uncertainty. Repeated samples, bootstrap intervals, or paired tests help distinguish a stable improvement from noise. Evaluation supports a bounded claim; it does not establish causality or universal safety.

The evaluation population should follow the decision the model will support. Sampling production traffic uniformly can underrepresent rare, high-impact cases, so a test set may deliberately oversample them while reporting weighted aggregate results. Thresholds and slices must be specified before inspecting candidate outputs to reduce the temptation to select favorable views.

Offline and online evidence answer different questions. Offline replay is repeatable and safe but cannot measure user adaptation, queueing, or integration failures. Shadowing exercises the live path without acting on predictions. A canary measures system effects on a limited population, but only if assignment is representative and guardrails can stop it. No single stage replaces the others.

## See it yourself

Construct 100 customers with ten rows each and give every customer a stable random label. Include customer ID as a feature. A random row split lets a lookup-style model see each customer's label during training and can approach perfect test accuracy. A customer-level split contains unseen IDs and should fall near chance.

The expected observation is a large score collapse even though row counts and model code are unchanged. It proves that the independent unit was the customer, not the row. Remove the ID but leave a customer-specific proxy such as postal address; if performance remains implausibly high, the exercise also demonstrates indirect leakage.

## Where it shows up

A content-moderation team might gate a release on recall at a fixed false-positive rate, with separate slices for language and abuse type. Shadow traffic verifies parsing and latency without hiding posts. A canary then compares appeals and moderator workload. Ongoing outcome labels arrive later, so deployment records must preserve the exact model and threshold that made each decision. This chain ties a benchmark score to operational evidence without pretending they are interchangeable.

## When it breaks

Benchmarks become targets and invite overfitting. Labels can encode historical bias. Delayed outcomes obscure regressions. Aggregate scores hide slices, and production users adapt to the system.

When a new model posts a surprising gain, first audit split keys, timestamps, duplicate or near-duplicate examples, and preprocessing fit scope before tuning anything. If offline gains disappear online, compare the served feature and model versions with the evaluation manifest, then inspect traffic mix and latency-induced fallbacks. If only one slice regresses, inspect its confusion examples and label agreement rather than averaging it away.

## Practice

**Build:** write an evaluation card for a moderation model: intended population, split unit, label process, primary metric, three slices, acceptance threshold, interval method, and one claim the test cannot support. Completion requires raw confusion counts and a reproducible scoring command.

**Break:** introduce duplicate users across splits and show the inflated result. Then create a slice comprising 2% of examples with zero recall while aggregate accuracy barely moves. Repair the evaluation, not the model.

**Explain back:** present the release argument to a skeptical reviewer. Distinguish what offline, shadow, and canary evidence establish, and identify the first leakage check you would make if the result looked too good.

## Check yourself

1. What is leakage, and why can it survive a train/test split?
2. When is recall more important than precision?
3. Why should model selection and final estimation use different data?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

### DEEP DIVE

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)

## Next

Continue to [Linear algebra for models](04-linear-algebra-for-models.md).
