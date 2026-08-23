# Modules and safe lifecycle

A useful Terraform module offers a small, stable infrastructure capability rather than wrapping every provider argument.

## Why it matters

Modules can encode security and operational defaults, but deep abstraction hides plans and couples unrelated lifecycles. Infrastructure replacement and deletion can destroy data, so review must focus on behavior.

## How it works

Define inputs around user intent and outputs around durable contracts. Pin external module versions and provider constraints. Keep a module cohesive enough to plan and own independently.

Lifecycle controls alter normal behavior. `create_before_destroy` can reduce downtime only when names, quotas, and dependencies permit coexistence. `prevent_destroy` is a guardrail, not a backup. `ignore_changes` transfers ownership of attributes away from Terraform and should name that owner.

Use `moved` blocks when refactoring addresses and import blocks for existing objects. Prefer staged migrations over state surgery. Version modules semantically and document upgrade steps.

A module contract includes accepted values, defaults, validation, outputs, provider requirements, security and reliability guarantees, lifecycle ownership, and upgrade behavior. Expose intent such as retention objective rather than every provider field. Escape hatches need bounded types, conflict rules, and an owner because an unstructured map can bypass all guarantees.

Composition should keep ownership visible. Root modules select accounts, Regions, providers, environment policy, and module versions. Child modules should not surprise callers by configuring providers or coupling unrelated resources. Test important plans and outputs across supported input combinations, including upgrades from the previous version.

## See it yourself

Move a local resource into a child module. First observe the destroy and create plan; then add a `moved` block and confirm identity is preserved. Test a valid input, invalid input, replacement-triggering change, and upgrade from the prior module version. A no-change local plan validates address mapping, not service health.

## Where it shows up

Platform teams publish modules for network segments, service identities, databases, and deployment foundations. Consumers compose them at a shallow root that makes provider, environment, and ownership decisions visible. A registry or repository records immutable versions, documentation, examples, test evidence, deprecation, and supported upgrade paths.

## When it breaks

One giant module makes every change risky. Deep nesting obscures addresses and plans. Boolean inputs create impossible combinations. Output changes break downstream consumers. Ignored attributes accumulate unexplained drift. `create_before_destroy` fails under unique-name, quota, cost, or data constraints. `prevent_destroy` blocks legitimate recovery without creating a backup. Major upgrades lack migration declarations.

Inspect module version, provider constraints, address changes, lifecycle rules, planned replacements, quotas, dependent outputs, and deprecation notices. Test migration in a production-shaped sandbox before asking callers to upgrade.

## Practice

**Observe:** audit one module's required inputs, defaults, outputs, provider ownership, lifecycle rules, tests, versions, and consumers.

**Build:** design a database module with five or fewer required intent inputs. Encode backup, deletion, encryption, availability, outputs, validation, and one bounded escape hatch; add contract and upgrade tests.

**Break safely:** rename an address, remove an output, exceed quota under `create_before_destroy`, and pass conflicting inputs in a disposable plan. Completion means unsafe changes fail before apply and the upgrade preserves remote identity where intended.

## Check yourself

1. What ownership decision does `ignore_changes` imply?
2. Why does `prevent_destroy` not protect data from service failure?

## Sources

### REQUIRED
- [Terraform module syntax](https://developer.hashicorp.com/terraform/language/modules/syntax)

### RECOMMENDED
- [Terraform lifecycle meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)

### DEEP DIVE
- [Terraform refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)

## Next

[Testing and automated workflows](04-testing-and-workflows.md)
