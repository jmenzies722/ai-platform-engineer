# Evaluating language models

Language-model evaluation must separate model capability, application behavior, factual support, safety, and serving performance.

## Why it matters

[Inference mechanics and efficiency](07-inference-mechanics-and-efficiency.md) shows configuration affects outputs and latency. A single benchmark score cannot authorize deployment across tasks and risks.

## How it works

Capability evaluations use controlled prompts to test knowledge or skills. Task evaluations measure an application contract end to end. Reference-based metrics work for constrained answers but can punish valid alternatives; model-based judges scale qualitative review but inherit bias, position effects, and model blind spots.

Factuality needs claim extraction and source verification, not stylistic preference. Calibration can include selective prediction: confidence or a verifier controls abstention, and risk is plotted against coverage. Safety tests distinguish attack success, harmful compliance, benign refusal, data exposure, and tool effects.

An evaluation manifest fixes model, tokenizer, prompt template, decoding, dataset, contamination checks, scoring code, judge and rubric. Report distributions, paired changes, uncertainty, slices, and examples. Keep a final set untouched and continuously collect production failures into a separate regression set.

## See it yourself

Judge two answers in A/B order, then B/A order. If the same content wins first position both times, the judge has position bias. Blind labels and randomize order; require consistency or human adjudication.

This tiny test falsifies judge invariance. It does not validate the judge on factuality, safety, or every style.

## Where it shows up

A coding assistant release needs compilation and test success, vulnerability checks, edit acceptance, latency, cost, and human review of representative failures. A general chat benchmark is diagnostic but not the release gate.

## When it breaks

Training contamination inflates results, prompt changes invalidate comparisons, judges prefer verbosity, and aggregate means hide catastrophic failures. Repeated leaderboard tuning overfits public tests.

On a surprising gain, lock artifacts, inspect paired examples, rerun order-swapped and alternate-judge checks, search contamination, and confirm with deterministic task outcomes where possible.

## Practice

**Observe:** score one answer separately for correctness, support, and style. **Build:** write a versioned 20-case evaluation manifest with paired output diff. **Break:** introduce judge position bias and prove the randomized check catches it.

## Check yourself

1. Why is application evaluation different from base capability?
2. What does risk-coverage reveal?
3. How can a judge model bias a release?
4. Which artifacts make a result reproducible?

## Sources

### REQUIRED

- [HELM: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110)

### RECOMMENDED

- [NIST AI 600-1 Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)

### DEEP DIVE

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)

## Next

Continue to [Transformer internals lab](lab-transformer-internals.md).
