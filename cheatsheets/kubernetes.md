# Kubernetes operator sheet

Treat Kubernetes as a set of reconcilers. Separate declared intent, observed
object status, scheduling, runtime startup, and request routing before changing
workloads.

## Confirm target and scope

```bash
# Read-only
kubectl config current-context
kubectl config view --minify
kubectl auth can-i get pods -n <namespace>
kubectl get namespace <namespace>
```

The context names a credential and cluster endpoint; it does not guarantee the
intended tenant. Confirm namespace and incident scope. `auth can-i` asks
authorization policy but does not grant access.

## What does the control plane currently observe?

```bash
# Read-only
kubectl get deployment,pod,service,endpointslice -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
```

Resource lists are point-in-time observations. For Deployments, compare desired,
updated, available, and unavailable replicas. Pod `STATUS` is a display summary,
not a complete state machine. Events are best-effort, aggregated, and retained
for a limited period; absence is not proof that nothing happened.

## Is desired state failing to reconcile?

```bash
# Read-only
kubectl describe deployment/<name> -n <namespace>
kubectl get deployment/<name> -n <namespace> -o yaml
kubectl rollout status deployment/<name> -n <namespace> --timeout=60s
kubectl get rs -n <namespace> -l <workload-label-selector>
```

Conditions, observed generation, ReplicaSets, and events show whether the
controller has processed the latest spec. `ProgressDeadlineExceeded` means the
rollout failed to progress before its deadline; it does not identify the cause.
`rollout status` waits and may return nonzero on timeout without changing state.

## Is scheduling blocked?

```bash
# Read-only
kubectl describe pod/<pod> -n <namespace>
kubectl get nodes -o wide
kubectl describe node/<node>
```

For `Pending`, read `PodScheduled` and scheduler events. Common discriminators
are insufficient requested resources, taints without tolerations, affinity,
topology constraints, unbound volumes, and unavailable nodes. Requests drive
scheduling; current low usage does not make an unschedulable request fit.

**Caution:** Reducing requests or removing constraints can cause contention or
violate isolation. Adding nodes may not help a volume, affinity, quota, or
admission failure.

## Did the container start and remain healthy?

```bash
# Read-only
kubectl get pod/<pod> -n <namespace> -o jsonpath='{range .status.containerStatuses[*]}{.name}{" ready="}{.ready}{" restarts="}{.restartCount}{" waiting="}{.state.waiting.reason}{" terminated="}{.lastState.terminated.reason}{"\n"}{end}'
kubectl logs pod/<pod> -n <namespace> -c <container> --since=15m --timestamps
kubectl logs pod/<pod> -n <namespace> -c <container> --previous --timestamps
```

`--previous` is crucial after a restart. `CrashLoopBackOff` is retry backoff, not
the crash cause. `OOMKilled` identifies cgroup memory termination but requires
correlation with limits, usage, and application allocation. A failed readiness
probe removes the Pod from ready endpoints; a failed liveness probe restarts it.

Logs can contain secrets and are incomplete after rotation or node loss. Bound
the time window and container.

## Does Service selection reach ready backends?

```bash
# Read-only
kubectl get service/<service> -n <namespace> -o yaml
kubectl get endpointslice -n <namespace> \
  -l kubernetes.io/service-name=<service> -o wide
kubectl get pods -n <namespace> -l <selector> --show-labels
```

No endpoints usually means selectors match no Pods or matched Pods are not
ready. Verify Service `port`, `targetPort`, protocol, selector, and endpoint
addresses. A populated EndpointSlice does not prove the process listens or that
NetworkPolicy permits traffic.

```bash
# Local mutation plus API tunnel; diagnostic only
kubectl port-forward -n <namespace> service/<service> 18080:<service-port>
```

Port-forward bypasses normal ingress and often part of the data path. Success
isolates the application from some routing layers; it does not validate client
reachability. Stop the process after the bounded test.

## Safe rollout decisions

```bash
# Read-only previews
kubectl diff -f <manifest>
kubectl apply --server-side --dry-run=server -f <manifest>
kubectl rollout history deployment/<name> -n <namespace>
```

Dry-run exercises admission but not every runtime dependency. Diff can expose
Secrets in terminal or CI output. Before a remote mutation, identify field
ownership, rollout strategy, disruption budgets, capacity, success metrics, and
the known-good revision.

```bash
# Remote mutation; approved rollback
kubectl rollout undo deployment/<name> -n <namespace> --to-revision=<revision>
kubectl rollout status deployment/<name> -n <namespace> --timeout=5m
```

Rollback restores a prior pod template, not external schemas, data, Secrets, or
side effects. Pause and escalate if compatibility is uncertain. Avoid deleting
Pods as a first response: the controller recreates them with unchanged causes
and evidence may be lost.

Escalate for control-plane unavailability, broad node failure, admission or RBAC
changes, data-bearing workloads, security incidents, or exhausted disruption
and capacity margins.

## Authoritative sources

- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)
- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Debug applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [Deployment rollouts](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Repository lesson: [Kubernetes](../16-kubernetes/README.md)
