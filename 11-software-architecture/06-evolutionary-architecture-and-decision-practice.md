# Evolutionary Architecture and Decision Practice

Architecture is a continuing decision practice that keeps change safe while evidence and constraints evolve.

## Why it matters

A diagram approved once can drift from runtime truth within a release. An ADR can fossilize a decision long after its assumptions fail. Conversely, a rewrite justified by “clean architecture” can discard working knowledge without improving a measurable outcome. Effective architecture records context, builds reversible paths, and tests important properties continuously.

## How it works

An architecture decision record captures title, status, context, decision, alternatives, consequences, and evidence that would trigger review. It is short enough to remain usable and immutable enough to preserve history; a later ADR supersedes it. The decision should name constraints and quality scenarios rather than claiming universal best practice.

Reversibility shapes investment. A two-way-door decision can use a lightweight experiment. A one-way or expensive decision, such as public data format, tenant isolation model, or irreversible migration, deserves prototypes, failure analysis, and rollback design. Real options favor preserving choices until information becomes valuable, but delay also has cost.

Evolution uses compatible intermediate states. Expand-and-contract first adds a new schema or API that old code can ignore, deploys code able to read both and write according to a controlled policy, backfills with checkpoints and validation, moves reads, then removes old shape only after telemetry proves no users remain. Feature flags separate deployment from release but require ownership, expiry, tested combinations, and safe defaults.

Fitness functions are automated checks for architectural characteristics: forbidden dependency tests, API compatibility, latency budgets, data-ownership linting, recovery exercises, or deployment independence. They detect specified drift; they cannot replace judgment or prove the system has the right boundaries. Runtime maps from traces, service catalogs, and data lineage complement source rules.

Socio-technical architecture recognizes that communication paths, on-call ownership, and repository boundaries influence design. Conway’s Law is a force to manage, not a command to reorganize constantly. A boundary without an accountable owner decays.

## See it yourself

Predict one failed fitness check because the payment module imports a UI package.

```bash
python3 - <<'PY'
rules = {
    "checkout": {"catalog", "payment"},
    "payment": {"ledger"},
    "catalog": set(),
    "ledger": set(),
}
actual = {
    "checkout": {"catalog", "payment"},
    "payment": {"ledger", "ui"},
}
violations = sorted(
    (source, target)
    for source, targets in actual.items()
    for target in targets
    if target not in rules.get(source, set())
)
print(violations)
PY
```

Expected observation: the executable constraint reports `payment` depending on `ui`.

Limits of the observation: a static edge rule cannot judge runtime reliability, data ownership, contract semantics, team structure, or whether the allowed architecture is wise.

## Where it shows up

A team replacing integer order IDs with opaque strings first adds a new column and representation, teaches readers both forms, dual-writes with reconciliation, backfills in resumable batches, migrates consumers using telemetry, and only then removes the old contract. The ADR states privacy and federation goals, operational cost, fallback, and the metric that allows contraction.

## When it breaks

Permanent dual-write paths, stale flags, ADRs with no owner, exceptions accumulating in dependency rules, and diagrams contradicted by traces indicate architectural drift. Migration errors cluster where compatibility assumptions were implicit. First inspect decision context, current dependency and data-flow evidence, exception age, flag inventory, schema usage, deployment coupling, and incidents. Do not launch a rewrite until the failed quality scenario and incremental alternatives are explicit.

## Practice

**Build:** complete the module lab and write one ADR with two credible alternatives, measurable consequences, rollback, owner, and review trigger. **Break:** introduce a forbidden dependency, incompatible event field, partial backfill, and stale feature flag. **Explain back:** show which fitness function catches each problem and which still requires human review. Success includes a reversible rollout, automatic compatibility checks, runtime validation, and a dated deletion plan.

## Check yourself

1. Why should a superseded ADR remain in the repository?
2. What can an architecture fitness function establish, and what can it not?

## Sources

### REQUIRED

- [Thoughtworks Technology Radar: Lightweight Architecture Decision Records](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [Martin Fowler: Evolutionary Architecture](https://martinfowler.com/articles/evodb.html)

### RECOMMENDED

- [AWS Prescriptive Guidance: ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)

### DEEP DIVE

- [Building Evolutionary Architectures](https://www.thoughtworks.com/insights/books/building-evolutionary-architectures)

## Next

Continue to [AWS](../12-aws/README.md).
