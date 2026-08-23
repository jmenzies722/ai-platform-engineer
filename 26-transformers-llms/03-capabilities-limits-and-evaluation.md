# Capabilities, limits, and evaluation

LLM capability is conditional on task, prompt, context, tools, and scoring method. A single benchmark number is not a system guarantee.

## Why it matters

Fluency encourages people to infer understanding and reliability that an evaluation never measured.

## How it works

An evaluation samples realistic inputs, captures exact configuration, and scores dimensions separately: correctness, completeness, citation support, refusal, latency, and cost. Programmatic checks work for schemas and known answers; calibrated human review is needed for nuanced outputs. Contamination, prompt sensitivity, and judge-model bias limit conclusions.

Start from a task claim, not a benchmark name. Sampling defines the population; a rubric operationalizes success; graders introduce measurement error. Blind paired review reduces some preference bias, and inter-rater agreement reveals ambiguity rather than proving truth. Confidence intervals describe sampling uncertainty but not omitted scenarios.

Capability and safety interact with scaffolding. Retrieval may improve support but introduce malicious text. Tools can make arithmetic reliable while increasing consequence. Evaluation should preserve component traces so a failure can be assigned to retrieval, orchestration, model reasoning, validation, or execution.

## See it yourself

Create 20 questions with source passages and supported answers. Ask each in direct, conversational, and JSON-request formats. Score answer correctness and whether every claim is supported. If 18 direct answers but only 12 JSON answers are correct, the system is format-sensitive. Reversing answer order in a pairwise judge can expose position bias. These observations bound stability and grading reliability; they do not measure general intelligence.

## Where it shows up

A support assistant release may require exact policy citations, correct escalation, and no invented account actions. Schema checks catch malformed responses, source matching checks citations, and trained reviewers assess nuanced helpfulness. Production sampling then tests traffic the curated set missed. Storing retrieval and prompt traces lets the team identify whether a citation regression began in indexing or generation.

## When it breaks

Public tests leak into training, averages hide severe cases, and automated judges share biases with the candidate model. When a score moves, first lock and compare the complete evaluation manifest, then inspect per-case paired differences rather than the mean. Check parser failures, judge order, and prompt versions. If only public items improve, test fresh private variants before claiming capability gain.

## Practice

**Build:** create at least 20 versioned cases for one real task, including abstention, adversarial content, and critical slices. Define rubric and acceptance gates before viewing candidates.

**Break:** contaminate two cases in the prompt and reverse pairwise answer order. Show how leakage and judge bias alter results.

**Explain back:** state the narrow claim your evaluation supports, three threats to validity, and the first artifact you would compare after a regression.

## Check yourself

1. Why separate factuality from style?
2. What is benchmark contamination?
3. Which claim can ten test cases support?

## Sources

### REQUIRED

- [NIST AI 600-1: Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [HELM](https://arxiv.org/abs/2211.09110)

### DEEP DIVE

- [Holistic Evaluation of Language Models](https://crfm.stanford.edu/helm/)

## Next

Continue to [LLM Engineering](../27-llm-engineering/README.md).
