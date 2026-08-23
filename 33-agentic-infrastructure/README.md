# 33 — Agentic Infrastructure

Agents repeatedly choose actions from model output. Infrastructure must constrain those choices, preserve evidence, and recover when plans fail.

## What you will learn

- Build bounded agent loops and durable state.
- Secure tools, credentials, and untrusted observations.
- Evaluate trajectories and control operational risk.

## Lessons

1. [Agent loops and durable state](01-agent-loops-and-durable-state.md)
2. [Tool security and isolation](02-tool-security-and-isolation.md)
3. [Evaluation and operations](03-evaluation-and-operations.md)

## Practice

Specify an agent run as a state machine with budgets, idempotency keys, approval points, and a replayable event log.

## Ready to continue

You can bound an agent loop, distinguish model authority from tool authority, and diagnose failures from trajectory evidence.

## Next

Begin [System Design](../34-system-design/README.md).
