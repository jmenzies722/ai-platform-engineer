# Evaluation and trajectory evidence

Agent evaluation must examine task outcome, the trajectory used to reach it, and the authority exercised under reproducible conditions.

## Why it matters

An agent may complete a task through unsafe, wasteful, leaked, or irreproducible actions that an outcome-only score misses. A single aggregate score can also average a severe policy violation into an apparently passing result.

## How it works

Version the scenario's initial state, permitted tools, tool behavior, hidden checks, budgets, rubric, model, prompt, policy, and evaluator. Outcome metrics remain task-specific. Trajectory metrics include action count, denials, retries, latency, cost, unnecessary access, reversibility, recovery, and progress. Authority metrics record capabilities requested and exercised, approval use, cross-tenant attempts, and consequential effects. Hard policy violations are gates, not values averaged into a utility score.

Separate deterministic checks from model-based judges. Contract, policy, exact state, receipt, and budget assertions should be executable. A judge may assess semantic usefulness only with a pinned rubric, blinded candidates, calibration examples, repeated scoring, and disagreement review. Keep held-out tests isolated from prompts and retrieval. Report denominators, confidence intervals, and slice results; a mean without failure counts or uncertainty is not release evidence.

Production traces connect run, state, model, prompt, tool, policy, principal, approval, effect receipt, latency, and resource use. Minimize and redact content, control access, and retain by policy. Preserve all consequential, denied, anomalous, and reconciliation events; sample only routine spans. Offline fixtures never cause external effects. Low-authority canaries test real timing and permissions after offline gates pass.

## See it yourself

Give two agents the same answer task. Agent A reads three relevant files in five actions for $0.03. Agent B scans 2,000 files, attempts a secret read, receives a denial, retries, and finishes in 40 actions for $0.40. Both receive outcome score 1. If utility is `outcome - cost` and the denial is assigned a finite penalty, enough outcome weight can make B pass. Treating the prohibited attempt as a hard gate makes that impossible. This proves safety constraints cannot generally be recovered from weighted averaging.

Now compare two candidates on 100 independent fixtures: A succeeds 90 times and B succeeds 92. The observed two-point difference is smaller than ordinary binomial uncertainty at this sample size, so claiming B is better is unsupported. The evaluator should publish interval or paired-bootstrap evidence and the per-fixture differences. This does not prove independence or production quality; it proves that a raw percentage alone is insufficient.

## Where it shows up

Before upgrading a coding agent, replay fixtures containing hostile observations, policy denial, approval refusal, ambiguous effects, crash recovery, no progress, and unavailable dependencies. Align candidate trajectories at the first changed durable event. A low-authority canary then measures real latency, denial, escalation, and safe-halt rates. The [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md) requires this versioned evaluation set and replay report.

## When it breaks

Mocks omit real permissions, replay changes external state, judges drift, cases leak into training or prompts, trace volume hides signals, and success criteria reward shortcuts. A changed initial state is not a model regression. Repeated denials may indicate policy or planning; missing events are an evaluation failure, not a neutral sample.

On regression, first verify scenario, initial-state, model, prompt, tool, policy, and evaluator digests. Re-run deterministic checks, align the first changed event, and inspect slices before reading generated prose. Never replay production effects to reproduce a score. Use recorded receipts or a local fake, and label conclusions that depend on mocks.

## Practice

**Build:** create ten deterministic scenarios with outcome, trajectory, authority, recovery, and cost measures. Add hard gates, a paired comparison, and evaluator-version metadata. **Break:** make a mock over-permissive, leak one hidden check, and remove one trace field; demonstrate the false pass and lost diagnosis. **Explain back:** defend which candidate is deployable and bound each claim to its sample and environment.

Use [Lab 19: Bound an Agent Runtime](../labs/19-agent-runtime-safety/README.md) as the deterministic fixture. Its denial reasons, approval-binding proof, budget counters, and audit chain become evaluation assertions, not screenshots.

## Check yourself

1. Which failures must be hard gates rather than score penalties?
2. What makes two candidate trajectories comparable?
3. Which telemetry must be preserved even when routine spans are sampled?

## Sources

### REQUIRED

- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

### DEEP DIVE

- [AgentBench](https://arxiv.org/abs/2308.03688)

## Next

Continue to [Agent runtime architecture](04-agent-runtime-architecture.md).
