# Contributing and Studying Through GitHub

This repository applies the evidence and review discipline that it teaches. Contributions may correct facts, deepen explanations, add bounded practice, improve assessment, or change curriculum structure. File volume and plausible prose are not useful outcomes. Read the [quality standard](QUALITY.md) before proposing work.

The curriculum systems are discoverable through [role tracks](tracks/README.md), [assessment gates](assessments/README.md), [certification overlays](certs/README.md), and [case studies](case-studies/README.md). These systems compose and assess the numbered curriculum; they do not replace its canonical lessons or lower its evidence standard.

## 1. Select or open an issue

Search open and closed issues first. Use the lesson, lab, project, research, or curriculum-system issue form. A valid issue is a review contract, not a topic label. It must state:

- the learner or engineering problem and who experiences it;
- the affected canonical files and the intended artifact type;
- what is in scope, what is not, and any version boundary;
- the current behavior or claim, with reproducible evidence when reporting a defect;
- primary or authoritative sources already found, plus unresolved uncertainty;
- observable acceptance criteria and the required reviewer expertise;
- safety, data, privilege, cost, and cleanup constraints;
- expected changes to navigation, prerequisites, assessments, and maintenance ownership.

Urgent factual or safety corrections may begin with a narrow issue, but they still require evidence, impact, affected versions, and a safe replacement model. Do not copy copyrighted course material, exam questions, private documentation, customer data, or another contributor's work into an issue.

For personal study, the issue may be private to a fork, but it should still name the mechanism to explain, artifact to build, controlled fault, evidence to retain, stop condition, and no-notes teach-back.

## 2. Create one focused branch

Branch from the current default branch after updating it. Use a short lowercase name such as:

```text
lesson/dns-resolution-evidence
lab/kubernetes-scheduling-fault
assessment/cloud-delivery-state-recovery
curriculum/backend-track-gates
fix/terraform-version-boundary
```

Keep one issue and one coherent review concern per branch. Separate unrelated corrections even when they are small. Do not rewrite shared history. Never commit credentials, tokens, private keys, production data, proprietary logs, generated secrets, or unredacted identifiers. If an artifact cannot be safely published, retain only an approved redacted summary and describe the evidence limitation.

## 3. Establish the evidence plan

Before changing prose or running a command:

1. Write the current mental model and the consequential claim.
2. Record assumptions, environment, versions, authority, resource bounds, and stop conditions.
3. Predict healthy behavior and at least one failure signature.
4. Select primary sources and explain what each source establishes.
5. Define the smallest build, fault, or comparison that can test the claim.
6. Decide what raw evidence to retain and what must be redacted.
7. Define recovery, cleanup, and the criterion that would disprove the proposed explanation.

Use the relevant files in [`templates/`](templates/). Preserve meaningful commands, configuration, versions, timestamps, output, and decision history. Trim noise only after retaining the raw source elsewhere when appropriate. Never fabricate output, silently repair results, invent interviews, imply external validation that did not occur, or present generated material as a primary source.

## 4. Make the change

Keep canonical teaching in the numbered lesson or existing practice artifact. Tracks select and sequence existing work. Assessments test it. Certification overlays map official blueprints without becoming parallel courses. Case studies apply it under staged evidence. Avoid duplicating explanations across these systems.

Write causal prose that distinguishes observation, interpretation, and decision. State uncertainty and product-specific behavior. Use repository-relative links for repository content and canonical external links for external claims. Mermaid is the diagram format. Use ordinary prose, lists, tables, and Mermaid edges instead of Unicode arrow glyphs or arrow-chain pedagogy.

Commands must identify their target, prerequisites, expected output, failure behavior, and cleanup. Destructive, privileged, cloud, load, security, packet-capture, and model-tool exercises require an authorized disposable scope, bounded cost and duration, explicit stop conditions, and verification that residual effects are gone.

## 5. Validate before review

Run the repository checks from the root:

```text
python3 .github/scripts/check_curriculum.py
python .github/scripts/render_mermaid.py
```

Also perform the validation appropriate to the change:

- reproduce commands and scripts in the stated clean environment;
- execute positive, negative, boundary, failure, recovery, and cleanup checks;
- inspect every changed local link and heading fragment;
- open each cited external source and confirm that it supports the nearby claim;
- render every changed Mermaid diagram and inspect labels and reading order;
- verify source dates, versions, quotations, attribution, licenses, and synthetic-data labels;
- test navigation from a root document and from the affected module or system index;
- read the diff without generated assistance and explain the mechanism, evidence, limits, and tradeoffs from memory.

Record skipped checks and why. A passing structural check does not prove factual accuracy, safe execution, or useful pedagogy.

## 6. Open the pull request

Link the issue and make the pull request description an evidence index. Include:

- problem, learner outcome, scope, and non-goals;
- changed files and any canonical-source or navigation decision;
- claim-to-source mapping, including source authority and version dates;
- build, controlled-failure, diagnosis, recovery, and cleanup evidence;
- exact validation commands and summarized results;
- safety, privacy, cost, accessibility, compatibility, and maintenance effects;
- known limitations, unresolved questions, and evidence not collected;
- recommended review order and named review specialties.

Keep the diff reviewable. Do not mix generated formatting churn with substantive changes. Preserve commits that explain a useful investigation, but remove secrets and unsafe artifacts from history before publishing. A pull request must not claim that CI validates external URLs, technical truth, or operational competence.

## 7. Review with explicit ownership

Every contribution needs a content owner who accepts maintenance responsibility and a reviewer other than the author. Use the ownership rules in [QUALITY.md](QUALITY.md). High-risk claims also need the relevant specialist: security for trust and authority, operators for destructive or cloud procedures, subject-matter reviewers for technical mechanisms, and assessment reviewers for gate validity.

Reviewers must:

- trace important claims to sources and retained evidence;
- reproduce a representative command, calculation, link path, or assessment step;
- challenge the causal model with a counterexample or failure condition;
- verify scope, version boundaries, safety, cost, cleanup, and learner prerequisites;
- check that diagrams agree with prose and do not replace explanation;
- reject duplicated canonical content, invented evidence, unsupported certainty, and completion criteria based only on file presence;
- leave a clear approval, requested change, or documented unresolved risk.

AI may help locate gaps or draft language. A human author remains accountable for every claim, command, source, and side effect. Generated review is not independent approval.

## 8. Merge and close the loop

Before merge, resolve review threads, rerun checks on the final revision, and ensure the issue acceptance criteria are mapped to evidence. Merge only when the required owner and specialist reviews are complete. Follow-up work must have an owner and issue; do not hide required correctness or safety work in an unowned note.

After merge:

1. Verify root and system-index navigation on the merged revision.
2. Re-run any deployment-neutral smoke check needed to detect merge damage.
3. Close or update the issue with the merged evidence and known limitations.
4. Record a review or expiry date for volatile product, exam, security, pricing, or version claims.
5. Observe learner feedback, broken links, upstream changes, and assessment leakage.
6. Open a correction when evidence changes; preserve the history of why the old claim was replaced.

For study contributions, complete the no-AI challenge after merge. Update [PROGRESS.md](PROGRESS.md) only when independent evidence supports a new competency level. Authorship, review approval, file completion, and an exam result do not by themselves prove Build, Debug, Operate, or Design competence.

## Source integrity and corrections

Prefer standards, official documentation, maintainer design documents, source code, primary papers, and direct measurements. Secondary sources may orient the reader but must not carry a disputed mechanism when a primary source exists. Attribute quotations and adapted diagrams, paraphrase responsibly, and state when a case, transcript, or measurement is synthetic.

When correcting a factual or unsafe statement, preserve the learning objective while replacing the inaccurate model. Cite the evidence, name affected versions and impact, update linked assessments or diagrams when their premise changed, and add a maintenance trigger if recurrence is plausible.
