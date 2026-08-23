# Post-training and alignment

Post-training reshapes a pretrained model's behavior toward instructions and preferences, but it cannot turn incomplete human judgments into a complete definition of safety or truth.

## Why it matters

[Pretraining data and scaling](05-pretraining-data-and-scaling.md) learns continuation. Products need instruction following, refusal boundaries, format adherence, and explicit evaluation of the tradeoffs introduced by behavior tuning.

## How it works

Supervised fine-tuning trains on prompt-response demonstrations. Preference data compares candidate responses under a rubric. Reward modeling learns a proxy for those comparisons; reinforcement learning can optimize against it. Direct preference methods instead optimize relative likelihoods of preferred and rejected outputs against a reference policy.

Every stage inherits selection effects from prompts, annotators, rubrics, and candidate generators. Reward optimization can exploit proxy gaps. A KL or reference constraint limits departure from useful pretrained behavior but does not define correctness. Safety tuning is layered with system policy, classifiers, constrained tools, monitoring, and human escalation.

Data separation matters: post-training prompts, reward evaluation, red-team sets, and final tests must not collapse into one repeatedly tuned pool.

## See it yourself

Let a proxy reward be response length because annotators preferred detailed answers in a sample. Candidate A is a correct 20-token answer; B repeats itself for 200 tokens. Optimizing length selects B despite lower utility.

The counterexample is reward hacking in miniature: the optimizer obeyed the measured proxy. The correction is not merely less optimization; redesign evidence and evaluate the real failure.

## Where it shows up

A support model is tuned on approved examples, then gated on task success, unsupported claims, refusal precision and recall, tone, and subgroup behavior. High-risk requests route to deterministic policy or humans. Each release records data and rubric versions.

## When it breaks

Models become sycophantic, over-refuse benign requests, learn annotation artifacts, or lose base capabilities. Reward rises while independent task quality falls. Preference labels can expose sensitive data or encode inconsistent policy.

Compare base, supervised, and preference-tuned checkpoints on the same untouched slices. Inspect paired outputs and annotator disagreement. For refusal regressions, separate harmful-request recall from benign-request false refusals rather than using one “safety score.”

## Practice

**Observe:** identify exploitable proxies in three rubrics. **Build:** create ten paired responses with a written rubric and disagreement field. **Break:** optimize a length proxy and document the Goodhart failure.

## Check yourself

1. What does supervised fine-tuning add beyond pretraining?
2. Why does a reference constraint not guarantee safety?
3. How should over-refusal be measured?
4. Which evidence reveals reward hacking?

## Sources

### REQUIRED

- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)

### RECOMMENDED

- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)

### DEEP DIVE

- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565)

## Next

Continue to [Inference mechanics and efficiency](07-inference-mechanics-and-efficiency.md).
