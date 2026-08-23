# Modules and safe lifecycle

A useful Terraform module offers a small, stable infrastructure capability rather than wrapping every provider argument.

## Why it matters

Modules can encode security and operational defaults, but deep abstraction hides plans and couples unrelated lifecycles. Infrastructure replacement and deletion can destroy data, so review must focus on behavior.

## How it works

Define inputs around user intent and outputs around durable contracts. Pin external module versions and provider constraints. Keep a module cohesive enough to plan and own independently.

Lifecycle controls alter normal behavior. `create_before_destroy` can reduce downtime only when names, quotas, and dependencies permit coexistence. `prevent_destroy` is a guardrail, not a backup. `ignore_changes` transfers ownership of attributes away from Terraform and should name that owner.

Use `moved` blocks when refactoring addresses and import blocks for existing objects. Prefer staged migrations over state surgery. Version modules semantically and document upgrade steps.

## See it yourself

Move a local resource into a child module. First observe the destroy/create plan; then add a `moved` block and confirm the plan preserves identity.

## Where it shows up

Platform teams publish modules for network segments, service identities, databases, and deployment foundations. Consumers compose them at a shallow root.

## When it breaks

One giant module makes every change risky. Boolean inputs create impossible combinations. Ignored attributes accumulate unexplained drift. `create_before_destroy` fails under unique-name or quota constraints.

## Practice

Design an interface for a database module with five or fewer required inputs. Include backup, deletion, encryption, outputs, and an explicit escape hatch.

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
