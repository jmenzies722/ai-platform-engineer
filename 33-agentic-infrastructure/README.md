# 33 — Agentic Infrastructure

Agents repeatedly choose actions from model output. Infrastructure must constrain those choices, preserve evidence, and recover when plans fail.

## What you will learn

- Build bounded runtimes with durable, replayable state and effects.
- Secure tools with isolation, workload identity, policy, and informed approval.
- Evaluate outcomes, trajectories, and exercised authority with reproducible evidence.
- Operate approval, escalation, containment, and fleet recovery with measurable bounds.

## Lessons

1. [Agent loops and durable state](01-agent-loops-and-durable-state.md)
2. [Tool security and isolation](02-tool-security-and-isolation.md)
3. [Evaluation and trajectory evidence](03-evaluation-and-operations.md)
4. [Agent runtime architecture](04-agent-runtime-architecture.md)
5. [Identity, capabilities, and approvals](05-identity-capabilities-and-approvals.md)
6. [Leases, fencing, and effect reconciliation](06-durable-execution-and-reconciliation.md)
7. [Human approval, escalation, and kill-switch operation](07-evaluation-and-trajectory-observability.md)
8. [Fleet reliability and recovery](08-safety-controls-and-fleet-operations.md)
9. [Practical lab: simulate a durable agent runtime](09-practical-agent-runtime-lab.md)

## Practice

Complete the runtime simulator and standalone [Lab 19: Bound an Agent Runtime](../labs/19-agent-runtime-safety/README.md). Prove bounded termination, least privilege, exact approval binding, fenced ownership, effect reconciliation, trajectory gates, and acknowledged emergency stop. Exercise backlog recovery with the [queue-overload drill](../incidents/12-queue-overload/README.md), then carry the evidence into the [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md).

## Ready to continue

You can bound and recover an agent loop, separate model intent from tool authority, fence ownership, reconcile or compensate effects, evaluate trajectories, operate human control points, and recover a fleet from auditable evidence.

## Next

Begin [System Design](../34-system-design/README.md).
