# Agentic Engineering

Agentic engineering builds bounded software loops that choose actions, use tools, and recover while pursuing a goal.

## Why it matters

**Prerequisite:** [AI Platform Engineering](./19-ai-platform-engineering.md).

Fixed workflows work when every branch can be specified in advance. Tool-using language models support tasks whose next step depends on uncertain intermediate results, external data, and changing state.

An agent runtime coordinates those decisions, tools, memory, and feedback. Nondeterminism, prompt injection, runaway cost, and unsafe side effects make durable state, bounded permissions, approval points, audit, and recovery part of the basic design.

## How it works

An agent is a bounded state machine whose transition proposal may come from a model; deterministic code validates, authorizes, executes, records, and evaluates each transition.

The runtime assembles trusted instructions and scoped context; the model proposes a tool call; schemas validate arguments; policy authorizes identity and resource; execution occurs with time/cost limits; results append to state; termination rules stop the loop.

Prompt text is not an authorization boundary. Retrieved content is untrusted data. Exactly-once effects remain unavailable across arbitrary failures, so operations need idempotency keys, reconciliation, or human confirmation. Evaluation must test trajectories and side effects, not final prose alone.

## Vocabulary

- **Agent:** A bounded loop that observes, proposes actions, uses tools, and updates state toward a goal.
- **Tool call:** A structured request for an external capability.
- **Trajectory:** The sequence of states, decisions, actions, and observations in a run.
- **Capability:** A specifically authorized operation on a defined resource scope.
- **Guardrail:** A control intended to detect, constrain, or block unsafe behavior.
- **Prompt injection:** Untrusted content attempting to alter model instructions or tool behavior.
- **Confused deputy:** A component tricked into misusing its authority for another party.
- **Sandbox:** An isolated environment that constrains code or tool execution.
- **Durable execution:** Persisted workflow progress that can resume after interruption.
- **Idempotency:** Safe repetition of an operation without duplicate intended effects.
- **Approval:** An explicit authorization checkpoint before a sensitive action.
- **Provenance:** Evidence of where data, instructions, decisions, or artifacts originated.

## See it yourself

```python
while budget.remaining() and not state.done:
    proposal = model.propose(state.redacted_view())
    call = schema.validate(proposal)
    policy.authorize(actor, call.capability, call.resource)
    result = tools.execute(call, idempotency_key=state.step_id)
    state.append(call, result)
```

Predict the persisted state if the tool succeeds but the caller times out before `state.append`. A naive retry may repeat the effect; an idempotency record should return the prior outcome. This supports keeping authorization, durable state, budgets, and side-effect control outside the model. The sketch does not prove safe execution, because schemas, policy, storage, and tool behavior are only assumed.

## Where it shows up

A deployment agent may read CI results and propose a rollback, but production mutation should use a narrow workload identity, a typed tool, an idempotency key, a change record, and an approval threshold. The model chooses among allowed proposals; deterministic policy decides authority. Durable state records what happened so a restart can resume without guessing or repeating a side effect.

## When it breaks

An agent may repeat a deployment, leak a secret, or continue after its budget should stop it. Prompt injection, excessive authority, ambiguous tool schemas, lost durable state, or missing idempotency can each cause such effects. First inspect the immutable trajectory: instruction provenance, identity, policy decision, arguments, tool result, persisted state, and external audit record.

## Practice

### Observe

Design a read-only incident agent with three typed tools. Threat-model untrusted logs, define budgets and stop conditions, and record an auditable trace.

### Build

Implement a deterministic agent loop simulator with schema validation, capability checks, idempotency, approval, timeout, and trajectory evaluation.

### Break

Inject malicious retrieved text, duplicate a tool response, withhold a result, and request a forbidden action. Verify bounded, explainable failure.

### Say it out loud

Explain why an agent is an execution system, not merely an LLM response.

**Success:** Include authority, typed tools, durable state, idempotency, limits, approval, and trajectory evidence.

## Check yourself

1. Why is a prompt not authorization?
2. What makes an agent loop durably resumable?
3. Why evaluate trajectories?

### Interview stretch

- Design least-privilege tool access.
- Prevent duplicate side effects after timeout.
- Operate an agent with measurable reliability.

## Sources

### REQUIRED

- “Artificial Intelligence Risk Management Framework (AI RMF 1.0)” — NIST. [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1). Provides a governance framework for trustworthy AI systems.

### RECOMMENDED

- “ReAct: Synergizing Reasoning and Acting in Language Models” — Yao et al. [arXiv](https://arxiv.org/abs/2210.03629). Establishes an influential observation/action trajectory pattern.

### DEEP DIVE

- “Toolformer” — Schick et al. [arXiv](https://arxiv.org/abs/2302.04761). Studies learned tool-use decisions and their limitations.

## Next

Continue with [../01-software-foundations/01-how-software-actually-executes.md](../01-software-foundations/01-how-software-actually-executes.md).
