# Identity, capabilities, and approvals

Agent authority comes from trusted workload identity and narrowly delegated capabilities, never from text supplied by the model.

## Why it matters

Prompt injection and ordinary planning errors become damaging only when an executor grants excessive or ambient authority.

## How it works

A principal delegates a task-scoped capability to a run. The executor derives run identity from authenticated context, validates typed arguments, resolves the target, evaluates current policy, obtains short-lived audience-bound credentials, and records the decision. Tools separate read, draft, and commit operations.

Approval is a fresh authorization event for a resolved consequence. The reviewer sees target, diff or effect, identity, policy, reversibility, and expiration. Approval cannot authorize a later changed payload. Credentials and approvals are scoped by tenant, resource, action, and time.

This lesson defines approval as an authorization primitive. [Human approval, escalation, and kill-switch operation](07-evaluation-and-trajectory-observability.md) later covers reviewer workflow, denial, escalation, containment acknowledgements, and safe resume.

## See it yourself

Compare `shell(command)` with `draft_issue_comment(issue_id,text)` and `publish_draft(draft_digest)`. The shell reaches unrelated files and hosts; narrow tools constrain object and action. Changing text after approval changes the digest and must invalidate approval.

## Where it shows up

An operations agent may read telemetry automatically, request approval for a reversible rollout, and be categorically denied direct secret reads or destructive production changes. Audit logs retain resolved resources with redaction.

## When it breaks

Shared service accounts erase attribution, policy trusts model-provided tenant IDs, confused-deputy calls cross tenants, and approval dialogs show opaque commands. Preserve principal, delegation, resolved arguments, policy version, credential audience, and approval digest.

## Practice

**Observe:** create an authority chain for one write. **Build:** define a deny-by-default capability manifest. **Break:** inject a tenant ID, reuse expired approval, mutate an approved payload, and target another object. Completion requires distinct denial evidence.

## Check yourself

1. Why must object authorization occur after resolution?
2. What binds approval to an exact effect?
3. Which identity belongs in audit and billing?

## Sources

### REQUIRED

- [NIST Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)

### RECOMMENDED

- [OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)

### DEEP DIVE

- [SPIFFE specification](https://spiffe.io/docs/latest/spiffe-about/overview/)

## Next

Continue to [Leases, fencing, and effect reconciliation](06-durable-execution-and-reconciliation.md).
