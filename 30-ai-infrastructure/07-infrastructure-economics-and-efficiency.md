# Infrastructure economics and efficiency

AI infrastructure economics measures cost per useful outcome, including idle reservation, failed work, engineering labor, and quality constraints.

## Why it matters

Cheap accelerator-hours can produce expensive training when jobs wait, restart, underutilize devices, or require extensive operator attention.

## How it works

Total cost includes acquisition or rental, power, cooling, network, storage, licenses, support, idle headroom, and labor. For training, useful denominators include accepted tokens, successful experiments, or target-quality runs. For serving, use requests or tokens meeting latency and quality SLOs. Chargeback attributes cost; showback supplies feedback without transfer.

Utilization decomposes into allocation, device activity, model FLOP utilization, and useful progress. Compare alternatives at equivalent quality and reliability. Spot or preemptible capacity is economical only when checkpoint overhead and interruption loss remain below the discount.

## See it yourself

A run uses 64 GPUs at $3 per GPU-hour for ten hours, then fails irrecoverably: $1,920 produced no accepted artifact. A reliable option at $3.50 with a verified checkpoint completes in 11 hours for $2,464. The first hourly rate is lower but its expected cost depends on completion probability. At 70% success, expected spend per success already exceeds $2,743.

## Where it shows up

FinOps joins scheduler allocations, device telemetry, experiment lineage, and artifact acceptance. Unit-cost regressions are segmented into price, idle time, step efficiency, retries, storage, and network so owners can act.

## When it breaks

Teams optimize a billed metric by harming quality, reserve devices to avoid queueing, or omit shared and idle costs. Mutable labels corrupt attribution. Reconcile trusted workload identity with invoices and resource meters; attach quality and SLO guardrails to every unit metric.

## Practice

**Observe:** calculate expected cost per successful run. **Build:** allocate shared cluster cost by trusted GPU-seconds and storage bytes. **Break:** lower precision until quality fails and buy discounted preemptible nodes without checkpoints. Completion requires a sensitivity analysis and a decision boundary.

## Check yourself

1. Why is cost per GPU-hour an incomplete objective?
2. Which idle capacity is economically intentional?
3. How does completion probability change unit cost?

## Sources

### REQUIRED

- [FinOps Framework: unit economics](https://www.finops.org/framework/capabilities/unit-economics/)

### RECOMMENDED

- [Google Cloud architecture: optimizing AI workloads](https://cloud.google.com/architecture/ai-ml)

### DEEP DIVE

- [MLPerf Training benchmark rules](https://github.com/mlcommons/training_policies)

## Next

Continue to [Control planes and operational observability](08-control-planes-and-operations.md).
