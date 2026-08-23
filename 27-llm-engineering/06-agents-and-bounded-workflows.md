# Agents and bounded workflows

An agent is a control loop that chooses actions from observations; reliability comes from bounded state and externally enforced policy, not from asking it to be careful.

## Why it matters

[Tool contracts and secure execution](05-tool-contracts-and-secure-execution.md) secures one action. Multi-step tasks add loops, stale plans, compounding errors, budget exhaustion, and ambiguous recovery.

## How it works

The loop receives a goal and current state, proposes a next action, executes through a policy boundary, records the observation, and stops on success, failure, or budget. A workflow fixes transitions in code; an agent chooses among allowed transitions. Prefer deterministic workflow for known business processes and reserve model choice for ambiguous steps.

State includes task ID, messages, tool results, approvals, artifact versions, remaining token, time and action budgets, and terminal status. Checkpoint after durable transitions. Each step is idempotent or compensatable. A planner can propose steps, but execution revalidates current facts and permissions.

Memory is retrieval over stored records, not magic continuity. It needs scope, provenance, retention, privacy, and conflict rules. Summaries are lossy and must not replace authoritative transaction state.

## See it yourself

Define states `draft`, `approved`, `executed`, and `failed`. Permit execution only from `approved` and record an action digest. A repeated execute event returns the existing result. An approval for a changed digest is invalid.

This tiny state machine excludes several unsafe paths by construction; a prompt describing the same policy does not.

## Where it shows up

An incident agent gathers read-only evidence, proposes a remediation, waits for an authorized operator, and invokes one scoped action. A hard deadline, action count, and service allow-list contain loops and blast radius.

## When it breaks

Agents loop on unchanged observations, treat tool errors as success, overwrite state, act on stale approvals, or let retrieved text redefine goals. Multiple workers execute one step concurrently.

Inspect the event log as a state machine: prior state, proposal, policy decision, effect ID, observation, next state, and remaining budget. Use leases or compare-and-swap for ownership, and a dead-letter terminal path for repeated failure.

## Practice

**Observe:** turn a free-form task into states and invariants. **Build:** implement a three-state agent simulator with budgets and replay-safe actions. **Break:** deliver one event twice and prove one effect.

## Check yourself

1. When is a workflow preferable to an agent?
2. Why must execution revalidate a plan?
3. What makes memory a security boundary?
4. How does an event log diagnose loops?

## Sources

### REQUIRED

- [Google SRE: Distributed Periodic Scheduling with Cron](https://sre.google/sre-book/distributed-periodic-scheduling/)

### RECOMMENDED

- [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### DEEP DIVE

- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)

## Next

Continue to [LLM application evaluations](07-llm-application-evaluations.md).
