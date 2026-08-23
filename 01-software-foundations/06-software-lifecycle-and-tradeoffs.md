# Software Lifecycle and Engineering Tradeoffs

Software engineering is the disciplined management of change: turning an uncertain need into a small, reviewable, testable, operable, and replaceable system.

## Why it matters

A technically elegant rewrite can increase delivery risk if it changes storage, interfaces, deployment, and operations at once. Conversely, repeatedly patching a fragile component can make every future change expensive. The responsible decision compares alternatives against constraints and reversible evidence rather than treating novelty or familiarity as proof.

## How it works

Work begins by clarifying the user outcome, system boundary, constraints, and unacceptable failures. Requirements include functional behavior and quality attributes such as latency, security, availability, accessibility, and maintainability. A design records important decisions, alternatives, and consequences. Decomposition creates components with cohesive responsibilities and narrow interfaces; it does not guarantee simplicity if ownership remains tangled.

Implementation should proceed in reviewable increments with automated checks near the changed contract. Unit tests isolate rules, integration tests exercise boundaries, and end-to-end tests sample complete paths; none replaces production observation. Delivery adds versioning, migration, rollout, rollback or forward-fix plans, and ownership. Small canaries and feature controls reduce blast radius but add states that must be removed later. Maintenance includes dependency updates, incident learning, documentation, and deleting obsolete code. Tradeoffs should name the metric or risk being exchanged. Technical debt is not merely old code; it is a deliberate or accidental choice that makes future change costlier and should have an owner and trigger for repayment.

## See it yourself

**Tiny Proof:** write two candidate designs as data and make the selection rule explicit. Predict that changing a constraint can change the responsible choice without making either design universally best.

```bash
python3 - <<'PY2'
options = {
    "in_process": {"latency": 1, "isolation": 1, "operations": 1},
    "service": {"latency": 3, "isolation": 3, "operations": 3},
}
weights = {"latency": -2, "isolation": 3, "operations": -1}
for name, qualities in options.items():
    score = sum(weights[key] * value for key, value in qualities.items())
    print(name, score)
PY2
```

Expected observation: the visible weights determine the ranking, making disagreement inspectable instead of hiding it behind “best practice.”

Limits of this proof: real qualities are not clean ordinal numbers, weights involve stakeholders, and a score does not remove uncertainty. A decision record must include evidence, assumptions, and consequences, not only arithmetic.

## Where it shows up

Replacing a synchronous library call with a remote service buys deployment and failure isolation while adding network latency, authentication, version skew, retries, and operational ownership. A staged extraction can first establish an internal interface, measure call patterns, run both paths for comparison, and migrate one caller. That sequence creates stopping points where evidence can invalidate the plan before the highest-cost step.

## When it breaks

Requirements churn may indicate an unclear outcome; changes touching every component suggest weak boundaries; tests passing while releases fail suggest an untested deployment contract; permanent feature flags and dual writes suggest unfinished migration. First reconstruct the decision and compare its assumptions with current evidence. Prefer the smallest reversible experiment that discriminates between alternatives. Do not invoke “technical debt” as a license for an unbounded rewrite.

## Practice

**Build:** choose a small program from this module and write a one-page change proposal containing outcome, non-goals, constraints, interface, failure modes, tests, rollout, and removal plan. **Break:** inject one false assumption and identify which measurement would expose it before full rollout. **Explain back:** distinguish requirement, design, implementation, verification, deployment, and operation. Success means a reviewer can reject or approve the change based on explicit evidence and every temporary mechanism has a deletion condition.

## Check yourself

1. Why is reversibility valuable when requirements are uncertain?
2. How do unit, integration, and end-to-end tests provide different evidence?

## Sources

### REQUIRED

- [SWEBOK Guide](https://www.computer.org/education/bodies-of-knowledge/software-engineering)

### RECOMMENDED

- [Architecture Decision Records](https://adr.github.io/)

### DEEP DIVE

- [Software Engineering at Google](https://abseil.io/resources/swe-book)

## Next

Continue to [Python](../02-python/README.md).
