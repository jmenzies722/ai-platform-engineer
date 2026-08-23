# Agent runtime architecture

An agent runtime is a bounded state machine around an untrusted planner, not an unconstrained loop around a language model.

## Why it matters

Model outputs are probabilistic and observations may be hostile. Deterministic infrastructure must own authority, budgets, transitions, and termination.

## How it works

The runtime assembles versioned context, asks the model for a typed proposal, validates syntax and state preconditions, authorizes through policy, executes a narrow tool, records the observation, and chooses the next state. The model proposes; the runtime decides. Limits cover steps, wall time, tokens, cost, retries, and repeated no-progress patterns.

Runs have explicit terminal states such as succeeded, failed, cancelled, budget-exhausted, and needs-reconciliation. Context is a projection of durable events; summaries are versioned and treated as potentially lossy. Concurrency ownership prevents two workers from advancing one run simultaneously.

## See it yourself

Set a ten-step budget and feed an agent the same failing proposal repeatedly. The runtime terminates after the bound even if the model requests continuation. Add a no-progress detector keyed by normalized action and error to stop earlier. This proves termination comes from runtime policy, not model cooperation.

## Where it shows up

Coding, support, and operations agents share the same skeleton but receive different capabilities, identity, isolation, approvals, and budgets. Run traces identify model, prompt, policy, tool, and state versions.

## When it breaks

Free-form parsing executes unintended arguments, duplicate workers race, context truncation drops constraints, and cancellation does not reach active tools. Inspect lease ownership, event sequence, budget counters, validated call, and cancellation acknowledgement.

## Practice

**Observe:** draw all states and authorities. **Build:** implement a typed bounded loop with leases and terminal states. **Break:** return malformed calls, repeat an error, and race two workers. Completion requires one ordered history and deterministic termination.

## Check yourself

1. Which decisions must remain outside the model?
2. Why is a summary not the audit source?
3. What makes cancellation complete?

## Sources

### REQUIRED

- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

### DEEP DIVE

- [ReAct](https://arxiv.org/abs/2210.03629)

## Next

Continue to [Identity, capabilities, and approvals](05-identity-capabilities-and-approvals.md).
