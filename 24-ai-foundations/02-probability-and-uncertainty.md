# Probability and uncertainty

AI predictions are usually claims under uncertainty. Probability gives those claims a calculus, but only when their assumptions and reference populations are explicit.

## Why it matters

A score of 0.9 can drive a medical intervention, fraud review, or harmless ranking change. Those decisions require different evidence. Engineers must know whether a number is a normalized model score, an estimated frequency, or a poorly calibrated expression of confidence.

## How it works

A random variable maps outcomes to values. A distribution assigns probability mass or density. Conditional probability \(P(A\mid B)\) updates the event of interest after observing \(B\). Bayes' rule combines likelihood and prior:

\[
P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}.
\]

Expected value summarizes a distribution for a particular quantity, while variance measures spread. Calibration asks whether events predicted at probability \(p\) occur about fraction \(p\) over an appropriate group. It differs from discrimination: a classifier can rank examples well while assigning unreliable probabilities.

Probability statements always depend on a model and reference class. An aleatoric uncertainty describes variation left even with perfect knowledge, such as a fair die roll. Epistemic uncertainty comes from limited knowledge, such as sparse observations in a new region. More data may reduce the latter but not the former. A model's softmax entropy does not reliably separate them; neural networks can be sharply confident far from their training data.

Decisions require costs, not probability alone. If a false negative costs 100 times a false positive, a threshold near 0.5 is rarely justified. Expected utility combines outcome probabilities with consequence values. An abstention option is valuable when uncertainty is high and review has finite cost. Calibration should be checked after deployment by time and important subgroup because prevalence and score meaning can move.

## See it yourself

Suppose 1% of 10,000 requests are abusive. Of 100 abusive requests, 95 are caught. Of 9,900 safe requests, 495 are falsely flagged. A total of 590 requests are flagged, but only \(95/590\), about 16.1%, are abusive. The detector's 95% sensitivity did not mean a flag was 95% likely to be correct.

Repeat with a 10% abuse rate: 950 true positives and 450 false positives make precision about 67.9%. The detector has not changed; the population has. This proves why dashboards must retain base rates and confusion counts rather than display one decontextualized percentage.

## Where it shows up

In fraud review, a calibrated probability can rank cases and estimate reviewer demand. Operations chooses a threshold from fraud loss, customer friction, and review capacity. When traffic composition changes during a promotion, the same score threshold may yield a different queue and precision. Monitoring therefore connects score distributions to delayed adjudication outcomes, not merely service latency. Conditional distributions also underlie next-token generation, but token probabilities are not factual confidence.

## When it breaks

Distribution shift invalidates observed frequencies. Small samples produce noisy estimates. Correlated observations violate convenient independence assumptions. A single aggregate calibration curve can hide severe subgroup errors.

When predicted probabilities look stable but outcomes worsen, first build reliability tables by recent time window and important slice, including sample counts and confidence intervals. A consistent offset suggests recalibration or prevalence shift; failure concentrated in a slice suggests representation or data coverage. If intervals are wide, gather evidence before “fixing” noise. For abrupt all-score shifts, first verify feature ranges and model version.

## Practice

**Build:** create ten probability bins for at least 1,000 predictions. Report count, average score, observed frequency, and expected calibration error; completion means another person can reproduce every bin.

**Break:** change the positive base rate by resampling while keeping conditional score behavior fixed. Show which headline metrics move, then test whether the original threshold still respects a stated review-capacity limit.

**Explain back:** use the abuse calculation to explain sensitivity, precision, base rate, and calibration without conflating them. End by naming the first table you would inspect after a calibration alert.

## Check yourself

1. Why is \(P(A\mid B)\) usually different from \(P(B\mid A)\)?
2. Can an accurate classifier be poorly calibrated?
3. What changes when the base rate changes?

## Sources

### REQUIRED

- [NIST Engineering Statistics Handbook: probability distributions](https://www.itl.nist.gov/div898/handbook/eda/section3/eda36.htm)

### RECOMMENDED

- [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

### DEEP DIVE

- [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)

## Next

Continue to [Data, evaluation, and evidence](03-data-evaluation-and-evidence.md).
