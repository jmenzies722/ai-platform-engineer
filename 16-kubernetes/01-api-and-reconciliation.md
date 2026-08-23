# The API and reconciliation

Kubernetes is an API-centered control system: clients declare objects, and controllers continuously compare desired and observed state.

## Why it matters

Commands are transient, but API objects persist. Understanding reconciliation lets you debug causes instead of repeatedly deleting symptoms.

## How it works

The API server authenticates and authorizes requests, runs admission, validates objects, and stores them in etcd. A resource's `spec` expresses intent; `status` reports observations. Controllers watch changes and reconcile toward desired state through idempotent actions.

Objects carry metadata including name, namespace, labels, annotations, generation, and resource version. Optimistic concurrency rejects updates based on stale resource versions. Conditions summarize state with reason and observed generation.

## See it yourself

Run `kubectl get deployment NAME -o yaml`. Separate user-authored spec, defaulted fields, controller-owned status, and managed fields. Compare `metadata.generation` with a condition's `observedGeneration`.

## Where it shows up

Deployments manage ReplicaSets, ReplicaSets manage Pods, and custom operators apply the same pattern to domain resources.

## When it breaks

Two controllers fight over one field. A controller reports stale status. Admission rejects an object before storage. etcd or API-server trouble prevents new intent even while existing workloads continue briefly.

## Practice

Apply a Deployment with two replicas, then manually delete one Pod. Observe the owner reference and replacement. Explain why deletion did not change desired replica count.

## Check yourself

1. Which component durably records desired state?
2. Why must reconciliation be idempotent?

## Sources

### REQUIRED
- [Kubernetes API concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/)

### RECOMMENDED
- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)

### DEEP DIVE
- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

## Next

[Pods, scheduling, and workload controllers](02-workloads-and-scheduling.md)
