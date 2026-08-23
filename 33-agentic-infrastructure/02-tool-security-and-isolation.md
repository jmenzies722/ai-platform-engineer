# Tool security and isolation

Tool execution must be authorized by deterministic controls outside the model and isolated according to consequence.

## Why it matters

Models process attacker-controlled text and can make incorrect plans. Granting broad ambient credentials converts those failures into real damage.

## How it works

Expose narrow typed tools, validate arguments, bind short-lived credentials to run identity, and enforce resource and network scopes. Separate read from write capabilities. Require approval for consequential or irreversible actions. Sandboxes bound filesystem, process, network, and resource access; audit logs retain decisions without leaking secrets.

Capability design starts from the smallest meaningful operation. `close_issue(id, reason)` is easier to authorize and audit than arbitrary HTTP or shell access. The executor derives identity from trusted run context, not model arguments, and evaluates current policy immediately before action. Credentials expire and are audience-bound so leakage has limited reach.

Isolation is defense against both malicious input and ordinary model error. Filesystem roots, syscall filters, egress allow-lists, CPU and memory limits, and disposable environments constrain blast radius. Approval should display resolved target and effect; approving an opaque command delegates the very judgment the control was meant to preserve.

## See it yourself

Compare `shell(command)` with `read_issue(id)`, `draft_reply(id,text)`, and `submit_reply(id,draft_id)`. The shell can read credentials, scan files, or call arbitrary hosts; the narrow tools expose only issue-scoped objects. Send `id=../../secret` and an unauthorized repository ID: validation and authorization should reject both before execution. This proves typing reduces reach but still requires object-level checks.

## Where it shows up

A coding agent receives a disposable workspace, repository-scoped token, denied metadata endpoints, and no production credentials. Read operations may run automatically, while deployment requires a separate capability and informed approval. Audit events store tool name, resolved resource, policy result, and outcome, with secret values redacted.

## When it breaks

Prompt injection reaches authority, secrets enter context, symlinks escape file scopes, and approval dialogs hide the actual effect. After an unexpected action, first preserve the proposed call, trusted run identity, resolved arguments, policy decision, credential scope, sandbox and network events, and approval record. Determine which deterministic boundary failed before changing prompts.

## Practice

**Build:** define and test a deny-by-default capability manifest for issue triage. **Break:** inject tool instructions in issue text, attempt path traversal, cross-repository access, and secret egress; prove each denial from audit evidence. **Explain back:** distinguish model intent, validation, authorization, isolation, and approval, naming the authority in each step.

## Check yourself

1. Where must authorization happen?
2. Why use short-lived credentials?
3. What makes approval informed?

## Sources

### REQUIRED

- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

### RECOMMENDED

- [NIST application container security](https://csrc.nist.gov/pubs/sp/800/190/final)

### DEEP DIVE

- [gVisor security model](https://gvisor.dev/docs/architecture_guide/security/)

## Next

Continue to [Evaluation and trajectory evidence](03-evaluation-and-operations.md).
