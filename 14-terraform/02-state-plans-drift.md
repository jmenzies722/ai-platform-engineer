# State, plans, and drift

Terraform state maps configuration addresses to remote objects and caches enough attributes to calculate change.

## Why it matters

State is not merely a cache you can casually delete. Losing or racing it can orphan infrastructure, duplicate resources, or expose secrets. A saved plan is a reviewable proposal, not a timeless guarantee.

## How it works

During planning Terraform refreshes its view through providers, compares configuration with state and remote reality, then proposes create, update, replace, or destroy actions. Apply updates remote objects and records resulting state.

Teams should use a remote backend with locking, encryption, access control, backups, and audit logs. State can contain credentials and sensitive values even when CLI output redacts them. Marking a value `sensitive` controls display, not storage.

Drift is remote change outside the configuration workflow. Resolve it deliberately: import the intended reality into code, or apply configuration to restore declared intent. Never edit state JSON by hand.

State has lineage and serial metadata so Terraform can reject unrelated or stale snapshots. Backends determine storage and locking behavior; workspaces select distinct state instances but do not create security boundaries by themselves. Split state by ownership, lifecycle, credentials, and blast radius, then pass small explicit outputs rather than reading broad state whenever possible.

A speculative plan supports review but cannot be applied. A saved plan captures decisions against a state snapshot and variables, yet can still fail when remote preconditions change. Refresh-only mode records provider-observed differences without modifying remote resources; it must not be used to silently approve unauthorized drift.

## See it yourself

Change a `terraform_data` input and inspect plan symbols, addresses, before and after values, unknowns, and replacement causes. Save with `terraform plan -out=plan.bin`, hash it, and use `terraform show plan.bin`. Compare lineage and serial before and after apply without publishing state. This proves local workflow behavior, not backend locking or remote API safety.

## Where it shows up

CI creates speculative pull-request plans with read-only credentials and applies a saved approved plan through a protected, serialized job. Separate state files limit blast radius but require explicit cross-stack contracts. Audit records connect source revision, variable set, provider locks, plan digest, approver, apply identity, and resulting state serial.

## When it breaks

Concurrent applies race without locking. Stale plans fail or act on outdated assumptions. Partial applies leave remote mutations and incomplete downstream work. Manual console edits recur. Backend restore can overwrite valid newer state. Insufficient read permission hides attributes; provider upgrades produce representation-only differences. Broad state combines unrelated systems into one failure domain.

Stop writers before state recovery. Preserve backend versions, lock identity, state lineage and serial, plan, provider locks, and API audit events. A state backup repairs mappings only; it cannot undo remote deletion, data mutation, or external side effects.

## Practice

**Observe:** classify a sample plan by action, replacement cause, blast radius, downtime, data risk, permissions, cost, and ownership. Escalate stateful replacement.

**Build:** design a remote-backend workflow with encryption, access control, versioning, locking, recovery test, serialized apply, and state retention.

**Break safely:** create a stale local saved plan and simulate lock contention. Completion means unsafe apply stops, evidence identifies the active writer or changed serial, and recovery uses supported backend and Terraform operations.

## Check yourself

1. Why can state contain secrets despite `sensitive = true`?
2. What three realities does planning compare?

## Sources

### REQUIRED
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)

### RECOMMENDED
- [Terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)

### DEEP DIVE
- [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)

## Next

[Modules and safe lifecycle](03-modules-and-lifecycle.md)
