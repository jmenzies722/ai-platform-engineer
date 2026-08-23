# Drift operations and state recovery

Drift management is an ownership decision: determine whether remote reality or reviewed configuration should prevail, then reconcile through an auditable plan without corrupting state.

## Why it matters

Out-of-band emergency edits, failed applies, provider behavior, and deleted resources make configuration, state, and remote objects disagree. Blindly applying may erase a valid emergency fix; blindly accepting drift makes declarations fictional.

## How it works

A normal plan refreshes provider observations, updates Terraform's in-memory view, and compares desired configuration to refreshed state. `-refresh-only` proposes state updates without changing remote objects. Exit code mode can let automation distinguish no changes, differences, and errors. State lineage and serial protect continuity; locking protects concurrent writers.

Classify each difference as intended external ownership, approved temporary remediation, unauthorized change, provider normalization, or stale observation. Restore declared intent with a normal reviewed apply, adopt approved reality by changing configuration, or use refresh-only when only recorded observations need correction. `ignore_changes` creates an explicit shared-ownership boundary and should identify the external owner.

Recovery begins by stopping writers, preserving backend versions and logs, confirming workspace and lineage, and comparing state with provider reality. Use `state list`, `state show`, import, remove, or move commands only with a reviewed address map. Never hand-edit JSON or treat a state backup as a remote rollback.

## See it yourself

Apply a disposable `terraform_data` configuration, inspect `terraform state pull`, and record lineage and serial without publishing the file. Change its input in configuration and run `terraform plan -detailed-exitcode`; observe the shell code. Do not assume all provider drift can be simulated by editing local state.

## Where it shows up

A drift job runs read-only plans on each independently owned stack and opens evidence for review rather than auto-applying production. During an incident, an operator temporarily changes capacity, records the exception, and later updates configuration or restores intent after stability returns.

## When it breaks

Automation auto-remediates while responders are still mitigating. Refresh records malicious remote changes as if approved. State is restored over a newer valid serial. Credentials cannot read all attributes, yielding misleading plans. A provider upgrade causes broad representation changes.

Before action, capture plan, backend version, lock owner, provider versions, API audit events, and incident context. Escalate unexplained replacement, deletion, identity change, or state lineage mismatch.

## Practice

**Observe:** run a read-only drift plan for a sandbox stack and classify every action by owner, cause, and required decision.

**Build:** define a drift workflow with schedule, credentials, exit-code handling, evidence retention, routing, exception expiry, and a prohibition on unattended destructive apply.

**Break safely:** interrupt a disposable apply or remove a local state binding after backing up state. Recover with supported commands. Completion means one active writer, preserved lineage, correct remote identity, and a final no-change plan.

## Check yourself

1. When should configuration change to match drift?
2. What does refresh-only intentionally avoid?
3. Why must recovery stop all state writers first?
4. Which plan actions require immediate escalation?

## Sources

### REQUIRED

- [Terraform refresh-only mode](https://developer.hashicorp.com/terraform/cli/commands/plan#refresh-only-mode)

### RECOMMENDED

- [Terraform state purpose](https://developer.hashicorp.com/terraform/language/state/purpose)

### DEEP DIVE

- [Terraform backend state locking](https://developer.hashicorp.com/terraform/language/state/locking)

## Next

[Containers](../15-containers/README.md)
