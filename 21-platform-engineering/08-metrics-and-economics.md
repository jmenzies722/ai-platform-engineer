# Metrics and platform economics

Platform measurement connects user outcomes, delivery and reliability, risk, adoption, and full cost. Economics determines whether shared capabilities create enough durable value to justify their build, operation, migration, and opportunity costs.

## Why it matters

Activity metrics reward interface traffic and resource growth. Cost totals without allocation encourage indiscriminate cuts. A platform can improve developer satisfaction while becoming unreliable or can reduce cloud spend by shifting toil back to application teams.

## How it works

Build a measurement tree from mission to outcomes and guardrails. For a deployment journey, outcomes might include lead time, hands-on effort, successful completion, recovery, and policy compliance. Guardrails include platform availability, tenant fairness, support load, and change failure. Adoption and satisfaction explain reach and perception but do not substitute for outcomes.

Define every measure with event, population, denominator, window, owner, freshness, segmentation, and gaming risk. Record missing data explicitly. Use distributions and cohorts because medians hide severe tails and global averages hide blocked segments.

Model total cost of ownership: engineering and product labor, cloud and licenses, on-call, support, security, migrations, training, and allocated shared services. Choose a useful unit such as active service-month, successful deployment, or environment-hour. Unit cost needs quality context; a cheaper failed deployment is not efficiency.

Estimate value conservatively from avoided duplicated work, reduced hands-on time, fewer failures, faster recovery, risk reduction, and enabled opportunities. Do not convert every saved minute into cash unless capacity actually changes. Compare build, buy, reuse, and do-nothing alternatives, including switching and exit costs.

## Vocabulary

- **measurement tree:** hierarchy linking mission to outcomes, drivers, and guardrails
- **unit cost:** total relevant cost divided by a defined useful output
- **total cost of ownership:** lifecycle cost to build, operate, support, migrate, and retire
- **opportunity cost:** value of the best work displaced by the investment

## See it yourself

Suppose a platform costs $1.2 million yearly and supports 300 active services. The simple cost is $4,000 per service-year. Predict why this is insufficient. If only 180 services use the production journey, 40% of support belongs to another capability, and failed requests are counted as usage, the denominator and allocation misrepresent cost. Recompute by capability and successful output, then attach reliability and outcome measures.

## Where it shows up

A platform team compares managed database self-service with ticket fulfillment. It measures hands-on labor, elapsed time, restoration evidence, incidents, cloud spend, and support. Self-service costs more in infrastructure but lowers repeated labor and materially improves restore compliance, producing a defensible investment decision.

## When it breaks

Instrumentation drops failed events, savings claims assume all freed time becomes output, and chargeback encourages teams to bypass shared controls. Cost allocation debates create false precision. Team rankings turn metrics into targets and damage reporting.

Triangulate telemetry, finance data, user research, tickets, and incident records. Document confidence and alternative explanations. Stop or narrow investments when outcome improvements do not survive segmentation or full-cost analysis.

## Practice

**Observe:** build a measurement dictionary for one journey with five outcomes and three guardrails. Completion means a reviewer can reproduce each numerator, denominator, and exclusion.

**Design:** prepare an investment review for a service deployment capability. Include baseline, target segment, TCO, unit cost, value mechanisms, uncertainty, alternatives, and stop criteria.

**Break:** remove failed operations from the dataset and show how success rate and unit cost change. Add them back, explain the bias, and propose an instrumentation test.

**Design review:** present a complete platform proposal containing user evidence, product charter, capability contract, paved road, tenancy model, operating model, governance and exception policy, adoption rollout, and economics. A reviewer must be able to reject it using explicit stop criteria.

## Check yourself

1. Why should adoption and satisfaction remain separate from task outcomes?
2. Which costs are commonly omitted from a platform business case?
3. When is developer time saved a defensible economic benefit?
4. What evidence should cause a platform team to stop an investment?

## Sources

### REQUIRED

- [FinOps Framework](https://www.finops.org/framework/)

### RECOMMENDED

- [DORA metrics guidance](https://dora.dev/guides/dora-metrics-four-keys/)

### DEEP DIVE

- [Google SRE: The art of SLOs](https://sre.google/resources/practices-and-processes/art-of-slos/)

## Next

Continue to [Developer Platforms](../22-developer-platforms/README.md).
