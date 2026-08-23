# Cost and efficiency

Cost is a design constraint expressed per useful outcome, with ownership and feedback close enough to change behavior.

## Why it matters

A system can meet latency and availability targets while being economically impossible to scale, and blunt cost cuts can quietly destroy reliability or quality.

## How it works

Construct a cost model from workload units: request, active tenant, indexed document, generated token, successful workflow, or retained gigabyte-month. Separate fixed commitments from variable costs and direct resources from shared overhead. Include replicas, failover reserve, indexes, logs, network transfer, backups, support, licenses, and engineering operations.

Attribute costs with reliable identity and tags, but do not mistake allocation for optimization. Find the marginal cost of one more unit and the dominant sensitivity. Utilization matters alongside provisioned capacity; right-sizing, autoscaling, batching, compression, storage tiers, retention, and algorithmic changes each affect different terms.

Optimization is constrained by SLOs, security, quality, and recovery. Keep cost budgets and anomaly alerts. Use showback to reveal consequences, quotas to bound accidents, and chargeback only when attribution and incentives are mature. Compare build and buy across integration, portability, support, migration, and exit costs, not only list price.

## See it yourself

If model input costs $3 per million tokens, output costs $15, and a request averages 8,000 input plus 1,000 output tokens, token cost is about $0.039 before retrieval, compute, storage, and retries. Doubling context adds $0.024 per request. This sensitivity may justify retrieval pruning more than a minor database discount.

## Where it shows up

An evaluation platform can batch low-priority work, cache immutable model calls, cap retries, and record cost per completed case. A cheaper model is not an improvement if lower quality causes more human review or repeated calls, so unit economics must follow the actual outcome.

## When it breaks

Costs become opaque through untagged shared resources, unlimited cardinality in telemetry, retry amplification, idle accelerators, forgotten data, and discounts that conceal lock-in. Investigate a bill change by rate, volume, mix, and allocation before demanding broad reductions.

## Practice

**Build:** model monthly and marginal cost for the document assistant under base, peak, and failover scenarios. Include model tokens, accelerators, retrieval, storage, logs, network, and support. **Break:** double context, reduce cache hits, and raise availability. **Explain back:** propose three optimizations and state the reliability or quality guardrail for each.

## Check yourself

1. Why is cost per useful outcome better than total spend alone?
2. Which cost terms are commonly omitted from build-versus-buy?
3. How can a cheaper model increase total cost?

## Sources

### REQUIRED

- [FinOps Framework](https://www.finops.org/framework/)

### RECOMMENDED

- [AWS Well-Architected: Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)

### DEEP DIVE

- [Google Cloud Architecture Framework: Cost optimization](https://cloud.google.com/architecture/framework/cost-optimization)

## Next

Continue to [Designing AI systems](12-designing-ai-systems.md).
