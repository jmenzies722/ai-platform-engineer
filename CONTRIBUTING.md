# Contributing and Studying Through GitHub

This repository uses the same evidence and review discipline it teaches. Contributions may be technical corrections, deeper explanations, labs, references, incident scenarios, or curriculum decisions. Shallow lesson generation is not useful.

## Work through a focused change

### 1. Open or Select an Issue

Use the lesson, lab, project, or research issue form. Define the learner problem, authoritative evidence, scope, and observable acceptance criteria. Search existing issues first.

For a personal study cycle, the issue can state:

- concept to explain;
- artifact to build;
- controlled failure to induce;
- evidence to capture;
- explain-back or interview check.

### 2. Create a Focused Branch

Use a descriptive branch such as:

```text
study/linux-process-model
lesson/networking-dns-resolution
lab/kubernetes-scheduling-failure
```

Keep unrelated study notes and corrections separate. Never commit credentials, private production data, or unredacted sensitive logs.

### 3. Work From a Prediction

Before running a lab or editing a technical explanation:

1. write the current mental model;
2. predict behavior and failure signatures;
3. consult primary sources;
4. build or reproduce;
5. break one assumption;
6. debug from evidence;
7. update the explanation with what changed.

Use the templates in [`templates/`](templates/) and preserve meaningful command output, versions, and diagrams. Trim noise; do not fabricate results.

### 4. Validate Locally

At minimum:

- verify relative links and headings;
- render Mermaid diagrams or inspect their syntax;
- run lab scripts in their stated environment;
- run Markdown and repository checks when available;
- verify each external reference resolves to the claimed authoritative source;
- read the change without AI and explain it back.

### 5. Open a Pull Request

Describe:

- learner or engineering problem;
- files and behavior changed;
- sources and why they are authoritative;
- build/break/debug evidence;
- limitations, version boundaries, safety, and cost;
- exact starting point for reviewers.

Link the issue. Keep the pull request reviewable and preserve its commit history where it explains the investigation.

### 6. Review as an Engineer and Educator

Review for:

- factual and causal correctness;
- distinction between abstraction and implementation;
- a clear explanation of purpose, mechanism, evidence, failure, and tradeoffs;
- commands that are safe, reproducible, and explained;
- real canonical references;
- useful failure models and observable completion criteria;
- accessibility of the mental model without dilution.

AI review can identify gaps, but a human contributor remains accountable for every claim and command.

### 7. Close the Loop

After merge, complete the no-AI challenge and update [PROGRESS.md](PROGRESS.md) only when the evidence supports a new competency level. A merged documentation change does not itself prove operational competency.

## Content Standards

- Use a serious engineering voice and define assumptions.
- Prefer standards, official documentation, maintainer design documents, and primary papers.
- Avoid SEO-style filler, unexplained command sequences, and false certainty.
- Do not create future lesson files merely to make the tree look complete.
- Mark product/version-specific behavior and distinguish it from durable principles.
- Attribute quotations and diagrams; paraphrase responsibly.
- Use repository-relative links for repository content.

## Lesson Contract

Every complete lesson follows [`templates/LESSON.md`](templates/LESSON.md). Module READMEs introduce the subject, link the lessons and practice, state what readiness looks like, and point to the next module.

## Lab Safety

Use disposable local environments for destructive experiments. Cloud labs must identify potential charges, permissions, cleanup, and a stop condition. Never ask learners to weaken shared infrastructure or security controls for convenience.

## Corrections

For a factual or unsafe error, open a focused issue and cite evidence. State affected versions and impact. A correction should preserve the learning objective while removing the inaccurate model.
