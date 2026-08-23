# Testing and automated workflows

Terraform workflows should reject malformed configuration early, test module contracts in isolation, and apply only a reviewed plan under serialized and auditable authority.

## Why it matters

A valid configuration can still violate security, availability, or cost requirements. Applying from a developer laptop hides credentials and evidence; applying an unreviewed regenerated plan permits reality to differ from what reviewers approved.

## How it works

Layer feedback by cost. `terraform fmt -check` enforces canonical form, `terraform validate` checks syntax and internal consistency after initialization, and provider lock files preserve selected checksums. Static policy can inspect configuration or plan data. Terraform test files can run plan or apply operations against an isolated test configuration and assert outputs or resource attributes. Provider-backed tests may create real billable resources and require explicit cleanup.

A team workflow initializes from locked dependencies, validates, tests, plans with the intended variables, renders the plan for review, and applies the saved binary plan after approval. The apply identity needs only the permissions required by the stack. Remote state locking serializes writers. Production applies should reject speculative plans from untrusted contexts and record commit, plan digest, actor, state lineage, and result.

Tests cannot prove provider APIs will remain available or production data is safe. Use post-apply checks and service telemetry to verify actual behavior.

## See it yourself

Create a `terraform_data` resource and a `.tftest.hcl` file asserting its output. Run `terraform fmt -check`, `terraform validate`, `terraform test`, then `terraform plan -out=tfplan` and `terraform show tfplan`. Change configuration after saving. Predict what applying the old plan will do, but use only disposable local state.

## Where it shows up

A network module test asserts expected CIDR derivation and outputs. Pull requests generate speculative plans with no write credentials. A protected environment approves the saved plan, then a federated workload identity performs one serialized apply and publishes state and deployment evidence.

## When it breaks

Tests share a backend and race. Mock-heavy tests validate assumptions rather than provider behavior. Plan output leaks sensitive values into logs. Apply silently regenerates a plan. A canceled job leaves a lock or partially created test resources. Provider initialization downloads unreviewed versions.

Diagnose with initialization logs, dependency locks, test state, backend lock ownership, saved-plan metadata, and provider errors. Force-unlock only after proving no writer is active and preserving the lock evidence.

## Practice

**Observe:** audit one infrastructure pipeline for inputs, credentials, backend, concurrency, plan retention, approval, and evidence.

**Build:** add format, validate, contract test, policy, saved-plan review, protected apply, and post-apply verification stages to a disposable module.

**Break safely:** make one assertion fail, alter configuration after planning, and simulate concurrent apply. Completion means each unsafe path stops before remote mutation and reports evidence that identifies the violated contract.

## Check yourself

1. What does `validate` not establish about infrastructure behavior?
2. Why apply the reviewed saved plan?
3. Which tests may create billable remote resources?
4. When is force-unlocking state safe?

## Sources

### REQUIRED

- [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)

### RECOMMENDED

- [Terraform automation guidance](https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform)

### DEEP DIVE

- [Terraform plan internals and purpose](https://developer.hashicorp.com/terraform/cli/commands/plan)

## Next

[Import, refactoring, and adoption](05-import-and-refactoring.md)
