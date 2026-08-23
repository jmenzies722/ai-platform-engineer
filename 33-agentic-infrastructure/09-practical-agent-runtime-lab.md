# Practical lab: simulate a durable agent runtime

Build a standard-library runtime that makes state, identity, tool authority, crashes, evaluation, observability, and safety controls executable.

## Why it matters

Security claims about agents are credible only when controlled failures show the deterministic boundary still holds.

## How it works

Represent each run as append-only JSON events with sequence number, state, principal, budget, proposal, validated call, policy decision, approval digest, effect key, and result. Implement typed `read_record`, `draft_change`, and `commit_change` tools over an in-memory tenant-scoped store. Derive authority from run context.

Add a worker lease with fencing token, idempotent effect ledger, crash injection points, step and cost limits, no-progress detection, cancellation, and global commit disable. Replay events to reconstruct state. Redact tool payloads in operational metrics while retaining protected audit records.

## See it yourself

Crash immediately after `commit_change` stores its effect but before the result event. Resume and reconcile by idempotency key; assert one committed change. Race a stale worker after lease transfer; assert its fenced event is rejected. Inject hostile record text requesting cross-tenant access; assert the proposal has no authority.

## Where it shows up

This fixture becomes a regression harness for model, prompt, tool, and policy updates. Replacing the scripted planner with a model must not change executor guarantees.

## When it breaks

Never evaluate by touching real services. Keep effect stores local and seeded. Fail closed for commits when policy is unavailable, but permit authorized reads and emergency cancellation if their dependencies remain healthy. Preserve ambiguous outcomes for reconciliation.

## Practice

**Build:** implement replay, budgets, typed validation, tenant authorization, approvals, leases, idempotency, cancellation, redaction, and twenty-five tests. **Break:** test prompt injection, traversal-like IDs, mutated approval, duplicate delivery, four crash windows, stale worker, policy outage, runaway loop, and kill switch. **Explain back:** compare two trajectories and conduct an incident drill. Completion requires bounded termination, no cross-tenant effects, exactly one committed effect, deterministic replay, and cancellation acknowledgement.

## Check yourself

1. Which guarantee must hold with any planner?
2. How does the lab represent an uncertain commit?
3. What proves the kill switch reached executors?

## Sources

### REQUIRED

- [AWS Builders' Library: idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

### RECOMMENDED

- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

### DEEP DIVE

- [gVisor security model](https://gvisor.dev/docs/architecture_guide/security/)

## Next

Continue to [System Design](../34-system-design/README.md).
