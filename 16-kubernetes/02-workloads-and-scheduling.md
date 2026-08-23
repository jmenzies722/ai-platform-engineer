# Pods, scheduling, and workload controllers

A Pod is Kubernetes' scheduling unit; controllers create and replace Pods to provide durable workload behavior.

## Why it matters

Pods are disposable. Treating one as a server with permanent identity defeats rescheduling, rollout, and recovery.

## How it works

Containers in a Pod share a network namespace and can share volumes. The scheduler filters feasible nodes using requests, selectors, affinity, taints, and topology, then scores candidates and records a binding. The kubelet on that node asks the runtime to start containers.

Deployments manage stateless rolling updates through ReplicaSets. StatefulSets provide ordered identities and volume claims, not automatic application consistency. Jobs represent finite work. Resource requests inform scheduling; limits constrain runtime. Readiness controls traffic, liveness can restart a stuck container, and startup probes protect slow starts.

Scheduling separates placement from execution. The scheduler considers only Pods without a node, filters hard constraints, scores feasible nodes, and writes a binding. The kubelet admits the Pod against node resources, mounts volumes, configures networking, and asks the runtime to start containers. Init containers gate application startup; sidecars and application containers share Pod lifecycle and resource competition.

Topology spread and anti-affinity distribute replicas, while taints repel Pods unless tolerated. Pod priority can preempt lower-priority work but cannot create capacity. Disruption budgets constrain voluntary eviction for selected workloads; they do not protect against node loss or prove enough Ready replicas serve correctly.

## See it yourself

Compare Pod YAML, `kubectl describe pod`, events, node allocatable resources, requests, and scheduler status. Predict placement, QoS class, and behavior under one node loss. A Pending Pod's events often name the failed scheduling constraints, but stale or aggregated events require checking current spec and nodes.

## Where it shows up

Web services use Deployments with surge and unavailable bounds, databases may use StatefulSets plus application-specific replication, and batch pipelines use Jobs with idempotent tasks, deadlines, and retry limits. DaemonSets place node agents. Production workload choice encodes identity, completion, rollout, and disruption semantics.

## When it breaks

Missing requests overcommit nodes. Oversized requests strand capacity. Low CPU limits throttle and low memory limits OOM-kill. Aggressive liveness creates restart loops; readiness tied to every dependency removes all endpoints. Pods remain Pending from resources, affinity, taints, quota, unbound volumes, or admission. Rollouts stall because new and old replicas exceed quota or topology.

Gather conditions, events, scheduler message, node pressure, requests and actual use, probes, container states, prior logs, controller strategy, PDB, quota, and volume topology before deleting Pods.

## Practice

**Observe:** trace a Pod from controller template through scheduler binding, kubelet admission, runtime start, readiness, and Service endpoint.

**Build:** create a Deployment with measured requests, justified limits, startup and readiness probes, topology spread, rollout bounds, and a PDB.

**Break safely:** specify impossible CPU, an untolerated taint, and failing readiness in a local cluster. Completion means each Pending or unready state is distinguished and repair restores traffic without disabling safeguards.

## Check yourself

1. What is the scheduler's output?
2. Why should dependency failure usually affect readiness before liveness?

## Sources

### REQUIRED
- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

### RECOMMENDED
- [Kubernetes scheduling](https://kubernetes.io/docs/concepts/scheduling-eviction/)

### DEEP DIVE
- [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## Next

[Services, configuration, and failure diagnosis](03-service-and-operations.md)
