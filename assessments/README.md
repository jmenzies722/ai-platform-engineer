# Curriculum Assessment Gates

These gates test whether a learner can Explain, Build, Debug, Operate, and Design with inspectable evidence. They do not award credit for reading, file completion, tool output without interpretation, or multiple-choice recall. The progression extends the evidence rules in [PROGRESS.md](../PROGRESS.md) and the explanation standard in [TEACH-BACK.md](../TEACH-BACK.md).

## Gate sequence

| Gate | Curriculum scope | Primary assessment |
|---|---|---|
| [Foundations](gates/foundations.md) | History through computer systems | Inspect and explain a bounded program, then repair an evidence defect |
| [Systems, Linux, and Networking](gates/systems-linux-networking.md) | Linux through software architecture | Build and diagnose a local service across process, protocol, data, and API boundaries |
| [Cloud Delivery](gates/cloud-delivery.md) | AWS, DevOps, Terraform, and containers | Review and execute a safe, evidence-preserving infrastructure delivery change |
| [Kubernetes Reliability](gates/kubernetes-reliability.md) | Kubernetes through security | Operate a workload through partial failure, mitigation, recovery, and learning |
| [Platform](gates/platform.md) | Platform engineering, developer platforms, and control planes | Design and prove a narrow, tenant-safe self-service control plane |
| [AI Platform](gates/ai-platform.md) | AI foundations through agentic infrastructure | Govern an AI workload from reproducible evidence through bounded operation |
| [Staff](gates/staff.md) | System design and senior/staff engineering | Lead an evidence-driven cross-team decision under changed assumptions |

Gates are cumulative. A later gate may sample earlier skills, but its challenge is calibrated to the new scope. Passing one gate does not automatically raise every domain in [PROGRESS.md](../PROGRESS.md); update only dimensions supported by the reviewed evidence.

## Roles

- **Candidate:** owns the work, states assumptions, protects the environment, and distinguishes observation from interpretation.
- **Evaluator:** selects the hidden fault or changed condition, preserves a consistent challenge envelope, asks review prompts, and scores only inspectable evidence.
- **Facilitator, when separate:** prepares disposable fixtures, keeps solutions hidden, enforces stop conditions, and records any assistance.

The evaluator must not become a pair programmer. Clarifications about scope and safety are allowed and must be recorded. Implementation hints, diagnosis hints, or unexplained access to a solution make the affected dimension unscorable until a fresh variant is attempted.

## Standard assessment flow

1. Verify the gate prerequisites from linked curriculum artifacts and prior evidence.
2. Freeze the challenge envelope: environment, versions, time and resource bounds, allowed interfaces, prohibited actions, and cleanup target.
3. Require a prediction and safety check before mutation.
4. Observe the candidate completing the challenge. The evaluator introduces the gate's hidden fault or changed assumption.
5. Collect the evidence packet before discussing the result.
6. Run the oral review using the gate prompts. Explanations are given without notes first; artifacts may then be opened to test precision.
7. Score with [the common rubric](rubric.md), apply the gate-specific pass rule, and record rework precisely.
8. Verify cleanup and evidence handling. Record the outcome in the review log in [PROGRESS.md](../PROGRESS.md).

## Challenge calibration

The fault lists in each gate define variant classes, not permission to improvise arbitrary difficulty. Before an attempt, the assessment owner prepares a private variant card containing:

- fixture and dependency identities, resource bounds, starting health, and expected cleanup state;
- the single primary fault or changed assumption, any allowed secondary symptom, and the mechanism being sampled;
- evidence available at the start, evidence revealed only after a justified test, and intentionally missing or misleading signals;
- actions that are allowed, prohibited, or require an explicit safety check;
- the minimum observable claims for each dimension and the critical conditions that cannot be compensated;
- assistance rules, accessibility accommodations, and any change that would invalidate or restart the attempt; and
- a reference solution used to check fixture behavior, not to require one implementation or diagnosis path.

Use a clean fixture and one primary variant from the gate's listed classes. Compound faults are reserved for a score of 3 and must not be necessary to earn a 2. Gate owners trial new cards with at least two reviewers, verify that the evidence can discriminate the intended mechanism, and retire cards that leak, depend on accidental tool behavior, or produce materially different difficulty.

Scores support an evidence claim against the gate rubric; they are not a leaderboard. Results from different variants are comparable only at the level of the published capability anchors, not by completion speed or artifact volume. Record the variant identifier and fixture hash without publishing hidden fault details.

## Standard evidence packet

Every submission must be reproducible by an evaluator and contain:

1. an index mapping each claim to a file, command output, test, trace, diagram, or decision record;
2. environment and version information, exact setup and rerun instructions, and immutable input identities or hashes where relevant;
3. the initial prediction, healthy baseline, timeline, and changed observations;
4. source, configuration, tests, and machine-readable output needed to inspect the build;
5. ranked hypotheses, discriminating tests, contradictory evidence, the correction, and recovery proof;
6. operating contract: limits, SLI or success signal, alert or decision threshold, runbook, rollback trigger, and ownership;
7. design record: requirements, invariants, boundaries, alternatives, tradeoffs, failure modes, security and cost considerations, and revisit triggers;
8. safety record: authorization, scope checks, redaction, resource bounds, stop conditions, and cleanup proof;
9. a short limitations statement naming what the evidence does not establish; and
10. assistance and provenance disclosure, including reused prior work, generated material, and evaluator hints.

Raw output alone is not evidence of understanding. Each retained observation must identify the supported claim and at least one plausible claim it does not prove, following the practice in [the labs](../labs/README.md).

## Evidence reuse

Existing lab and project work may establish prerequisites or supply a baseline. The candidate must identify it as prior work and provide its history. Each gate still requires a fresh evaluator-controlled fault, changed assumption, or review. A polished artifact with no reproducible history, no raw evidence, or no ability to explain and modify it is insufficient.

The incident solutions under [incidents](../incidents/README.md) remain closed until hypotheses, falsifying evidence, and a safe mitigation are written. If a candidate has already read a selected solution, the evaluator selects another incident or creates a bounded variant from the gate's listed assets.

## Integrity and safety

- Use only authorized, disposable or explicitly scoped systems. Never use production data, credentials, customer identifiers, or unapproved cloud resources.
- Confirm repository, account, region, cluster context, namespace, process identity, and mutation target before acting.
- Keep load, retries, queues, storage, cost, and duration bounded. Stop when authorization, blast radius, data handling, or cleanup assumptions are invalid.
- Do not disable TLS verification, policy, admission, locking, tests, or other controls merely to obtain a passing output.
- Treat missing, denied, stale, sampled, or incomplete evidence as unknown rather than healthy.
- Redact secrets without erasing identifiers needed for correlation. Preserve hashes, timestamps, versions, and decision history.
- Never fabricate output, edit a result to match a claim, conceal assistance, or present another person's work as fresh evidence.
- Prefer reversible mitigation. State rollback criteria before applying a change, and prove cleanup from the environment rather than asserting it.

A safety breach, fabricated evidence, undisclosed solution access, or unauthorized side effect is an immediate gate stop. The evaluator preserves the record, contains any effect, and schedules a new variant only after the unsafe mechanism is understood.

## Outcomes

- **Pass:** the gate-specific challenge is complete, every required dimension meets its threshold, no critical rubric condition fails, and the packet is independently inspectable.
- **Rework:** the attempt is safe and authentic but one or more named claims lack sufficient evidence. Only the specified dimensions and coupled recovery proof need reassessment.
- **Stop:** integrity, authorization, or safety failed. This is not ordinary rework; containment and a fresh challenge are required.

Scores are not averaged to hide a weak dimension. A strong design cannot compensate for unsafe operation, and a successful demo cannot compensate for an unexplained mechanism.
