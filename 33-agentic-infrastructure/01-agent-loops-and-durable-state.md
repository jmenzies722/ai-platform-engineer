# Agent loops and durable state

An agent loop observes state, proposes an action, executes through a controlled interface, and records the result before continuing.

## Why it matters

Long-running tasks cross timeouts and failures. Without durable state, retries duplicate actions and postmortems become guesswork.

## How it works

Represent runs as explicit states and append immutable events for prompts, model responses, tool requests, approvals, results, and budgets. Checkpoints permit resume. Idempotency keys deduplicate side effects. Limits on steps, time, tokens, and money guarantee termination or escalation.

State transition logic, not conversational text, decides whether an action is pending, committed, or retryable. The durable log is written before and after external effects using a protocol that can reconcile ambiguous outcomes. A checkpoint is a projection for faster resume; events remain the audit source. Context can be summarized, but the summary is versioned because compression can discard constraints.

## See it yourself

Use states `RESEARCH`, `DRAFT`, `REVIEW`, `DONE`. Record tool intent with key `run7-search1`, execute, then crash before result acknowledgement. On replay, the tool or effect ledger returns the prior result for that key rather than executing again. If no result can be queried, state becomes `NEEDS_RECONCILIATION`, not blind retry. This demonstrates why durable state must account for uncertain commit.

## Where it shows up

An operations agent gathering diagnostics may survive a controller restart while commands continue remotely. Each command intent, authorization, and bounded result enters the run log. A resumed model receives verified current state rather than assuming the last proposed command completed. Budgets prevent diagnosis from becoming an endless or costly loop.

## When it breaks

State and side effects commit separately, observations grow without bound, and loops mistake repeated failure for progress. For duplicate or stuck runs, first reconstruct the event timeline around the last durable transition and external idempotency record. Repeated identical action-error pairs indicate no-progress detection failure; missing acknowledgements indicate reconciliation, not planning.

## Practice

**Build:** implement a replayable state machine with terminal states, event sequence numbers, and budgets. **Break:** crash before and after one mock side effect and corrupt a summary; demonstrate deduplication and validation. **Explain back:** reconstruct the run solely from events and state why the next action is safe.

## Check yourself

1. Why use an event log?
2. Where is idempotency required?
3. What guarantees loop termination?

## Sources

### REQUIRED

- [AWS Builders' Library: idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

### DEEP DIVE

- [ReAct](https://arxiv.org/abs/2210.03629)

## Next

Continue to [Tool security and isolation](02-tool-security-and-isolation.md).
