# Autoscaling, upgrades, and cluster operations

Scaling and upgrading Kubernetes are coupled control-loop operations: signals change desired capacity, while version and node transitions must preserve API compatibility, workload availability, data safety, and rollback options.

## Why it matters

Autoscaling can amplify a bad dependency or fail because Pods cannot schedule. An apparently routine upgrade can remove an API, evict too many replicas, or strand zonal storage. Control-plane success does not prove workloads remain healthy.

## How it works

The HorizontalPodAutoscaler adjusts replica count from observed metrics relative to targets; accurate resource requests are required for utilization targets. Vertical scaling recommends or changes requests and may restart Pods. Node autoscaling adds or removes capacity for unschedulable Pods, subject to provider limits, topology, disruption constraints, and startup delay. These loops have different signals and time constants, so stabilize one before tuning another.

Upgrades begin with supported version skew, deprecated API discovery, add-on and CRD compatibility, backup or recovery evidence, and capacity headroom. Upgrade control plane, critical add-ons, then nodes in bounded cohorts. Cordon prevents new scheduling; drain requests eviction and respects PodDisruptionBudgets for supported controllers, but a PDB is not an availability guarantee. Readiness and user SLIs gate each step.

Rollout history may permit workload rollback; control-plane downgrade is often unsupported. Plan roll-forward and restore paths before starting.

## See it yourself

Inspect `kubectl get hpa`, `kubectl top pods`, requests, replicas, events, PDBs, node versions, and deprecated API reports in a disposable or read-only context. Predict whether a load increase yields replicas and whether those replicas can schedule. Missing metrics or Pending Pods distinguish scaling-loop failure from application capacity.

## Where it shows up

An API HPA scales on CPU and queue depth while node autoscaling supplies capacity. Maximum replicas cap dependency pressure. During an upgrade, one node pool drains at a time, topology spread retains replicas, a canary pool validates runtime compatibility, and error and latency guardrails stop progression.

## When it breaks

Missing requests make utilization undefined. Scale-to-many overwhelms databases. Metrics lag causes oscillation. New Pods remain Pending due to quota, affinity, storage topology, or insufficient nodes. A PDB blocks maintenance, or a broad drain bypasses standalone Pods. Removed APIs prevent controllers from updating objects. Webhooks unavailable during upgrade block admission.

Use HPA conditions, metric timestamps, scheduling events, quota, node-autoscaler decisions, disruption budgets, API warnings, add-on health, and user SLIs. Pause automation before changing multiple loops at once.

## Practice

**Observe:** trace one workload's demand signal through HPA desired replicas, scheduler feasibility, node capacity, readiness, Service endpoints, and user latency.

**Build:** write an upgrade runbook with compatibility inventory, recovery prerequisites, canary cohort, drain limits, PDB review, storage checks, guardrails, and completion evidence.

**Break safely:** in a local cluster, set an impossible request or remove metrics, then diagnose why replicas or capacity do not become Ready. Rehearse cordon and drain on one worker. Completion means workload availability is measured, disruption stays bounded, and rollback or roll-forward criteria are explicit.

## Check yourself

1. Why can an HPA increase desired replicas without increasing service capacity?
2. What does a PDB not guarantee?
3. Which compatibility checks precede a cluster upgrade?
4. Why should scaling maxima reflect dependency capacity?

## Sources

### REQUIRED

- [Kubernetes Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### RECOMMENDED

- [Kubernetes cluster upgrade guidance](https://kubernetes.io/docs/tasks/administer-cluster/cluster-upgrade/)

### DEEP DIVE

- [Kubernetes version skew policy](https://kubernetes.io/releases/version-skew-policy/)

## Next

[Distributed Systems](../17-distributed-systems/README.md)
