# How to Learn

Use each lesson to make a claim testable. Reading alone creates recognition; the aim is a model you can use when the system behaves differently from your expectation.

## Start with the question

Before learning a product or term, identify the problem it solves. Ask what work was difficult, unsafe, expensive, or unreliable without it. Then define the abstraction by its contract, not by its marketing.

## Follow the mechanism

Trace inputs, state, decisions, side effects, and outputs. Name the boundary at which each claim is true. Study an internal detail only when it explains correctness, performance, security, cost, or failure.

A useful explanation answers:

- What state exists before the operation?
- Which component is allowed to change it?
- What evidence shows that the change occurred?
- Which assumptions remain hidden?

## Predict before running

Write the expected observation before each command or program. Run the smallest safe experiment that can distinguish your hypothesis from a plausible alternative. Keep exact output and errors.

An observation supports a bounded claim. A successful HTTP response does not prove every replica is healthy; an existing process does not prove that it is making progress. State the limit.

## Build and break

Build a reduced version from a blank file. Keep it small enough to explain every meaningful line. Then violate one assumption at a time and compare the symptom with your prediction.

Learning faults must be bounded. Do not use uncontrolled allocation, process creation, spending, production data, or destructive targets. Prefer disposable local environments and explicit limits.

## Debug from evidence

Describe the symptom precisely, including scope and time. Find the last boundary known to be working. Form a hypothesis that a small observation can disprove. Change one variable, compare the result, and preserve the evidence.

Do not start with a favorite cause. “The network,” “Kubernetes,” and “the model” are areas of inquiry, not diagnoses.

## Practice operation

For systems you may own, define user-visible health, capacity limits, telemetry, recovery, rollback, access control, and cost. A runbook should let another engineer detect a known failure and recover safely.

## Practice design

State users, workload, quality requirements, failure assumptions, and non-goals before choosing technology. Compare alternatives against those constraints. A sound decision can explain what would make another choice better.

## End a session

For a focused session:

1. Read the opening, **Why it matters**, and **How it works**.
2. Close the file and write the mechanism from memory.
3. Complete **See it yourself** after recording a prediction.
4. Choose one task from **Practice**.
5. Answer **Check yourself** without copying lesson phrases.
6. Record evidence and the weakest remaining point in [PROGRESS.md](PROGRESS.md).

Use [TEACH-BACK.md](TEACH-BACK.md) to test whether your explanation is concise and causal.

## Use AI deliberately

Write your prediction and plan before asking for help. AI may propose questions, counterexamples, code, or review, but you remain responsible for commands, sources, safety, and conclusions.

Some exercises ask you to work without assistance. For those attempts, use the lesson, primary documentation, local tools, and your own notes. Preserve your first answer. Review it afterward so the change in your model remains visible.

## Choose depth

A first pass should establish the mechanism, one observation, one failure mode, and a correct explanation. Go deeper when the subject underpins your work, recurs in incidents, controls a major cost or security boundary, or informs a design you own.

Advance when the evidence relevant to the next task exists. Return when practice exposes a gap.
