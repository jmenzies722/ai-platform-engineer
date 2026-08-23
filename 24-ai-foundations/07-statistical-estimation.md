# Statistical estimation and uncertainty

An evaluation number is an estimate from a sample, not a permanent property of a model. Statistical reasoning tells engineers how much evidence that estimate contains.

## Why it matters

[Optimization dynamics](06-optimization-dynamics.md) can fit parameters, but deployment decisions depend on noisy measurements from a target population. Tiny benchmark gains often vanish under resampling or shift.

## How it works

An estimator maps a sample to a quantity such as a mean, error rate, or coefficient. Bias is systematic deviation from the target; variance is sensitivity to the sampled data. Mean squared estimation error decomposes into squared bias plus variance and irreducible noise under standard assumptions.

For independent Bernoulli outcomes, the sample accuracy \(\hat p\) has standard error approximately \(\sqrt{\hat p(1-\hat p)/n}\). Confidence intervals describe a procedure's long-run coverage, not the probability that a fixed parameter lies in one computed interval. Bootstrap intervals resample observed units, but the resampling unit must preserve dependence: resampling rows is invalid when many rows belong to one user.

Hypothesis tests control a chosen false-positive rate under assumptions. A small p-value is not effect size, practical value, or probability the null is true. Repeated metric and slice searches inflate false discoveries. Predeclared primary metrics, paired comparisons, and correction or confirmation on fresh data reduce this risk.

## See it yourself

Two classifiers each see the same 100 examples. A is correct on 82 and B on 84. Treating results as independent discards pairing. Build a disagreement table: suppose B fixes four of A's errors but breaks two of A's correct answers. Only six examples inform the difference.

Swap the A/B labels independently within those six disagreements. Under the no-difference null, seeing at least a 4-to-2 advantage is common. The observed two-point gain is insufficient evidence here. This tiny randomization test shows why shared examples should be compared pairwise.

## Where it shows up

An abuse model may improve global accuracy while harming a low-volume language slice. Report effect sizes, uncertainty, counts, and decision costs for declared slices. Delay-sensitive labels require a fixed maturation window; otherwise the newest model looks artificially good because recent failures have not arrived.

## When it breaks

Leakage, dependent samples, optional stopping, stale labels, and population mismatch produce narrow but misleading intervals. If a result is surprisingly strong, reproduce the split by immutable IDs, inspect duplicates and timestamps, and calculate user-level rather than row-level uncertainty.

When experiments disagree, compare sampling frames and paired per-example outcomes before averaging headline metrics. More decimal places never repair weak evidence.

## Practice

**Observe:** calculate a binomial standard error at \(n=100\) and \(n=10{,}000\). **Build:** bootstrap a paired accuracy difference by user; completion means a seeded rerun reproduces the interval. **Break:** resample events instead of users and show the falsely narrow interval.

## Check yourself

1. Why does pairing usually improve a model comparison?
2. What probability claim does a 95% confidence procedure make?
3. How does searching twenty metrics alter false-positive risk?
4. Why can more rows fail to increase the effective sample size?

## Sources

### REQUIRED

- [NIST Handbook: confidence limits for proportions](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

### RECOMMENDED

- [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

### DEEP DIVE

- [Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations](https://doi.org/10.1007/s10654-016-0149-3)

## Next

Continue to [Decision-centered evaluation](08-decision-centered-evaluation.md).
