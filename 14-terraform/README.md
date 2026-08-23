# 14 — Terraform

Terraform compares configuration, prior state, and provider-reported reality to propose infrastructure changes you can review before applying.

## What you will learn

- Read declarative configuration and its dependency graph.
- Explain why state is sensitive, shared, and operationally critical.
- Design stable modules and test their contracts before deployment.
- Run reviewed workflows for import, refactoring, drift, and recovery.

## Lessons

1. [Configuration, providers, and the graph](01-configuration-and-graph.md)
2. [State, plans, and drift](02-state-plans-drift.md)
3. [Modules and safe lifecycle](03-modules-and-lifecycle.md)
4. [Testing and automated workflows](04-testing-and-workflows.md)
5. [Import, refactoring, and adoption](05-import-and-refactoring.md)
6. [Drift operations and state recovery](06-drift-and-recovery.md)

## Practice

Complete the [local Terraform change-control lab](lab-change-control.md). It uses only built-in `terraform_data` resources to exercise graph inspection, tests, saved plans, refactoring, drift detection, and recovery.

## Ready to continue

You can explain the graph and state model, review replacement risk, test module contracts, import existing objects without recreation, distinguish drift from intended change, and recover state through supported workflows.

## Next

Continue to [Containers](../15-containers/README.md).
