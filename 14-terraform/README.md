# 14 — Terraform

Terraform compares configuration, prior state, and provider-reported reality to propose infrastructure changes you can review before applying.

## What you will learn

- Read declarative configuration and its dependency graph.
- Explain why state is sensitive, shared, and operationally critical.
- Review plans, manage drift, and design stable modules.

## Lessons

1. [Configuration, providers, and the graph](01-configuration-and-graph.md)
2. [State, plans, and drift](02-state-plans-drift.md)
3. [Modules and safe lifecycle](03-modules-and-lifecycle.md)

## Practice

Use the local provider or `terraform_data` to create a tiny configuration. Run `fmt`, `validate`, `plan`, inspect state, change one input, and predict the next plan before running it.

## Ready to continue

You can explain what Terraform state does, identify implicit dependencies, review replacement risk in a plan, and choose module boundaries around stable contracts.

## Next

Continue to [Containers](../15-containers/README.md).
