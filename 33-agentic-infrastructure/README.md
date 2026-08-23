# 33 — Agentic Infrastructure

Agents repeatedly choose actions from model output. Infrastructure must constrain those choices, preserve evidence, and recover when plans fail.

## What you will learn

- Build bounded runtimes with durable, replayable state and effects.
- Secure tools with isolation, workload identity, policy, and informed approval.
- Evaluate trajectories and operate agents with observable safety controls.

## Lessons

1. [Agent loops and durable state](01-agent-loops-and-durable-state.md)
2. [Tool security and isolation](02-tool-security-and-isolation.md)
3. [Evaluation and operations](03-evaluation-and-operations.md)
4. [Agent runtime architecture](04-agent-runtime-architecture.md)
5. [Identity, capabilities, and approvals](05-identity-capabilities-and-approvals.md)
6. [Durable execution and effect reconciliation](06-durable-execution-and-reconciliation.md)
7. [Evaluation and trajectory observability](07-evaluation-and-trajectory-observability.md)
8. [Safety controls and fleet operations](08-safety-controls-and-fleet-operations.md)
9. [Practical lab: simulate a durable agent runtime](09-practical-agent-runtime-lab.md)

## Practice

Complete the runtime simulator. Prove bounded termination, effect deduplication, least privilege, crash recovery, trajectory scoring, and emergency stop from its event log.

## Ready to continue

You can bound and recover an agent loop, separate model intent from tool authority, protect identities and effects, evaluate trajectories, and operate a fleet from auditable evidence.

## Next

Begin [System Design](../34-system-design/README.md).
