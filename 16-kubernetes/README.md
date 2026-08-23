# 16 — Kubernetes

Kubernetes stores desired state in an API and runs controllers that continually work to make cluster reality match it.

## What you will learn

- Trace a workload from API object through scheduling to a node.
- Use Deployments, Services, configuration, probes, and resources correctly.
- Operate persistent storage, workload identity, authorization, and policy boundaries.
- Reason about autoscaling and upgrades, then debug with status, events, logs, metrics, and network evidence.

## Lessons

1. [The API and reconciliation](01-api-and-reconciliation.md)
2. [Pods, scheduling, and workload controllers](02-workloads-and-scheduling.md)
3. [Services, configuration, and failure diagnosis](03-service-and-operations.md)
4. [Persistent storage and data workloads](04-storage-and-data.md)
5. [Identity, policy, and workload security](05-security-and-policy.md)
6. [Autoscaling, upgrades, and cluster operations](06-scaling-and-upgrades.md)

## Practice

Complete the [local Kubernetes operations lab](lab-local-cluster.md) using kind, minikube, or an existing disposable cluster. It covers reconciliation, scheduling, Service failure, storage, security context, scaling evidence, rollout, and cleanup.

## Ready to continue

You can trace API admission and reconciliation, explain scheduling and controller ownership, diagnose network and storage failures, constrain workload authority, and plan a safe scaling or upgrade operation.

## Next

Continue to [Distributed Systems](../17-distributed-systems/README.md).
