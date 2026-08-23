# 16 — Kubernetes

Kubernetes stores desired state in an API and runs controllers that continually work to make cluster reality match it.

## What you will learn

- Trace a workload from API object through scheduling to a node.
- Use Deployments, Services, configuration, probes, and resources correctly.
- Debug with object status, events, logs, and network evidence.

## Lessons

1. [The API and reconciliation](01-api-and-reconciliation.md)
2. [Pods, scheduling, and workload controllers](02-workloads-and-scheduling.md)
3. [Services, configuration, and failure diagnosis](03-service-and-operations.md)

## Practice

Complete the [local Kubernetes diagnosis lab](lab-local-cluster.md) using kind, minikube, or an existing disposable cluster.

## Ready to continue

You can distinguish a Pod from a Deployment, explain scheduler and controller responsibilities, and diagnose a non-ready workload without restarting it blindly.

## Next

Continue to [Distributed Systems](../17-distributed-systems/README.md).
