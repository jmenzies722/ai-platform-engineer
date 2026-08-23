# Assessment Rubric

Use this rubric with every [assessment gate](README.md). Score the five capability dimensions from 0 to 3 using the candidate's evidence packet, observed work, and oral review. Also evaluate the non-compensable integrity and safety conditions.

## Scoring scale

| Score | Meaning |
|---:|---|
| 0 | No usable evidence, incorrect mechanism, unsafe action, or work cannot be attributed to the candidate |
| 1 | Guided or partial performance; claims are plausible but important evidence, boundaries, or recovery are missing |
| 2 | Independent, correct performance for the gate's stated scope; evidence is reproducible and limitations are explicit |
| 3 | Handles a novel variant, reconciles contradictory evidence, quantifies tradeoffs, and improves the surrounding method |

A score describes the demonstrated gate attempt, not general seniority or potential.

## Dimension anchors

### Explain

| Score | Observable standard |
|---:|---|
| 0 | Repeats labels, gives a materially false account, or cannot connect evidence to behavior |
| 1 | Names components and a likely sequence but omits state ownership, boundaries, failure evidence, or limits |
| 2 | Leads with the consequential claim; gives a causal, ordered, bounded mechanism; names state owners, contracts, a failure symptom, first evidence, and limitations |
| 3 | Adapts the model to a changed condition, predicts a novel observation, resolves conflicting signals, and teaches the mechanism without losing precision |

For a 2 or 3, the explanation must also meet the usable range in [TEACH-BACK.md](../TEACH-BACK.md), with no zero in mechanism or precision.

### Build

| Score | Observable standard |
|---:|---|
| 0 | No working artifact, copied artifact cannot be changed, or behavior depends on uncontrolled manual steps |
| 1 | Happy path works with guidance, but contracts, tests, reproducibility, bounds, or failure behavior are incomplete |
| 2 | Produces the scoped artifact from documented inputs; tests important invariants and negative paths; versions interfaces; keeps authority and resources bounded |
| 3 | Independently adapts the artifact to a novel requirement, validates compatibility and performance, and makes another evaluator's reproduction straightforward |

### Debug

| Score | Observable standard |
|---:|---|
| 0 | Guesses, applies broad restarts or changes before preserving evidence, or cannot separate relevant failure layers |
| 1 | Finds the fault after hints or through undirected trial and error; hypotheses and falsification are incomplete |
| 2 | Starts from impact, preserves a baseline, ranks plausible hypotheses, runs discriminating tests, accounts for contradictions, identifies the causal mechanism, and proves the correction |
| 3 | Diagnoses an unfamiliar or compound fault, detects misleading or missing telemetry, improves the diagnostic method, and states what would disprove the conclusion |

Matching the facilitator's root cause is not itself a pass. Sound reasoning with justified uncertainty can pass; an unsupported lucky guess cannot.

### Operate

| Score | Observable standard |
|---:|---|
| 0 | Exceeds authority or bounds, cannot recover, loses accepted state, or leaves resources running |
| 1 | Runs the happy path but depends on supervision for context checks, mitigation, rollback, observability, or cleanup |
| 2 | Verifies scope, monitors user and subsystem signals, applies the smallest reversible mitigation, follows declared stop and rollback triggers, proves sustained recovery, and completes cleanup |
| 3 | Coordinates a novel or compound event, makes explicit risk and cost decisions under pressure, detects control-plane or telemetry blindness, and leaves a tested runbook or control improvement |

### Design

| Score | Observable standard |
|---:|---|
| 0 | Begins with products or diagrams without requirements; ignores a critical correctness, security, reliability, or ownership constraint |
| 1 | Provides a coherent happy-path design but assumptions, capacity, alternatives, failure modes, evolution, or evidence plans are weak |
| 2 | Traces components to measured requirements and invariants; quantifies key limits; defines boundaries, ownership, security, operability, cost, migration, alternatives, and revisit triggers |
| 3 | Revises the design under changed assumptions, exposes uncertainty and dissent, compares credible options with sensitivity analysis, and defines staged evidence gates and an exit path |

## Evidence quality

The evaluator checks every dimension against these questions:

- Can a claim be traced to raw, timestamped, versioned evidence?
- Can another person reproduce the result from the packet?
- Does the candidate distinguish observation, interpretation, and decision?
- Are contradictory, denied, stale, or missing signals retained and handled honestly?
- Are claims bounded to what the environment and test actually establish?
- Does source history or a live modification demonstrate authorship and understanding?

If evidence quality is weak for one claim, score the affected dimension rather than subtracting a generic presentation point.

## Integrity and safety conditions

All conditions are required:

- scope, identity, authorization, and target were verified before mutation;
- data, secrets, logs, and captured traffic were synthetic, approved, or appropriately redacted;
- duration, load, retries, queues, cost, and side effects remained within the declared envelope;
- dangerous bypasses and destructive shortcuts were not used;
- assistance, reused work, source provenance, and prior solution access were disclosed;
- evidence was not fabricated, selectively altered, or stripped of relevant contradictions; and
- cleanup, rollback, and residual effects were inspected.

Any material failure is a **Stop**, not a low score. A minor, contained process omission with no unsafe effect may be **Rework** only when the gate file explicitly permits it.

## Evaluator procedure

1. Review prerequisites and choose a fresh variant. Record the selected fault or changed condition privately.
2. Inspect the candidate's safety plan before allowing execution.
3. Observe enough live work to verify authorship, command targeting, hypothesis formation, and response to unexpected output.
4. Require one live modification or rerun from a clean state.
5. Ask the gate's review prompts in an order that prevents a memorized walkthrough.
6. Score each dimension independently and cite packet evidence for every score.
7. Check the gate-specific thresholds and critical requirements.
8. Issue a written outcome containing scores, passed claims, gaps, rework scope, and any evidence-retention or cleanup action.

Do not award points for volume, visual polish, tool choice, or agreement with the evaluator's preferred architecture.

## Pass and rework

Unless a gate raises the threshold:

- each of Explain, Build, Debug, Operate, and Design must score at least 2;
- all gate-specific critical requirements must pass;
- integrity and safety conditions must pass; and
- the evidence packet must be independently inspectable.

The gate result is not the arithmetic sum. Record a vector such as `Explain 2, Build 2, Debug 3, Operate 2, Design 2`.

For **Rework**, name the failed claim and smallest fresh proof that can close it. Rework must include a new observation or variant, not just edited prose. Reassess coupled dimensions when the change invalidates prior evidence, such as a design change that alters operation or a fix that changes the failure mode.

For **Stop**, require containment and mechanism review before any new attempt. Never reuse the compromised challenge variant.

## Assessment record

```text
Gate:
Date and evaluator:
Environment and challenge variant:
Evidence packet location and identity:
Assistance and prior-work disclosure:

Explain:
Build:
Debug:
Operate:
Design:

Critical requirements:
Integrity and safety:
Outcome:
Claims demonstrated:
Rework or next proof:
Cleanup and retention verification:
```
