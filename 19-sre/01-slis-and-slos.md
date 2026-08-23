# SLIs and user-centered SLOs

An SLO is a target for a precisely defined user outcome over a window. It is useful only when the SLI population, goodness rule, measurement point, and exclusions resist ambiguity and gaming.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

An event-based availability SLI is good eligible events divided by eligible events. Latency SLIs classify events against a threshold or distribution. Define user, operation, eligibility, good result, measurement location, target, window, and missing-data behavior.

Rolling windows support continuous decisions; calendar windows align reports but reset risk artificially. Client-side or edge measurement often captures more user harm than server uptime. Use a small number of tiered objectives tied to product needs.

## See it yourself

At 1,000,000 eligible requests and a 99.9% objective, `0.001 × 1,000,000 = 1,000` bad requests are allowed. Excluding 10,000 timeouts from the denominator can make the ratio look better while users suffer, proving denominator policy is part of the promise.

## Where it shows up

Checkout success, stream start, job freshness, and control-plane convergence require different SLIs. Write an SLI specification with query tests and an owner; version it when semantics change.

## When it breaks

Retries can hide first-attempt pain, low traffic can make ratios unstable, missing telemetry can count as success, and broad aggregation can hide a harmed region. Inspect numerator, denominator, exclusions, volume, and cohort breakdown.

## Practice

Draft an SLI for checkout and evaluate ten edge cases including cancellation and timeout. Build test events and an executable classifier. Break it with missing outcomes. Completion means policy determines each classification and missing data cannot silently improve reliability.

## Check yourself

1. Which population does your SLI promise to serve?
2. Why is server uptime often a poor availability SLI?
3. How do exclusions alter the product promise?
4. When would a latency threshold outperform a percentile objective?

## Sources

### REQUIRED

- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

### RECOMMENDED

- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)

### DEEP DIVE

- [OpenSLO specification](https://openslo.com/)

## Next

[Error budgets and burn-rate control](02-error-budgets.md)
