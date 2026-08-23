# Designing AI systems

AI system design combines ordinary distributed-systems discipline with probabilistic quality, changing artifacts, untrusted content, and expensive inference.

## Why it matters

A model demonstration can hide the data lifecycle, evaluation gaps, authority boundaries, fallbacks, and operational costs that determine whether the product is safe and useful.

## How it works

Define the user decision and the harm of a wrong, missing, slow, or manipulated result. Establish a non-model baseline. Decompose the system into data and consent, model or provider, prompt and policy, retrieval, tools, orchestration, evaluation, serving, and feedback. Version every behavior-bearing artifact and preserve lineage from response to model, prompt, source versions, tool results, and policy.

Quality needs a task-specific evaluation set with representative slices, difficult counterexamples, and explicit adjudication. Separate retrieval measures from answer measures and system outcomes. Offline evaluation enables repeatability; shadow, canary, and online measures expose real distributions. Human review needs sampling rules, guidance, disagreement handling, privacy protection, and an escalation path.

Treat model output as untrusted. Validate structured output, constrain tool schemas, enforce authorization outside the model, bound steps and spend, and require confirmation for consequential actions. Design provider timeouts, quotas, model fallback, and degraded product behavior. Monitor drift in inputs, retrieval corpus, policy, model versions, quality slices, latency, and unit cost.

## See it yourself

A retrieval system has high answer fluency but low citation entailment. Replacing the model may not help if relevant passages never enter context. Measure retrieval recall, ranking, citation coverage, groundedness, and task success separately. The component metric tells you which experiment can actually discriminate among causes.

## Where it shows up

An agent that drafts account changes may propose an action, but a deterministic policy service verifies identity, scope, limits, and confirmation before execution. The event log captures proposal, evidence, authorization decision, effect identity, and final result for replay and audit.

## When it breaks

AI systems fail through benchmark leakage, unrepresentative averages, prompt injection, stale retrieval, unconstrained loops, silent provider changes, and feedback that amplifies bias. Freeze identifiers and preserve examples before changing multiple artifacts. Compare affected slices and replay a known evaluation set through one change at a time.

## Practice

**Build:** design a cited document assistant with baseline, architecture, artifact registry, evaluation matrix, tool policy, rollout, fallback, feedback, and cost controls. **Break:** poison a document, remove a provider, shift one language slice, and rotate the embedding model. **Explain back:** show which controls are statistical, deterministic, and human-governed.

## Check yourself

1. Why must retrieval and generation be evaluated separately?
2. Which decisions must remain outside model authority?
3. What lineage is required to reproduce one response?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)

### DEEP DIVE

- [MITRE ATLAS](https://atlas.mitre.org/)

## Next

Continue to [Evolution and design review](13-evolution-and-design-review.md).
