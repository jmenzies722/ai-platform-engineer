# 14 — Governed Agent Runtime

Build the runtime in an independent repository using synthetic accounts and reversible tools. The core claim is controlled, recoverable action under uncertainty.

## Problem and users

Operators want agents to complete multi-step work, but model outputs are untrusted and external tools have real side effects. Requesters need useful automation, approvers need bounded decisions, tool owners need stable contracts, and investigators need replayable evidence. A chat loop with broad credentials is not an agent platform.

## Constraints and safety envelope

- Support durable workflows, at least three typed tools, scoped identity, budget/deadline, approval, cancellation, and replay.
- Use sandbox or fake external systems; destructive effects require explicit human approval and idempotency protection.
- Treat prompts, retrieved content, model output, tool results, and memory as untrusted data.
- Exclude autonomous financial/legal decisions, unrestricted shell/browser access, and evaluation based only on subjective demos.

## Architecture expectations

Separate request API, workflow state machine, model gateway, policy/approval service, tool broker, sandbox, credential exchange, memory, event log, evaluator, and operator console or CLI. Define leases, checkpoints, deduplication, side-effect receipts, compensation, pause/resume, model/tool versioning, and replay semantics. Distinguish deterministic orchestration from probabilistic planning.

## Milestone plan

1. Threat-model tasks/tools and publish workflow, tool, identity, budget, and event contracts.
2. Execute a deterministic durable workflow with crash recovery and idempotent side effects.
3. Add model planning, policy, approvals, sandboxing, memory limits, audit, and evaluation suites.
4. Red-team indirect injection, confused deputy, runaway cost, partial effects, outage, and forensic replay.

## Required artifacts

- State and trust diagrams, tool schemas, policy matrix, threat model, ADRs, and residual-risk register.
- Versioned evaluation set with success, safety, policy, recovery, and cost metrics plus confidence intervals.
- Tamper-evident event/receipt examples, replay report, approval UX evidence, and incident runbooks.
- Per-task token/tool/compute accounting and workload capacity model.

## Tests and failure drills

Use state-machine, property, policy, authorization, tool contract, idempotency, sandbox escape, and replay tests. Inject prompt injection in tool data, forged approval, tool timeout, rate limit, model refusal, malformed arguments, duplicate callback, worker crash after side effect, expired credential, poisoned memory, budget exhaustion, and unavailable approver. Verify safe halt is distinct from successful completion.

## Observability, security, and cost

Record workflow state age, attempts, model/tool versions, policy decisions, approval latency, tool receipts, side-effect status, budget consumption, evaluation outcome, and redacted traces. Issue per-run least-privilege credentials, validate tool arguments/results, isolate execution, constrain network/filesystem, encrypt memory, retain minimally, and audit every privilege transition. Cap tokens, wall time, tool calls, retries, and concurrent work; report cost per attempted, successful, and safely aborted task.

## Explicit success rubric

| Claim | Graduation evidence |
|---|---|
| Task utility | Held-out tasks meet the declared success threshold with reproducible scoring. |
| Safety | Injection, privilege, budget, and destructive-action tests cannot bypass policy or approval. |
| Durability | Crashes and duplicate delivery neither lose workflow state nor repeat protected side effects. |
| Accountability | A reviewer reconstructs each decision, identity, input version, approval, and effect from the event log. |
| Graceful failure | Uncertainty, unavailable dependencies, and exhausted budgets end in explicit recoverable states. |

## Stretch work

Add information-flow labels, multi-agent delegation with attenuated capabilities, counterfactual replay, or formal workflow invariant checking.

## Authoritative sources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OAuth 2.0 Security Best Current Practice, RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)
- [The Update Framework specification](https://theupdateframework.github.io/specification/latest/)

## Mapped modules

[20 Security](../../20-security/README.md), [23 Control Planes](../../23-control-planes/README.md), [27 LLM Engineering](../../27-llm-engineering/README.md), [32 AI Platform Engineering](../../32-ai-platform-engineering/README.md), [33 Agentic Infrastructure](../../33-agentic-infrastructure/README.md), and [19 Site Reliability Engineering](../../19-sre/README.md).
