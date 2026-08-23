# The API and reconciliation

Kubernetes is an API-centered control system: clients declare objects, and controllers continuously compare desired and observed state.

## Why it matters

Commands are transient, but API objects persist. Understanding reconciliation lets you debug causes instead of repeatedly deleting symptoms.

## How it works

The API server authenticates and authorizes requests, runs admission, validates objects, and stores them in etcd. A resource's `spec` expresses intent; `status` reports observations. Controllers watch changes and reconcile toward desired state through idempotent actions.

Objects carry metadata including name, namespace, labels, annotations, generation, and resource version. Optimistic concurrency rejects updates based on stale resource versions. Conditions summarize state with reason and observed generation.

Discovery exposes available resources and versions. Clients submit declarative objects or patches; defaulting can add fields before persistence. Server-side apply records field managers and reports conflicts when independent actors claim the same field. Finalizers delay deletion until a controller completes external cleanup, while owner references enable dependent garbage collection.

Watch streams deliver changes after a resource version but can expire or disconnect, so controllers list, watch, and relist rather than treating events as a durable queue. Reconciliation should derive action from current state, tolerate duplicate events, use stable external identity, bound retries, and report status without claiming unobserved success.

## See it yourself

Run `kubectl get deployment NAME -o yaml`. Separate user-authored spec, defaulted fields, controller-owned status, managed fields, owner references, finalizers, generation, and resource version. Compare generation with a condition's observed generation. Apply one field through a distinct field manager in a sandbox and observe ownership. This demonstrates API semantics, not controller correctness.

## Where it shows up

Deployments manage ReplicaSets, ReplicaSets manage Pods, and custom operators apply the same pattern to cloud databases or certificates. The controller must record an external provider ID before retries create duplicates and use finalization to clean it without making namespace deletion permanently unsafe.

## When it breaks

Two controllers fight over one field. A controller reports stale status or hot-loops after an unbounded retry. Admission rejects before storage. A finalizer has no functioning owner and blocks deletion. A watch gap loses assumed events. etcd or API-server trouble prevents new intent while existing workloads continue briefly; node partitions create divergent observations.

Diagnose request identity and audit event, admission response, stored spec, generation, managed fields, conditions, controller logs and queue depth, owner references, finalizers, and external identity. Deleting the child often removes the best evidence while reconciliation recreates it.

## Practice

**Observe:** trace one Deployment write through authentication, authorization, admission, storage, ReplicaSet reconciliation, Pod creation, and status.

**Build:** apply two replicas, inspect field ownership and conditions, then delete one Pod and observe its owner and replacement.

**Break safely:** create a field conflict and a harmless custom object with a removable test finalizer in a disposable cluster. Completion means conflict and deletion blockage are diagnosed from metadata, then repaired without bypassing unknown cleanup.

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
