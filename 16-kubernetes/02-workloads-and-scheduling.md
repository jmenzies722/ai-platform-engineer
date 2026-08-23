# Pods, scheduling, and workload controllers

A Pod is Kubernetes' scheduling unit; controllers create and replace Pods to provide durable workload behavior.

## Why it matters

Pods are disposable. Treating one as a server with permanent identity defeats rescheduling, rollout, and recovery.

## How it works

Containers in a Pod share a network namespace and can share volumes. The scheduler filters feasible nodes using requests, selectors, affinity, taints, and topology, then scores candidates and records a binding. The kubelet on that node asks the runtime to start containers.

Deployments manage stateless rolling updates through ReplicaSets. StatefulSets provide ordered identities and volume claims, not automatic application consistency. Jobs represent finite work. Resource requests inform scheduling; limits constrain runtime. Readiness controls traffic, liveness can restart a stuck container, and startup probes protect slow starts.

## See it yourself

Compare `kubectl describe pod POD` with `kubectl get events --sort-by=.lastTimestamp`. A Pending Pod's events often name the exact failed scheduling predicate.

## Where it shows up

Web services use Deployments, databases may use StatefulSets plus application-specific replication, and batch pipelines use Jobs or CronJobs.

## When it breaks

Missing requests overcommit nodes. Too-low limits cause throttling or OOM kills. Aggressive liveness probes create restart loops. A Pod remains Pending when no node satisfies all constraints.

## Practice

Create a Deployment with requests, limits, readiness, and topology spread. Predict behavior when one node is unavailable and when readiness fails.

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
