# Configuration, providers, and the graph

Terraform configuration describes resource relationships; Terraform turns those references into a dependency graph and asks providers to realize it.

## Why it matters

Declarative syntax is not an execution script. Treating file order as operation order creates fragile designs and hides dependencies Terraform could otherwise schedule safely.

## How it works

A provider translates Terraform's resource operations into a remote API. Resource arguments state desired inputs; exported attributes become values other resources can reference. A reference such as `subnet_id = aws_subnet.app.id` creates an implicit dependency. Terraform can process unrelated graph vertices concurrently.

Values may be known only after apply. Data sources read existing information, but excessive live reads can make plans slow or permission-heavy. Use `for_each` with stable semantic keys when instances have identity; numeric `count` indices can shift after deletion.

## See it yourself

```hcl
resource "terraform_data" "config" {
  input = { environment = "dev" }
}

output "environment" {
  value = terraform_data.config.output.environment
}
```

Run `terraform init`, `terraform validate`, and `terraform plan`. The output reference establishes a graph edge without an explicit `depends_on`.

## Where it shows up

Network IDs feed compute resources; role ARNs feed workload configuration; module outputs feed callers. Provider aliases support distinct Regions or accounts.

## When it breaks

Hidden dependencies cause races. Broad `depends_on` serializes unrelated work and produces needless unknown values. Provider upgrades can change schemas or behavior if versions are unconstrained.

## Practice

Add two independent `terraform_data` resources and a third that references both. Predict the graph, then inspect it with `terraform graph`.

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
