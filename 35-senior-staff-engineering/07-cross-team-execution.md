# Cross-team execution

Staff execution turns shared intent into a sequence of owned, testable commitments while keeping integration and risk visible.

## Why it matters

Programs often appear green inside each team while failing at interfaces, migration, adoption, or decisions that nobody owns.

## How it works

Define the outcome and critical path. Decompose work by independently verifiable deliverables and integration points, not departmental activity lists. Map dependencies with provider, consumer, contract, needed date, acceptance evidence, and fallback. Name one directly responsible owner for each decision and deliverable.

Use milestones that demonstrate end-to-end capability in production-like conditions. Keep a decision log, risk register, and commitment ledger. Report confidence and changed evidence rather than optimistic percent complete. Surface scope pressure early and explicitly decide what stops, narrows, or moves.

Sequence high-uncertainty and high-coupling work early. Create compatibility windows and consumer-driven tests. Pilot with real users, fund migration, and measure adoption. The staff engineer closes gaps but resists becoming coordinator, architect, debugger, and approver for every stream.

## See it yourself

Six teams each report 90 percent completion, but no producer has tested against a consumer and identity migration is unowned. An end-to-end milestone fails immediately. The failure is useful because it reveals interface work while there is still time to change scope.

## Where it shows up

Execution mechanisms matter in platform launches, region moves, API deprecations, reliability initiatives, and model-provider migrations.

## When it breaks

Execution breaks through status theater, hidden dependencies, no migration owner, late integration, and heroic central coordination. Replace color reports with evidence, inspect the critical path, and renegotiate commitments where capacity is fictional.

## Practice

**Build:** create an execution plan for migrating six services to a model gateway. Include end-to-end milestones, interface contracts, dependency ledger, decision rights, adoption, and stop conditions. **Break:** delay identity work and lose one consumer team. **Explain back:** revise scope and sequence without hiding objective impact.

## Check yourself

1. Why are end-to-end milestones stronger than percent complete?
2. What belongs in a dependency contract?
3. When does gap-closing become unhealthy centralization?

## Sources

### REQUIRED

- [DORA research](https://dora.dev/research/)

### RECOMMENDED

- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)

### DEEP DIVE

- [Team Topologies resources](https://teamtopologies.com/key-concepts)

## Next

Continue to [Risk and responsible escalation](08-risk-and-responsible-escalation.md).
