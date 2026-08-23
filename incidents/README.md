# Incident Practice

This directory contains evidence-first incident simulations and post-incident analysis. Scenarios should force diagnosis from incomplete symptoms; do not read a solution until you have written and tested hypotheses.

## Scenarios

| Incident | Difficulty | Focus | Status |
|---|---:|---|---|
| [DNS Resolution Failure](01-dns-failure/README.md) | Starter | Resolver path, caching, evidence, recovery | Scaffold ready |

## Method

1. Record the user-visible impact and establish a timeline.
2. Separate observations from interpretations.
3. Rank hypotheses by explanatory power, likelihood, and test cost.
4. Test across boundaries; preserve contradicting evidence.
5. Mitigate impact before optimizing the diagnosis.
6. Prove recovery from the user’s perspective.
7. Read `solution.md`, compare reasoning, and write prevention/detection changes.

Use [templates/INCIDENT.md](../templates/INCIDENT.md) for new scenarios. Never include real credentials, customer data, or sensitive production logs.
