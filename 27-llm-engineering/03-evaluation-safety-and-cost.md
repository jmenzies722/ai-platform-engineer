# Evaluation, safety, and cost

An LLM application is acceptable only when quality, risk, latency, and cost work together under realistic traffic.

## Why it matters

Improving one dimension can regress another: more context may improve recall while increasing latency, exposure, and spend.

## How it works

Version an evaluation set and record model, prompt, retrieval, tools, and decoding settings. Gate releases on task metrics and critical safety cases. Measure token use, cache hits, retries, tool calls, and latency percentiles. Layer input limits, content controls, authorization, output validation, and monitoring instead of relying on one model refusal.

Measure cost per accepted task rather than per request: cheap calls that fail and retry may cost more than a stronger first pass. Tail latency should include retrieval and tools, not only model time. Hard safety gates cover unacceptable failures even when averages improve; soft objectives permit explicit quality-cost tradeoffs.

Threat models connect actors, assets, entry points, and consequences to controls. Input filtering reduces obvious abuse, sandboxing limits execution, authorization protects resources, and output validation bounds consumers. Because each control has blind spots, defense in depth aims to prevent one model error from becoming one uncontrolled effect.

## See it yourself

Run 100 fixed cases with 2,000- and 8,000-token context limits. Suppose supported-answer rate rises from 82% to 86%, p95 latency from 1.2 to 2.1 seconds, and tokens per accepted answer from 1,800 to 5,900. Calculate incremental accepted answers and cost. The larger context is not simply “better”; its four-point gain must justify latency, spend, and extra untrusted surface.

## Where it shows up

A model gateway can route ordinary cases to a cheaper model and escalate uncertain cases. It records route, cache status, retries, policy decisions, and accepted outcome, allowing cost per success and refusal quality to be compared. Budget alarms and abuse controls operate per tenant so one workload cannot consume fleet capacity.

## When it breaks

Static tests miss adaptive attacks, judge scores drift, and averages hide rare high-impact failures. When cost jumps, first decompose by request count, prompt tokens, generated tokens, retries, model route, and tool calls. When safety alerts rise, preserve the exact input and control decisions, then determine whether prevention, authorization, or monitoring failed. Do not start by weakening a gate to restore pass rate.

## Practice

**Build:** create a release scorecard with task quality, critical safety gates, p50/p95 latency, and cost per accepted task. Make it compare two configurations from raw case records.

**Break:** add a retry loop and oversized retrieved context. Show the cost and tail-latency signatures, then enforce budgets.

**Explain back:** defend one release decision, including a tradeoff you rejected and the first evidence you would inspect for a cost or safety regression.

## Check yourself

1. Why measure cost per successful task?
2. What belongs in a release record?
3. Why are model refusals insufficient authorization?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [OpenAI safety best practices](https://platform.openai.com/docs/guides/safety-best-practices)

### DEEP DIVE

- [MITRE ATLAS](https://atlas.mitre.org/)

## Next

Continue to [MLOps](../28-mlops/README.md).
