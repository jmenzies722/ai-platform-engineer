# State, plans, and drift

Terraform state maps configuration addresses to remote objects and caches enough attributes to calculate change.

## Why it matters

State is not merely a cache you can casually delete. Losing or racing it can orphan infrastructure, duplicate resources, or expose secrets. A saved plan is a reviewable proposal, not a timeless guarantee.

## How it works

During planning Terraform refreshes its view through providers, compares configuration with state and remote reality, then proposes create, update, replace, or destroy actions. Apply updates remote objects and records resulting state.

Teams should use a remote backend with locking, encryption, access control, backups, and audit logs. State can contain credentials and sensitive values even when CLI output redacts them. Marking a value `sensitive` controls display, not storage.

Drift is remote change outside the configuration workflow. Resolve it deliberately: import the intended reality into code, or apply configuration to restore declared intent. Never edit state JSON by hand.

## See it yourself

Change a `terraform_data` input and inspect the plan symbols and before/after values. Save it with `terraform plan -out=plan.bin`; use `terraform show plan.bin` to review the exact plan.

## Where it shows up

CI plans on pull requests and applies after protected approval. Separate state files limit blast radius but create explicit cross-stack contracts.

## When it breaks

Concurrent applies race without locking. Stale plans become invalid after state changes. Manual console edits recur after every apply. Overly broad state combines unrelated systems into one failure domain.

## Practice

Classify a sample plan by action, blast radius, downtime, data risk, permissions, and cost. Escalate every replacement of a stateful resource.

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
