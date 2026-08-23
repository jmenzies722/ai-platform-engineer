# Kubernetes

Kubernetes continually works to make a cluster match the workload state you declared.

## Why it matters

**Prerequisite:** [Containers](./12-containers.md).

Scripts can start a few containers, but they do not reliably place, restart, discover, and update thousands of workloads across changing machines. Cluster schedulers and reconciliation systems addressed that fleet problem.

Kubernetes made desired state available through an extensible API. The same flexibility that supports ordinary services, GPU operators, and AI controllers also creates configuration, controller, networking, and tenancy complexity.

## How it works

Kubernetes is a distributed database of desired and observed state plus independent controllers that repeatedly reduce the difference.

Clients submit objects to the API server; admission validates/mutates; etcd persists state; controllers create dependent objects; the scheduler binds Pods to nodes; kubelets start containers and report status.

Reconciliation is level-based and must be idempotent. Scheduling filters infeasible nodes then scores feasible ones. Readiness controls traffic, while liveness triggers restart; confusing them creates outages.

## Vocabulary

- **Reconciliation:** Repeatedly driving observed state toward desired state.
- **API server:** The authenticated Kubernetes API boundary for cluster state and operations.
- **etcd:** The consistent key-value store used for Kubernetes control-plane state.
- **Controller:** A control loop that reconciles resources.
- **Scheduler:** The component that assigns unscheduled Pods to nodes.
- **Kubelet:** The node agent that manages declared Pod execution.
- **Pod:** Kubernetes' smallest deployable workload unit, containing one or more containers.
- **Deployment:** A controller-managed declaration for replicated stateless Pods and rollouts.
- **Service:** A stable network identity and endpoint selection abstraction.
- **CRD:** A custom resource definition extending the Kubernetes API.
- **Finalizer:** A key that delays resource deletion until cleanup completes.
- **Admission:** Request-time validation or mutation before API objects are persisted.

## See it yourself

This tiny controller makes reconciliation visible without requiring a Kubernetes cluster:

```python
desired = 3
actual = {"pod-a"}

def reconcile():
    next_id = 1
    while len(actual) < desired:
        while f"pod-{next_id}" in actual:
            next_id += 1
        actual.add(f"pod-{next_id}")
    while len(actual) > desired:
        actual.pop()

reconcile()
print(sorted(actual))

actual.remove("pod-a")  # a running instance disappears
reconcile()
print(sorted(actual))   # the controller restores the count
```

Predict both printed lists before running the controller. Each should contain three names, and the second should replace the removed instance. This supports reconciliation: observed state is corrected toward a declared count. It does not model asynchronous APIs, stable identities, placement, safe deletion, or the failure behavior of Kubernetes controllers.

## Where it shows up

A GPU Pod can remain Pending while the scheduler is healthy. Its resource request, node labels, taints, affinity, and device topology may leave no feasible node. The scheduler records why candidates were rejected; it cannot manufacture capacity or ignore policy. Events and node allocatable state explain this case better than restarting the scheduler.

## When it breaks

A Pod stuck Pending may reflect an impossible selector, insufficient quota or resources, an unbound volume, or an admission dependency. First read object conditions and recent events, then compare the request with node allocatable state and scheduling constraints. Restarting components before reading API evidence destroys useful context.

## Practice

### Observe

Deploy a service, inspect generated ReplicaSet and Pods, change replicas, delete a Pod, and observe reconciliation restoring desired state.

### Build

Write pseudocode for a controller reconciling a `ModelDeployment` with status conditions and idempotent cleanup.

### Break

Use an impossible node selector, failing readiness probe, and blocking finalizer. Diagnose from API evidence only.

### Say it out loud

Explain what happens after a Kubernetes object is accepted.

**Success:** Trace persisted intent through controllers, scheduling, node execution, and status, while preserving asynchronous failure boundaries.

## Check yourself

1. Why are controllers level-based?
2. What does the scheduler decide?
3. How do readiness and liveness differ?

### Interview stretch

- Debug a Pending GPU Pod.
- Design an idempotent operator.
- Explain why etcd health affects the control plane.

## Sources

### REQUIRED

- “Kubernetes Components” — Kubernetes project. [Official docs](https://kubernetes.io/docs/concepts/overview/components/). Canonical architecture overview.

### RECOMMENDED

- “Kubernetes API Concepts” — Kubernetes project. [Official docs](https://kubernetes.io/docs/reference/using-api/api-concepts/). Defines desired state, resource versions, and API behavior.

### DEEP DIVE

- “Large-scale cluster management at Google with Borg” — Verma et al. [Google Research](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/). Explains scheduling lineage and production pressures.

## Next

Continue with [./14-sre-and-observability.md](./14-sre-and-observability.md).
