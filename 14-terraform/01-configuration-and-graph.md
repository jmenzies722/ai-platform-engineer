# Configuration, providers, and the graph

Terraform configuration describes resource relationships; Terraform turns those references into a dependency graph and asks providers to realize it.

## Why it matters

Declarative syntax is not an execution script. Treating file order as operation order creates fragile designs and hides dependencies Terraform could otherwise schedule safely.

## How it works

A provider translates Terraform's resource operations into a remote API. Resource arguments state desired inputs; exported attributes become values other resources can reference. A reference such as `subnet_id = aws_subnet.app.id` creates an implicit dependency. Terraform can process unrelated graph vertices concurrently.

Values may be known only after apply. Data sources read existing information, but excessive live reads can make plans slow or permission-heavy. Use `for_each` with stable semantic keys when instances have identity; numeric `count` indices can shift after deletion.

Expressions evaluate variables, locals, resource attributes, functions, conditions, and collection transformations. Types and validation make module boundaries explicit. `null`, unknown, and sensitive are distinct: null can mean omission, unknown defers a value until apply, and sensitive limits display but not propagation or storage. Dynamic blocks and comprehensions can remove repetition but should not hide resource identity.

Terraform infers create and destroy ordering from graph edges, then reverses relevant dependencies during deletion. `depends_on` is for behavioral dependencies that cannot be expressed through data references. Provider configuration, module calls, replacement edges, and lifecycle rules also affect the graph.

## See it yourself

```hcl
resource "terraform_data" "config" {
  input = { environment = "dev" }
}

output "environment" {
  value = terraform_data.config.output.environment
}
```

Run `terraform init`, `terraform validate`, `terraform plan`, and `terraform graph` in a disposable directory. Predict which values are known and which vertices can execute concurrently. The output reference establishes a graph edge without an explicit `depends_on`; graph output supports the dependency claim but does not prove remote APIs honor every semantic prerequisite.

## Where it shows up

Network IDs feed compute resources, role ARNs feed workload configuration, and module outputs feed callers. Provider aliases support distinct Regions or accounts, but child modules must declare and receive aliases deliberately. Stable keyed instances make plans intelligible when regions, tenants, or services are added and removed.

## When it breaks

Hidden dependencies cause races. Broad `depends_on` serializes unrelated work and produces needless unknown values. Positional indices shift identity. Unknown values prevent policy decisions until apply. Provider aliases accidentally target the wrong account or Region. Unconstrained provider upgrades change schemas or behavior.

Diagnose with evaluated addresses, graph edges, provider selections, account context, planned unknowns, and API error timestamps. Never repair a graph problem by adding broad dependencies before naming the missing behavioral relationship.

## Practice

**Observe:** annotate a plan with addresses, known and unknown values, create, update, replace, and destroy edges, and provider contexts.

**Build:** add two independent `terraform_data` resources and a third referencing both. Use typed variables, validation, locals, and stable `for_each` keys; predict and inspect the graph.

**Break safely:** remove a reference, shift a `count` list, and misroute a provider alias in disposable configuration. Completion means each risky plan is detected before apply and repaired through explicit identity or dependency.

## Check yourself

1. What creates an implicit dependency?
2. Why are stable `for_each` keys safer than positional indices?

## Sources

### REQUIRED
- [Terraform language resources](https://developer.hashicorp.com/terraform/language/resources)

### RECOMMENDED
- [Terraform dependency graph](https://developer.hashicorp.com/terraform/internals/graph)

### DEEP DIVE
- [Terraform provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)

## Next

[State, plans, and drift](02-state-plans-drift.md)
