# LLM application evaluations

Application evals convert real requirements and failures into repeatable release evidence across model, prompt, retrieval, tools, and policy.

## Why it matters

[Agents and bounded workflows](06-agents-and-bounded-workflows.md) introduces stateful behavior. Component quality can rise while end-to-end task success falls, so evaluation must follow the full trace.

## How it works

Start from a task taxonomy and threat model. Build cases from specifications, representative traffic, incidents, edge cases, and adversarial tests, with privacy-safe curation. Each case defines inputs, permitted context and tools, expected invariants, scoring method, and severity.

Use deterministic graders for schemas, citations, calculations, tool arguments, side effects, and policy invariants. Human or model judges handle nuanced qualities under a concrete rubric; calibrate them against blinded human labels and track disagreement. Pairwise evaluation reduces scale drift but still needs randomized order.

Report task success, retrieval-stage metrics, unsupported-claim rate, tool correctness, safety violations, latency, and cost. Weighting should reflect intended traffic, while critical failures retain zero-tolerance gates. Store full version identity and privacy-safe traces.

## See it yourself

An answer cites the correct document but claims the opposite of its text. Citation presence passes; entailment fails. A second answer is faithful to a stale policy and therefore still incorrect.

These cases prove that citation, faithfulness, source validity, and task correctness require separate checks.

## Where it shows up

A policy assistant has deterministic checks for source IDs and JSON, rubric scoring for completeness, adversarial injection cases, and a final human audit. Production abstentions and corrected answers feed a regression queue after review.

## When it breaks

Golden answers reject valid variation, judge prompts leak expected labels, datasets overrepresent easy cases, and repeated tuning overfits regressions. Storing raw conversations creates privacy risk.

On a score change, diff outcomes by case and pipeline stage, confirm artifact identities, inspect paired traces, and rerun judge calibration. Do not accept aggregate improvement that violates a critical invariant.

## Practice

**Observe:** split one “correctness” score into testable claims. **Build:** create 20 cases with deterministic and rubric graders. **Break:** bias a judge by answer order and catch it with swaps.

## Check yourself

1. Which properties should use deterministic graders?
2. Why can a faithful answer still be wrong?
3. How should critical rare failures affect release?
4. What prevents regression-set overfitting?

## Sources

### REQUIRED

- [NIST AI 600-1 Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [HELM](https://arxiv.org/abs/2211.09110)

### DEEP DIVE

- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

## Next

Continue to [Operating LLM applications](08-operating-llm-applications.md).
