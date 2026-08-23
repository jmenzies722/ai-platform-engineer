# Scope, judgment, and decisions

Senior judgment turns ambiguity into a decision whose assumptions, consequences, and evidence are visible to others.

## Why it matters

The largest technical risks often live between teams, across time horizons, or outside any ticket's stated scope.

## How it works

Frame the outcome, stakeholders, constraints, invariants, and uncertainties. Separate reversible from irreversible choices. Generate credible alternatives, identify decision criteria, and record why one path was chosen. Use small experiments for uncertain facts and escalation for value or authority conflicts.

Good scope includes what will not be solved and where ownership ends. Facts, forecasts, preferences, and constraints should not be blended: each needs different challenge. Reversible decisions can use bounded trials; choices that lock data, public contracts, or organizational dependency deserve stronger evidence. A decision record preserves context and revisit conditions, not an illusion of permanence.

## See it yourself

Rewrite “we need a vector database” as: retrieve from 500,000 documents, p95 under 200 ms, hourly updates, tenant filtering, two operators, and measured relevance target. Compare database extension, managed service, and lexical baseline on 100 queries. If lexical meets the target, the original solution statement was premature. The experiment turns preference into evidence.

## Where it shows up

For a cross-team storage choice, a staff engineer identifies who owns data correctness, migration, and on-call before selecting technology. They make cost and lock-in explicit, run the smallest discriminating test, and record the executive or risk-owner decision when values conflict. The artifact lets later teams revisit assumptions without relitigating history.

## When it breaks

Premature certainty suppresses evidence, endless analysis avoids ownership, and decisions remain implicit. When work stalls, first inspect the decision statement, named owner, criteria, unknowns, and deadline or trigger. Missing evidence calls for an experiment; conflicting values call for the accountable owner; repeated reopening calls for checking whether revisit conditions actually occurred.

## Practice

**Build:** write a one-page decision with alternatives, criteria, owner, disconfirming evidence, and revisit trigger. **Break:** remove a key assumption and introduce a stakeholder constraint; show how the decision process responds. **Explain back:** distinguish fact uncertainty from value conflict and name when escalation is responsible.

## Check yourself

1. Which choices deserve more rigor?
2. What makes a decision reversible?
3. When should you escalate?

## Sources

### REQUIRED

- [Architecture Decision Records](https://adr.github.io/)

### RECOMMENDED

- [Google SRE: managing incidents](https://sre.google/workbook/incident-response/)

### DEEP DIVE

- [NIST systems security engineering](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)

## Next

Continue to [Influence and technical leadership](02-influence-and-technical-leadership.md).
