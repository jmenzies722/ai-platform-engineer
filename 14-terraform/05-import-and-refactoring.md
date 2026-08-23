# Import, refactoring, and adoption

Import and refactoring change Terraform's ownership map without necessarily changing remote infrastructure, so address mapping and post-change plans are the primary safety evidence.

## Why it matters

Organizations often adopt existing resources or reorganize configuration. A wrong import can bind an address to the wrong production object; an unrecorded address move can propose destroy and create for infrastructure that should retain identity.

## How it works

Configuration addresses identify resource instances, including module paths and `for_each` keys. Import associates an existing remote object ID with a configured address and records its observed attributes in state; it does not generate a complete design or prove arguments match organizational intent. Import blocks make adoption reviewable and repeatable.

Before import, write the smallest accurate resource configuration, verify provider and account, back up state through the backend, identify the remote object uniquely, and run a plan. After import, iterate configuration until the plan shows only intended changes. Never import one remote object to multiple active addresses.

Use `moved` blocks to declare old and new addresses during refactoring. They preserve identity across module extraction, resource renaming, and stable instance-key changes when mappings are one-to-one. More complex splits or merges require staged migration and service-specific validation. Keep moved declarations long enough for supported upgrade paths.

## See it yourself

With a disposable `terraform_data.example`, apply locally, rename its address, and observe the proposed delete and create. Add `moved { from = terraform_data.example to = terraform_data.renamed }` and verify the no-replacement plan. This demonstrates address migration for local state, not safety for every remote API.

## Where it shows up

A team imports manually created DNS records before making configuration authoritative. A module upgrade moves a resource into a child module while preserving its cloud ID. Reviewers require the address map, pre-change identity, plan, and service health evidence.

## When it breaks

The CLI points at the wrong workspace, account, or Region. Import ID syntax is provider-specific and identifies an unexpected object. Incomplete configuration immediately proposes destructive normalization. A moved block maps the wrong keyed instance. Removing migration declarations strands consumers skipping versions.

Stop when the plan includes unexplained replacement or deletion. Compare provider-reported IDs, state addresses, account context, and configuration. Restore state backup only through backend and Terraform-supported operations, and remember that state rollback cannot reverse remote side effects.

## Practice

**Observe:** choose an unmanaged sandbox object and record account, provider alias, immutable ID, current attributes, dependencies, and owner.

**Build:** author configuration and an import block, then produce a post-import plan with every difference classified. Refactor one address with a moved block.

**Break safely:** intentionally target a wrong local address, inspect the plan, remove the bad binding with supported state commands, and repeat correctly. Completion means the remote object is never recreated and the final plan contains no unexplained action.

## Check yourself

1. What does import add that configuration alone does not?
2. Why can successful import still produce a dangerous plan?
3. When is a moved block sufficient for refactoring?
4. Why cannot restoring state undo a remote mutation?

## Sources

### REQUIRED

- [Terraform import blocks](https://developer.hashicorp.com/terraform/language/import)

### RECOMMENDED

- [Terraform moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)

### DEEP DIVE

- [Terraform state command reference](https://developer.hashicorp.com/terraform/cli/commands/state)

## Next

[Drift operations and state recovery](06-drift-and-recovery.md)
